from dataclasses import dataclass
from bike import Bike


@dataclass
class Picture:
    """
        Class representing pictures of bikes.
        Many-to-one relationship: one bike -> several pictures.
    """
    id: int
    bike: Bike = None
    name: str       # Filename like "toto.jpg"
    is_principal: bool
    data: str       # Blob (rawbyte encoding)
