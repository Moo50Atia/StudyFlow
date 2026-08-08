"""
utils.py
Helper functions, regex validation routines, and logging utilities.
"""

import os
import re
import logging
from typing import Optional
from urllib.parse import urlparse

# Regular Expressions
URL_REGEX = re.compile(
    r'^https?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_REGEX = re.compile(r'^\+?[0-9\s\-()]{7,25}$')
LINKEDIN_REGEX = re.compile(r'^https?://(www\.)?linkedin\.com/(in|company)/[a-zA-Z0-9_-]+/?$', re.IGNORECASE)

PLACEHOLDERS = {'tbd', 'placeholder', 'todo', 'n/a', 'na', 'none', 'null', 'undefined', '-', '--', 'temp'}

def is_valid_url(url: Optional[str]) -> bool:
    if not url or not isinstance(url, str):
        return False
    u = url.strip()
    return bool(URL_REGEX.match(u))

def is_valid_email(email: Optional[str]) -> bool:
    if not email or not isinstance(email, str):
        return False
    e = email.strip().lower()
    if any(p in e for p in ['example.com', 'test.com', 'fake.com']):
        return False
    return bool(EMAIL_REGEX.match(e))

def is_valid_phone(phone: Optional[str]) -> bool:
    if not phone or not isinstance(phone, str):
        return False
    p = phone.strip()
    if any(seq in p for seq in ['123456', '000000', '111111']):
        return False
    return bool(PHONE_REGEX.match(p))

def is_valid_linkedin(url: Optional[str]) -> bool:
    if not url or not isinstance(url, str):
        return False
    u = url.strip()
    return bool(LINKEDIN_REGEX.match(u)) or ('linkedin.com/' in u.lower() and is_valid_url(u))

def is_placeholder(val: Optional[str]) -> bool:
    if not val or not isinstance(val, str):
        return False
    v = val.strip().lower()
    return v in PLACEHOLDERS

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """Configures a file and console logger."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')

        # File Handler
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Stream Handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

def ensure_directories(paths: list):
    """Ensure directory list exists on disk."""
    for p in paths:
        os.makedirs(p, exist_ok=True)
