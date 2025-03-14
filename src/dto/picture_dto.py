import psycopg2
from psycopg2 import sql
from src.db import Database
from src.entities.picture import Picture
from src.entities.bike import Bike

class PictureDTO:

    @staticmethod
    def get_all_pictures() -> list[Picture]:
        """
        Requests all pictures from the database and returns them. By default there is no bike related to the Picture.

        :return: the list of all pictures, empty list if no picture in the database
        :rtype: list[Picture]
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, name, is_principal, data FROM PICTURE;"
                cur.execute(query)
                pictures = cur.fetchall()

                return [Picture(p[0], None, p[1], p[2], p[3]) for p in pictures]
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching pictures: {error}")
            return []


    @staticmethod
    def get_picture_by_id(id: int) -> Picture | None:
        """
        Requests one picture with the correct id from the database.

        :param int id: the id of the picture
        :return: the picture with the correct id, None if not found
        :rtype: Picture | None
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, name, is_principal, data FROM PICTURE WHERE id=%s;"
                cur.execute(query, (id,))
                fetched = cur.fetchone()

                if fetched is not None:
                    return Picture(fetched[0], None, fetched[1], fetched[2], fetched[3])

                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching picture by ID {id}: {error}")
            return None


    @staticmethod
    def get_principal_picture_by_bike(bike: Bike) -> Picture | None:
        """
        Requests the principal picture of a bike from the database, sets the bike as a picture's attribute.

        :param Bike bike: the bike associated with the picture
        :return: the principal picture with the correct associated bike, None if not found
        :rtype: Picture | None
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, name, is_principal, data FROM PICTURE WHERE bike_id=%s AND is_principal IS TRUE;"
                cur.execute(query, (bike.id,))
                fetched = cur.fetchone()

                if fetched is not None:
                    return Picture(fetched[0], bike, fetched[1], fetched[2], fetched[3])

                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching principal picture for bike ID {bike.id}: {error}")
            return None


    @staticmethod
    def get_all_pictures_by_bike(bike: Bike) -> list[Picture]:
        """
        Requests all pictures of a bike from the database and set the bike as an attribute for each of them.

        :param Bike bike: the bike associated with the pictures
        :return: all pictures with the correct associated bike, empty list if not found
        :rtype: list[Picture]
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, name, is_principal, data FROM PICTURE WHERE bike_id=%s;"
                cur.execute(query, (bike.id,))
                pictures = cur.fetchall()

                return [Picture(p[0], bike, p[1], p[2], p[3]) for p in pictures]
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching pictures for bike ID {bike.id}: {error}")
            return []


    @staticmethod
    def create_picture(picture: Picture) -> int:
        """
        Inserts a new picture into the database and returns its id.

        :param Picture picture: the picture to insert
        :return: the id of the inserted picture
        :rtype: int
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = """
                INSERT INTO PICTURE (bike_id, name, is_principal, data)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """
                if picture.bike is None:
                    raise Exception("No bike for this picture")
                cur.execute(query, (picture.bike.id, picture.name, picture.is_principal, picture.data))
                conn.commit()
                return cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error creating picture: {error}")
            if conn:
                conn.rollback()
            return -1


    @staticmethod
    def update_picture(picture: Picture):
        """
        Updates an existing picture in the database.

        :param Picture picture: the picture with updated information
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = """
                UPDATE PICTURE
                SET bike_id=%s, name=%s, is_principal=%s, data=%s
                WHERE id=%s;
                """
                if picture.bike is None:
                    raise Exception("No bike for this picture")
                cur.execute(query, (picture.bike.id, picture.name, picture.is_principal, picture.data, picture.id))
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error updating picture: {error}")
            if conn:
                conn.rollback()


    @staticmethod
    def delete_picture(picture: Picture):
        """
        Deletes a picture from the database.

        :param picture Picture: the picture to delete
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "DELETE FROM PICTURE WHERE id=%s;"
                cur.execute(query, (id,))
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error deleting picture with ID {id}: {error}")
            if conn:
                conn.rollback()

