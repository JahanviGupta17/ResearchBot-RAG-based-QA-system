# **ResearchBot – AI-Powered Research Assistant**

**Transforming research papers into actionable insights using LLMs and RAG pipelines.**

---

## **Problem Statement**

Researchers and students often struggle with extracting relevant insights from large volumes of research papers. Manual reading and summarization are:

- Time-consuming  
- Error-prone  
- Inefficient for comparing multiple documents  

**ResearchBot** addresses this by enabling fast, context-aware retrieval and answer generation from PDF documents.

---

## **Solution**

ResearchBot leverages **Large Language Models (LLMs)** and **Retrieval-Augmented Generation (RAG)** pipelines to:

- Extract and preprocess text from uploaded PDFs  
- Chunk documents for semantic understanding  
- Index content using **FAISS** vector database  
- Provide precise, grounded answers to user queries  
- Offer a simple, interactive **Streamlit** interface  

---

## **Pipeline Overview**
     +-----------------+
     | Upload PDFs     |
     +--------+--------+
              |
              v
     +-----------------+
     | Text Extraction |
     | & Chunking      |
     +--------+--------+
              |
              v
     +-----------------+
     | Embeddings      |
     | (Gemini API)    |
     +--------+--------+
              |
              v
     +-----------------+
     | FAISS Vector DB |
     +--------+--------+
              |
              v
     +-----------------+
     | RAG Pipeline    |
     | (LLM Querying)  |
     +--------+--------+
              |
              v
     +-----------------+
     | Answers to User |
     +-----------------+

## **Key Functionalities**

### 1. PDF Upload & Processing
- Multiple PDFs supported  
- Text extraction and chunking for efficient semantic search  

### 2. Vector Database Indexing
- Uses **FAISS** for storing embeddings  
- Enables semantic retrieval of most relevant document sections  

### 3. RAG Pipeline for Question Answering
- Combines retrieved document content with LLM reasoning  
- Produces contextually accurate, reference-based answers  

### 4. Interactive Streamlit Interface
- Upload PDFs and ask questions in real-time  
- View processed chunks and retrieved references  

### 5. Embeddings & LLM Integration
- Uses **Google Gemini embeddings** for semantic understanding  
- Integrates LLM for generating natural, human-like responses  
- Modular design allows switching LLMs or embeddings easily  

### 6. Modular & Production-Ready Architecture
- Separate modules for **vector indexing**, **RAG service**, and **UI**  
- Clean Python codebase for maintainability and deployment  

---

## **Tech Stack**

- **Programming Language:** Python  
- **Libraries & Frameworks:** LangChain, langchain-community, FAISS, Streamlit, PyPDF2, Pandas, Numpy  
- **Deployment Ready:** Supports local and cloud-based execution  


