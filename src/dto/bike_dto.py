from src.db import Database
from src.entities.bike import Bike


class BikeDTO:

    @classmethod
    def get_all_bikes(self) -> list[Bike]:
        """
        Requests all the bikes with their main picture from the database and returns them.
        Pictures are not returned as part of the bike, you can store them in it by querying the PictureDTO.get_photos_by_bike(bike).

        :return: the list of all bikes, empty list if no bike in the database
        :rtype: list[Bike]
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, bicycode, entry_date, exit_date, brand, bike_type, wheel_size, frame_size, is_electric, origin, bike_status, bike_state, next_action, ref, value, bike_dest, public_desc, private_desc, name, exit_type FROM BIKE;"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query)
        bikes = cur.fetchall()

        return [
            Bike(
                b[0], b[1], b[2], b[3], b[4],
                b[6], b[7], b[8], b[9], b[10],
                b[11], b[12], b[13], b[14], b[15],
                b[16], b[17], b[18], b[19], b[20]
            ) for b in bikes]

    @classmethod
    def get_bike_by_id(self, id: int) -> Bike | None:
        """
        Requests one bike with the correct id in the database.
        The list of pictures of the bike is init as an empty list.

        :param str id: the id of the bike
        :return: the bike with the correct id, None if not found
        :rtype: Bike | None
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, bicycode, entry_date, exit_date, brand, bike_type, wheel_size, frame_size, is_electric, origin, bike_status, bike_state, next_action, ref, value, bike_dest, public_desc, private_desc, name, exit_type FROM BIKE WHERE id=%s;"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query, (id,))
        fetched = cur.fetchone()

        # The bike has been found in database, last empty list is for pictures
        if fetched is not None:
            return Bike(
                fetched[0], fetched[1], fetched[2], fetched[3], fetched[4],
                fetched[6], fetched[7], fetched[8], fetched[9], fetched[10],
                fetched[11], fetched[12], fetched[13], fetched[14], fetched[15],
                fetched[16], fetched[17], fetched[18], fetched[19], fetched[20]
            )

        # If no bike has been found then None is returned
        return None
