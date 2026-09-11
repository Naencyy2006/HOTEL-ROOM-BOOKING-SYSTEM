from .user import User

class User:
    # Danh sách các vai trò (roles) và trạng thái (statuses) hợp lệ
    ROLES = ["Member", "Receptionist", "Admin"]

    # Danh sách các trạng thái hợp lệ
    STATUSES = ["Active", "Locked", "Inactive"]

    # Khởi tạo đối tượng User với các thuộc tính
    def __init__(
        self,
        user_id=None,
        full_name=None,
        email=None,
        phone=None,
        gender=None,
        year_of_birth=None,
        password_hash=None,
        role="Member",
        status="Active",
        created_at=None
    ):
        # Kiểm tra tính hợp lệ của role và status
        if role not in self.ROLES:
            raise ValueError(f"Invalid role: {role}")

        # Kiểm tra tính hợp lệ của status
        if status not in self.STATUSES:
            raise ValueError(f"Invalid status: {status}")

        # Gán các thuộc tính cho đối tượng User
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.gender = gender
        self.year_of_birth = year_of_birth
        self.password_hash = password_hash
        self.role = role
        self.status = status
        self.created_at = created_at

    # Lớp phương thức để tạo đối tượng User từ một hàng dữ liệu (row) từ cơ sở dữ liệu
    @classmethod
    def from_row(cls, row):
        return cls(
            user_id=row[0],
            full_name=row[1],
            email=row[2],
            phone=row[3],
            gender=row[4],
            year_of_birth=row[5],
            password_hash=row[6],
            role=row[7],
            status=row[8],
            created_at=row[9]
        )

    # Phương thức để chuyển đổi đối tượng User thành một từ điển (dictionary)
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "gender": self.gender,
            "year_of_birth": self.year_of_birth,
            "password_hash": self.password_hash,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at
        }

    # Phương thức kiểm tra xem người dùng có đang hoạt động hay không
    def is_active(self):
        return self.status == "Active"

    # Phương thức kiểm tra xem người dùng có phải là thành viên hay không
    def is_member(self):
        return self.role == "Member"

    # Phương thức kiểm tra xem người dùng có phải là nhân viên lễ tân hay không
    def is_receptionist(self):
        return self.role == "Receptionist"

    # Phương thức kiểm tra xem người dùng có phải là quản trị viên hay không
    def is_admin(self):
        return self.role == "Admin"