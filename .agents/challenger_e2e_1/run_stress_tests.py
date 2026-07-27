import subprocess
import sys
import os

SCRIPT_PATH = "verify_funding_db.py"
REF_PATH = ".agents/challenger_e2e_1/test_inputs/reference.json"
TEST_INPUTS_DIR = ".agents/challenger_e2e_1/test_inputs"

test_cases = [
    ("empty_lists.json", REF_PATH, 0),
    ("malformed_strings.json", REF_PATH, 0),
    ("malicious_inputs.json", REF_PATH, 0),
    ("boundary_violations.json", REF_PATH, 0),
    ("case_differences.json", REF_PATH, 0),
    ("empty_optional_fields.json", REF_PATH, 0),
    ("empty_lists.json", ".agents/challenger_e2e_1/test_inputs/malformed_reference.json", 0)
]

print("Starting verification of verify_funding_db.py against stress test cases...\n")

for filename, ref, min_count in test_cases:
    db_path = os.path.join(TEST_INPUTS_DIR, filename)
    print(f"============================================================")
    print(f"TEST CASE: {filename} with reference {ref}")
    print(f"============================================================")
    cmd = [
        sys.executable, SCRIPT_PATH,
        db_path,
        "--reference-path", ref,
        "--min-count", str(min_count)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        print(f"Return Code: {res.returncode}")
        print("STDOUT:")
        print(res.stdout)
        print("STDERR:")
        print(res.stderr)
    except Exception as e:
        print(f"CRASH/EXCEPTION: {e}")
    print("\n")
