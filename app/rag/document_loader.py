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

            pdf_documents = loader.load()

            for page_number, document in enumerate(pdf_documents, start=1):

                document.metadata["file_name"] = pdf.name
                document.metadata["document_id"] = pdf.stem
                document.metadata["page"] = page_number

            documents.extend(pdf_documents)

        print(f"Total Pages Loaded : {len(documents)}")

        return documents