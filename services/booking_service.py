from datetime import date, datetime
from services import room_service


class BookingError(Exception):
    pass


def calculate_total(check_in: date, check_out: date, price_per_night: float) -> float:
    """Tương ứng Booking.calculateTotal(): double."""
    nights = (check_out - check_in).days
    if nights <= 0:
        raise BookingError("Ngày check-out phải sau ngày check-in.")
    return round(nights * price_per_night, 2)


def book_room(conn, user_id: int, room_type_id: int, check_in: date, check_out: date) -> dict:
    """
    Tương ứng Member.bookRoom(roomTypeId, checkIn, checkOut): Booking.
    Trả về dict thông tin booking vừa tạo (Pending Payment).
    """
    room_type = room_service.get_room_type_info(conn, room_type_id)
    if room_type is None:
        raise BookingError("Loại phòng không tồn tại.")

    if not room_service.is_room_type_available(conn, room_type_id, check_in, check_out):
        raise BookingError("Loại phòng đã hết trong khoảng ngày đã chọn.")

    total_price = calculate_total(check_in, check_out, room_type["price_per_night"])

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO booking (user_id, room_id, room_type_id, check_in, check_out,
                              total_price, status, created_at)
        VALUES (%s, NULL, %s, %s, %s, %s, 'Pending Payment', %s)
        """,
        (user_id, room_type_id, check_in, check_out, total_price, datetime.now()),
    )
    conn.commit()
    booking_id = cursor.lastrowid
    cursor.close()

    return get_booking(conn, booking_id)


def confirm_booking(conn, booking_id: int) -> bool:
    """
    Tương ứng Booking.confirmBooking(): boolean.
    Gọi sau khi payment_service.process_payment() trả về thành công.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE booking SET status = 'Confirmed' WHERE booking_id = %s "
        "AND status = 'Pending Payment'",
        (booking_id,),
    )
    conn.commit()
    ok = cursor.rowcount > 0
    cursor.close()
    return ok


def get_booking(conn, booking_id: int):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM booking WHERE booking_id = %s", (booking_id,))
    row = cursor.fetchone()
    cursor.close()
    return row


def list_bookings_by_member(conn, user_id: int, status: str = None) -> list:
    """
    Dùng cho use-case "View Booking History" / màn hình My Bookings, History
    trong views/member.py.
    """
    cursor = conn.cursor(dictionary=True)
    if status:
        cursor.execute(
            "SELECT * FROM booking WHERE user_id = %s AND status = %s "
            "ORDER BY created_at DESC",
            (user_id, status),
        )
    else:
        cursor.execute(
            "SELECT * FROM booking WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,),
        )
    rows = cursor.fetchall()
    cursor.close()
    return rows