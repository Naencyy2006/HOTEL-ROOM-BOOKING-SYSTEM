class Room:
    STATUSES = ["Available", "Occupied", "Maintenance"]

    def __init__(
        self,
        room_number=None,
        room_type_id=None,
        floor=1,
        status="Available"
    ):
        if status not in self.STATUSES:
            raise ValueError(f"Invalid room status: {status}")

        self.room_number = room_number
        self.room_type_id = room_type_id
        self.floor = floor
        self.status = status

    @classmethod
    def from_row(cls, row):
        return cls(
            room_number=row[0],
            room_type_id=row[1],
            floor=row[2],
            status=row[3]
        )

    def to_dict(self):
        return {
            "room_number": self.room_number,
            "room_type_id": self.room_type_id,
            "floor": self.floor,
            "status": self.status
        }

    def is_available(self):
        return self.status == "Available"

    def is_occupied(self):
        return self.status == "Occupied"

    def is_maintenance(self):
        return self.status == "Maintenance"