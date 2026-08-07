class ConversationMemory:

    def __init__(self):

        self.history = []

    def add(self, user_query, response):

        self.history.append({
            "user": user_query,
            "assistant": response
        })

    def get_history(self):

        return self.history

    def clear(self):

        self.history = []


# ----------------------------------------
# Global Memory Instance
# ----------------------------------------

memory = ConversationMemory()