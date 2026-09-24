from langchain_ollama import ChatOllama

from database.schema_context import SchemaContext
from database.sql_observability import SQLGenerationTrace


class SQLGenerator:

    def __init__(
        self,
        model_name: str = "qwen3",
        temperature: float = 0,
    ):

        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature,
        )

    def generate_sql(self, user_question: str) -> str:

        trace = SQLGenerationTrace(user_question)

        try:

            schema = SchemaContext.format_schema()

            relationships = (
                SchemaContext.format_relationships()
            )

            prompt = f"""
You are a SQL generation assistant.

Your task is to convert the user's natural-language
question into a SQLite SELECT query.

IMPORTANT RULES:

1. Generate SELECT statements only.
2. Never generate INSERT, UPDATE, DELETE, DROP,
   ALTER, CREATE, TRUNCATE, PRAGMA, ATTACH or DETACH.
3. Use only tables and columns provided in the schema.
4. Use the provided relationships when joins are required.
5. Do not invent tables or columns.
6. Do not execute the query.
7. Return ONLY the SQL query.
8. Do not use markdown code fences.
9. Do not provide explanations.

DATABASE SCHEMA:

{schema}

RELATIONSHIPS:

{relationships}

USER QUESTION:

{user_question}

SQL:
"""

            response = self.llm.invoke(prompt)

            sql = response.content.strip()

            trace.complete(
                generated_sql=sql,
                success=True,
            )

            return sql

        except Exception as exc:

            trace.complete(
                generated_sql="",
                success=False,
                error=str(exc),
            )

            raise