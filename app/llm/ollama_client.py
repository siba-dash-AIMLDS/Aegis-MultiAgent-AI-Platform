from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen3",
    temperature=0
)


def ask_llm(system_prompt: str, user_prompt: str) -> str:

    messages = [
        ("system", system_prompt),
        ("human", user_prompt)
    ]

    response = llm.invoke(messages)

    return response.content