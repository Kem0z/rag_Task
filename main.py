from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_engine import RAGEngine
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Challenge API")

# Initialize RAG Engine on startup
rag_engine = RAGEngine()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved_context: list[str]
    latency_ms: int

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    logger.info(f"Received question: {request.question}")
    
    result = rag_engine.process_query(request.question)
    
    if "error" in result:
        logger.error(f"Generation failed: {result['error']}")
        raise HTTPException(status_code=500, detail=result['error'])
        
    return result

@app.get("/")
def health_check():
    return {"status": "active", "service": "RAG API"}