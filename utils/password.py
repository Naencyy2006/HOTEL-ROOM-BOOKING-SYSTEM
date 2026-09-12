import hashlib
import os

def hash_password(password: str) -> str:
    # Tạo chuỗi salt ngẫu nhiên 16 byte dưới dạng hex
    salt = os.urandom(16).hex()
    
    # Kết hợp salt với mật khẩu và mã hóa bằng SHA-256
    hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    
    # Trả về chuỗi kết hợp salt và hash dạng 'salt:hash' để lưu vào CSDL
    return f"{salt}:{hashed}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    if not stored_password:
        return False

    # Hỗ trợ cả định dạng mật khẩu cũ (SHA-256 plain) và mới (salt:hash)
    if ':' in stored_password:
        try:
            salt, hashed = stored_password.split(':', 1)
            recalculated_hash = hashlib.sha256((salt + provided_password).encode('utf-8')).hexdigest()
            return recalculated_hash == hashed
        except ValueError:
            return False

    # Dữ liệu cũ từ seed.sql: lưu plain SHA-256 (không salt)
    legacy_hash = hashlib.sha256(provided_password.encode('utf-8')).hexdigest()
    return legacy_hash == stored_password