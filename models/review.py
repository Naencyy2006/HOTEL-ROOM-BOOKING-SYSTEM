class Review:
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
        self.review_id = review_id
        self.user_id = user_id
        self.room_id = room_id
        self.booking_id = booking_id
        self.rating = rating
        self.comment = comment
        self.status = status
        self.review_date = review_date

    @classmethod # Phương thức lớp để tạo đối tượng Review từ một hàng dữ liệu (row) từ cơ sở dữ liệu
    def from_row(cls, row):
        return cls(*row)

    # Phương thức để chuyển đổi đối tượng Review thành dictionary
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