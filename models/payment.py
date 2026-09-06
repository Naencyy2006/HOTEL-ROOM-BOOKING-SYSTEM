class Payment:
    def __init__(
        self,
        payment_id=None,
        booking_id=None,
        amount=0.0,
        payment_date=None,
        payment_method="",
        transaction_code=None,
        status="Paid"
    ):
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.transaction_code = transaction_code
        self.status = status

    @classmethod
    def from_row(cls, row):
        return cls(*row)

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