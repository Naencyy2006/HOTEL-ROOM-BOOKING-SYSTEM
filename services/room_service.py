

from datetime import date


def get_available_count(conn, room_type_id: int, check_in: date, check_out: date) -> int:
    """
    Tương ứng RoomType.getAvailableCount(checkIn, checkOut): int (Class Diagram).
    Đếm số phòng còn trống của 1 room_type trong khoảng [check_in, check_out).
    Công thức: tổng số phòng thuộc room_type đó (status != 'Maintenance')
               - số phòng đã bị giữ bởi booking có overlap ngày và status
                 thuộc ('Pending Payment', 'Confirmed', 'Checked-in').
    """
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) FROM rooms
        WHERE room_type_id = %s AND status != 'Maintenance'
        """,
        (room_type_id,),
    )
    total_rooms = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*) FROM booking
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
    """True nếu còn ít nhất 1 phòng trống cho khoảng ngày yêu cầu."""
    return get_available_count(conn, room_type_id, check_in, check_out) > 0


def update_room_status(conn, room_number: str, new_status: str) -> bool:
    """
    Tương ứng Room.updateStatus(newStatus): void.
    new_status ví dụ: 'Available' | 'Occupied' | 'Maintenance'.
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
    """
    Tương ứng Room.releaseRoom(): void.
    Gọi khi huỷ booking / check-out xong -> trả phòng về 'Available'.
    """
    return update_room_status(conn, room_number, "Available")


def get_room_type_info(conn, room_type_id: int):
    """Lấy thông tin room_type (giá/đêm, sức chứa, mô tả...) để tính tổng tiền."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM room_types WHERE room_type_id = %s", (room_type_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    return row