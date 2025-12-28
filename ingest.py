import os

# Ensure this path is set for D drive usage
os.environ['HF_HOME'] = "D:/rag_Task/hf_cache"

from datasets import load_dataset
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Configuration
DB_PATH = "D:/rag_Task/chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def ingest_data():
    print("--- 1. Loading TriviaQA (Streaming Mode) ---")
    # streaming=True means we don't download the huge file. We just stream data over the network.
    dataset_stream = load_dataset("trivia_qa", "rc", split="validation", streaming=True)
    
    # We take only the first 600 documents. 
    # This satisfies the "500-2000" requirement without killing disk space.
    dataset = dataset_stream.take(600)

    print("--- 2. Preprocessing & Chunking ---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )

    docs = []
    # We must iterate differently because it is a stream, not a list
    for entry in dataset:
        # TriviaQA structure: 'search_results' -> 'search_context'
        context_list = entry.get("search_results", {}).get("search_context", [])
        question_id = entry.get("question_id", "unknown")
        
        for idx, text in enumerate(context_list):
            if len(text) < 50:  # Skip garbage/empty text
                continue
                
            chunks = text_splitter.split_text(text)
            for chunk in chunks:
                docs.append(Document(
                    page_content=chunk,
                    metadata={"source_id": question_id, "chunk_index": idx}
                ))

    print(f"Generated {len(docs)} chunks from the subset.")
    print("--- 3. Generating Embeddings & Saving to Vector DB ---")

    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Create/Overwrite the Vector Store
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding_function,
        persist_directory=DB_PATH
    )
    
    print(f"SUCCESS: Vector DB saved to {DB_PATH}")

if __name__ == "__main__":
    ingest_data()
