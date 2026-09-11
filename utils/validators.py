import re

# VALIDATE EMAIL
def validate_email(email: str) -> bool:
    # Kiểm tra định dạng email chuẩn bằng Regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

# VALIDATE PASSWORD
def validate_password(password: str) -> bool:
    # Ràng buộc hệ thống: Mật khẩu phải chứa ít nhất 6 ký tự
    return len(password) >= 6

def validate_phone(phone: str) -> bool:
    # Kiểm tra định dạng số điện thoại chứa từ 9 đến 11 chữ số
    pattern = r'^\d{9,11}$'
    return bool(re.match(pattern, phone.strip()))

# VALIDATE FULL NAME
def validate_full_name(full_name: str) -> bool:
    if not full_name or not full_name.strip():
        return False
    pattern = r'^[A-Za-zÀ-ỹ\s]+$'
    return bool(re.match(pattern, full_name.strip()))

# VALIDATE YEAR OF BIRTH
def validate_year_of_birth(year_of_birth: int) -> bool:
    try:
        year = int(year_of_birth)
    except (ValueError, TypeError):
        return False
    return 1900 <= year <= 2026

# VALIDATE GENDER
def validate_gender(gender: str) -> bool:

    allowed_genders = [
        "Male",
        "Female",
        "Other"
    ]

    return gender in allowed_genders

# VALIDATE USER ROLE
def validate_role(role: str) -> bool:
    allowed_roles = [
        "Member",
        "Receptionist",
        "Admin"
    ]
    return role in allowed_roles

# VALIDATE USER STATUS
def validate_user_status(status: str) -> bool:
    allowed_statuses = [
        "Active",
        "Locked",
        "Inactive"
    ]
    return status in allowed_statuses

# VALIDATE ROOM STATUS
def validate_room_status(status: str) -> bool:

    allowed_statuses = [
        "Available",
        "Occupied",
        "Maintenance"
    ]
    return status in allowed_statuses

# VALIDATE BOOKING STATUS
def validate_booking_status(status: str) -> bool:
    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Checked-in",
        "Completed",
        "Canceled"
    ]

    return status in allowed_statuses

# VALIDATE PAYMENT STATUS
def validate_payment_status(status: str) -> bool:
    allowed_statuses = [
        "Paid",
        "Failed",
        "Refunded"
    ]
    return status in allowed_statuses

# VALIDATE RATING
def validate_rating(rating: int) -> bool:
    try:
        rating = int(rating)
    except (ValueError, TypeError):
        return False
    return 1 <= rating <= 5

# VALIDATE DATE RANGE
def validate_date_range(check_in, check_out) -> bool:
    if not check_in or not check_out:
        return False
    return check_out > check_in


# CALCULATE NUMBER OF NIGHTS
def calculate_nights(check_in, check_out) -> int:
    if not validate_date_range(
        check_in,
        check_out
    ):
        return 0
    return (check_out - check_in).days

