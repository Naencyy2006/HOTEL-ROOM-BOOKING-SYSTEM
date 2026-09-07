class Review:
    STATUSES = ["Published", "Hidden", "Deleted"]

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
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        if status not in self.STATUSES:
            raise ValueError(f"Invalid review status: {status}")

        self.review_id = review_id
        self.user_id = user_id
        self.room_id = room_id
        self.booking_id = booking_id
        self.rating = rating
        self.comment = comment
        self.status = status
        self.review_date = review_date

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

    def is_published(self):
        return self.status == "Published"

    def is_hidden(self):
        return self.status == "Hidden"

    def is_deleted(self):
        return self.status == "Deleted"