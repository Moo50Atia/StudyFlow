"""
validator.py
Validation Engine for verifying enrichment JSON outputs before database persistence.
"""

import logging
from typing import Dict, Any, List
from models import ValidationResult, SourceRecord, ContactRecord
from utils import (
    is_valid_url, is_valid_email, is_valid_phone, 
    is_valid_linkedin, is_placeholder
)

class DataValidator:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def validate_result(self, raw_dict: Dict[str, Any], entity_id: int) -> ValidationResult:
        """Validate and sanitize enrichment data dictionary."""
        errors: List[str] = []
        warnings: List[str] = []
        sources: List[SourceRecord] = []
        contacts: List[ContactRecord] = []
        cleaned: Dict[str, Any] = {}

        # 1. Source URL & Confidence Score
        source_url = raw_dict.get('source_url') or raw_dict.get('official_website')
        if source_url and is_valid_url(source_url):
            source_url = source_url.strip()
        else:
            source_url = None
            warnings.append("No valid source URL provided in enrichment data.")

        confidence = raw_dict.get('confidence_score', 1.0)
        try:
            confidence = float(confidence)
            confidence = max(0.0, min(1.0, confidence))
        except (ValueError, TypeError):
            confidence = 1.0

        # 2. Validate Official Website
        website = raw_dict.get('official_website')
        if website and not is_placeholder(website):
            if is_valid_url(website):
                cleaned['official_website'] = website.strip()
                sources.append(SourceRecord(
                    field_name='official_website',
                    field_value=website.strip(),
                    source_type='Official Website',
                    source_url=source_url or website.strip(),
                    confidence_score=confidence
                ))
            else:
                warnings.append(f"Invalid official website format: {website}")

        # 3. Validate Official Email
        contacts_dict = raw_dict.get('contacts', {}) if isinstance(raw_dict.get('contacts'), dict) else {}
        social_dict = raw_dict.get('social', {}) if isinstance(raw_dict.get('social'), dict) else {}

        email = raw_dict.get('official_email') or contacts_dict.get('general_email') or contacts_dict.get('funding_email') or contacts_dict.get('support_email')
        if email and not is_placeholder(email):
            if is_valid_email(email):
                cleaned['official_email'] = email.strip().lower()
                sources.append(SourceRecord(
                    field_name='official_email',
                    field_value=email.strip().lower(),
                    source_type='Official Website',
                    source_url=source_url,
                    confidence_score=confidence
                ))
            else:
                warnings.append(f"Invalid email format: {email}")

        # 4. Validate Phone
        phone = raw_dict.get('phone') or contacts_dict.get('phone')
        if phone and not is_placeholder(phone):
            if is_valid_phone(phone):
                cleaned['phone'] = phone.strip()
                sources.append(SourceRecord(
                    field_name='phone',
                    field_value=phone.strip(),
                    source_type='Official Website',
                    source_url=source_url,
                    confidence_score=confidence
                ))
            else:
                warnings.append(f"Invalid phone format: {phone}")

        # 5. Validate LinkedIn
        linkedin = raw_dict.get('linkedin') or social_dict.get('linkedin')
        if linkedin and not is_placeholder(linkedin):
            if is_valid_linkedin(linkedin):
                cleaned['linkedin'] = linkedin.strip()
                sources.append(SourceRecord(
                    field_name='linkedin',
                    field_value=linkedin.strip(),
                    source_type='Official Website',
                    source_url=source_url,
                    confidence_score=confidence
                ))
            else:
                warnings.append(f"Invalid LinkedIn URL: {linkedin}")

        # 6. Validate Lists (Programs, Eligibility, Documents, Steps, Success Stories)
        for key in ['funding_programs', 'eligibility', 'required_documents', 'application_process', 'success_stories']:
            items = raw_dict.get(key, [])
            clean_items = []
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, str) and item.strip() and not is_placeholder(item):
                        clean_items.append(item.strip())
                    elif isinstance(item, dict):
                        # Extract program name/title from dict representation if available
                        title = item.get('Opportunity Title') or item.get('program_name') or item.get('title') or item.get('name') or item.get('criterion') or item.get('document_name')
                        if title and isinstance(title, str) and title.strip():
                            sponsor = item.get('Sponsor') or item.get('sponsor')
                            full_title = f"{title.strip()} (Sponsor: {sponsor.strip()})" if sponsor and isinstance(sponsor, str) else title.strip()
                            clean_items.append(full_title)
                        else:
                            clean_items.append(json.dumps(item))
            cleaned[key] = clean_items

        # 7. Validate Public Contacts (supporting list or people key)
        raw_contacts = raw_dict.get('contacts', [])
        if not isinstance(raw_contacts, list):
            raw_contacts = raw_dict.get('people', [])

        if isinstance(raw_contacts, list):
            for c in raw_contacts:
                if isinstance(c, dict) and c.get('name') and not is_placeholder(c.get('name')):
                    c_name = c['name'].strip()
                    c_pos = c.get('position') or c.get('role')
                    c_email = c.get('email') if is_valid_email(c.get('email')) else None
                    c_linkedin = (c.get('linkedin') or c.get('profile_url')) if is_valid_linkedin(c.get('linkedin') or c.get('profile_url')) else None
                    c_phone = c.get('phone') if is_valid_phone(c.get('phone')) else None
                    c_conf = float(c.get('confidence_score', confidence))
                    
                    contacts.append(ContactRecord(
                        name=c_name,
                        position=c_pos,
                        email=c_email,
                        linkedin=c_linkedin,
                        phone=c_phone,
                        confidence_score=c_conf,
                        source_url=source_url
                    ))

        is_valid = len(errors) == 0
        self.logger.info(f"Validation completed for entity #{entity_id}. Valid: {is_valid}, Warnings: {len(warnings)}, Sources: {len(sources)}, Contacts: {len(contacts)}")

        return ValidationResult(
            is_valid=is_valid,
            cleaned_data=cleaned,
            sources=sources,
            contacts=contacts,
            errors=errors,
            warnings=warnings,
            confidence_score=confidence
        )
