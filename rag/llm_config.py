import os
import sys
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Embedding Models
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"
GEMINI_EMBEDDING_MODEL = "models/embedding-001"

# LLM Models
OLLAMA_LLM_MODEL = "qwen2.5:3b-instruct"
GEMINI_LLM_MODEL = "gemini-1.5-flash"

if "gemini" in LLM_PROVIDER:
    if LLM_PROVIDER == "gemini":
        GEMINI_LLM_MODEL = "gemini-1.5-flash"
    elif LLM_PROVIDER == "gemini-1.5-flash-latest":
        GEMINI_LLM_MODEL = "gemini-1.5-flash"
    else:
        GEMINI_LLM_MODEL = LLM_PROVIDER


from typing import Any, Optional

def get_llm(system_prompt: Optional[str] = None) -> Any:
    """
    Returns the configured LLM instance.
    """
    if "gemini" in LLM_PROVIDER:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        if not GOOGLE_API_KEY:
            print("[ERROR] GOOGLE_API_KEY is missing for Gemini provider.")
            sys.exit(1)
            
        return ChatGoogleGenerativeAI(
            model=GEMINI_LLM_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.2,
            convert_system_message_to_human=True # Sometimes needed for older chains, but usually fine
        )
        # Note: System prompt is usually passed during invocation for Chat models, 
        # but if we need it bound, we can do that. 
        # For this simple usage, we'll return the base chat model.
        
    else: # Default to Ollama
        from langchain_ollama import OllamaLLM
        
        return OllamaLLM(
            model=OLLAMA_LLM_MODEL,
            base_url=OLLAMA_BASE_URL,
            system=system_prompt, # OllamaLLM accepts system prompt in init
            temperature=0.2,
            num_ctx=4096,
        )

def get_embeddings() -> Any:
    """
    Returns the configured Embeddings instance.
    """
    if "gemini" in LLM_PROVIDER:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        
        if not GOOGLE_API_KEY:
            print("[ERROR] GOOGLE_API_KEY is missing for Gemini provider.")
            sys.exit(1)
            
        return GoogleGenerativeAIEmbeddings(
            model=GEMINI_EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
        )
        
    else: # Default to Ollama
        from langchain_ollama import OllamaEmbeddings
        
        return OllamaEmbeddings(
            model=OLLAMA_EMBEDDING_MODEL, 
            base_url=OLLAMA_BASE_URL
        )

def get_chroma_db_path() -> str:
    return "./chroma_db"
