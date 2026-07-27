"""
Pipeline Execution Context & Checkpoint Framework
==================================================
Manages stateful execution context, checkpoints, rollbacks, and journals for AI pipeline stages.
"""

from typing import Dict, Any, Optional, List
import json
import os
import time


class ExecutionContext:
    def __init__(self, run_id: str, material_id: str):
        self.run_id = run_id
        self.material_id = material_id
        self.started_at = time.time()
        self.current_stage = "Stage 1"
        self.metadata: Dict[str, Any] = {}


class CheckpointManager:
    def __init__(self, checkpoint_dir: str = "Generating/Materials"):
        self.checkpoint_dir = checkpoint_dir

    def save_checkpoint(self, material_id: str, stage_name: str, state_data: Dict[str, Any]) -> str:
        target_dir = os.path.join(self.checkpoint_dir, material_id, "checkpoints")
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, f"{stage_name}_checkpoint.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"stage": stage_name, "timestamp": time.time(), "state": state_data}, f, indent=2)
        return file_path

    def load_checkpoint(self, material_id: str, stage_name: str) -> Optional[Dict[str, Any]]:
        file_path = os.path.join(self.checkpoint_dir, material_id, "checkpoints", f"{stage_name}_checkpoint.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
