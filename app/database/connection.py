import sqlite3


class DatabaseConnection:

    def __init__(self):

        self.db_path = "app/data/aegis.db"

    def connect(self):

        return sqlite3.connect(self.db_path)