import os
import streamlit as st
import pdfplumber
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from huggingface_hub import InferenceClient

# Environment
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN not found. Set it in .env file")


# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# LLM Client (Chat-based)

llm = InferenceClient(token=HF_TOKEN)

# PDF Extraction

def extract_pdf_text(pdf_files):
    text = ""
    for pdf in pdf_files:
        with pdfplumber.open(pdf) as pdf_doc:
            for page in pdf_doc.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    return text


# Text Chunking

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_text(text)

# FAISS Index
def create_faiss_index(chunks):
    db = FAISS.from_texts(chunks, embeddings)
    db.save_local("faiss_index")

def load_faiss_index():
    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

# Chunk Summarization (Chat API)

def summarize_chunk(text, source_id):
    response = llm.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {
                "role": "user",
                "content": f"""
Summarize the following content in 1–2 clear sentences.
Keep only important facts.
Cite as [Source {source_id}].

Text:
{text}
"""
            }
        ],
        max_tokens=120,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

def build_context(docs):
    context = ""
    for i, doc in enumerate(docs):
        context += summarize_chunk(doc.page_content, i + 1) + " "
    return context

# Final Answer Generation
def answer_question(question):
    db = load_faiss_index()
    docs = db.similarity_search(question, k=3)

    if not docs:
        return "Not enough information found."

    context = build_context(docs)

    prompt = f"""
Use ONLY the context below to answer the question.
Cite sources like [Source X].
If the answer is not present, say so.

Context:
{context}

Question:
{question}
"""

    response = llm.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": "You are a research assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

# Streamlit UI
st.set_page_config(
    page_title="ResearchBot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 ResearchBot – Multi-PDF Research Assistant")

with st.sidebar:
    st.header("📁 Document Ingestion")
    pdfs = st.file_uploader(
        "Upload PDF documents",
        type="pdf",
        accept_multiple_files=True
    )

    if st.button("Index Documents"):
        if not pdfs:
            st.warning("Upload at least one PDF")
        else:
            with st.spinner("Indexing PDFs..."):
                text = extract_pdf_text(pdfs)
                chunks = split_text(text)
                create_faiss_index(chunks)
                st.success("PDFs indexed successfully")

question = st.text_input("❓ Enter your question")

if question:
    with st.spinner("Generating answer..."):
        answer = answer_question(question)
    st.subheader("🤖 Answer")
    st.write(answer)
