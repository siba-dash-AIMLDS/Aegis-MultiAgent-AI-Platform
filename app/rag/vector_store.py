from langchain_community.vectorstores import FAISS

from rag.embeddings import EmbeddingModel


class VectorStore:

    def __init__(self):

        self.embedding = EmbeddingModel().get_embedding_model()

    def create_vector_store(self, chunks):

        vector_db = FAISS.from_documents(
            chunks,
            self.embedding
        )

        return vector_db