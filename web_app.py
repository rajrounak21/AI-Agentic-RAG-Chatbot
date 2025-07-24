import os
from uuid import uuid4
import streamlit as st
from dotenv import load_dotenv

from agents.ingestionAgent import IngestionAgent
from agents.retrievalAgent import RetrievalAgent
from agents.LLMResponseAgent import LLMResponseAgent
from mcp import create_mcp_message

# Load API key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Main UI
st.title("📘 AI Q&A System with MCP Tracing")

# Upload documents
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("Upload files and ask questions.")
uploaded_files = st.sidebar.file_uploader(
    "📂 Upload documents",
    type=["pdf", "docx", "pptx", "csv", "txt", "md"],
    accept_multiple_files=True
)
# Sidebar
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state["chat_history"] = []
    st.rerun()
# Load & process documents
if uploaded_files:
    os.makedirs("uploaded_docs", exist_ok=True)
    file_paths = []
    for file in uploaded_files:
        save_path = os.path.join("uploaded_docs", file.name)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
        file_paths.append(save_path)

    # Init agents
    ingestion_agent = IngestionAgent()
    retrieval_agent = RetrievalAgent(persist_dir="vector_store")
    llm_agent = LLMResponseAgent()

    # Ingest
    docs = ingestion_agent.run(file_paths)
    ingest_msg = create_mcp_message(
        sender="IngestionAgent",
        receiver="RetrievalAgent",
        msg_type="DOCUMENT_PARSED",
        trace_id=str(uuid4()),
        payload={"documents": docs}
    )

    retrieval_agent.store_documents(ingest_msg["payload"]["documents"])
    st.success("✅ Documents processed and indexed.")

# Ask UI
st.markdown("### 💬 Ask your question")
query = st.text_input("Type your question")
ask_clicked = st.button("🔍 Ask")

# Query logic
if ask_clicked and query:
    retrieval_agent = RetrievalAgent(persist_dir="vector_store")
    llm_agent = LLMResponseAgent()

    # Retrieve relevant docs
    retrieved_docs = retrieval_agent.retrieve(query)
    top_chunks = []
    sources = []
    for doc in retrieved_docs:
        if hasattr(doc, "page_content"):
            top_chunks.append(doc.page_content)
            sources.append(doc.metadata.get("source", "Unknown") if hasattr(doc, "metadata") else "Unknown")
        else:
            top_chunks.append(str(doc))
            sources.append("Unknown")

    # Create MCP trace object
    mcp_msg = {
        "type": "RETRIEVAL_RESULT",
        "sender": "RetrievalAgent",
        "receiver": "LLMResponseAgent",
        "trace_id": str(uuid4()),
        "payload": {
            "retrieved_context": top_chunks,
            "query": query
        }
    }

    # Get answer from LLM
    answer, _ = llm_agent.run(query, retrieved_docs)

    # Display
    st.markdown("### ✅ Answer")
    st.write(answer)

    st.markdown("📚 **Sources used:**")
    st.code(", ".join(sources))

    st.markdown("---")
    st.markdown("### 🛰️ MCP Trace")
    st.json(mcp_msg)

    # Save to session history
    st.session_state["chat_history"].append({
        "question": query,
        "answer": answer,
        "sources": sources,
        "trace": mcp_msg
    })

# Show chat history
if st.session_state["chat_history"]:
    st.markdown("## 🧾 Conversation History")
    for i, item in enumerate(st.session_state["chat_history"], 1):
        question = item.get("question", "[Missing question]")
        answer = item.get("answer", "[Missing answer]")
        sources = item.get("sources", [])
        trace = item.get("trace", {})

        st.markdown(f"**Q{i}: {question}**")
        st.markdown(f"🟢 *{answer}*")
        st.markdown("📚 **Sources used:**")
        st.code(", ".join(sources))

        with st.expander("🔍 MCP Trace Log"):
            st.json(trace)
        st.markdown("---")
