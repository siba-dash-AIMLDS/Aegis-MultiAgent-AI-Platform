from app.database.connection import DatabaseConnection
from app.database.sql_security import SQLSecurity
from app.database.sql_observability import SQLExecutionTrace


class QueryExecutor:

    MAX_RESULT_ROWS = 1000

    def __init__(self):
        self.connection = DatabaseConnection()

    def execute(self, query):

        trace = SQLExecutionTrace(query)

        # Validate SQL before execution
        is_valid, message = SQLSecurity.validate_read_only_query(query)

        if not is_valid:

            trace.complete(
                success=False,
                row_count=0,
                error=message,
            )

            raise ValueError(message)

        conn = self.connection.connect()

        try:

            cursor = conn.cursor()

            cursor.execute(query)

            rows = cursor.fetchmany(
                self.MAX_RESULT_ROWS
            )

            columns = [
                column[0]
                for column in cursor.description
            ]

            trace.complete(
                success=True,
                row_count=len(rows),
            )

            return columns, rows

        except Exception as exc:

            trace.complete(
                success=False,
                row_count=0,
                error=str(exc),
            )

            raise

        finally:

            conn.close()