import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Configuration
DATA_PATH = "./rag/docs/sop_qa.md"
CHROMA_PATH = "./chroma_db"
MODEL_NAME = "qwen2.5:3b-instruct" # Using the same model for embeddings if compatible, or a dedicated embedding model like 'nomic-embed-text' if available. 
# For simplicity with Ollama, we often use a dedicated embedding model, but let's try 'qwen2.5:3b-instruct' or check if we need to pull 'nomic-embed-text'.
# Usually LLMs are not good embedding models. 
# Let's assume the user has 'nomic-embed-text' or we can try to use the LLM. 
# Better practice: Use a specific embedding model. I'll use 'nomic-embed-text' and command the user to pull it if needed, or default to the LLM if it works (often suboptimal).
# Let's stick to the requested model 'qwen2.5:3b-instruct' for simplicity unless it fails, but actually standard advice is 'nomic-embed-text' or 'mxbai-embed-large'.
# I will use 'nomic-embed-text' as default for embeddings in the code and ask to pull it.
EMBEDDING_MODEL = "nomic-embed-text" 

def ingest_data():
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] File {DATA_PATH} not found.")
        return

    print("📄 Loading SOP document...")
    loader = UnstructuredMarkdownLoader(DATA_PATH)
    data = loader.load()

    print("✂️ Splitting document...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(data)
    print(f"   Split into {len(chunks)} chunks.")

    print(f"📦 Creating embeddings with {EMBEDDING_MODEL}...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    print("💾 Saving to ChromaDB...")
    # Persist the DB
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_PATH
    )
    print(f"✅ Ingestion complete! Data saved to {CHROMA_PATH}")

if __name__ == "__main__":
    ingest_data()
