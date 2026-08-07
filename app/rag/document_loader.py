from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


class DocumentLoader:

    def __init__(self, document_path: str):

        self.document_path = Path(document_path)

    def load_documents(self):

        documents = []

        pdf_files = sorted(self.document_path.glob("*.pdf"))

        for pdf in pdf_files:

            print(f"Loading : {pdf.name}")

            loader = PyPDFLoader(str(pdf))

            documents.extend(loader.load())

        print(f"Total Pages Loaded : {len(documents)}")

        return documents