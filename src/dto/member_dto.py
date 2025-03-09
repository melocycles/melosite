from src.db import Database
from src.entities.member import Member


class MemberDTO:

    @classmethod
    def get_all_members(self) -> list[Member]:
        """
        Requests all the members from the database and returns them.

        :return: the list if all members, empty list of no member in the database
        :rtype: list[Member]
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, username, password, role, uuid FROM MEMBER;"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query)
        members = cur.fetchall()

        return [Member(m[0], m[1], m[2], m[3], m[4]) for m in members]

    @classmethod
    def get_member_by_username(self, username: str) -> Member | None:
        """
        Requests one member with the correct username in the database.

        :param str username: the username of the member
        :return: the member with the correct username, None if not found
        :rtype: Member | None
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, username, password, role, uuid FROM MEMBER WHERE username=%s"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query, (username,))
        fetched = cur.fetchone()

        # The member has been found in database
        if fetched is not None:
            return Member(fetched[0], fetched[1], fetched[2], fetched[3], fetched[4])

        # If no member has been found then None is returned
        return None

    @classmethod
    def get_member_by_id(self, id: int) -> Member | None:
        """
        Requests one member with the correct id from the database.

        :param int id: the id of the member
        :return: the member with the correct id, None if not found
        :rtype: Member | None
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, username, password, role, uuid FROM MEMBER WHERE id=%s"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query, (id,))
        fetched = cur.fetchone()

        # The member has been found in database
        if fetched is not None:
            return Member(fetched[0], fetched[1], fetched[2], fetched[3], fetched[4])

        # If no member has been found then None is returned
        return None

    @classmethod
    def get_all_members_by_role(self, role: str) -> list[Member]:
        """
        Requests all the members from the database having the correct role and returns them.

        :return: the list of all members, empty list of no member in the database
        :rtype: list[Member]
        """
        conn = Database.get_db()
        cur = conn.cursor()
        query = "SELECT id, username, password, role, uuid FROM MEMBER"

        # Maybe add try catch, the psycopg2 doc is not clear about thrown errors
        cur.execute(query)
        members = cur.fetchall()

        return [Member(m[0], m[1], m[2], m[3], m[4]) for m in members]
