#validation utilities
import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number (8 digits starting with 2, 5, or 9)"""
    if not phone:
        return True  # Phone is optional
    pattern = r'^[259]\d{7}$'
    return re.match(pattern, phone.replace(' ', '')) is not None


def validate_date(date_str: str) -> bool:
    """Validate date format(YYYY-MM-DD)"""
    if not date_str:
        return False
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_not_empty(value: str) -> bool:
    """check if value is Not empty"""
    return bool(value and value.strip())


def validate_number(value: str, min_val: float = None, max_val: float = None) -> bool:
    """ValiDAte numeric input"""
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True
    except ValueError:
        return False

def validate_text_only_letters(text: str) -> bool:
    pattern = r'^[A-Za-z\s]+$'
    return bool(re.match(pattern, text.strip()))

def validate_integer(value: str, min_val: int = None, max_val: int = None) -> bool:
    """Validate integer input"""
    try:
        num = int(value)
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True
    except ValueError:
        return False