import psycopg2
from psycopg2 import sql
from src.db import Database
from src.entities.bike import Bike

class BikeDTO:

    @staticmethod
    def get_all_bikes() -> list[Bike]:
        """
        Requests all the bikes from the database and returns them.
        Pictures are not returned as part of the bike, you can store them in it by querying the PictureDTO.get_photos_by_bike(bike).

        :return: the list of all bikes, empty list if no bike in the database
        :rtype: list[Bike]
        """
        conn = None
        try:
            conn = Database.get_db()
            cur = conn.cursor()
            query = """
            SELECT id, bicycode, entry_date, exit_date, brand, bike_type, wheel_size, frame_size, is_electric, origin, bike_status, bike_state, next_action, ref, value, bike_dest, public_desc, private_desc, name, exit_type
            FROM BIKE;
            """
            cur.execute(query)
            bikes = cur.fetchall()

            return [
                Bike(
                    b[0], b[1], b[2], b[3], b[4],
                    b[5], b[6], b[7], b[8], b[9],
                    b[10], b[11], b[12], b[13], b[14],
                    b[15], b[16], b[17], b[18], b[19]
                ) for b in bikes
            ]
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching bikes: {error}")
            return []
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_bike_by_id(id: int) -> Bike | None:
        """
        Requests one bike with the correct id in the database.
        The list of pictures of the bike is init as an empty list.

        :param int id: the id of the bike
        :return: the bike with the correct id, None if not found
        :rtype: Bike | None
        """
        conn = None
        try:
            conn = Database.get_db()
            cur = conn.cursor()
            query = """
            SELECT id, bicycode, entry_date, exit_date, brand, bike_type, wheel_size, frame_size, is_electric, origin, bike_status, bike_state, next_action, ref, value, bike_dest, public_desc, private_desc, name, exit_type
            FROM BIKE
            WHERE id=%s;
            """
            cur.execute(query, (id,))
            fetched = cur.fetchone()

            if fetched is not None:
                return Bike(
                    fetched[0], fetched[1], fetched[2], fetched[3], fetched[4],
                    fetched[5], fetched[6], fetched[7], fetched[8], fetched[9],
                    fetched[10], fetched[11], fetched[12], fetched[13], fetched[14],
                    fetched[15], fetched[16], fetched[17], fetched[18], fetched[19]
                )

            return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching bike by ID {id}: {error}")
            return None
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def create_bike(bike: Bike) -> int:
        """
        Inserts a new bike into the database.

        :param Bike bike: the bike to insert
        :return: the id of the inserted bike
        :rtype: int
        """
        conn = None
        try:
            conn = Database.get_db()
            cur = conn.cursor()
            query = """
            INSERT INTO BIKE (bicycode, entry_date, exit_date, brand, bike_type, wheel_size, frame_size, is_electric, origin, bike_status, bike_state, next_action, ref, value, bike_dest, public_desc, private_desc, name, exit_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
            cur.execute(query, (
                bike.bicycode, bike.entry_date, bike.exit_date, bike.brand, bike.bike_type,
                bike.wheel_size, bike.frame_size, bike.is_electric, bike.origin, bike.bike_status,
                bike.bike_state, bike.next_action, bike.ref, bike.value, bike.bike_dest,
                bike.public_desc, bike.private_desc, bike.name, bike.exit_type
            ))
            conn.commit()
            return cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error creating bike: {error}")
            if conn:
                conn.rollback()
            return -1
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def update_bike(bike: Bike):
        """
        Updates an existing bike in the database.

        :param Bike bike: the bike with updated information
        """
        conn = None
        try:
            conn = Database.get_db()
            cur = conn.cursor()
            query = """
            UPDATE BIKE
            SET bicycode=%s, entry_date=%s, exit_date=%s, brand=%s, bike_type=%s, wheel_size=%s, frame_size=%s, is_electric=%s, origin=%s, bike_status=%s, bike_state=%s, next_action=%s, ref=%s, value=%s, bike_dest=%s, public_desc=%s, private_desc=%s, name=%s, exit_type=%s
            WHERE id=%s;
            """
            cur.execute(query, (
                bike.bicycode, bike.entry_date, bike.exit_date, bike.brand, bike.bike_type,
                bike.wheel_size, bike.frame_size, bike.is_electric, bike.origin, bike.bike_status,
                bike.bike_state, bike.next_action, bike.ref, bike.value, bike.bike_dest,
                bike.public_desc, bike.private_desc, bike.name, bike.exit_type, bike.id
            ))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error updating bike: {error}")
            if conn:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def delete_bike(id: int):
        """
        Deletes a bike from the database by its id.

        :param int id: the id of the bike to delete
        """
        conn = None
        try:
            conn = Database.get_db()
            cur = conn.cursor()
            query = "DELETE FROM BIKE WHERE id=%s;"
            cur.execute(query, (id,))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error deleting bike with ID {id}: {error}")
            if conn:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

