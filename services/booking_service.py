from datetime import date, datetime
from services import room_service


class BookingError(Exception):
    pass


def calculate_total(check_in: date, check_out: date, price_per_night: float) -> float:
    """Corresponds to Booking.calculateTotal(): double."""
    nights = (check_out - check_in).days
    if nights <= 0:
        raise BookingError("Check-out date must be after check-in date.")
    return round(nights * price_per_night, 2)


def book_room(conn, user_id: int, room_type_id: int, check_in: date, check_out: date) -> dict:
    """
    Corresponds to Member.bookRoom(roomTypeId, checkIn, checkOut): Booking.
    Return the newly created booking as a dictionary (Pending Payment).
    """
    room_type = room_service.get_room_type_info(conn, room_type_id)
    if room_type is None:
        raise BookingError("Room type does not exist.")

    if not room_service.is_room_type_available(conn, room_type_id, check_in, check_out):
        raise BookingError("No rooms of this type are available for the selected dates.")

    total_price = calculate_total(check_in, check_out, room_type["price_per_night"])

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO bookings (user_id, room_id, room_type_id, check_in, check_out,
                              total_price, status, created_at)
        VALUES (%s, NULL, %s, %s, %s, %s, 'Pending Payment', %s)
        """,
        (user_id, room_type_id, check_in, check_out, total_price, datetime.now()),
    )
    conn.commit()
    booking_id = cursor.lastrowid
    cursor.close()

    return get_booking(conn, booking_id)


def create_booking(conn, user_id: int, room_type_id: int, check_in, check_out) -> dict:
    """Create a booking from date objects or YYYY-MM-DD strings."""
    if isinstance(check_in, str):
        check_in = date.fromisoformat(check_in)
    if isinstance(check_out, str):
        check_out = date.fromisoformat(check_out)
    return book_room(conn, user_id, room_type_id, check_in, check_out)


def confirm_booking(conn, booking_id: int) -> bool:
    """
    Corresponds to Booking.confirmBooking(): boolean.
    Called after payment_service.process_payment() succeeds.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE bookings SET status = 'Confirmed' WHERE booking_id = %s "
        "AND status = 'Pending Payment'",
        (booking_id,),
    )
    conn.commit()
    ok = cursor.rowcount > 0
    cursor.close()
    return ok


def get_booking(conn, booking_id: int):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookings WHERE booking_id = %s", (booking_id,))
    row = cursor.fetchone()
    cursor.close()
    return row


def list_bookings_by_member(conn, user_id: int, status: str = None) -> list:
    """
    Used by the "View Booking History" use case and the My Bookings and History screens.
    trong views/member.py.
    """
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT
            b.*,
            rt.type_name,
            rt.capacity,
            r.room_number,
            p.payment_date,
            p.payment_method,
            p.transaction_code,
            p.status AS payment_status,
            ch.hours_before_checkin,
            ch.refund_percent,
            ch.policy_description
        FROM bookings b
        LEFT JOIN room_types rt ON rt.room_type_id = b.room_type_id
        LEFT JOIN rooms r ON r.room_number = b.room_id
        LEFT JOIN payments p ON p.payment_id = (
            SELECT p2.payment_id
            FROM payments p2
            WHERE p2.booking_id = b.booking_id
            ORDER BY p2.payment_date DESC, p2.payment_id DESC
            LIMIT 1
        )
        LEFT JOIN cancellation_history ch ON ch.cancellation_id = (
            SELECT ch2.cancellation_id
            FROM cancellation_history ch2
            WHERE ch2.booking_id = b.booking_id
            ORDER BY ch2.canceled_at DESC, ch2.cancellation_id DESC
            LIMIT 1
        )
        WHERE b.user_id = %s
    """
    if status:
        query += " AND b.status = %s"
        params = (user_id, status)
    else:
        params = (user_id,)
    query += " ORDER BY b.created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    return rows