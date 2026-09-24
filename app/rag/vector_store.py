from pathlib import Path

from langchain_community.vectorstores import FAISS

from rag.embeddings import EmbeddingModel


class VectorStore:

    def __init__(self):

        self.embedding = EmbeddingModel.get_embedding_model()

    def create_vector_store(self, chunks):

        return FAISS.from_documents(
            chunks,
            self.embedding
        )

    def save_vector_store(self, vector_db, index_path: Path):

        index_path.mkdir(
            parents=True,
            exist_ok=True
        )

        vector_db.save_local(
            str(index_path)
        )

        print(
            f"FAISS index persisted to: {index_path}"
        )

    def load_vector_store(self, index_path: Path):

        if not index_path.exists():

            return None

        index_file = index_path / "index.faiss"
        metadata_file = index_path / "index.pkl"

        if not index_file.exists() or not metadata_file.exists():

            return None

        print(
            f"Loading persisted FAISS index from: {index_path}"
        )

        vector_db = FAISS.load_local(
            str(index_path),
            self.embedding,
            allow_dangerous_deserialization=True
        )

        return vector_db