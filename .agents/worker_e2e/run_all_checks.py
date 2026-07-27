import subprocess
import sys

def run_cmd(args):
    print(f"Running: {' '.join(args)}")
    result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8')
    print(f"Exit code: {result.returncode}")
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    print("-" * 50)
    return result.returncode

def main():
    print("Executing E2E compliance validation tests...")
    print("-" * 50)
    
    # 1. Run pytest suite
    code1 = run_cmd(["pytest", "test_verify_funding_db.py"])
    
    # 2. Run verify_funding_db.py against Valid Dummy
    code2 = run_cmd([
        sys.executable, "verify_funding_db.py", 
        "Funding/ContentForFunding_Expanded_Valid_Dummy.json", 
        "--reference-path", "Funding/ContentForFunding.json", 
        "--min-count", "2"
    ])
    
    # 3. Run verify_funding_db.py against Invalid Dummy
    code3 = run_cmd([
        sys.executable, "verify_funding_db.py", 
        "Funding/ContentForFunding_Expanded_Invalid_Dummy.json", 
        "--reference-path", "Funding/ContentForFunding.json", 
        "--min-count", "2"
    ])
    
    success = (code1 == 0 and code2 == 0 and code3 == 1)
    if success:
        print("ALL CHECKS PASSED: Pytest passed (0), Valid dummy passed (0), and Invalid dummy failed (1) as expected.")
        sys.exit(0)
    else:
        print("ERROR: Some checks did not return the expected exit codes.")
        sys.exit(1)

if __name__ == "__main__":
    main()
