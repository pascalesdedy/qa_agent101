from typing import Optional
from langchain_chroma import Chroma
from rag.llm_config import get_llm, get_embeddings, get_chroma_db_path
from rag.prompts import SYSTEM_PROMPT
from rag.logger import setup_logger

logger = setup_logger("qa_brain")

try:
    embeddings = get_embeddings()
    db = Chroma(persist_directory=get_chroma_db_path(), embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    embeddings = get_embeddings()
    db = Chroma(persist_directory=get_chroma_db_path(), embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})
except Exception as e:
    logger.error(f"RAG Init failed: {e}")
    retriever = None

# Initialize LLM
llm = get_llm(system_prompt=SYSTEM_PROMPT)

def get_context(query: str) -> str:
    if not retriever:
        return ""
    try:
        docs = retriever.invoke(query)
        if not docs:
            logger.info("No documents retrieved for query.")
            return ""
        return "\n\n".join([d.page_content for d in docs])
    except Exception as e:
        logger.warning(f"Retrieval failed: {e}")
        return ""

def ask_qa_streaming(prompt: str):
    """
    Stream token response using LangChain's built-in streaming capabilities.
    """
    
    logger.info("Retrieving context...")
    context = get_context(prompt)
    if context:
        logger.info(f"Found {len(context)} chars of context.")
    else:
        logger.warning(f"No relevant context found in SOP (or retrieval failed).")

    full_prompt = f"CONTEXT FROM SOP:\n{context}\n\nUser: {prompt}"
    
    try:
        print("\n[QA OUTPUT]\n") # Keep this print for user UX in CLI
        full_response = ""
        for chunk in llm.stream(full_prompt):
            print(chunk, end="", flush=True)
            full_response += chunk
        print("\n") # New line after streaming
        return full_response
        
    except Exception as e:
        error_msg = f"Generation failed: {str(e)}"
        logger.error(error_msg)
        return f"\n[ERROR] {error_msg}"

if __name__ == "__main__":
    print("🧠 QA AI Assistant Ready (with RAG for SOP) (type 'exit' to quit)")
    print("Mode: STREAMING REAL-TIME TOKENS\n")
    
    while True:
        try:
            q = input("\n[QA INPUT] ")
            if q.lower() in ["exit", "quit"]:
                break
            
            # Use the streaming function strictly
            ask_qa_streaming(q)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
