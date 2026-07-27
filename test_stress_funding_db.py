import json
import pytest
import os
import sys
from verify_funding_db import DatabaseVerifier

# Complete mock reference config mimicking ContentForFunding.json structure
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

def test_linkedin_phishing_bypass(tmp_path, ref_file):
    # Stress test: LinkedIn URL bypass
    # An attacker can bypass the LinkedIn domain check by using a URL containing 'linkedin.com' in the query or path.
    bad_univ = VALID_UNIVERSITY.copy()
    bad_univ["LinkedIn"] = "https://phishing-site.com/?q=linkedin.com"
    
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
    db_file = tmp_path / "phishing_linkedin.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    verifier = DatabaseVerifier(str(db_file), str(ref_file), min_count=2)
    success = verifier.verify()
    
    # Assert that this fails (but under current code, it passes, which is a bug!)
    # We will log the bug details.
    has_linkedin_error = any("Invalid LinkedIn URL" in err for err in verifier.errors)
    assert not success, "Should fail verification due to malicious LinkedIn URL"
    assert has_linkedin_error, "Should report LinkedIn URL format violation"

def test_phone_no_digits(tmp_path, ref_file):
    # Stress test: Phone validation allows non-numeric characters (spaces and symbols only)
    bad_univ = VALID_UNIVERSITY.copy()
    bad_univ["Phone"] = "+   -()--   " # Length 13, only spaces and punctuation
    
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
    db_file = tmp_path / "bad_phone.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    verifier = DatabaseVerifier(str(db_file), str(ref_file), min_count=2)
    success = verifier.verify()
    
    has_phone_error = any("Invalid Phone format" in err for err in verifier.errors)
    assert not success, "Should fail verification due to phone with no digits"
    assert has_phone_error, "Should report Phone format violation"

def test_reference_json_crashes(tmp_path):
    # Stress test: Uncaught AttributeError if reference file is null
    bad_ref_file = tmp_path / "bad_ref.json"
    bad_ref_file.write_text("null", encoding='utf-8')
    
    db_file = tmp_path / "empty_db.json"
    db_file.write_text(json.dumps({"ContentForFunding": {}}), encoding='utf-8')
    
    verifier = DatabaseVerifier(str(db_file), str(bad_ref_file), min_count=0)
    try:
        success = verifier.verify()
        assert not success, "Should fail verification"
        assert any("Failed to parse reference JSON" in err or "Reference file is missing" in err for err in verifier.errors)
    except AttributeError as e:
        pytest.fail(f"Verifier crashed with AttributeError instead of handling bad reference JSON format: {e}")

def test_reference_json_not_dict_category_crashes(tmp_path):
    # Stress test: Uncaught AttributeError if a category inside reference is not a dict
    bad_ref_content = {
        "ContentForFunding": {
            "Universities": "not-a-dict"
        }
    }
    bad_ref_file = tmp_path / "bad_ref.json"
    bad_ref_file.write_text(json.dumps(bad_ref_content), encoding='utf-8')
    
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
    db_file = tmp_path / "db.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    verifier = DatabaseVerifier(str(db_file), str(bad_ref_file), min_count=1)
    try:
        success = verifier.verify()
        assert not success, "Should fail verification"
    except AttributeError as e:
        pytest.fail(f"Verifier crashed with AttributeError because ref_meta is not a dict: {e}")

def test_empty_normalized_names(tmp_path, ref_file):
    # Stress test: Entity names that normalize to empty strings cause false positive duplicate name warnings
    univ1 = VALID_UNIVERSITY.copy()
    univ1["Name"] = "Inc."
    univ1["Official_Website"] = "https://cu1.edu.eg"
    
    univ2 = VALID_UNIVERSITY.copy()
    univ2["Name"] = "LLC"
    univ2["Official_Website"] = "https://cu2.edu.eg"
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [univ1, univ2]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "dup_empty_names.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    verifier = DatabaseVerifier(str(db_file), str(ref_file), min_count=2)
    verifier.verify()
    
    has_dup_name_error = any("Duplicate entity name" in err for err in verifier.errors)
    assert not has_dup_name_error, "Should not report duplicate name for 'Inc.' and 'LLC' which just normalize to empty"

def test_empty_normalized_urls(tmp_path, ref_file):
    # Stress test: URLs that normalize to empty strings (e.g. 'https://') cause false duplicate warnings
    univ1 = VALID_UNIVERSITY.copy()
    univ1["Name"] = "Univ One"
    univ1["Official_Website"] = "https://"
    
    univ2 = VALID_UNIVERSITY.copy()
    univ2["Name"] = "Univ Two"
    univ2["Official_Website"] = "http://"
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [univ1, univ2]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "dup_empty_urls.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    verifier = DatabaseVerifier(str(db_file), str(ref_file), min_count=2)
    verifier.verify()
    
    has_dup_url_error = any("Duplicate website" in err for err in verifier.errors)
    assert not has_dup_url_error, "Should not report duplicate website for empty/invalid normalized URLs"

def test_url_case_sensitivity(tmp_path, ref_file):
    # Test case sensitivity: URLs that differ only in path/query case should not be duplicates
    univ1 = VALID_UNIVERSITY.copy()
    univ1["Name"] = "Univ One"
    univ1["Official_Website"] = "https://example.com/PageA?Param=X"
    
    univ2 = VALID_UNIVERSITY.copy()
    univ2["Name"] = "Univ Two"
    univ2["Official_Website"] = "https://example.com/pagea?Param=x"
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [univ1, univ2]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "url_case_sensitivity.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    verifier = DatabaseVerifier(str(db_file), str(ref_file), min_count=2)
    verifier.verify()
    
    has_dup_url_error = any("Duplicate website" in err for err in verifier.errors)
    assert not has_dup_url_error, "Should not report duplicate website for case-sensitive differences in path/query"

def test_optional_field_whitespace_bypass(tmp_path, ref_file):
    # Test that optional fields containing only whitespace are skipped,
    # but required fields containing only whitespace fail.
    
    # 1. Optional field contains only whitespace (should skip format check and pass)
    univ_opt_space = VALID_UNIVERSITY.copy()
    univ_opt_space["LinkedIn"] = "   "
    univ_opt_space["Phone"] = "   "
    
    # 2. Required field contains only whitespace (should fail)
    univ_req_space = VALID_UNIVERSITY.copy()
    univ_req_space["Name"] = "   "
    
    target_content_pass = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [univ_opt_space]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file_pass = tmp_path / "opt_space_pass.json"
    db_file_pass.write_text(json.dumps(target_content_pass), encoding='utf-8')
    
    verifier_pass = DatabaseVerifier(str(db_file_pass), str(ref_file), min_count=2)
    success_pass = verifier_pass.verify()
    assert success_pass, "Should pass because optional fields containing only whitespace are skipped"
    
    target_content_fail = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [univ_req_space]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file_fail = tmp_path / "req_space_fail.json"
    db_file_fail.write_text(json.dumps(target_content_fail), encoding='utf-8')
    
    verifier_fail = DatabaseVerifier(str(db_file_fail), str(ref_file), min_count=2)
    success_fail = verifier_fail.verify()
    assert not success_fail, "Should fail because required field contains only whitespace"
    assert any("Field 'Name' cannot be empty" in err for err in verifier_fail.errors)
