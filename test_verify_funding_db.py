import subprocess
import json
import pytest
import sys
import os

# Find the script path relative to this test file
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "verify_funding_db.py")

# Complete reference config mimicking ContentForFunding.json structure
MOCK_REFERENCE_CONTENT = {
    "ContentForFunding": {
        "Universities": {
            "Why": "Partnerships",
            "Priority": "Critical",
            "Category_For_Company": ["Research Project"]
        },
        "Government": {
            "Why": "Grants",
            "Priority": "Critical",
            "Structure": {}
        }
    }
}

VALID_UNIVERSITY = {
    "Name": "Cairo University",
    "Category": "Universities",
    "Category_For_Company": ["Research Project"],
    "Priority": "Critical",
    "Country": "Egypt",
    "City": "Giza",
    "Official_Website": "https://cu.edu.eg",
    "Official_Email": "info@cu.edu.eg",
    "LinkedIn": "https://linkedin.com/school/cairo-university",
    "Phone": "+20235676105",
    "Description": "Cairo University description detailing research partnership options."
}

VALID_GOVERNMENT = {
    "Name": "Science & Technology Development Fund",
    "Official_Website": "https://stdf.eg",
    "Funding_Programs": ["Research Grant Program"],
    "Last_Project_Link": "https://stdf.eg/awards",
    "Eligibility": ["Egyptian researchers"],
    "Required_Documents": ["Research proposal", "Budget plan"],
    "Funding_Amount": "1,000,000 EGP",
    "Application_Process": ["Submit online", "Technical evaluation"],
    "Success_Stories": ["Funded 500+ national energy projects"],
    "Acceptance_Rate": "20%",
    "Expected_Duration": "6 months",
    "Notes": "Non-dilutive government funding.",
    "Steps_For_Any_Project_To_Get_Funded": ["Create portal account"],
    "Steps_For_This_Project_To_Get_Funded": ["Target clean energy program track"]
}


@pytest.fixture
def ref_file(tmp_path):
    f = tmp_path / "ContentForFunding.json"
    f.write_text(json.dumps(MOCK_REFERENCE_CONTENT), encoding='utf-8')
    return f


def run_validator(db_file, ref_file, min_count=2):
    # Runs the verify_funding_db.py script
    return subprocess.run([
        sys.executable, SCRIPT_PATH, 
        str(db_file), 
        "--reference-path", str(ref_file),
        "--min-count", str(min_count)
    ], capture_output=True, text=True, encoding='utf-8')


def test_fully_valid_db(tmp_path, ref_file):
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "valid_db.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 0
    assert "SUCCESS" in result.stdout


def test_missing_root_key(tmp_path, ref_file):
    target_content = {
        "WrongRoot": {}
    }
    db_file = tmp_path / "missing_root.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=0)
    assert result.returncode == 1
    assert "Root key 'ContentForFunding' is missing" in result.stderr


def test_missing_category(tmp_path, ref_file):
    # Omit Government category
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            }
        }
    }
    db_file = tmp_path / "missing_category.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=0)
    assert result.returncode == 1
    assert "Missing category in target file: 'Government'" in result.stderr


def test_metadata_mismatch(tmp_path, ref_file):
    # Alter the priority metadata of Universities from 'Critical' to 'Low'
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Low",  # MISMATCH
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "mismatch.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=0)
    assert result.returncode == 1
    assert "metadata mismatch. Field 'Priority' expected 'Critical'" in result.stderr


def test_missing_required_field(tmp_path, ref_file):
    bad_univ = VALID_UNIVERSITY.copy()
    del bad_univ["Country"]  # Country is required
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [bad_univ]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "missing_field.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=1)
    assert result.returncode == 1
    assert "Missing required field: 'Country'" in result.stderr


def test_invalid_type(tmp_path, ref_file):
    bad_gov = VALID_GOVERNMENT.copy()
    bad_gov["Funding_Programs"] = "Should be list, but string"
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [bad_gov]
            }
        }
    }
    db_file = tmp_path / "bad_type.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=1)
    assert result.returncode == 1
    assert "must be a list, got str" in result.stderr


def test_placeholder_validation(tmp_path, ref_file):
    bad_univ = VALID_UNIVERSITY.copy()
    bad_univ["Official_Email"] = "fake@email.com"  # Placeholder email
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [bad_univ]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "placeholder.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=1)
    assert result.returncode == 1
    assert "Placeholder pattern detected: 'fake@email.com'" in result.stderr or "Dummy domain placeholder detected: 'fake@email.com'" in result.stderr


def test_duplicate_name(tmp_path, ref_file):
    # Two entities under different categories but with identical normalized names
    dup_gov = VALID_GOVERNMENT.copy()
    dup_gov["Name"] = "Cairo University LLC"  # Normalizes to 'cairouniversity' same as VALID_UNIVERSITY
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [dup_gov]
            }
        }
    }
    db_file = tmp_path / "dup_name.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 1
    assert "Duplicate entity name: 'Cairo University LLC'" in result.stderr


def test_duplicate_website(tmp_path, ref_file):
    dup_gov = VALID_GOVERNMENT.copy()
    dup_gov["Official_Website"] = "http://www.cu.edu.eg/"  # Normalizes to 'cu.edu.eg' same as VALID_UNIVERSITY
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [dup_gov]
            }
        }
    }
    db_file = tmp_path / "dup_website.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 1
    assert "Duplicate website:" in result.stderr


def test_insufficient_entity_count(tmp_path, ref_file):
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "insufficient_count.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    # Require 5, but we only have 2
    result = run_validator(db_file, ref_file, min_count=5)
    assert result.returncode == 1
    assert "Total entity count 2 is less than required minimum 5" in result.stderr
