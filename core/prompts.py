from langchain_core.prompts import ChatPromptTemplate

# Centralized prompt strings
RAG_SYSTEM_PROMPT = (
    "You are an expert research assistant helping a user analyze multiple documents. "
    "Use the provided context to answer the user's questions thoroughly and accurately. "
    "Synthesize information across different parts of the context if necessary. "
    "If the answer is not contained within the provided context, state clearly that you cannot find the answer in the current documents. "
    "Do not hallucinate or guess.\n\n"
    "Context:\n{context}"
)


def get_rag_prompt_template():
    """Returns the formatted ChatPromptTemplate."""
    return ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_PROMPT),
        ("human", "{input}"),
    ])
