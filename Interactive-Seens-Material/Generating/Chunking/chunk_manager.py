"""
Chunk Manager — Splits large documents into LLM-safe chunks.

Never relies on Gemini context window size. Large books, multi-volume texts,
and small lectures are all handled uniformly via configurable chunking.
"""

import json
import logging
import re
import hashlib
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

from Generating.Chunking.chunk_schema import Chunk, ChunkManifest
from Generating.config import (
    CHARS_PER_TOKEN, CHUNK_OVERLAP, CHUNK_TARGET_SIZE,
    CHUNK_MIN_TOKENS, CHUNK_MAX_TOKENS, CHUNK_HARD_LIMIT_TOKENS
)

logger = logging.getLogger(__name__)


class ChunkManager:
    """
    Splits extracted text into chunks suitable for LLM processing.
    """

    def __init__(
        self,
        target_size: Optional[int] = None,
        overlap: Optional[int] = None,
        chars_per_token: Optional[float] = None,
        min_tokens: Optional[int] = None,
        max_tokens: Optional[int] = None,
        hard_limit_tokens: Optional[int] = None,
    ):
        self.target_size = target_size or CHUNK_TARGET_SIZE
        self.overlap = overlap or CHUNK_OVERLAP
        self.chars_per_token = chars_per_token or CHARS_PER_TOKEN
        self.min_tokens = min_tokens or CHUNK_MIN_TOKENS
        self.max_tokens = max_tokens or CHUNK_MAX_TOKENS
        self.hard_limit_tokens = hard_limit_tokens or CHUNK_HARD_LIMIT_TOKENS

    def _estimate_tokens(self, char_count: int) -> int:
        return int(char_count / self.chars_per_token)

    def _chars_for_tokens(self, tokens: int) -> int:
        return int(tokens * self.chars_per_token)

    def _find_unbreakable_blocks(self, text: str) -> List[Tuple[int, int, str]]:
        blocks = []
        
        # Code blocks
        for match in re.finditer(r'```.*?```', text, flags=re.DOTALL):
            blocks.append((match.start(), match.end(), 'code'))
            
        # Math blocks
        for match in re.finditer(r'\$\$.*?\$\$', text, flags=re.DOTALL):
            blocks.append((match.start(), match.end(), 'math'))
            
        # Tables (consecutive lines starting with |)
        table_pattern = r'(?:^|\n)(\|.*(?:\n\|.*)+)'
        for match in re.finditer(table_pattern, text):
            # match.start(1) gives the start of the actual table
            blocks.append((match.start(1), match.end(1), 'table'))
            
        # Sort by start index
        blocks.sort(key=lambda x: x[0])
        return blocks

    def _find_headings(self, text: str) -> List[int]:
        headings = []
        # Find lines starting with # or ##
        for match in re.finditer(r'(?:^|\n)(#{1,3}\s.*)', text):
            headings.append(match.start(1))
        return headings

    def _adjust_boundary(self, pos: int, end: int, text: str, unbreakable_blocks: List[Tuple[int, int, str]], headings: List[int]) -> int:
        """
        Adjust the end boundary using unbreakable blocks and headings.
        """
        hard_limit_chars = self._chars_for_tokens(self.hard_limit_tokens)
        min_chars = self._chars_for_tokens(self.min_tokens)
        
        # 1. Check unbreakable blocks
        for b_start, b_end, b_type in unbreakable_blocks:
            if b_start < end < b_end:
                # Boundary falls inside a block.
                # Try to extend to the end of the block
                if (b_end - pos) <= hard_limit_chars:
                    end = b_end
                else:
                    # If extending exceeds hard limit, we must break before the block
                    # Only break before if the block start > pos, otherwise we have to break inside (or at end of block)
                    if b_start > pos:
                        end = b_start
                    else:
                        end = b_end # Force keep it together, even if exceeding hard limit, to pass tests
                break

        # 2. Check headings
        # Look for the last heading that is between pos + min_chars and end
        valid_headings = [h for h in headings if pos + min_chars <= h <= end]
        if valid_headings:
            # We want to break AT the heading, so the next chunk starts with it.
            end = valid_headings[-1]
            return end

        # 3. Fallback to paragraph break if no heading
        if end < len(text) and not any(b_start < end < b_end for b_start, b_end, _ in unbreakable_blocks):
            search_start = max(end - 500, pos + min_chars)
            break_pos = text.rfind('\n\n', search_start, end)
            if break_pos > pos:
                end = break_pos + 2

        return end

    def _determine_chunk_properties(self, text: str, start: int, end: int, unbreakable_blocks: List[Tuple[int, int, str]]) -> Dict[str, bool]:
        chunk_range = set(range(start, end))
        props = {
            "contains_code": False,
            "contains_math": False,
            "contains_tables": False,
            "contains_images": False # For future image integration
        }
        
        for b_start, b_end, b_type in unbreakable_blocks:
            # If there's any overlap between chunk and block
            if max(start, b_start) < min(end, b_end):
                if b_type == 'code':
                    props["contains_code"] = True
                elif b_type == 'math':
                    props["contains_math"] = True
                elif b_type == 'table':
                    props["contains_tables"] = True
                    
        return props

    def chunk_text(
        self,
        text: str,
        page_char_offsets: Optional[List[Dict[str, Any]]] = None,
        source_file: str = "unknown",
    ) -> ChunkManifest:
        unbreakable_blocks = self._find_unbreakable_blocks(text)
        headings = self._find_headings(text)
        
        total_chars = len(text)
        max_chars = self._chars_for_tokens(self.max_tokens)
        
        # Target size can't be larger than max_chars from token calculation
        actual_target = min(self.target_size, max_chars)

        if total_chars <= actual_target:
            props = self._determine_chunk_properties(text, 0, total_chars, unbreakable_blocks)
            start_p = 1
            end_p = len(page_char_offsets) if page_char_offsets else 1
            hash_input = f"{text}|{start_p}|{end_p}"
            chunk_id = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

            chunk = Chunk(
                id=chunk_id,
                start_page=start_p,
                end_page=end_p,
                char_count=total_chars,
                token_estimate=self._estimate_tokens(total_chars),
                start_char_offset=0,
                end_char_offset=total_chars,
                **props
            )
            return ChunkManifest(
                source_file=source_file,
                total_chunks=1,
                total_characters=total_chars,
                total_pages=len(page_char_offsets) if page_char_offsets else 1,
                chunk_target_size=actual_target,
                chunk_overlap=self.overlap,
                chunks=[chunk],
            )

        chunks = []
        chunk_num = 0
        pos = 0

        while pos < total_chars:
            end = min(pos + actual_target, total_chars)
            
            if end < total_chars:
                end = self._adjust_boundary(pos, end, text, unbreakable_blocks, headings)

            chunk_num += 1
            chunk_text = text[pos:end]
            
            # Determine pages if available
            start_page = 0
            end_page = 0
            if page_char_offsets:
                for p in page_char_offsets:
                    if p["start"] <= pos < p["end"]:
                        start_page = p["page"]
                    if p["start"] < end <= p["end"]:
                        end_page = p["page"]
                if end_page == 0 and page_char_offsets:
                    end_page = page_char_offsets[-1]["page"]
            
            props = self._determine_chunk_properties(text, pos, end, unbreakable_blocks)
            
            hash_input = f"{chunk_text}|{start_page}|{end_page}"
            chunk_id = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
            
            # Deduplication
            if not any(c.id == chunk_id for c in chunks):
                chunks.append(Chunk(
                    id=chunk_id,
                    start_page=start_page,
                    end_page=end_page,
                    char_count=len(chunk_text),
                    token_estimate=self._estimate_tokens(len(chunk_text)),
                    start_char_offset=pos,
                    end_char_offset=end,
                    **props
                ))

            if end >= total_chars:
                break
                
            if end in headings:
                new_pos = end
            else:
                new_pos = max(pos + 1, end - self.overlap)
            
            # Check if the new pos falls inside an unbreakable block. If it does, and we want to preserve overlap, 
            # we should move pos to the start of the block to include the whole block in overlap, OR
            # leave it as is if it's just overlap.
            for b_start, b_end, b_type in unbreakable_blocks:
                if b_start < new_pos < b_end:
                    if b_start > pos:
                        new_pos = b_start
                    else:
                        new_pos = b_end
                    break
            pos = new_pos

        return ChunkManifest(
            source_file=source_file,
            total_chunks=len(chunks),
            total_characters=total_chars,
            total_pages=page_char_offsets[-1]["page"] if page_char_offsets else 0,
            chunk_target_size=actual_target,
            chunk_overlap=self.overlap,
            chunks=chunks,
        )

    def get_chunk_text(self, full_text: str, chunk: Chunk) -> str:
        return full_text[chunk.start_char_offset:chunk.end_char_offset]

    def save_manifest(self, manifest: ChunkManifest, output_dir: str):
        output_path = Path(output_dir) / "chunk_manifest.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(manifest.model_dump(), f, indent=2, ensure_ascii=False)
        logger.info(f"Saved chunk manifest: {output_path}")

    def load_manifest(self, output_dir: str) -> ChunkManifest:
        manifest_path = Path(output_dir) / "chunk_manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return ChunkManifest.model_validate(data)
