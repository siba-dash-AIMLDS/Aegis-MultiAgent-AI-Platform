from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:

    def __init__(
        self,
        chunk_size=1000,
        chunk_overlap=200
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split_documents(self, documents):

        chunks = self.splitter.split_documents(documents)

        for chunk_number, chunk in enumerate(chunks, start=1):

            file_name = chunk.metadata.get("file_name", "unknown")
            page_number = chunk.metadata.get("page", 0)

            chunk.metadata["chunk_id"] = (
                f"{file_name}:page-{page_number}:chunk-{chunk_number}"
            )

        print(f"Total Chunks : {len(chunks)}")

        return chunks