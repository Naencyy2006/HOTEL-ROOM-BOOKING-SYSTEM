

from datetime import datetime
from services import booking_service, payment_service, room_service


class CancellationError(Exception):
    pass


def calculate_refund(total_price: float, check_in: datetime, now: datetime = None) -> dict:
    """
    Tương ứng Booking.calculateRefund(): double.
    Trả về dict {hours_before, refund_amount, refund_percent} để hiển thị
    cho member xem trước khi họ bấm xác nhận huỷ (đúng luồng use-case:
    "hệ thống hiển thị điều khoản huỷ trước khi member xác nhận").
    """
    now = now or datetime.now()
    hours_before = (check_in - now).total_seconds() / 3600

    if hours_before > 48:
        percent = 1.0
    elif hours_before >= 24:
        percent = 0.5
    else:
        percent = 0.0

    return {
        "hours_before_checkin": round(hours_before, 1),
        "refund_percent": percent,
        "refund_amount": round(total_price * percent, 2),
    }


def cancel_booking(conn, booking_id: int) -> dict:
    """
    Tương ứng Booking.processCancellation(): boolean.
    Thực hiện toàn bộ luồng chính của use-case Cancel Booking:
      1. Kiểm tra booking đang Confirmed & đã Paid.
      2. Kiểm tra còn được phép huỷ (chưa qua check-in).
      3. Tính tiền hoàn theo chính sách.
      4. Cập nhật booking -> Canceled, trả phòng -> Available.
      5. Gọi payment_service.process_refund() nếu có hoàn tiền.
    """
    booking = booking_service.get_booking(conn, booking_id)
    if booking is None:
        raise CancellationError("Booking not found.")
    if booking["status"] != "Confirmed":
        raise CancellationError("Only confirmed bookings can be cancelled.")

    now = datetime.now()
    check_in_dt = datetime.combine(booking["check_in"], datetime.min.time())
    if now >= check_in_dt:
        raise CancellationError("A booking cannot be cancelled after check-in.")

    refund_info = calculate_refund(booking["total_price"], check_in_dt, now)

    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE bookings
        SET status = 'Canceled', refund_price = %s, canceled_at = %s
        WHERE booking_id = %s
        """,
        (refund_info["refund_amount"], now, booking_id),
    )
    conn.commit()
    cursor.close()

    # Trả phòng vật lý (nếu đã gán room_number ở bước check-in) về Available
    # if booking.get("room_number"):
    #     room_service.release_room(conn, booking["room_number"])

    if booking.get("room_id"):
        room_service.release_room(conn, booking["room_id"])

    # Ghi nhận hoàn tiền
    payment = payment_service.get_payment_by_booking(conn, booking_id)
    if payment:
        payment_service.process_refund(conn, payment["payment_id"], refund_info["refund_amount"])

    return {
        "booking_id": booking_id,
        "status": "Canceled",
        **refund_info,
    }