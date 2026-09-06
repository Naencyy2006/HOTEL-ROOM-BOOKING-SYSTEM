
class User:
    ROLES = ["Member", "Receptionist", "Admin"]

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