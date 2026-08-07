from database.connection import DatabaseConnection


class QueryExecutor:

    def __init__(self):

        self.connection = DatabaseConnection()

    def execute(self, query):

        conn = self.connection.connect()

        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        conn.close()

        return columns, rows