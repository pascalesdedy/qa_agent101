import os
import glob
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Configuration
DATA_DIR = "./rag/docs/" # Changed to directory
CHROMA_PATH = "./chroma_db"
EMBEDDING_MODEL = "nomic-embed-text" 

def ingest_data():
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Directory {DATA_DIR} not found.")
        return

    print(f"📂 Scanning directory: {DATA_DIR}")
    files = glob.glob(os.path.join(DATA_DIR, "*.md"))
    
    if not files:
        print("⚠️ No markdown files found.")
        return

    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for file_path in files:
        print(f"📄 Loading {file_path}...")
        loader = UnstructuredMarkdownLoader(file_path)
        data = loader.load()
        chunks = text_splitter.split_documents(data)
        all_chunks.extend(chunks)
        print(f"   - {len(chunks)} chunks.")

    if not all_chunks:
        print("⚠️ No content to ingest.")
        return

    print(f"📦 Creating embeddings for {len(all_chunks)} total chunks with {EMBEDDING_MODEL}...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    print("💾 Saving to ChromaDB...")
    # Persist the DB
    db = Chroma.from_documents(
        documents=all_chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_PATH
    )
    print(f"✅ Ingestion complete! Data saved to {CHROMA_PATH}")

if __name__ == "__main__":
    ingest_data()
