from .booking import Booking

class Booking:

    # Xác định các trạng thái có thể có của một lượt đặt chỗ.
    STATUSES = [
        "Pending",
        "Confirmed",
        "Checked-in",
        "Completed",
        "Canceled"
    ]
    # Khởi tạo đối tượng Booking với các thuộc tính
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
        # Kiểm tra tính hợp lệ của status
        if status not in self.STATUSES:
            raise ValueError(f"Invalid booking status: {status}")

        # Gán các thuộc tính cho đối tượng Booking
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

    # Phương thức để tạo đối tượng Booking từ một hàng dữ liệu (row) từ cơ sở dữ liệu
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

    # Phương thức để chuyển đổi đối tượng Booking thành một từ điển (dictionary)
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

    # Các phương thức kiểm tra trạng thái của lượt đặt chỗ
    def is_confirmed(self):
        return self.status == "Confirmed"

    # Phương thức kiểm tra xem lượt đặt chỗ có đang được sử dụng hay không
    def is_checked_in(self):
        return self.status == "Checked-in"

    # Phương thức kiểm tra xem lượt đặt chỗ có đã hoàn tất hay không
    def is_completed(self):
        return self.status == "Completed"

    # Phương thức kiểm tra xem lượt đặt chỗ có bị hủy hay không
    def is_canceled(self):
        return self.status == "Canceled"