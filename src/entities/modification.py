import datetime
from dataclasses import dataclass
from bike import Bike


@dataclass
class Modification:
    """
        Class representing modifications on bikes.
        Act as a log.
    """
    id: int
    bike: Bike = None               # The modified bike
    timestamp: datetime.datetime    # Time of modification
    volunteer: str                  # Name of the modifier
    modified_field: str             # Bike field
    old_value: str
    new_value: str
