import requests
import json
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import sys

SYSTEM_PROMPT = """
You are a Senior QA Engineer with 10+ years of experience.

Your ONLY responsibility is software quality assurance.
You do NOT answer questions outside QA domain.

Your expertise:
- Test Planning & Test Strategy
- Test Scenario & Test Case Design
- BDD / Gherkin
- Functional, Regression, Negative, Edge Case testing
- Web & Mobile Testing
- Playwright Automation (JavaScript / TypeScript)
- TestRail structure and best practices
- Requirement analysis & risk-based testing

Rules you MUST follow:
1. Always produce structured, clear, and concise output
2. Prefer tables or bullet lists when applicable
3. Use professional QA terminology
4. Do NOT give generic explanations
5. Do NOT hallucinate features not mentioned
6. Ask clarification ONLY if requirement is ambiguous or missing critical info
7. When creating test cases:
   - Include positive, negative, and edge cases
   - Consider validation, boundary, and error handling
8. When using BDD:
   - Use Given / When / Then format
   - One clear assertion per scenario
9. ALWAYS Use the provided CONTEXT from the SOP to answer questions if relevant.

Output format guidelines:
- Use clear section headers
- Avoid unnecessary verbosity
- Focus on practical, executable test cases

"""

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# RAG Configuration
CHROMA_PATH = "./chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"

try:
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})
except Exception as e:
    print(f"[ERROR] RAG Init failed: {e}")
    retriever = None

llm = OllamaLLM(
    model="qwen2.5:3b-instruct",
    system=SYSTEM_PROMPT,
    temperature=0.2,
    num_ctx=4096,
)

def get_context(query: str):
    if not retriever:
        return ""
    try:
        docs = retriever.invoke(query)
        return "\n\n".join([d.page_content for d in docs])
    except Exception as e:
        print(f"[WARN] Retrieval failed: {e}")
        return ""

def ask_qa(prompt: str):
    # This function is not used in the main loop but kept for compatibility
    context = get_context(prompt)
    full_prompt = f"CONTEXT FROM SOP:\n{context}\n\nUser: {prompt}"
    response = llm.invoke(full_prompt)

    # DEBUG GUARD
    if response is None or response.strip() == "":
        return "[ERROR] Model returned empty response"

    return response


def ask_qa_streaming(prompt: str):
    """
    Stream token response real-time dari Ollama tanpa LangChain
    """
    
    print("🔍 Retrieving context...")
    context = get_context(prompt)
    if context:
        print(f"📄 Found {len(context)} chars of context.\n")
    else:
        print("⚠️ No relevant context found in SOP (or retrieval failed).\n")

    full_prompt = f"{SYSTEM_PROMPT}\n\nCONTEXT FROM SOP:\n{context}\n\nUser: {prompt}"
    
    payload = {
        "model": "qwen2.5:3b-instruct",
        "prompt": full_prompt,
        "stream": True,
        "temperature": 0.2,
        "num_ctx": 4096,
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True, timeout=300)
        response.raise_for_status()
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                token = data.get("response", "")
                if token:
                    print(token, end="", flush=True)
                    full_response += token
                
                # Stop jika done = true
                if data.get("done", False):
                    break
        
        print()  # New line setelah streaming selesai
        return full_response
        
    except requests.exceptions.ConnectionError:
        error_msg = "[ERROR] Tidak dapat terhubung ke Ollama API di localhost:11434. Pastikan Ollama sudah berjalan."
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"[ERROR] {str(e)}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    print("🧠 QA AI Assistant Ready (with RAG for SOP) (type 'exit' to quit)")
    print("Mode: STREAMING REAL-TIME TOKENS\n")
    
    while True:
        try:
            q = input("\n[QA INPUT] ")
            if q.lower() in ["exit", "quit"]:
                break
            
            print("\n[QA OUTPUT]\n")
            print(ask_qa(q))
        except KeyboardInterrupt:
            print("\nExiting...")
            break
