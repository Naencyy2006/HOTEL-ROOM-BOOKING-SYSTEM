

from datetime import datetime, time
from services import booking_service, payment_service, room_service


class CancellationError(Exception):
    pass


def calculate_refund(total_price: float, check_in: datetime, now: datetime = None) -> dict:
    """
    Corresponds to Booking.calculateRefund(): double.
    Return {hours_before, refund_amount, refund_percent} so the member can review
    it before confirming cancellation, as required by the use case.
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
        Corresponds to Booking.processCancellation(): boolean.
        Execute the main Cancel Booking use case:
            1. Check that the booking is Confirmed or Pending Payment.
            2. Check that cancellation is still allowed (before check-in).
            3. Calculate the refund according to policy.
            4. Update the booking to Canceled and the room to Available.
            5. Call payment_service.process_refund() when a refund applies.
    """
    booking = booking_service.get_booking(conn, booking_id)
    if booking is None:
        raise CancellationError("Booking not found.")
    if booking["status"] not in ("Confirmed", "Pending Payment"):
        raise CancellationError("Only active bookings can be cancelled.")

    now = datetime.now()
    check_in_dt = datetime.combine(booking["check_in"], time(14, 0))
    if now >= check_in_dt:
        raise CancellationError("A booking cannot be cancelled after check-in.")

    # An unpaid booking can be canceled but does not generate a refund.
    refund_total = booking["total_price"] if booking["status"] == "Confirmed" else 0
    refund_info = calculate_refund(refund_total, check_in_dt, now)

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

    # Return the assigned physical room to Available.
    if booking.get("room_id"):
        room_service.release_room(conn, booking["room_id"])

    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cancellation_history (
            cancellation_id INT AUTO_INCREMENT PRIMARY KEY,
            booking_id INT NOT NULL,
            canceled_at DATETIME NOT NULL,
            hours_before_checkin DECIMAL(8, 2) NOT NULL,
            refund_percent DECIMAL(5, 2) NOT NULL,
            refund_amount DECIMAL(12, 2) NOT NULL,
            policy_description VARCHAR(255) NOT NULL,
            CONSTRAINT fk_cancellation_booking
                FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
                ON UPDATE CASCADE ON DELETE RESTRICT
        )
        """
    )
    if refund_info["refund_percent"] == 1.0:
        policy_description = "More than 48 hours before check-in: no cancellation fee."
    elif refund_info["refund_percent"] == 0.5:
        policy_description = "Between 24 and 48 hours before check-in: 50% refund."
    else:
        policy_description = "Within 24 hours of check-in: no refund."
    cursor.execute(
        """
        INSERT INTO cancellation_history
            (booking_id, canceled_at, hours_before_checkin, refund_percent,
             refund_amount, policy_description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            booking_id,
            now,
            refund_info["hours_before_checkin"],
            refund_info["refund_percent"] * 100,
            refund_info["refund_amount"],
            policy_description,
        ),
    )
    conn.commit()
    cursor.close()

    # Record the refund.
    payment = payment_service.get_payment_by_booking(conn, booking_id)
    if payment:
        payment_service.process_refund(conn, payment["payment_id"], refund_info["refund_amount"])

    return {
        "booking_id": booking_id,
        "status": "Canceled",
        **refund_info,
    }