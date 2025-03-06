import datetime
from dataclasses import dataclass
from picture import Picture


@dataclass
class Bike:
    """
        Class representing bikes stored in the application.
    """
    id: int
    bicycode: str
    entry_date: datetime.datetime
    exit_date: datetime.datetime
    brand: str
    bike_type: str
    wheel_size: str
    frame_size: str
    is_electric: bool
    bike_status: str
    bike_state: str
    next_action: str
    ref: str
    value: str
    bike_dest: str
    public_desc: str
    private_desc: str
    exit_type: str
    name: str
    photos: list[Picture]
