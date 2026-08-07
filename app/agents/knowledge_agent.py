from graph.state import AgentState

from rag.index_manager import IndexManager
from rag.retriever import Retriever


def knowledge_agent(state: AgentState):

    print("===== Knowledge Agent =====")

    # ----------------------------------------
    # Execute only if selected by Planner
    # ----------------------------------------
    if "KnowledgeAgent" not in state["execution_plan"]:

        print("Knowledge Agent Skipped")

        state["knowledge_result"] = "Knowledge Agent Skipped."

        return state

    print("Knowledge Agent Executing...")

    # ----------------------------------------
    # Build / Load FAISS Index
    # ----------------------------------------
    index_manager = IndexManager()

    vector_db = index_manager.build_index()

    retriever = Retriever(vector_db)

    # ----------------------------------------
    # Semantic Search
    # ----------------------------------------
    user_query = state["user_request"]

    documents = retriever.search(user_query)

    # ----------------------------------------
    # Prepare Response
    # ----------------------------------------
    result = """
Knowledge Agent

Relevant Information

----------------------------------------
"""

    if not documents:

        result += "\nNo relevant documents found."

    else:

        for doc in documents:

            source = doc.metadata.get("source", "")

            file_name = source.split("\\")[-1]

            result += f"\nSource : {file_name}\n\n"

            result += doc.page_content

            result += "\n\n----------------------------------------\n"

    # ----------------------------------------
    # Update Workflow State
    # ----------------------------------------
    state["knowledge_result"] = result

    return state