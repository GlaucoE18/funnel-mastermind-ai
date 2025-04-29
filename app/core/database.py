
# Arquivo: app/core/database.py
import os
from supabase import create_client
from langchain.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings

class Database:
    def __init__(self):
        # Inicializa cliente Supabase
        self.supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        
        # Configura embedding model
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Inicializa o vector store
        self.vector_store = SupabaseVectorStore(
            client=self.supabase,
            embedding=self.embeddings,
            table_name=settings.SUPABASE_TABLE,
            query_name="match_documents"
        )
    
    def get_vector_store(self):
        """Retorna a instância do vector store."""
        return self.vector_store