import os
from uuid import uuid4
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema.document import Document  # for type clarity

class RetrievalAgent:
    def __init__(self, persist_dir="vector_store", k=5):
        self.persist_dir = persist_dir
        self.k = k
        self.vectordb = None
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def store_documents(self, documents: list[Document]):
        print("[RetrievalAgent] Storing documents in Chroma vector DB...")
        self.vectordb = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

    def load_vectorstore(self):
        if self.vectordb is None:
            print("[RetrievalAgent] Loading Chroma vector DB from disk...")
            self.vectordb = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )

    def retrieve(self, query: str) -> list[Document]:
        self.load_vectorstore()
        retriever = self.vectordb.as_retriever(search_kwargs={"k": self.k})
        documents = retriever.get_relevant_documents(query)
        return documents  # returns LangChain Document objects
