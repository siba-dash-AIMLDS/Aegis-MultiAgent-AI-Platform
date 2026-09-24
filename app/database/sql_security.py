import re

from database.schema_context import SchemaContext, ALLOWED_TABLES


class SQLSecurity:

    FORBIDDEN_KEYWORDS = {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "ATTACH",
        "DETACH",
        "PRAGMA",
    }

    SQL_FUNCTIONS = {
        "COUNT",
        "SUM",
        "AVG",
        "MIN",
        "MAX",
        "COALESCE",
        "ROUND",
    }

    SQL_KEYWORDS = {
        "SELECT",
        "FROM",
        "WHERE",
        "AND",
        "OR",
        "NOT",
        "NULL",
        "IS",
        "IN",
        "AS",
        "ON",
        "JOIN",
        "INNER",
        "LEFT",
        "RIGHT",
        "OUTER",
        "GROUP",
        "BY",
        "ORDER",
        "ASC",
        "DESC",
        "HAVING",
        "LIMIT",
        "OFFSET",
        "DISTINCT",
        "CASE",
        "WHEN",
        "THEN",
        "ELSE",
        "END",
        "LIKE",
        "BETWEEN",
    }

    @classmethod
    def validate_read_only_query(cls, query: str) -> tuple[bool, str]:

        if not query or not query.strip():
            return False, "SQL query is empty."

        normalized = query.strip()

        # Remove a single trailing semicolon.
        if normalized.endswith(";"):
            normalized = normalized[:-1].strip()

        # Prevent multiple SQL statements.
        if ";" in normalized:
            return False, "Multiple SQL statements are not allowed."

        # Only SELECT statements are allowed.
        if not re.match(r"^SELECT\b", normalized, re.IGNORECASE):
            return False, "Only SELECT statements are allowed."

        # Check for forbidden SQL operations.
        for keyword in cls.FORBIDDEN_KEYWORDS:

            pattern = rf"\b{keyword}\b"

            if re.search(pattern, normalized, re.IGNORECASE):
                return False, (
                    f"Forbidden SQL operation detected: {keyword}"
                )

        # Validate referenced tables.
        valid, message = cls._validate_tables(normalized)

        if not valid:
            return False, message

        # Validate columns.
        valid, message = cls._validate_columns(normalized)

        if not valid:
            return False, message

        return True, "SQL query accepted."

    @classmethod
    def _validate_tables(cls, query: str) -> tuple[bool, str]:

        table_matches = re.findall(
            r"\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)",
            query,
            re.IGNORECASE,
        )

        for table in table_matches:

            if table.lower() not in ALLOWED_TABLES:
                return False, (
                    f"Table is not allowed: {table}"
                )

        return True, "Tables accepted."

    @classmethod
    def _validate_columns(cls, query: str) -> tuple[bool, str]:

        schema = SchemaContext.get_schema()

        # Build a flat set of all valid columns.
        allowed_columns = {
            column.lower()
            for columns in schema.values()
            for column in columns
        }

        # ---------------------------------------------------------
        # 1. Validate qualified columns:
        #    employees.id
        #    orders.customer_id
        # ---------------------------------------------------------

        qualified_columns = re.findall(
            r"\b([A-Za-z_][A-Za-z0-9_]*)\."
            r"([A-Za-z_][A-Za-z0-9_]*)\b",
            query,
            re.IGNORECASE,
        )

        for table, column in qualified_columns:

            table = table.lower()
            column = column.lower()

            if table not in schema:
                continue

            if column not in {
                allowed_column.lower()
                for allowed_column in schema[table]
            }:
                return False, (
                    f"Column is not allowed: "
                    f"{table}.{column}"
                )

        # ---------------------------------------------------------
        # 2. Remove qualified references from the query.
        # ---------------------------------------------------------

        cleaned_query = re.sub(
            r"\b[A-Za-z_][A-Za-z0-9_]*\."
            r"[A-Za-z_][A-Za-z0-9_]*\b",
            "",
            query,
        )

        # ---------------------------------------------------------
        # 3. Extract SQL identifiers.
        # ---------------------------------------------------------

        identifiers = re.findall(
            r"\b[A-Za-z_][A-Za-z0-9_]*\b",
            cleaned_query,
        )

        for identifier in identifiers:

            normalized = identifier.lower()

            # Ignore SQL keywords.
            if normalized.upper() in cls.SQL_KEYWORDS:
                continue

            # Ignore SQL functions.
            if normalized.upper() in cls.SQL_FUNCTIONS:
                continue

            # Ignore allowed table names.
            if normalized in ALLOWED_TABLES:
                continue

            # Ignore numeric-looking identifiers.
            if normalized.isdigit():
                continue

            # Ignore valid unqualified columns.
            if normalized in allowed_columns:
                continue

            # Ignore wildcard.
            if normalized == "*":
                continue

            return False, (
                f"Column or identifier is not allowed: "
                f"{identifier}"
            )

        return True, "Columns accepted."