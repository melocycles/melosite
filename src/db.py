from flask import g
import psycopg2

#  WARN: This maybe not a great implementation and will only work in localhost
# TODO: Check if this code can get a db conn on heroku


class Database():
    """
        Class used to get the connection to the database
    """

    def __init__(self, host: str,
                 db_name: str,
                 user: str,
                 password: str,
                 is_localhost=False):
        """Setup the data for a postgres db connection.

        Keyword arguments:
        host -- name of the host (ex: "localhost")
        db_name -- name of the database (ex: "melodb")
        user -- user that will launch database (ex: "postgres")
        password -- password for the user (ex: nice try hehe)
        is_localhost -- is the app running in localhost or on server (default False)
        """
        self._host = host
        self._db_name = db_name
        self._user = user
        self._password = password
        self._is_localhost = is_localhost

    def get_db(self) -> psycopg2.connection:
        """Returns the database connection, if it does not exist it creates it."""
        if "db" not in g:
            g.db = psycopg2.connect(
                host=self._host,
                database=self._db_name,
                user=self._user,
                password=self._password
            )
        # This is a typical implementation of a singleton design pattern
        # There is and will exist only ONE connection to the database in one app run
        return g.db
