
from graph.state import AgentState

from rag.index_manager import IndexManager
from rag.retriever import Retriever
from rag.security import RetrievalSecurity
import logging
from rag.observability import RetrievalTrace


def knowledge_agent(state: AgentState):

    print("===== Knowledge Agent =====")

    if "KnowledgeAgent" not in state["execution_plan"]:

        print("Knowledge Agent Skipped")

        state["knowledge_result"] = "Knowledge Agent Skipped."

        return state

    print("Knowledge Agent Executing...")

    index_manager = IndexManager()

    vector_db = index_manager.build_index()

    retriever = Retriever(
        vector_db,
        k=3,
        score_threshold=1.5
    )

    user_query = state["user_request"]

    retrieval_trace = RetrievalTrace(
        query=user_query,
        top_k=3,
        score_threshold=1.5
    )

    retrieval_results = retriever.search_relevant(user_query)

    security_flags = 0
    sources = []

    result = """
Knowledge Agent

Relevant Information

----------------------------------------
"""

    if not retrieval_results:

        result += "\nNo relevant documents found."

    else:

        for item in retrieval_results:

            doc = item["document"]
            sources.append(item["file_name"])

            security_result = RetrievalSecurity.sanitize_document(
                doc.page_content
            )

            if security_result["injection_detected"]:
                security_flags += 1

                print(
                    f"Potential prompt injection detected in "
                    f"{item['file_name']} "
                    f"page {item['page']}"
                )

                result += (
                    f"\nSource : {item['file_name']}\n"
                    f"Document : {item['document_id']}\n"
                    f"Page : {item['page']}\n"
                    f"Chunk ID : {item['chunk_id']}\n"
                    f"Retrieval Score : {item['score']:.4f}\n"
                    f"Security Status : POTENTIAL_PROMPT_INJECTION\n\n"
                    "Retrieved content was flagged as containing "
                    "instruction-like text and was not supplied as "
                    "trusted instructions.\n"
                )

                result += (
                    "\n----------------------------------------\n"
                )

                continue

            result += (
                f"\nSource : {item['file_name']}\n"
                f"Document : {item['document_id']}\n"
                f"Page : {item['page']}\n"
                f"Chunk ID : {item['chunk_id']}\n"
                f"Retrieval Score : {item['score']:.4f}\n"
                f"Security Status : CLEAN\n\n"
            )

            result += doc.page_content

            result += (
                "\n\n----------------------------------------\n"
            )

    retrieval_trace.complete(
        retrieved_count=len(retrieval_results),
        accepted_count=len(retrieval_results),
        sources=sources,
        security_flags=security_flags,
    )

    state["knowledge_result"] = result

    return state

