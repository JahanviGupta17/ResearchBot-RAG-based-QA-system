# src/rag_service.py
from langchain_community.chat_models import ChatGooglePalm
from langchain.chains import RetrievalQA

class RAGService:
    def __init__(self, vector_index, model_name="gemini-1", temperature=0):
        from config import GEMINI_API_KEY

        # Initialize Gemini LLM
        self.llm = ChatGooglePaLM(
            model=model_name,
            api_key=GEMINI_API_KEY,
            temperature=temperature
        )

        self.vector_index = vector_index
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_index.index.as_retriever(),
            return_source_documents=True
        )

    def answer_query(self, query):
        """
        Ask a question and get answer with sources
        """
        if self.vector_index.index is None:
            raise ValueError("Vector index not built. Cannot answer queries.")
        
        result = self.qa_chain.run(query)
        return result
