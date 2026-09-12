from .room import Room

class Room:

    # Valid room statuses.
    STATUSES = ["Available", "Occupied", "Maintenance"]

    # Initialize a Room object with its attributes.
    def __init__(
        self,
        room_number=None,
        room_type_id=None,
        floor=1,
        status="Available"
    ):
        # Validate the room status.
        if status not in self.STATUSES:
            raise ValueError(f"Invalid room status: {status}")

        # Assign the attributes to the Room object.
        self.room_number = room_number
        self.room_type_id = room_type_id
        self.floor = floor
        self.status = status

    @classmethod
    # Create a Room object from a database row.
    def from_row(cls, row):
        return cls(
            room_number=row[0],
            room_type_id=row[1],
            floor=row[2],
            status=row[3]
        )
    # Convert the Room object to a dictionary.
    def to_dict(self):
        return {
            "room_number": self.room_number,
            "room_type_id": self.room_type_id,
            "floor": self.floor,
            "status": self.status
        }

    # Check whether the room is available.
    def is_available(self):
        return self.status == "Available"

    # Check whether the room is occupied.
    def is_occupied(self):
        return self.status == "Occupied"

    # Check whether the room is under maintenance.
    def is_maintenance(self):
        return self.status == "Maintenance"