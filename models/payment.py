class Payment:
    STATUSES = ["Paid", "Failed", "Refunded"]

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
        if status not in self.STATUSES:
            raise ValueError(f"Invalid payment status: {status}")

        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.transaction_code = transaction_code
        self.status = status

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

    def is_paid(self):
        return self.status == "Paid"

    def is_refunded(self):
        return self.status == "Refunded"