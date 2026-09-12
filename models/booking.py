from .booking import Booking

class Booking:

    # Define the possible booking statuses.
    STATUSES = [
        "Pending",
        "Confirmed",
        "Checked-in",
        "Completed",
        "Canceled"
    ]
    # Initialize a Booking object with its attributes.
    def __init__(
        self,
        booking_id=None,
        user_id=None,
        room_id=None,
        room_type_id=None,
        check_in=None,
        check_out=None,
        total_price=0.0,
        refund_price=0.0,
        status="Pending",
        created_at=None,
        canceled_at=None
    ):
        # Validate the booking status.
        if status not in self.STATUSES:
            raise ValueError(f"Invalid booking status: {status}")

        # Assign the attributes to the Booking object.
        self.booking_id = booking_id
        self.user_id = user_id
        self.room_id = room_id
        self.room_type_id = room_type_id
        self.check_in = check_in
        self.check_out = check_out
        self.total_price = total_price
        self.refund_price = refund_price
        self.status = status
        self.created_at = created_at
        self.canceled_at = canceled_at

    # Create a Booking object from a database row.
    @classmethod
    def from_row(cls, row):
        return cls(
            booking_id=row[0],
            user_id=row[1],
            room_id=row[2],
            room_type_id=row[3],
            check_in=row[4],
            check_out=row[5],
            total_price=row[6],
            refund_price=row[7],
            status=row[8],
            created_at=row[9],
            canceled_at=row[10]
        )

    # Convert the Booking object to a dictionary.
    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "user_id": self.user_id,
            "room_id": self.room_id,
            "room_type_id": self.room_type_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "total_price": self.total_price,
            "refund_price": self.refund_price,
            "status": self.status,
            "created_at": self.created_at,
            "canceled_at": self.canceled_at
        }

    # Booking status helper methods.
    def is_confirmed(self):
        return self.status == "Confirmed"

    # Check whether the booking is currently checked in.
    def is_checked_in(self):
        return self.status == "Checked-in"

    # Check whether the booking is completed.
    def is_completed(self):
        return self.status == "Completed"

    # Check whether the booking is canceled.
    def is_canceled(self):
        return self.status == "Canceled"