
import streamlit as st
import tempfile
from src.document_processor import DocumentProcessor
from src.vector_index import VectorIndex
from src.rag_service import RAGService
from src.qa_logger import QALogger

# Streamlit page config
st.set_page_config(page_title="Gemini RAG QA", layout="wide", page_icon="🧠")

# Custom CSS for ChatGPT-like interface
st.markdown("""
<style>
.chat-box {
    background-color: #f5f5f5;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.chat-user {
    font-weight: bold;
    color: #333;
}
.chat-bot {
    background-color: #e6f7ff;
    padding: 10px;
    border-radius: 8px;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

st.title("ResearchBOT: RAG based QA System")
st.markdown("Upload research papers (PDFs) and ask questions. Answers are grounded in your documents!")

# Initialize objects
document_processor = DocumentProcessor()
vector_index = None
rag_service = None
qa_logger = QALogger()

# --- PDF Upload ---
uploaded_files = st.file_uploader(
    "Upload PDF(s)",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:
    all_text = ""
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            pdf_path = tmp_file.name
        text = document_processor.extract_text(pdf_path)
        all_text += text + "\n\n"

    chunks = document_processor.chunk_text(all_text)
    st.success(f"Processed {len(uploaded_files)} PDF(s) → {len(chunks)} text chunks.")

    # Build vector index
    vector_index = VectorIndex()
    vector_index.build_index(chunks)
    retriever = vector_index.get_retriever()
    rag_service = RAGService(retriever)
    st.info("RAG pipeline ready!")

# --- Chat Interface ---
if rag_service:
    question = st.text_input("Ask your question:")
    if st.button("Send") and question:
        with st.spinner("Thinking..."):
            answer = rag_service.ask(question)
            st.markdown(f"""
            <div class='chat-box'>
                <div class='chat-user'>You:</div>
                <div>{question}</div>
                <div class='chat-bot'><b>Gemini RAG:</b> {answer}</div>
            </div>
            """, unsafe_allow_html=True)
            qa_logger.log(question, answer)

# --- Q&A History ---
if st.checkbox("Show Q&A History"):
    history = qa_logger.fetch_all()
    for q, a, t in history:
        st.markdown(f"""
        <div class='chat-box'>
            <div class='chat-user'>Q ({t}):</div>
            <div>{q}</div>
            <div class='chat-bot'>A: {a}</div>
        </div>
        """, unsafe_allow_html=True)
