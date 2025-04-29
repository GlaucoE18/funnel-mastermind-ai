# Arquivo: app/core/config.py
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações da aplicação
class Settings:
    # Informações da aplicação
    APP_NAME = "Funnel Mastermind AI"
    APP_VERSION = "2.0.0"
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4o"
    
    # Supabase (banco vetorial)
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_TABLE = "funnel_documents"
    
    # Configurações de processamento de documentos
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Configurações do sistema de recuperação
    SIMILARITY_TOP_K = 5

# Instância global das configurações
settings = Settings()

