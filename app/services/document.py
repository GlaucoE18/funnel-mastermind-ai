# Arquivo: app/services/document.py
import os
import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.core.config import settings

class DocumentProcessor:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
    
    def process_pdf(self, file, metadata=None):
        """Processa um arquivo PDF e adiciona ao banco de conhecimento."""
        if metadata is None:
            metadata = {}
        
        # Cria arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name
        
        try:
            # Carrega PDF
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()
            
            # Adiciona metadados
            for doc in documents:
                doc.metadata.update(metadata)
            
            # Divide em chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Adiciona ao vector store
            ids = self.vector_store.add_documents(chunks)
            
            return {
                "success": True,
                "document_count": len(documents),
                "chunk_count": len(chunks),
                "metadata": metadata
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        
        finally:
            # Remove arquivo temporário
            os.unlink(temp_file_path)
