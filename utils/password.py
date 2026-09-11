import hashlib
import os

def hash_password(password: str) -> str:
    """Mã hóa mật khẩu bằng SHA-256 kèm Salt."""
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Xác thực mật khẩu nhập vào với chuỗi đã mã hóa trong CSDL."""
    try:
        salt, hashed = stored_password.split(':')
        recalculated_hash = hashlib.sha256((salt + provided_password).encode('utf-8')).hexdigest()
        return recalculated_hash == hashed
    except ValueError:
        return False