from llm.ollama_client import ask_llm


response = ask_llm(
    "You are a helpful assistant.",
    "Say Hello Orion."
)

print(response)