#!/usr/bin/env python3
"""
verify_stem.py
Automated validation script for STEM.json.
Checks JSON schema, required fields, formatting, year ranges, dummy placeholders, and URL correctness.
"""

import os
import sys
import json
import argparse
import re
from typing import List, Dict, Any
from urllib.parse import urlparse

# Regular expression for validating standard HTTP/HTTPS URLs
URL_REGEX = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domain name
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP address
    r'(?::\d+)?'  # Optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

# Regular expression for email validation (used in contacts checks)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Case-insensitive exact matching placeholders
EXACT_PLACEHOLDERS = {
    'tbd', 'placeholder', 'todo', 'n/a', 'na', 'none', 'null', 'nil', '-', '--', 'undefined', 'temp'
}

# Substring patterns for case-insensitive placeholder checking
SUBSTRING_PLACEHOLDERS = ['placeholder', 'dummy', 'fake', 'test@']

# Regex to detect whole-word placeholders
PLACEHOLDER_REGEX = re.compile(
    r'\b(tbd|todo|n/a|na|none|null|nil|undefined|temp|dummy|fake|placeholder)\b',
    re.IGNORECASE
)

# Dummy/Test Domains
DUMMY_DOMAINS = ['example.com', 'test.com', 'email.com', 'domain.com', 'fake.com']


