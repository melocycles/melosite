import datetime
from dataclasses import dataclass
from picture import Picture


@dataclass
class Bike:
    """
    Class representing bikes stored in the application.
    """
    id: int = -1
    bicycode: str
    entry_date: datetime.datetime
    exit_date: datetime.datetime
    brand: str
    bike_type: str
    wheel_size: str
    frame_size: str
    is_electric: bool
    origin: str
    bike_status: str
    next_action: str
    ref: str
    value: str
    bike_dest: str
    public_desc: str
    private_desc: str
    name: str
    exit_type: str
    pictures: list[Picture] = []

    def add_picture(self, picture: Picture):
        """
        Add the picture to the list of pictures, adds the bike ref to the picture too.
        :param picture Picture: the picture to add
        """
        picture.bike = self
        self.pictures.append(picture)


    def remove_picture(self, picture: Picture):
        """
        Removes the picture from the list of pictures, removes the bike ref in the picture too.
        :param picture Picture: the picture to remove
        """
        picture.bike = None
        self.pictures.remove(picture)

