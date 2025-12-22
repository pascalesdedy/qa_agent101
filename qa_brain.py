import sys
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

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

def ask_qa_streaming(prompt: str):
    """
    Stream token response using LangChain's built-in streaming capabilities.
    """
    
    print("🔍 Retrieving context...")
    context = get_context(prompt)
    if context:
        print(f"📄 Found {len(context)} chars of context.\n")
    else:
        print("⚠️ No relevant context found in SOP (or retrieval failed).\n")

    full_prompt = f"CONTEXT FROM SOP:\n{context}\n\nUser: {prompt}"
    
    try:
        print("[QA OUTPUT]\n")
        full_response = ""
        for chunk in llm.stream(full_prompt):
            print(chunk, end="", flush=True)
            full_response += chunk
        print("\n") # New line after streaming
        return full_response
        
    except Exception as e:
        error_msg = f"\n[ERROR] Generation failed: {str(e)}"
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
            
            # Use the streaming function strictly
            ask_qa_streaming(q)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
