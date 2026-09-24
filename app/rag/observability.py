import logging
import time


logger = logging.getLogger("aegis-rag")


class RetrievalTrace:

    def __init__(self, query: str, top_k: int, score_threshold: float):
        self.query = query
        self.top_k = top_k
        self.score_threshold = score_threshold
        self.start_time = time.perf_counter()

    def complete(
        self,
        retrieved_count: int,
        accepted_count: int,
        sources: list[str],
        security_flags: int,
    ):
        duration_ms = round(
            (time.perf_counter() - self.start_time) * 1000,
            2,
        )

        logger.info(
            "RAG_RETRIEVAL "
            "query=%r "
            "top_k=%s "
            "threshold=%s "
            "retrieved=%s "
            "accepted=%s "
            "security_flags=%s "
            "sources=%s "
            "duration_ms=%s",
            self.query,
            self.top_k,
            self.score_threshold,
            retrieved_count,
            accepted_count,
            security_flags,
            sources,
            duration_ms,
        )

        return {
            "query": self.query,
            "top_k": self.top_k,
            "score_threshold": self.score_threshold,
            "retrieved_count": retrieved_count,
            "accepted_count": accepted_count,
            "security_flags": security_flags,
            "sources": sources,
            "duration_ms": duration_ms,
        }