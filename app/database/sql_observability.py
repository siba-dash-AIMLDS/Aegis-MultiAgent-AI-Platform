import logging
import time
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "sql_execution.log"


logger = logging.getLogger("aegis-sql")

logger.propagate = False
logger.setLevel(logging.INFO)

if not logger.handlers:

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


class SQLGenerationTrace:

    def __init__(self, question: str):

        self.question = question
        self.start_time = time.perf_counter()

    def complete(
        self,
        generated_sql: str,
        success: bool = True,
        error: str | None = None,
    ):

        duration_ms = round(
            (time.perf_counter() - self.start_time) * 1000,
            2,
        )

        logger.info(
            "NL_TO_SQL | "
            "success=%s | "
            "duration_ms=%s | "
            "error=%s | "
            "question=%r | "
            "generated_sql=%r",
            success,
            duration_ms,
            error,
            self.question,
            generated_sql,
        )

        return {
            "question": self.question,
            "generated_sql": generated_sql,
            "success": success,
            "duration_ms": duration_ms,
            "error": error,
        }


class SQLExecutionTrace:

    def __init__(self, query: str):

        self.query = query
        self.start_time = time.perf_counter()

    def complete(
        self,
        success: bool,
        row_count: int,
        error: str | None = None,
    ):

        duration_ms = round(
            (time.perf_counter() - self.start_time) * 1000,
            2,
        )

        logger.info(
            "SQL_EXECUTION | "
            "success=%s | "
            "row_count=%s | "
            "duration_ms=%s | "
            "error=%s | "
            "query=%r",
            success,
            row_count,
            duration_ms,
            error,
            self.query,
        )

        return {
            "query": self.query,
            "success": success,
            "row_count": row_count,
            "duration_ms": duration_ms,
            "error": error,
        }