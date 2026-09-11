from config.database import get_db_connection
from utils.password import hash_password, verify_password
from utils.validators import validate_email, validate_password, validate_phone

class AuthService:
    def __init__(self):
        self.current_user = None

    def register(self, full_name: str, dob: str, gender: str, phone: str, email: str, password: str, confirm_password: str):
        """Đăng ký tài khoản Member mới[cite: 1]."""
        if not validate_email(email):
            return False, "Định dạng Email không hợp lệ."
        if not validate_password(password):
            return False, "Mật khẩu phải có tối thiểu 6 ký tự[cite: 1]."
        if password != confirm_password:
            return False, "Mật khẩu xác nhận không khớp[cite: 1]."
        if not validate_phone(phone):
            return False, "Số điện thoại không hợp lệ."

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Kiểm tra trùng lặp email[cite: 1]
            cursor.execute("SELECT user_id FROM USERS WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "Email đã được sử dụng trong hệ thống[cite: 1]."

            # Mã hóa mật khẩu và lưu người dùng[cite: 1]
            hashed_pwd = hash_password(password)
            year_of_birth = int(dob.split('-')[0]) if '-' in dob else None

            query = """
                INSERT INTO USERS (full_name, email, phone, gender, year_of_birth, password_hash, role, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Member', 'Active')
            """
            cursor.execute(query, (full_name, email, phone, gender, year_of_birth, hashed_pwd))
            conn.commit()
            return True, "Đăng ký tài khoản thành công![cite: 1]"
        except Exception as e:
            conn.rollback()
            return False, f"Lỗi hệ thống: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    def login(self, email: str, password: str):
        """Xác thực người dùng và phân quyền truy cập[cite: 1]."""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM USERS WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user or not verify_password(user['password_hash'], password):
                return False, "Email hoặc mật khẩu không chính xác[cite: 1].", None

            if user['status'] == 'Locked':
                return False, "Tài khoản của bạn đã bị khóa do vi phạm chính sách[cite: 1].", None

            self.current_user = user
            return True, "Đăng nhập thành công!", user
        finally:
            cursor.close()
            conn.close()

    def logout(self):
        """Đăng xuất người dùng khỏi phiên làm việc[cite: 1]."""
        self.current_user = None
        return True, "Đã đăng xuất thành công."

    def reset_password(self, email: str, new_password: str, confirm_password: str):
        """Khôi phục mật khẩu khi quên[cite: 1]."""
        if not validate_password(new_password):
            return False, "Mật khẩu mới phải có ít nhất 6 ký tự[cite: 1]."
        if new_password != confirm_password:
            return False, "Mật khẩu xác nhận không khớp[cite: 1]."

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT user_id FROM USERS WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                return False, "Email không tồn tại trong hệ thống[cite: 1]."

            hashed_pwd = hash_password(new_password)
            cursor.execute("UPDATE USERS SET password_hash = %s WHERE email = %s", (hashed_pwd, email))
            conn.commit()
            return True, "Đặt lại mật khẩu thành công[cite: 1]."
        except Exception as e:
            conn.rollback()
            return False, f"Lỗi: {str(e)}"
        finally:
            cursor.close()
            conn.close()