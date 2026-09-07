class RoomType:

    # Khởi tạo đối tượng RoomType với các thuộc tính
    def __init__(
        self,
        room_type_id=None,
        type_name=None,
        capacity=1,
        description=None,
        price_per_night=0.0
    ):

        # Gán các thuộc tính cho đối tượng RoomType
        self.room_type_id = room_type_id
        self.type_name = type_name
        self.capacity = capacity
        self.description = description
        self.price_per_night = price_per_night

    # Phương thức để tạo đối tượng RoomType từ một hàng dữ liệu (row) từ cơ sở dữ liệu
    @classmethod
    def from_row(cls, row):
        return cls(
            room_type_id=row[0],
            type_name=row[1],
            capacity=row[2],
            description=row[3],
            price_per_night=row[4]
        )

    # Phương thức để chuyển đổi đối tượng RoomType thành một từ điển (dictionary)
    def to_dict(self):
        return {
            "room_type_id": self.room_type_id,
            "type_name": self.type_name,
            "capacity": self.capacity,
            "description": self.description,
            "price_per_night": self.price_per_night
        }

    