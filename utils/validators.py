import re

def validate_email(email: str) -> bool:
    """Kiểm tra định dạng email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def validate_password(password: str) -> bool:
    """Mật khẩu phải chứa ít nhất 6 ký tự[cite: 1]."""
    return len(password) >= 6

def validate_phone(phone: str) -> bool:
    """Kiểm tra định dạng số điện thoại (9-11 chữ số)."""
    pattern = r'^\d{9,11}$'
    return bool(re.match(pattern, phone.strip()))