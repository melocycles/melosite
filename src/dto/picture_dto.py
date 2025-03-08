from src.db import Database
from src.entities.picture import Picture
from src.entities.bike import Bike


class PictureDTO:

    @classmethod
    def get_all_pictures(self) -> list[Picture]:
        """
        Requests all pictures from the database and returns them.

        :return: the list of all pictures, empty list if no picture in the database
        :rtype: list[Picture]
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, name, is_principal, data FROM PICTURE;"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query)
        pictures = cur.fetchall()

        return [Picture(p[0], None, p[1], p[2], p[3]) for p in pictures]

    @classmethod
    def get_picture_by_id(self, id: int) -> Picture | None:
        """
        Requests one picture with the correct id from the database.

        :param int id: the id of the picture
        :return: the picture with the correct id, None if not found
        :rtype: Picture | None
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, name, is_principal, data FROM PICTURE WHERE id=%s;"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query, (id,))
        fetched = cur.fetchone()

        # The picture has been found in database
        if fetched is not None:
            return Picture(fetched[0], None, fetched[1], fetched[2], fetched[3])

        # If no member has been found then None is returned
        return None

    @classmethod
    def get_principal_picture_by_bike(self, bike: Bike) -> Picture | None:
        """
        Requests the principal picture of a bike from the database.

        :param Bike bike: the bike associated to the picture
        :return: the principal picture with the correct associated bike, None if not found
        :rtype: Picture | None
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, name, is_principal, data FROM PICTURE WHERE bike_id=%s AND is_principal IS TRUE;"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query, (bike.id,))
        fetched = cur.fetchone()

        # The picture has been found in database
        if fetched is not None:
            return Picture(fetched[0], bike, fetched[1], fetched[2], fetched[3])

        # If no picture has been found then None is returned
        return None

    @classmethod
    def get_all_pictures_by_bike(self, bike: Bike) -> list[Picture]:
        """
        Requests all pictures of a bike from the database.

        :param Bike bike: the bike associated to the picture
        :return: all pictures with the correct associated bike, None if not found
        :rtype: list[Picture] | None
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, name, is_principal, data FROM PICTURE WHERE bike_id=%s AND is_principal IS TRUE;"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query, (bike.id,))
        pictures = cur.fetchall()

        return [Picture(p[0], bike, p[1], p[2], p[3]) for p in pictures]
