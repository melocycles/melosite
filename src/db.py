from flask import g
import psycopg2
from __future__ import annotations

#  WARN: This maybe not a great implementation and will only work in localhost
# TODO: Check if this code can get a db conn on heroku


class Database():
    """
        Class used to get the connection to the database.
        This class is not instiable, you can get the db connection using Database.get_db()
    """

    @staticmethod
    def get_db(self) -> psycopg2.connect:
        """Returns the database connection, if it does not exist it creates it."""
        if "db" not in g:
            g.db = psycopg2.connect(
                host="localhost",
                database="melodb",
                user="postgres",
                password="mdp"
            )
        # This is a typical implementation of a singleton design pattern
        # There is and will exist only ONE connection to the database in one app run
        return g.db
