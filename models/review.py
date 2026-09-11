from .review import Review

class Review:
    # Các trạng thái có thể có của đánh giá
    STATUSES = ["Published", "Hidden", "Deleted"]

    # Khởi tạo đối tượng Review với các thuộc tính
    def __init__(
        self,
        review_id=None,
        user_id=None,
        room_id=None,
        booking_id=None,
        rating=5,
        comment=None,
        status="Published",
        review_date=None
    ):
        # Kiểm tra tính hợp lệ của rating và status
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        # Kiểm tra tính hợp lệ của status
        if status not in self.STATUSES:
            raise ValueError(f"Invalid review status: {status}")

        # Gán các thuộc tính cho đối tượng Review
        self.review_id = review_id
        self.user_id = user_id
        self.room_id = room_id
        self.booking_id = booking_id
        self.rating = rating
        self.comment = comment
        self.status = status
        self.review_date = review_date

    # Phương thức để tạo đối tượng Review từ một hàng dữ liệu (row) từ cơ sở dữ liệu
    @classmethod
    def from_row(cls, row):
        return cls(
            review_id=row[0],
            user_id=row[1],
            room_id=row[2],
            booking_id=row[3],
            rating=row[4],
            comment=row[5],
            status=row[6],
            review_date=row[7]
        )

    # Phương thức để chuyển đổi đối tượng Review thành một từ điển (dictionary)
    def to_dict(self):
        return {
            "review_id": self.review_id,
            "user_id": self.user_id,
            "room_id": self.room_id,
            "booking_id": self.booking_id,
            "rating": self.rating,
            "comment": self.comment,
            "status": self.status,
            "review_date": self.review_date
        }
    # Các phương thức kiểm tra trạng thái của đánh giá
    def is_published(self):
        return self.status == "Published"

    # Phương thức kiểm tra xem đánh giá có bị ẩn hay không
    def is_hidden(self):
        return self.status == "Hidden"

    # Phương thức kiểm tra xem đánh giá có bị xóa hay không
    def is_deleted(self):
        return self.status == "Deleted"