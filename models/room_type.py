from .room_type import RoomType

class RoomType:

    # Initialize a RoomType object with its attributes.
    def __init__(
        self,
        room_type_id=None,
        type_name=None,
        capacity=1,
        description=None,
        price_per_night=0.0
    ):

        # Assign the attributes to the RoomType object.
        self.room_type_id = room_type_id
        self.type_name = type_name
        self.capacity = capacity
        self.description = description
        self.price_per_night = price_per_night

    # Create a RoomType object from a database row.
    @classmethod
    def from_row(cls, row):
        return cls(
            room_type_id=row[0],
            type_name=row[1],
            capacity=row[2],
            description=row[3],
            price_per_night=row[4]
        )

    # Convert the RoomType object to a dictionary.
    def to_dict(self):
        return {
            "room_type_id": self.room_type_id,
            "type_name": self.type_name,
            "capacity": self.capacity,
            "description": self.description,
            "price_per_night": self.price_per_night
        }

    