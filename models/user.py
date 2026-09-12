from .user import User

class User:
    # Valid user roles.
    ROLES = ["Member", "Receptionist", "Admin"]

    # Valid user statuses.
    STATUSES = ["Active", "Locked", "Inactive"]

    # Initialize a User object with its attributes.
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
        # Validate the role and status.
        if role not in self.ROLES:
            raise ValueError(f"Invalid role: {role}")

        # Validate the user status.
        if status not in self.STATUSES:
            raise ValueError(f"Invalid status: {status}")

        # Assign the attributes to the User object.
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

    # Create a User object from a database row.
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

    # Convert the User object to a dictionary.
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

    # Check whether the user is active.
    def is_active(self):
        return self.status == "Active"

    # Check whether the user is a member.
    def is_member(self):
        return self.role == "Member"

    # Check whether the user is a receptionist.
    def is_receptionist(self):
        return self.role == "Receptionist"

    # Check whether the user is an administrator.
    def is_admin(self):
        return self.role == "Admin"