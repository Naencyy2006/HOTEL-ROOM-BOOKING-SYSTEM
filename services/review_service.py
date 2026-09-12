def add_review(conn, user_id, room_id, booking_id, rating, comment):
    """Create a review for a completed booking."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO reviews "
            "(user_id, room_id, booking_id, rating, comment, status) "
            "VALUES (%s, %s, %s, %s, %s, 'Published')",
            (user_id, room_id, booking_id, rating, comment),
        )
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
