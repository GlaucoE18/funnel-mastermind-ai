# Arquivo: app/services/query.py
from app.core.llm import LLM

class QueryService:
    def __init__(self, vector_store):
        self.llm = LLM(vector_store)
    
    def ask(self, question):
        """Processa uma pergunta e retorna a resposta."""
        return self.llm.query(question)
    
    def analyze_funnel(self, funnel_description):
        """Analisa um funil de vendas."""
        from app.core.prompts import FUNNEL_ANALYSIS_PROMPT
        
        prompt = FUNNEL_ANALYSIS_PROMPT.format(funnel_description=funnel_description)
        return self.ask(prompt)
    
    def create_email(self, offer, audience, objective):
        """Cria um e-mail F4."""
        from app.core.prompts import EMAIL_F4_PROMPT
        
        prompt = EMAIL_F4_PROMPT.format(
            offer=offer,
            audience=audience,
            objective=objective
        )
        return self.ask(prompt)
