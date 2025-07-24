# 📘 AI Agentic RAG Chatbot with MCP Tracing

A multi-agent RAG (Retrieval-Augmented Generation) system that allows users to upload documents (PDF, DOCX, PPTX, CSV, etc.) and ask multi-turn questions. It uses LangChain agents, Google Generative AI, and ChromaDB for contextual Q\&A with traceable message passing.

---

## 🔧 Features

* 📂 Upload multiple document types (PDF, DOCX, PPTX, TXT, CSV, MD)
* 💬 Ask questions based on document content
* 🛰️ MCP-style tracing between agents (LLM, Retrieval, Ingestion)
* 🧠 LLM response using Gemini 2.0 Flash (via LangChain)
* 🗂️ Chroma vector DB for persistent retrieval
* 🧭 Streamlit UI with multi-turn chat history and source trace
* ✅ Works with Google Generative AI via API Key

---

### 🏗️ Project Structure

```
AI-Agentic-RAG-Chatbot/
├── .env                   # Your Google API key (DO NOT upload to GitHub)
├── requirements.txt       # All Python dependencies
├── README.md              # Project overview, setup, and usage
├── web_app.py             # Main Streamlit application

├── agents/                # Modular agent definitions
│   ├── ingestionAgent.py      # Handles file parsing and chunking
│   ├── retrievalAgent.py      # Vector store operations (Chroma)
│   └── LLMResponseAgent.py    # Uses Gemini/GPT for answer generation

├── mcp.py                 # Helper for generating MCP trace messages
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/rajrounak21/AI-Agentic-RAG-Chatbot.git
cd AI-Agentic-RAG-Chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and add your Google GenAI API key:

```env
GOOGLE_API_KEY=your_google_genai_key
```

### 4. Run the App Locally

```bash
streamlit run web_app.py
```

---

## 📬 Contact

Made with 💙 by **Rounak Raj**

* GitHub: [@rajrounak21](https://github.com/rajrounak21)
* Email: [rajrounak366@gmail.com](mailto:rajrounak366@gmail.com)
