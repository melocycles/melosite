from src.db import Database
from src.entities.modification import Modification
from src.entities.bike import Bike


class ModificationDTO:

    @staticmethod
    def get_all_modifications() -> list[Modification]:
        """
        Requests all the modifications from the database and returns them. No bike is assigned to them you need to do it yourself in the controller.

        :return: the list if all modifications, empty list of no modification in the database
        :rtype: list[Modification]
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, timestamp, volunteer, modified_field, old_value, new_value FROM MODIFICATION;"
                cur.execute(query)
                modifications = cur.fetchall()
                return [Modification(m[0], None, m[1], m[2], m[3], m[4], m[5]) for m in modifications]

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching modifications: {error}")
            return []


    @staticmethod
    def get_modifications_by_bike(bike: Bike) -> list[Modification] | None:
        """
        Requests the modifications with the correct bike from the database.

        :param Bike bike: the associated bike
        :return: the modifications with the correct associated bike, empty list if not found
        :rtype: list[Modification]
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, timestamp, volunteer, modified_field, old_value, new_value FROM MODIFICATION WHERE bike_id=%s;"
                cur.execute(query, (bike.id,))
                modifications = cur.fetchall()
                return [Modification(m[0], bike, m[1], m[2], m[3], m[4], m[5]) for m in modifications]

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching modifications for bike {bike.id}: {error}")
            return []


@staticmethod
    def create_modification(modification: Modification) -> int:
        """
        Inserts a new modification into the database and returns its id.

        :param Modification modification: the modification to insert
        :return: the id of the inserted modification, -1 if something went wrong
        :rtype: int
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = """
                INSERT INTO MODIFICATION (bike_id, timestamp, volunteer, modified_field, old_value, new_value)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """
                cur.execute(query, (modification.bike.id if modification.bike else None, modification.timestamp, modification.volunteer, modification.modified_field, modification.old_value, modification.new_value))
                conn.commit()
                return cur.fetchone()[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error creating modification: {error}")
            if conn:
                conn.rollback()
            return -1


    @staticmethod
    def update_modification(modification: Modification):
        """
        Updates an existing modification in the database.

        :param Modification modification: the modification with updated information
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = """
                UPDATE MODIFICATION
                SET bike_id=%s, timestamp=%s, volunteer=%s, modified_field=%s, old_value=%s, new_value=%s
                WHERE id=%s;
                """
                cur.execute(query, (modification.bike.id if modification.bike else None, modification.timestamp, modification.volunteer, modification.modified_field, modification.old_value, modification.new_value, modification.id))
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error updating modification: {error}")
            if conn:
                conn.rollback()


    @staticmethod
def delete_modification(modif: Modification):
        """
        Deletes a modification from the database.

        :param modif Modification: the id of the modification to delete
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "DELETE FROM MODIFICATION WHERE id=%s;"
                cur.execute(query, (id,))
                conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error deleting modification with ID {id}: {error}")
            if conn:
                conn.rollback()
