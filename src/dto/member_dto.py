import psycopg2
from src.db import Database
from src.entities.member import Member

class MemberDTO:

    @staticmethod
    def get_all_members() -> list[Member]:
        """
        Requests all the members from the database and returns them.

        :return: the list of all members, empty list if no member in the database
        :rtype: list[Member]
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, username, password, role, uuid FROM MEMBER;"
                cur.execute(query)
                members = cur.fetchall()

                return [Member(m[0], m[1], m[2], m[3], m[4]) for m in members]
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching members: {error}")
            return []


    @staticmethod
    def get_member_by_username(username: str) -> Member | None:
        """
        Requests one member with the correct username in the database.

        :param str username: the username of the member
        :return: the member with the correct username, None if not found
        :rtype: Member | None
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, username, password, role, uuid FROM MEMBER WHERE username=%s;"
                cur.execute(query, (username,))
                fetched = cur.fetchone()

                if fetched is not None:
                    return Member(fetched[0], fetched[1], fetched[2], fetched[3], fetched[4])

            return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching member by username {username}: {error}")
            return None

    @staticmethod
    def get_member_by_id(id: int) -> Member | None:
        """
        Requests one member with the correct id from the database.

        :param int id: the id of the member
        :return: the member with the correct id, None if not found
        :rtype: Member | None
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, username, password, role, uuid FROM MEMBER WHERE id=%s;"
                cur.execute(query, (id,))
                fetched = cur.fetchone()

                if fetched is not None:
                    return Member(fetched[0], fetched[1], fetched[2], fetched[3], fetched[4])

            return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching member by ID {id}: {error}")
            return None


    @staticmethod
    def get_all_members_by_role(role: str) -> list[Member]:
        """
        Requests all the members from the database having the correct role and returns them.

        :param str role: the role of the members to fetch
        :return: the list of all members with the specified role, empty list if no member found
        :rtype: list[Member]
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "SELECT id, username, password, role, uuid FROM MEMBER WHERE role=%s;"
                cur.execute(query, (role,))
                members = cur.fetchall()

                return [Member(m[0], m[1], m[2], m[3], m[4]) for m in members]
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching members by role {role}: {error}")
            return []

    @staticmethod
    def create_member(member: Member) -> int:
        """
        Inserts a new member into the database and returns its id.

        :param Member member: the member to insert
        :return: the id of the inserted member, -1 if the request fails
        :rtype: int
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur
                query = """
                INSERT INTO MEMBER (username, password, role, uuid)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """
                cur.execute(query, (member.username, member.password, member.role, member.uuid))
                conn.commit()
                return cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error creating member: {error}")
            if conn:
                conn.rollback()
            return -1


    @staticmethod
    def update_member(member: Member):
        """
        Updates an existing member in the database.

        :param Member member: the member with updated information
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = """
                UPDATE MEMBER
                SET username=%s, password=%s, role=%s, uuid=%s
                WHERE id=%s;
                """
                cur.execute(query, (member.username, member.password, member.role, member.uuid, member.id))
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error updating member: {error}")
            if conn:
                conn.rollback()

    @staticmethod
    def delete_member(member: Member):
        """
        Deletes a member from the database.

        :param Member member: the member to delete
        """
        conn = None
        try:
            conn = Database.get_db()
            with conn.cursor() as cur:
                query = "DELETE FROM MEMBER WHERE id=%s;"
                cur.execute(query, (member.id,))
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error deleting member with ID {member.id}: {error}")
            if conn:
                conn.rollback()

