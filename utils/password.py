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
    try:
        # Tách salt và chuỗi hash cũ từ dữ liệu đã lưu
        salt, hashed = stored_password.split(':')
        
        # Tính toán lại hash bằng mật khẩu người dùng nhập và salt
        recalculated_hash = hashlib.sha256((salt + provided_password).encode('utf-8')).hexdigest()
        
        # So sánh hai chuỗi hash, trả về True nếu trùng khớp
        return recalculated_hash == hashed
    except ValueError:
        # Xử lý trường hợp định dạng chuỗi lưu trữ không hợp lệ
        return False