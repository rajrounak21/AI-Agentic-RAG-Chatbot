from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Tuple
from langchain.schema.document import Document

class LLMResponseAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    def run(self, query: str, retrieved_docs: List[Document]) -> Tuple[str, List[str]]:
        """
        Builds a prompt from retrieved docs and invokes the LLM.

        Returns:
        - Answer string
        - List of document sources used
        """
        # Combine context chunks
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        sources = list({doc.metadata.get("source", "Unknown") for doc in retrieved_docs})

        prompt = f"""You are a helpful assistant. Use only the context below to answer the question.

Context:
{context}

Question:
{query}
"""

        response = self.llm.invoke(prompt)
        return response.content.strip(), sources
