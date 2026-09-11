from .payment import Payment

class Payment:
    # Các trạng thái thanh toán hợp lệ
    STATUSES = ["Paid", "Failed", "Refunded"]

    # Khởi tạo đối tượng Payment với các thuộc tính
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
        # Kiểm tra tính hợp lệ của status
        if status not in self.STATUSES:
            raise ValueError(f"Invalid payment status: {status}")

        # Gán các thuộc tính cho đối tượng Payment
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.transaction_code = transaction_code
        self.status = status

    # Phương thức để tạo đối tượng Payment từ một hàng dữ liệu (row) từ cơ sở dữ liệu
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

    # Phương thức để chuyển đổi đối tượng Payment thành một từ điển (dictionary)
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

    # Các phương thức kiểm tra trạng thái thanh toán
    def is_paid(self):
        return self.status == "Paid"

    # Phương thức kiểm tra xem thanh toán có thất bại hay không
    def is_refunded(self):
        return self.status == "Refunded"