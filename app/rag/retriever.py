from typing import Any


class Retriever:

    def __init__(
        self,
        vector_db,
        k: int = 3,
        score_threshold: float = 1.5
    ):

        self.vector_db = vector_db
        self.k = k
        self.score_threshold = score_threshold

    def search_with_scores(self, query: str) -> list[dict[str, Any]]:

        results = self.vector_db.similarity_search_with_score(
            query,
            k=self.k
        )

        formatted_results = []

        for document, score in results:

            metadata = document.metadata

            formatted_results.append(
                {
                    "document": document,
                    "score": float(score),
                    "source": metadata.get("source", "unknown"),
                    "file_name": metadata.get("file_name", "unknown"),
                    "document_id": metadata.get("document_id", "unknown"),
                    "page": metadata.get("page", 0),
                    "chunk_id": metadata.get("chunk_id", "unknown"),
                }
            )

        return formatted_results

    def search_relevant(self, query: str) -> list[dict[str, Any]]:

        results = self.search_with_scores(query)

        return [
            result
            for result in results
            if result["score"] <= self.score_threshold
        ]

    def search(self, query: str):

        results = self.search_relevant(query)

        return [
            result["document"]
            for result in results
        ]

    def debug_search(self, query: str):

        results = self.search_with_scores(query)

        print("")
        print("========== RAG RETRIEVAL DEBUG ==========")
        print(f"Query: {query}")
        print(f"Top K: {self.k}")
        print(f"Threshold: {self.score_threshold}")

        for index, result in enumerate(results, start=1):

            score = result["score"]
            file_name = result["file_name"]
            document_id = result["document_id"]
            page = result["page"]
            chunk_id = result["chunk_id"]

            status = (
                "ACCEPT"
                if score <= self.score_threshold
                else "REJECT"
            )

            print(
                f"{index}. "
                f"score={score:.4f} "
                f"status={status} "
                f"file={file_name} "
                f"document={document_id} "
                f"page={page} "
                f"chunk={chunk_id}"
            )

        print("==========================================")
        print("")

        return results