def get_user_by_id(conn, user_id):
    """Return a user record by ID."""
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT user_id, full_name, email, phone, gender, year_of_birth, "
            "role, status, created_at FROM users WHERE user_id = %s",
            (user_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()


def update_user(conn, user_id, data):
    """Update the editable profile fields for a user."""
    allowed_fields = {"full_name", "email", "phone", "gender", "year_of_birth"}
    changes = [(field, value) for field, value in data.items() if field in allowed_fields]
    if not changes:
        return False

    assignments = ", ".join(f"{field} = %s" for field, _ in changes)
    values = [value for _, value in changes] + [user_id]
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"UPDATE users SET {assignments} WHERE user_id = %s",
            tuple(values),
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
