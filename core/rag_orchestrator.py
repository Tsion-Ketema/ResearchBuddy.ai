from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from core.llm_factory import get_chat_model
from core.prompts import get_rag_prompt_template


def ask_question(vectorstore, question: str) -> str:
    """Handles the RAG orchestration: searches vectorstore and passes to LLM."""
    llm = get_chat_model()
    prompt_template = get_rag_prompt_template()

    # Create chains
    question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
    retriever = vectorstore.as_retriever()
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # Execute query
    response = rag_chain.invoke({"input": question})
    return response["answer"]
