# 🧠 RAG System Technical Challenge

A production-grade Retrieval Augmented Generation (RAG) system capable of answering questions based on the TriviaQA dataset. This project uses **FastAPI** for serving, **ChromaDB** for vector storage, and **LangChain** for orchestration.

## 🚀 Features

- **Data Ingestion:** Streams and processes the TriviaQA dataset (subset) without massive disk usage.
- **Vector Search:** Uses `sentence-transformers` (all-MiniLM-L6-v2) and ChromaDB for semantic search.
- **RAG Pipeline:** Retrieves relevant context and generates accurate answers.
- **Hybrid Support:** configured to run with **Ollama (Llama 3)** locally or **OpenAI** (configurable).
- **API:** Fast and async API endpoints built with FastAPI.
- **Dockerized:** Ready for container deployment.

## 🛠️ Tech Stack

- **Language:** Python 3.10
- **Framework:** FastAPI
- **LLM Orchestration:** LangChain
- **Vector Database:** ChromaDB
- **Embeddings:** HuggingFace (SentenceTransformers)
- **Containerization:** Docker

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Kem0z/rag-challenge.git
cd rag-challenge