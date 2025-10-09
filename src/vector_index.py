# src/vector_index.py

from langchain_community.embeddings import GooglePalmEmbeddings
from langchain_community.vectorstores import FAISS

class VectorIndex:
    def __init__(self, model_name="gemini-1"):
        from config import GEMINI_API_KEY

        # Initialize embeddings
        self.embeddings = GooglePalmEmbeddings(
            model=model_name,
            api_key=GEMINI_API_KEY
        )
        self.index = None

    def build_index(self, texts):
        """
        Build FAISS vector index from list of text chunks
        """
        if not texts:
            raise ValueError("Text chunks list is empty")
        
        self.index = FAISS.from_texts(texts, self.embeddings)

    def query_index(self, query, top_k=5):
        """
        Query the FAISS index for similar documents
        """
        if self.index is None:
            raise ValueError("Index not built yet. Call build_index() first.")
        
        results = self.index.similarity_search(query, k=top_k)
        return results
