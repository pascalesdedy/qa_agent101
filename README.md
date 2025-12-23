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

## Configuration

The agent can be configured to connect to a local or remote Ollama instance.

1.  **Environment Setup**:
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```

2.  **Remote LLM (Optional)**:
    If your Ollama instance is running on a different machine, update `OLLAMA_BASE_URL` in `.env`:
    ```ini
    OLLAMA_BASE_URL=http://<REMOTE_IP>:11434
    ```

3.  **Google Gemini (Optional)**:
    To use Google Gemini instead of Ollama:
    - Set `LLM_PROVIDER=gemini` in `.env`.
    - Add your API key: `GOOGLE_API_KEY=your_api_key`.

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
