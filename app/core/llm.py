


# Arquivo: app/core/llm.py
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from app.core.config import settings
from app.core.prompts import QA_PROMPT

class LLM:
    def __init__(self, vector_store):
        # Inicializa modelo LLM
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=0.1,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Configuração do sistema de QA
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(
                search_kwargs={"k": settings.SIMILARITY_TOP_K}
            ),
            chain_type_kwargs={
                "prompt": PromptTemplate.from_template(QA_PROMPT)
            },
            return_source_documents=True
        )
    
    def query(self, question):
        """Realiza uma consulta ao LLM com base nos documentos recuperados."""
        response = self.qa_chain({"query": question})
        return {
            "answer": response["result"],
            "sources": [doc.metadata for doc in response["source_documents"]]
        }