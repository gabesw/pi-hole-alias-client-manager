import sqlite3
from typing import List

class AliasClientManager:
    def __init__(self, dbpath: str = '/etc/pihole/pihole-FTL.db'):
        """
        Initialize the AliasClientManager and set the path to the database.
        """
        self.dbpath = dbpath
        self.con: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None
    
    def open_db(self):
        """
        Open the database connection.
        """
        if not self.con:
            self.con = sqlite3.connect(self.dbpath, autocommit=True)
            self.cursor = self.con.cursor()

    def close_db(self):
        """
        Close the database connection.
        """
        if self.con:
            self.con.close()
            self.con = None
            self.cursor = None

    def list_alias_clients(self) -> List[tuple]:
        """
        List all alias clients.
        :return: List of tuples containing the aliases with the format (id, name, comment)
        """
        self.cursor.execute("SELECT * FROM aliasclient ORDER BY id;")
        return self.cursor.fetchall()

    def add_new_alias(self, name: str, comment: str | None) -> int:
        """
        Add a new alias client to the database.
        :param name: the alias name
        :param comment: an optional comment
        :return: the newly created alias ID
        """
        # First, find lowest unused id
        clients = self.list_alias_clients()
        id = 0
        for client in clients:
            if client[0] != id:
                break
            id += 1
        thecomment = "NULL" if comment is None else f"'{comment}'"
        self.cursor.execute(f"INSERT INTO aliasclient (id,name,comment) VALUES ({id}, '{name}', {thecomment});")
        return id

    def delete_alias(self, id: int):
        """
        Delete an alias client from the database.

        :param id: the alias ID
        """
        self.cursor.execute(f"DELETE FROM aliasclient WHERE id = {id};")
        self.cursor.execute(f"UPDATE network SET aliasclient_id = NULL WHERE aliasclient_id = {id};")

    def update_alias(self, id: int, name: str | None, comment: str | None):
        """
        Update an alias client in the database with the given parameters.

        :param id: the alias ID
        :param name: the new alias name, or None to keep the current name
        :param comment: the new comment, or None to keep the current comment
        """
        if name is None and comment is None:
            return
        update_name_string = f"name = '{name}'" if name is not None else ""
        if name is not None and comment is not None:
            update_name_string += ", "
        update_comment_string = f"comment = '{comment}'" if comment is not None else ""

        self.cursor.execute(f"UPDATE aliasclient SET {update_name_string}, {update_comment_string} WHERE id = {id};")

    def assign_device_to_alias(self, alias_id: int, macs: list[str], ips: list[str]):
        """
        Assign devices to an alias by modifying the network table.

        :param alias_id: the alias ID to which the devices will be assigned (or None to remove them from the alias)
        :param macs: a list of MAC addresses to assign to the alias
        :param ips: a list of IP addresses to assign to the alias
        """
        data = [(alias_id, mac.lower()) for mac in macs]
        data.extend((alias_id, f"ip-{ip}") for ip in ips)

        self.cursor.executemany("UPDATE network SET aliasclient_id = ? WHERE hwaddr = ?;", data)

    def remove_device_from_alias(self, macs: list[str], ips: list[str]):
        """
        Remove devices from an alias by modifying the network table.

        :param macs: a list of MAC addresses to remove from the alias
        :param ips: a list of IP addresses to remove from the alias
        """
        self.assign_device_to_alias(None, macs, ips)