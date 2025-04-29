# Arquivo: app/api/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.core.database import Database
from app.services.document import DocumentProcessor
from app.services.query import QueryService

# Inicializa o banco de dados
db = Database()
vector_store = db.get_vector_store()

# Inicializa serviços
document_processor = DocumentProcessor(vector_store)
query_service = QueryService(vector_store)

# Cria app FastAPI
app = FastAPI(
    title="Funnel Mastermind AI API",
    description="API para o assistente de funis de vendas e marketing digital",
    version="2.0.0"
)

# Modelos de dados
class Question(BaseModel):
    text: str

class FunnelAnalysis(BaseModel):
    description: str

class EmailRequest(BaseModel):
    offer: str
    audience: str
    objective: str

# Rotas da API
@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: Optional[str] = Form(None),
    category: Optional[str] = Form(None)
):
    """Endpoint para upload de documentos."""
    # Valida formato do arquivo
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")
    
    # Prepara metadados
    metadata = {
        "title": title,
        "filename": file.filename
    }
    
    if author:
        metadata["author"] = author
    
    if category:
        metadata["category"] = category
    
    # Processa o documento
    result = document_processor.process_pdf(file, metadata)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.post("/query")
async def query(question: Question):
    """Endpoint para consultas ao assistente."""
    result = query_service.ask(question.text)
    return result

@app.post("/analyze-funnel")
async def analyze_funnel(request: FunnelAnalysis):
    """Endpoint para análise de funis."""
    result = query_service.analyze_funnel(request.description)
    return result

@app.post("/create-email")
async def create_email(request: EmailRequest):
    """Endpoint para criação de e-mails."""
    result = query_service.create_email(
        request.offer,
        request.audience,
        request.objective
    )
    return result
