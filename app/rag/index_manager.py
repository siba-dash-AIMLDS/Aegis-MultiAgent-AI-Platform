from rag.document_loader import DocumentLoader
from rag.text_splitter import TextSplitter
from rag.vector_store import VectorStore


class IndexManager:

    def __init__(self):

        self.vector_db = None

    def build_index(self):

        if self.vector_db is not None:
            return self.vector_db

        loader = DocumentLoader(
            "app/data/documents"
        )

        documents = loader.load_documents()

        splitter = TextSplitter()

        chunks = splitter.split_documents(documents)

        self.vector_db = VectorStore().create_vector_store(chunks)

        print("FAISS Index Created Successfully")

        return self.vector_db