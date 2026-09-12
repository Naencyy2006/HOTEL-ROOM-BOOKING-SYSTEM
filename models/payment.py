from .payment import Payment

class Payment:
    # Valid payment statuses.
    STATUSES = ["Paid", "Failed", "Refunded"]

    # Initialize a Payment object with its attributes.
    def __init__(
        self,
        payment_id=None,
        booking_id=None,
        amount=0.0,
        payment_date=None,
        payment_method=None,
        transaction_code=None,
        status="Paid"
    ):
        # Validate the payment status.
        if status not in self.STATUSES:
            raise ValueError(f"Invalid payment status: {status}")

        # Assign the attributes to the Payment object.
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.transaction_code = transaction_code
        self.status = status

    # Create a Payment object from a database row.
    @classmethod
    def from_row(cls, row):
        return cls(
            payment_id=row[0],
            booking_id=row[1],
            amount=row[2],
            payment_date=row[3],
            payment_method=row[4],
            transaction_code=row[5],
            status=row[6]
        )

    # Convert the Payment object to a dictionary.
    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "booking_id": self.booking_id,
            "amount": self.amount,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "transaction_code": self.transaction_code,
            "status": self.status
        }

    # Payment status helper methods.
    def is_paid(self):
        return self.status == "Paid"

    # Check whether the payment was refunded.
    def is_refunded(self):
        return self.status == "Refunded"