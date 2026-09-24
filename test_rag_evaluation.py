import sys

sys.path.insert(0, "app")

from rag.index_manager import IndexManager
from rag.retriever import Retriever


EVALUATION_CASES = [
    {
        "query": "What is the leave policy?",
        "expected_source": "LeavePolicy.pdf",
        "should_retrieve": True,
    },
    {
        "query": "How many earned leaves can be carried forward?",
        "expected_source": "LeavePolicy.pdf",
        "should_retrieve": True,
    },
    {
        "query": "What are the working hours?",
        "expected_source": "HRPolicy.pdf",
        "should_retrieve": True,
    },
    {
        "query": "Can employees work from home?",
        "expected_source": "HRPolicy.pdf",
        "should_retrieve": True,
    },
    {
        "query": "What is the VPN requirement?",
        "expected_source": "ITSecurityPolicy.pdf",
        "should_retrieve": True,
    },
    {
        "query": "How much medical insurance coverage is provided?",
        "expected_source": "Insurance.pdf",
        "should_retrieve": True,
    },
    {
        "query": "What is the capital of France?",
        "expected_source": None,
        "should_retrieve": False,
    },
    {
        "query": "Who won the football World Cup?",
        "expected_source": None,
        "should_retrieve": False,
    },
]


def reciprocal_rank(sources, expected_source):
    if expected_source is None:
        return 0.0

    for rank, source in enumerate(sources, start=1):
        if source == expected_source:
            return 1.0 / rank

    return 0.0


def precision_at_k(sources, expected_source, k):
    if expected_source is None:
        return 0.0

    top_k = sources[:k]

    relevant_count = sum(
        1 for source in top_k
        if source == expected_source
    )

    return relevant_count / k


def evaluate():
    manager = IndexManager()
    vector_db = manager.build_index()

    retriever = Retriever(
        vector_db,
        k=3,
        score_threshold=1.5,
    )

    total = len(EVALUATION_CASES)

    passed = 0
    hit_at_1 = 0
    hit_at_3 = 0
    precision_at_1_total = 0.0
    precision_at_3_total = 0.0
    mrr_total = 0.0

    no_result_tests = 0
    no_result_passed = 0

    print("")
    print("=" * 90)
    print("AEGIS RAG EVALUATION")
    print("=" * 90)

    for index, case in enumerate(EVALUATION_CASES, start=1):

        query = case["query"]
        expected_source = case["expected_source"]
        should_retrieve = case["should_retrieve"]

        results = retriever.search_relevant(query)

        sources = [
            result["file_name"]
            for result in results
        ]

        # ---------------------------------------------------------
        # Basic test result
        # ---------------------------------------------------------

        if should_retrieve:
            expected_found = expected_source in sources
            passed_case = expected_found
        else:
            expected_found = len(results) == 0
            passed_case = expected_found

            no_result_tests += 1

            if passed_case:
                no_result_passed += 1

        if passed_case:
            passed += 1

        # ---------------------------------------------------------
        # Retrieval metrics
        # ---------------------------------------------------------

        rr = reciprocal_rank(
            sources,
            expected_source
        )

        p1 = precision_at_k(
            sources,
            expected_source,
            1
        )

        p3 = precision_at_k(
            sources,
            expected_source,
            3
        )

        if expected_source is not None:

            if len(sources) >= 1 and sources[0] == expected_source:
                hit_at_1 += 1

            if expected_source in sources[:3]:
                hit_at_3 += 1

        precision_at_1_total += p1
        precision_at_3_total += p3
        mrr_total += rr

        # ---------------------------------------------------------
        # Test output
        # ---------------------------------------------------------

        status = "PASS" if passed_case else "FAIL"

        print("")
        print(f"Test {index}: {status}")
        print(f"Query            : {query}")
        print(f"Expected Source  : {expected_source}")
        print(f"Retrieved Sources: {sources}")

        if expected_source:
            print(f"Reciprocal Rank  : {rr:.3f}")
            print(f"Precision@1      : {p1:.3f}")
            print(f"Precision@3      : {p3:.3f}")
        else:
            print("Reciprocal Rank  : N/A")
            print("Precision@1      : N/A")
            print("Precision@3      : N/A")

    # -------------------------------------------------------------
    # Aggregate metrics
    # -------------------------------------------------------------

    accuracy = (
        passed / total * 100
        if total
        else 0
    )

    hit_at_1_percentage = (
        hit_at_1 / 6 * 100
        if 6
        else 0
    )

    hit_at_3_percentage = (
        hit_at_3 / 6 * 100
        if 6
        else 0
    )

    precision_at_1 = (
        precision_at_1_total / 6
        if 6
        else 0
    )

    precision_at_3 = (
        precision_at_3_total / 6
        if 6
        else 0
    )

    mrr = (
        mrr_total / 6
        if 6
        else 0
    )

    no_result_accuracy = (
        no_result_passed / no_result_tests * 100
        if no_result_tests
        else 0
    )

    # -------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------

    print("")
    print("=" * 90)
    print("AEGIS RAG EVALUATION SUMMARY")
    print("=" * 90)

    print(f"Total Tests          : {total}")
    print(f"Passed               : {passed}")
    print(f"Failed               : {total - passed}")
    print(f"Overall Accuracy     : {accuracy:.2f}%")

    print("")
    print("Retrieval Metrics")
    print("-" * 90)

    print(f"Hit@1                : {hit_at_1}/{6} ({hit_at_1_percentage:.2f}%)")
    print(f"Hit@3                : {hit_at_3}/{6} ({hit_at_3_percentage:.2f}%)")
    print(f"Precision@1          : {precision_at_1:.3f}")
    print(f"Precision@3          : {precision_at_3:.3f}")
    print(f"MRR                  : {mrr:.3f}")

    print("")
    print("Out-of-Domain Rejection")
    print("-" * 90)

    print(
        f"No-Result Accuracy   : "
        f"{no_result_passed}/{no_result_tests} "
        f"({no_result_accuracy:.2f}%)"
    )

    print("=" * 90)


if __name__ == "__main__":
    evaluate()