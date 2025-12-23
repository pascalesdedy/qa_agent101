import os
import glob
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.llm_config import get_embeddings, get_chroma_db_path
from rag.logger import setup_logger

logger = setup_logger("ingest")

# Configuration
DATA_DIR = "./rag/docs/"  

def ingest_data() -> None:
    if not os.path.exists(DATA_DIR):
        logger.error(f"Directory {DATA_DIR} not found.")
        return

    logger.info(f"Scanning directory: {DATA_DIR}")
    files = glob.glob(os.path.join(DATA_DIR, "*.md"))
    
    if not files:
        logger.warning(f"No markdown files found.")
        return

    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for file_path in files:
        logger.info(f"Loading {file_path}...")
        loader = UnstructuredMarkdownLoader(file_path)
        data = loader.load()
        chunks = text_splitter.split_documents(data)
        all_chunks.extend(chunks)
        logger.info(f"   - {len(chunks)} chunks.")

    if not all_chunks:
        logger.warning("No content to ingest.")
        return

    logger.info(f"Creating embeddings for {len(all_chunks)} total chunks...")
    embeddings = get_embeddings()

    logger.info("Saving to ChromaDB...")
    # Persist the DB
    db = Chroma.from_documents(
        documents=all_chunks, 
        embedding=embeddings, 
        persist_directory=get_chroma_db_path()
    )
    logger.info(f"Ingestion complete! Data saved to {get_chroma_db_path()}")

if __name__ == "__main__":
    ingest_data()
