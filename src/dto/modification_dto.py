
from src.db import Database
from src.entities.modification import Modification
from src.entities.bike import Bike


class ModificationDTO:

    @classmethod
    def get_all_modifications(self) -> list[Modification]:
        """
        Requests all the modifications from the database and returns them.

        :return: the list if all modifications, empty list of no modification in the database
        :rtype: list[Modification]
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, timestamp, volunteer, modified_field, old_value, new_value FROM MODIFICATION;"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query)
        modifications = cur.fetchall()

        return [Modification(m[0], None, m[1], m[2], m[3], m[4], m[5]) for m in modifications]

    @classmethod
    def get_modification_by_id(self, bike: Bike) -> Modification | None:
        """
        Requests one modification with the correct bike from the database.

        :param Bike bike: the associated bike
        :return: the modification with the correct associated bike, None if not found
        :rtype: Modification | None
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, timestamp, volunteer, modified_field, old_value, new_value FROM MODIFICATION WHERE bike_id=%s;"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query, (bike.id,))
        fetched = cur.fetchone()

        # The modification has been found in database
        if fetched is not None:
            return Modification(m[0], bike, m[1], m[2], m[3], m[4], m[5])

        # If no modification has been found then None is returned
        return None
