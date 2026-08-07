class Retriever:

    def __init__(self, vector_db, k=3):

        self.retriever = vector_db.as_retriever(
            search_kwargs={"k": k}
        )

    def search(self, query):

        return self.retriever.invoke(query)