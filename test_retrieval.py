import sys

sys.path.insert(0, "app")

from rag.index_manager import IndexManager
from rag.retriever import Retriever


def run_test(query: str):

    print("")
    print("=" * 60)
    print(f"Testing query: {query}")
    print("=" * 60)

    manager = IndexManager()

    vector_db = manager.build_index()

    retriever = Retriever(
        vector_db,
        k=3,
        score_threshold=1.5
    )

    results = retriever.search_relevant(query)

    retriever.debug_search(query)

    print("")
    print("Relevant documents returned:")

    if not results:

        print("NO RELEVANT DOCUMENTS FOUND")

    else:

        for result in results:

            document = result["document"]
            score = result["score"]

            print(
                f"- score={score:.4f} "
                f"source={document.metadata.get('source', 'unknown')}"
            )


if __name__ == "__main__":

    run_test(
        "What is the leave policy?"
    )

    run_test(
        "What is the capital of France?"
    )