class StemVerifier:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.errors: List[str] = []

    def log_error(self, message: str):
        """Log a validation error."""
        if message not in self.errors:
            self.errors.append(message)

    def check_url(self, url: str, context: str) -> bool:
        """Validate if the string is a properly formatted URL."""
        if not isinstance(url, str):
            self.log_error(f"[{context}] URL must be a string, got {type(url).__name__}")
            return False
        
        val = url.strip()
        if not val:
            self.log_error(f"[{context}] URL cannot be empty")
            return False

        if not (val.startswith("http://") or val.startswith("https://")):
            if val.startswith("www.") or "." in val:
                self.log_error(f"[{context}] URL is missing scheme (http:// or https://): '{url}'")
            else:
                self.log_error(f"[{context}] Invalid URL scheme/format: '{url}'")
            return False

        if not URL_REGEX.match(val):
            self.log_error(f"[{context}] Invalid URL format: '{url}'")
            return False

        return True

    def check_linkedin_url(self, url: str, context: str) -> bool:
        """Validate that the URL is a correct LinkedIn link."""
        if not self.check_url(url, context):
            return False
        
        try:
            parsed = urlparse(url.strip())
            domain = parsed.netloc.lower()
            if "linkedin.com" not in domain and not domain.endswith("lnkd.in"):
                self.log_error(f"[{context}] LinkedIn URL must be from linkedin.com, got domain '{domain}'")
                return False
            return True
        except Exception as e:
            self.log_error(f"[{context}] Failed to parse LinkedIn URL: '{url}'. Error: {e}")
            return False

    def check_placeholders_and_formats(self, val: str, context: str):
        """Check strings for dummy values, placeholders, and scan for URLs/emails to validate."""
        if not isinstance(val, str):
            return

        val_clean = val.strip()
        if not val_clean:
            self.log_error(f"[{context}] String value is empty or only whitespace")
            return

        val_lower = val_clean.lower()

        # Check exact placeholders
        if val_lower in EXACT_PLACEHOLDERS:
            self.log_error(f"[{context}] Placeholder value detected: '{val_clean}'")
            return

        # Check substring placeholders
        for sub in SUBSTRING_PLACEHOLDERS:
            if sub in val_lower:
                self.log_error(f"[{context}] Placeholder pattern '{sub}' detected in: '{val_clean}'")
                return

        # Check regex placeholders (whole words)
        match = PLACEHOLDER_REGEX.search(val_lower)
        if match:
            self.log_error(f"[{context}] Placeholder word '{match.group(0)}' detected in: '{val_clean}'")
            return

        # Check dummy domains
        if any(dom in val_lower for dom in DUMMY_DOMAINS):
            self.log_error(f"[{context}] Dummy domain placeholder detected in: '{val_clean}'")
            return

        # Auto-detect website/URL and validate format
        if val_lower.startswith("http://") or val_lower.startswith("https://") or val_lower.startswith("www."):
            self.check_url(val_clean, context)

        # Auto-detect email and validate format
        if "@" in val_clean and " " not in val_clean:
            if not EMAIL_REGEX.match(val_clean):
                self.log_error(f"[{context}] Invalid Email format: '{val_clean}'")

    def recursive_value_scan(self, data: Any, context: str):
        """Recursively scan elements of any type for placeholders, URLs, and general validity."""
        if isinstance(data, dict):
            for k, v in data.items():
                self.recursive_value_scan(v, f"{context}.{k}")
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                self.recursive_value_scan(item, f"{context}[{idx}]")
        elif isinstance(data, str):
            self.check_placeholders_and_formats(data, context)

    def validate(self) -> bool:
        """Run validation on the target JSON file."""
        if not os.path.exists(self.file_path):
            self.log_error(f"Target file not found: {self.file_path}")
            return False

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.log_error(f"Failed to parse STEM.json as valid JSON: {e}")
            return False
        except Exception as e:
            self.log_error(f"Failed to read STEM.json: {e}")
            return False

        # 1. Root structure check: list with exactly 1 school object
        if not isinstance(data, list):
            self.log_error("Root of STEM.json must be a JSON array/list")
            return False

        if len(data) != 1:
            self.log_error(f"Root array of STEM.json must contain exactly 1 school object, but found {len(data)}")
            return False

        school = data[0]
        if not isinstance(school, dict):
            self.log_error("The school element in STEM.json must be a JSON object")
            return False

        # 2. Check for required top-level fields
        required_fields = [
            "Name", "Location", "Non_Official_Contacts", "Decision_Makers", 
            "General_Info", "Funding_And_Projects"
        ]
        for field in required_fields:
            if field not in school:
                self.log_error(f"School object is missing required field: '{field}'")

        # 3. Validate Name
        name = school.get("Name")
        if "Name" in school:
            if not isinstance(name, str):
                self.log_error(f"School 'Name' must be a string, got {type(name).__name__}")
            else:
                self.check_placeholders_and_formats(name, "School.Name")

        # 4. Validate Location (must be an object with keys: Address, Maps_Link)
        location = school.get("Location")
        if "Location" in school:
            if not isinstance(location, dict):
                self.log_error(f"School 'Location' must be a JSON object, got {type(location).__name__}")
            else:
                for k in ["Address", "Maps_Link"]:
                    if k not in location:
                        self.log_error(f"Location is missing required key: '{k}'")
                
                address = location.get("Address")
                maps_link = location.get("Maps_Link")
                
                if isinstance(address, str):
                    self.check_placeholders_and_formats(address, "Location.Address")
                elif address is not None:
                    self.log_error(f"Location.Address must be a string, got {type(address).__name__}")
                    
                if isinstance(maps_link, str):
                    self.check_url(maps_link, "Location.Maps_Link")
                    self.check_placeholders_and_formats(maps_link, "Location.Maps_Link")
                elif maps_link is not None:
                    self.log_error(f"Location.Maps_Link must be a string, got {type(maps_link).__name__}")

        # 5. Validate Non_Official_Contacts (must be an array of strings or contact details)
        contacts = school.get("Non_Official_Contacts")
        if "Non_Official_Contacts" in school:
            if not isinstance(contacts, list):
                self.log_error(f"School 'Non_Official_Contacts' must be an array, got {type(contacts).__name__}")
            else:
                for idx, contact in enumerate(contacts):
                    context = f"Non_Official_Contacts[{idx}]"
                    if isinstance(contact, str):
                        self.check_placeholders_and_formats(contact, context)
                    elif isinstance(contact, dict):
                        # Recursive validation of nested contact info details
                        self.recursive_value_scan(contact, context)
                    else:
                        self.log_error(f"[{context}] Contact entry must be a string or object, got {type(contact).__name__}")

        # 6. Validate Decision_Makers (must be array of objects: Name, Role, LinkedIn)
        dms = school.get("Decision_Makers")
        if "Decision_Makers" in school:
            if not isinstance(dms, list):
                self.log_error(f"School 'Decision_Makers' must be an array, got {type(dms).__name__}")
            else:
                for idx, dm in enumerate(dms):
                    context = f"Decision_Makers[{idx}]"
                    if not isinstance(dm, dict):
                        self.log_error(f"[{context}] Decision maker entry must be an object, got {type(dm).__name__}")
                        continue
                    
                    for k in ["Name", "Role", "LinkedIn"]:
                        if k not in dm:
                            self.log_error(f"[{context}] Missing key: '{k}'")
                    
                    dm_name = dm.get("Name")
                    role = dm.get("Role")
                    linkedin = dm.get("LinkedIn")
                    
                    if isinstance(dm_name, str):
                        self.check_placeholders_and_formats(dm_name, f"{context}.Name")
                    elif dm_name is not None:
                        self.log_error(f"[{context}.Name] Must be a string")
                        
                    if isinstance(role, str):
                        self.check_placeholders_and_formats(role, f"{context}.Role")
                    elif role is not None:
                        self.log_error(f"[{context}.Role] Must be a string")
                        
                    if isinstance(linkedin, str):
                        self.check_linkedin_url(linkedin, f"{context}.LinkedIn")
                        self.check_placeholders_and_formats(linkedin, f"{context}.LinkedIn")
                    elif linkedin is not None:
                        self.log_error(f"[{context}.LinkedIn] Must be a string")

        # 7. Validate General_Info
        general_info = school.get("General_Info")
        if "General_Info" in school:
            # General_Info structure is flexible but we must check it for placeholders and formats
            self.recursive_value_scan(general_info, "General_Info")

        # 8. Validate Funding_And_Projects (must be array of objects: Name, Year, Funding_Body, Amount, Description)
        funding = school.get("Funding_And_Projects")
        if "Funding_And_Projects" in school:
            if not isinstance(funding, list):
                self.log_error(f"School 'Funding_And_Projects' must be an array, got {type(funding).__name__}")
            else:
                if len(funding) < 1:
                    self.log_error("Funding_And_Projects must list at least one project/funding entry")
                
                for idx, entry in enumerate(funding):
                    context = f"Funding_And_Projects[{idx}]"
                    if not isinstance(entry, dict):
                        self.log_error(f"[{context}] Funding/project entry must be an object, got {type(entry).__name__}")
                        continue
                    
                    for k in ["Name", "Year", "Funding_Body", "Amount", "Description"]:
                        if k not in entry:
                            self.log_error(f"[{context}] Missing key: '{k}'")
                    
                    p_name = entry.get("Name")
                    year = entry.get("Year")
                    funding_body = entry.get("Funding_Body")
                    amount = entry.get("Amount")
                    description = entry.get("Description")
                    
                    for key, val in [("Name", p_name), ("Funding_Body", funding_body), ("Amount", amount), ("Description", description)]:
                        if isinstance(val, str):
                            self.check_placeholders_and_formats(val, f"{context}.{key}")
                        elif val is not None:
                            self.log_error(f"[{context}.{key}] Must be a string")
                            
                    # Validate Year: last 5 years (2021-2026)
                    if year is not None:
                        try:
                            year_val = int(year)
                            if not (2021 <= year_val <= 2026):
                                self.log_error(f"[{context}.Year] Year must be in range 2021-2026, got {year}")
                        except (ValueError, TypeError):
                            self.log_error(f"[{context}.Year] Year must represent an integer, got {year}")

        # Final recursive check for safety (scans entire parsed JSON tree for placeholders & format correctness)
        self.recursive_value_scan(data, "Root")

        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(description="Validate STEM.json schema and data.")
    parser.add_argument(
        "file",
        nargs="?",
        default=os.path.join(os.path.dirname(__file__), "STEM", "STEM.json"),
        help="Path to the JSON file to validate (default: STEM/STEM.json)"
    )
    args = parser.parse_args()

    verifier = StemVerifier(args.file)
    is_valid = verifier.validate()

    if is_valid:
        print(f"SUCCESS: '{args.file}' is fully valid.")
        sys.exit(0)
    else:
        print(f"FAILURE: Validation failed for '{args.file}'. Found {len(verifier.errors)} errors:", file=sys.stderr)
        for err in verifier.errors:
            print(f" - {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
