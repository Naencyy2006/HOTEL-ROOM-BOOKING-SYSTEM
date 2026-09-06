class Room:
    def __init__(
        self,
        room_number="",
        room_type_id=None,
        floor=1,
        status="Available"
    ):
        self.room_number = room_number
        self.room_type_id = room_type_id
        self.floor = floor
        self.status = status

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    def to_dict(self):
        return {
            "room_number": self.room_number,
            "room_type_id": self.room_type_id,
            "floor": self.floor,
            "status": self.status
        }