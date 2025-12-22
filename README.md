# QA Agent with RAG

This project implements an AI-powered Quality Assurance (QA) agent utilizing Retrieval Augmented Generation (RAG). It allows for querying Standard Operating Procedures (SOPs) and generating standardized TestRail test cases.

## Features

- **RAG for QA**: Retrieve and generate answers based on your internal SOPs.
- **Document Ingestion**: Easily ingest markdown documents into a ChromaDB vector store.
- **Standardized Templates**: Includes templates for TestRail test cases.

## Project Structure

- `qa_brain.py`: The main application logic for the QA agent.
- `ingest.py`: Script to ingest documentation (e.g., SOPs) into the vector database.
- `data/`: Directory for storing source documents.
- `rag/`: Contains auxiliary RAG documentation and templates.
- `chroma_db/`: Stores the vector embeddings.

## Getting Started

1.  **Ingest Data**:
    Run the ingestion script to process your documents:
    ```bash
    python ingest.py
    ```

2.  **Run the Agent**:
    Start the QA agent:
    ```bash
    python qa_brain.py
    ```
