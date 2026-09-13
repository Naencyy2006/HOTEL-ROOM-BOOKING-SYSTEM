

from datetime import date
from datetime import datetime


def get_available_count(conn, room_type_id: int, check_in: date, check_out: date) -> int:
    """
        Corresponds to RoomType.getAvailableCount(checkIn, checkOut): int (Class Diagram).
        Count available rooms of a room type during [check_in, check_out).
        Formula: total rooms of that type (status != 'Maintenance')
                         minus rooms held by bookings that overlap the dates and have a status
                         in ('Pending Payment', 'Confirmed', 'Checked-in').
    """
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) FROM rooms
        WHERE room_type_id = %s AND status = 'Available'
        """,
        (room_type_id,),
    )
    total_rooms = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*) FROM bookings
        WHERE room_type_id = %s
          AND status IN ('Pending Payment', 'Confirmed', 'Checked-in')
          AND check_in < %s AND check_out > %s
        """,
        (room_type_id, check_out, check_in),
    )
    overlapping_bookings = cursor.fetchone()[0]

    cursor.close()
    return max(total_rooms - overlapping_bookings, 0)


def is_room_type_available(conn, room_type_id: int, check_in: date, check_out: date) -> bool:
    """Return True if at least one room is available for the requested dates."""
    return get_available_count(conn, room_type_id, check_in, check_out) > 0


def search_rooms(conn, check_in=None, check_out=None) -> list:
    """Return room types that have availability for the requested dates."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT room_type_id, type_name, capacity, price_per_night, description "
        "FROM room_types ORDER BY room_type_id"
    )
    room_types = cursor.fetchall()
    cursor.close()

    if not check_in or not check_out:
        return room_types
    if isinstance(check_in, str):
        check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    if isinstance(check_out, str):
        check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
    return [
        room_type for room_type in room_types
        if is_room_type_available(conn, room_type["room_type_id"], check_in, check_out)
    ]


def update_room_status(conn, room_number: str, new_status: str) -> bool:
    """
    Corresponds to Room.updateStatus(newStatus): void.
    new_status examples: 'Available' | 'Occupied' | 'Maintenance'.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE rooms SET status = %s WHERE room_number = %s",
        (new_status, room_number),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    cursor.close()
    return updated


def release_room(conn, room_number: str) -> bool:
    """Release a room by number and set its status to Available."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE rooms SET status = 'Available' WHERE room_number = %s",
        (room_number,)
    )
    conn.commit()
    updated = cursor.rowcount > 0
    cursor.close()
    return updated

def get_room_type_info(conn, room_type_id: int):
    """Get room type information for calculating the total price."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM room_types WHERE room_type_id = %s", (room_type_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    return row