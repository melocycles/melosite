from dataclasses import dataclass
from bike import Bike


@dataclass
class Picture:
    """
        Class representing pictures of bikes.
        Many-to-one relationship: one bike -> several pictures.
    """
    id: int
    bike: Bike
    name: str       # Filename like "toto.jpg"
    data: str       # Blob (rawbyte encoding)
