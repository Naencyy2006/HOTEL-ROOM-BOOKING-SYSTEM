from .room import Room

class Room:

    # Danh sách các trạng thái hợp lệ cho phòng
    STATUSES = ["Available", "Occupied", "Maintenance"]

    # Khởi tạo đối tượng Room với các thuộc tính
    def __init__(
        self,
        room_number=None,
        room_type_id=None,
        floor=1,
        status="Available"
    ):
        # Kiểm tra tính hợp lệ của status
        if status not in self.STATUSES:
            raise ValueError(f"Invalid room status: {status}")

        # Gán các thuộc tính cho đối tượng Room
        self.room_number = room_number
        self.room_type_id = room_type_id
        self.floor = floor
        self.status = status

    @classmethod
    # Phương thức để tạo đối tượng Room từ một hàng dữ liệu (row) từ cơ sở dữ liệu
    def from_row(cls, row):
        return cls(
            room_number=row[0],
            room_type_id=row[1],
            floor=row[2],
            status=row[3]
        )
    # Phương thức để chuyển đổi đối tượng Room thành một từ điển (dictionary)
    def to_dict(self):
        return {
            "room_number": self.room_number,
            "room_type_id": self.room_type_id,
            "floor": self.floor,
            "status": self.status
        }

    # Phương thức kiểm tra xem phòng có sẵn hay không
    def is_available(self):
        return self.status == "Available"

    # Phương thức kiểm tra xem phòng có đang được sử dụng hay không
    def is_occupied(self):
        return self.status == "Occupied"

    # Phương thức kiểm tra xem phòng có đang bảo trì hay không
    def is_maintenance(self):
        return self.status == "Maintenance"