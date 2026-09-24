import json
from pathlib import Path

from rag.document_loader import DocumentLoader
from rag.text_splitter import TextSplitter
from rag.vector_store import VectorStore
from rag.embeddings import EMBEDDING_MODEL_NAME


class IndexManager:

    def __init__(self):

        self.vector_db = None

        self.project_root = Path(__file__).resolve().parents[2]

        self.document_path = (
            self.project_root
            / "app"
            / "data"
            / "documents"
        )

        self.index_path = (
            self.project_root
            / "app"
            / "data"
            / "vector_store"
        )

        self.manifest_path = (
            self.index_path
            / "manifest.json"
        )

        self.chunk_size = 1000
        self.chunk_overlap = 200

    def build_index(self):

        if self.vector_db is not None:

            return self.vector_db

        vector_store = VectorStore()

        # --------------------------------------------------
        # Try loading an existing persisted index
        # --------------------------------------------------

        if self._index_is_current():

            print("Loading existing FAISS index...")

            self.vector_db = (
                vector_store.load_vector_store(
                    self.index_path
                )
            )

            if self.vector_db is not None:

                print(
                    "Existing FAISS index loaded successfully."
                )

                return self.vector_db

        # --------------------------------------------------
        # Build a new index
        # --------------------------------------------------

        print("Building new FAISS index...")

        loader = DocumentLoader(
            str(self.document_path)
        )

        documents = loader.load_documents()

        if not documents:

            raise ValueError(
                "No PDF documents found for RAG indexing."
            )

        splitter = TextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        chunks = splitter.split_documents(
            documents
        )

        self.vector_db = (
            vector_store.create_vector_store(
                chunks
            )
        )

        # --------------------------------------------------
        # Persist FAISS index
        # --------------------------------------------------

        vector_store.save_vector_store(
            self.vector_db,
            self.index_path
        )

        # --------------------------------------------------
        # Persist index manifest
        # --------------------------------------------------

        self._save_manifest()

        print(
            "FAISS index created and persisted successfully."
        )

        return self.vector_db

    # ======================================================
    # Manifest Management
    # ======================================================

    def _get_document_manifest(self):

        documents = []

        for pdf in sorted(
            self.document_path.glob("*.pdf")
        ):

            stat = pdf.stat()

            documents.append(
                {
                    "name": pdf.name,
                    "size": stat.st_size,
                    "modified_time": stat.st_mtime
                }
            )

        return documents

    def _save_manifest(self):

        self.index_path.mkdir(
            parents=True,
            exist_ok=True
        )

        manifest = {
            "embedding_model": EMBEDDING_MODEL_NAME,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "documents": self._get_document_manifest()
        }

        with open(
            self.manifest_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                manifest,
                file,
                indent=2
            )

    def _index_is_current(self):

        if not self.index_path.exists():

            return False

        index_file = (
            self.index_path
            / "index.faiss"
        )

        metadata_file = (
            self.index_path
            / "index.pkl"
        )

        if not index_file.exists():

            return False

        if not metadata_file.exists():

            return False

        if not self.manifest_path.exists():

            return False

        try:

            with open(
                self.manifest_path,
                "r",
                encoding="utf-8"
            ) as file:

                manifest = json.load(file)

        except (OSError, json.JSONDecodeError):

            return False

        if (
            manifest.get("embedding_model")
            != EMBEDDING_MODEL_NAME
        ):

            return False

        if (
            manifest.get("chunk_size")
            != self.chunk_size
        ):

            return False

        if (
            manifest.get("chunk_overlap")
            != self.chunk_overlap
        ):

            return False

        current_documents = (
            self._get_document_manifest()
        )

        indexed_documents = (
            manifest.get("documents", [])
        )

        return current_documents == indexed_documents