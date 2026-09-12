

import uuid
from datetime import datetime
from services import booking_service


class PaymentError(Exception):
    pass


def _call_payment_gateway(amount: float, method: str) -> dict:
    """Giả lập gọi Payment Gateway, luôn trả về thành công cho mục đích demo."""
    return {
        "success": True,
        "reference_id": f"PG-{uuid.uuid4().hex[:10].upper()}",
    }


def process_payment(conn, booking_id: int, method: str) -> dict:
    """
    Tương ứng Payment.processPayment(): boolean.
    - Lấy booking để biết amount cần thanh toán.
    - Gọi payment gateway (giả lập).
    - Nếu thành công: lưu record payment, gọi booking_service.confirm_booking().
    """
    booking = booking_service.get_booking(conn, booking_id)
    if booking is None:
        raise PaymentError("Booking not found.")
    if booking["status"] != "Pending Payment":
        raise PaymentError("Booking is not awaiting payment.")

    amount = booking["total_price"]
    result = _call_payment_gateway(amount, method)
    if not result["success"]:
        raise PaymentError("Payment failed. Please try again.")

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO payments (booking_id, amount, payment_date, payment_method,
                               transaction_code, status)
        VALUES (%s, %s, %s, %s, %s, 'Paid')
        """,
        (booking_id, amount, datetime.now(), method, result["reference_id"]),
    )
    conn.commit()
    payment_id = cursor.lastrowid
    cursor.close()

    booking_service.confirm_booking(conn, booking_id)

    return get_payment(conn, payment_id)


def process_refund(conn, payment_id: int, refund_amount: float) -> bool:
    """
    Tương ứng Payment.processRefund(amount): boolean.
    Được cancellation_service gọi lại khi member huỷ booking.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE payments SET status = %s WHERE payment_id = %s",
        ("Refunded" if refund_amount > 0 else "No Refund", payment_id),
    )
    conn.commit()
    ok = cursor.rowcount > 0
    cursor.close()
    return ok


def get_payment(conn, payment_id: int):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM payments WHERE payment_id = %s", (payment_id,))
    row = cursor.fetchone()
    cursor.close()
    return row


def get_payment_by_booking(conn, booking_id: int):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM payments WHERE booking_id = %s ORDER BY payment_date DESC LIMIT 1",
        (booking_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    return row


def generate_receipt(payment: dict, booking: dict) -> str:
    """Tương ứng Payment.generateReceipt(): String."""
    return (
        f"----- HOÁ ĐƠN ĐIỆN TỬ -----\n"
        f"Mã booking     : {booking['booking_id']}\n"
        f"Ngày nhận phòng: {booking['check_in']}\n"
        f"Ngày trả phòng : {booking['check_out']}\n"
        f"Số tiền        : {payment['amount']:,.0f} VND\n"
        f"Phương thức    : {payment['payment_method']}\n"
        f"Mã giao dịch   : {payment['transaction_code']}\n"
        f"Ngày thanh toán: {payment['payment_date']}\n"
        f"----------------------------"
    )