import os
import time
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class RAGEngine:
    def __init__(self):
        self.db_path = "./chroma_db"
        self.embedding_model = "all-MiniLM-L6-v2"
        
        # Initialize Vector Store
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        self.vector_store = Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        # Initialize LLM (llama)
        self.llm = ChatOllama(model="llama3", temperature=0)

        # Define Prompt
        self.template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        self.prompt = ChatPromptTemplate.from_template(self.template)

    def process_query(self, question: str):
        start_time = time.time()
        
        # 1. Retrieve Context
        # We do this manually to capture the context for the API response
        retrieved_docs = self.retriever.invoke(question)
        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # 2. Generate Answer
        chain = (
            self.prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        try:
            answer = chain.invoke({"context": context_text, "question": question})
        except Exception as e:
            return {
                "error": str(e),
                "latency_ms": 0
            }

        end_time = time.time()
        latency = round((end_time - start_time) * 1000) # ms

        return {
            "question": question,
            "answer": answer,
            "retrieved_context": [doc.page_content for doc in retrieved_docs],
            "latency_ms": latency
        }