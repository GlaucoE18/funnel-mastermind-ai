
# Arquivo: app/ui/app.py
import streamlit as st
import requests
import json
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Funnel Mastermind AI",
    page_icon="🧠",
    layout="wide"
)

# URL da API
API_URL = "http://localhost:8000"  # Altere para URL de produção quando publicar

# Função para fazer upload de documento
def upload_document(file, title, author, category):
    files = {"file": (file.name, file, "application/pdf")}
    data = {
        "title": title,
        "author": author or "",
        "category": category or ""
    }
    
    response = requests.post(
        f"{API_URL}/documents/upload",
        files=files,
        data=data
    )
    
    return response.json()

# Função para fazer uma pergunta
def ask_question(question):
    response = requests.post(
        f"{API_URL}/query",
        json={"text": question}
    )
    
    return response.json()

# Função para analisar um funil
def analyze_funnel(description):
    response = requests.post(
        f"{API_URL}/analyze-funnel",
        json={"description": description}
    )
    
    return response.json()

# Função para criar um e-mail
def create_email(offer, audience, objective):
    response = requests.post(
        f"{API_URL}/create-email",
        json={
            "offer": offer,
            "audience": audience,
            "objective": objective
        }
    )
    
    return response.json()

# Cabeçalho
st.title("🧠 Funnel Mastermind AI")
st.subheader("Seu assistente pessoal para funis de vendas, copywriting e marketing digital")

# Criação das abas
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chat com o Assistente", 
    "📂 Upload de Documentos", 
    "🔍 Analise de Funis",
    "✉️ Criação de E-mails"
])

# Tab 1: Chat com o Assistente
with tab1:
    st.header("Converse com seu assistente especializado")
    
    # Inicializa histórico de chat se não existir
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Exibe histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Campo para nova mensagem
    if prompt := st.chat_input("Digite sua pergunta sobre funis, marketing, copywriting..."):
        # Adiciona mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Exibe mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Exibe indicador de "pensando"
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Pensando...")
            
            # Obtém resposta da API
            try:
                response = ask_question(prompt)
                answer = response["answer"]
                
                # Exibe fontes se existirem
                if "sources" in response and response["sources"]:
                    answer += "\n\n**Fontes:**\n"
                    for source in response["sources"]:
                        if "title" in source:
                            answer += f"- {source['title']}\n"
                
                # Atualiza placeholder com resposta
                message_placeholder.markdown(answer)
                
                # Adiciona resposta ao histórico
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                message_placeholder.markdown(f"Erro ao processar sua pergunta. Por favor, tente novamente. Detalhes: {str(e)}")

# Tab 2: Upload de Documentos
with tab2:
    st.header("Adicione documentos à base de conhecimento")
    
    with st.form("upload_form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Selecione um arquivo PDF", type=["pdf"])
        title = st.text_input("Título do documento", placeholder="Ex: Expert Secrets - Russell Brunson")
        author = st.text_input("Autor (opcional)", placeholder="Ex: Russell Brunson")
        category = st.text_input("Categoria (opcional)", placeholder="Ex: Copywriting, Funis, Email Marketing")
        
        submit_button = st.form_submit_button("Fazer Upload")
        
        if submit_button and uploaded_file is not None:
            with st.spinner("Processando documento..."):
                try:
                    result = upload_document(uploaded_file, title, author, category)
                    
                    if result.get("success", False):
                        st.success(f"Documento '{title}' processado com sucesso! Foram criados {result['chunk_count']} fragmentos de conhecimento.")
                    else:
                        st.error(f"Erro ao processar documento: {result.get('error', 'Erro desconhecido')}")
                
                except Exception as e:
                    st.error(f"Erro ao fazer upload: {str(e)}")

# Tab 3: Análise de Funis
with tab3:
    st.header("Analise um funil de vendas")
    
    description = st.text_area(
        "Descreva seu funil de vendas em detalhes",
        height=200,
        placeholder="Descreva seu funil de vendas em detalhes. Inclua etapas, produtos, pontos de conversão, e-mails, páginas, etc."
    )
    
    if st.button("Analisar Funil"):
        if description:
            with st.spinner("Analisando seu funil..."):
                try:
                    result = analyze_funnel(description)
                    st.markdown(result["answer"])
                    
                    # Exibe fontes se existirem
                    if "sources" in result and result["sources"]:
                        st.subheader("Fontes de conhecimento utilizadas:")
                        for source in result["sources"]:
                            if "title" in source:
                                st.write(f"- {source['title']}")
                
                except Exception as e:
                    st.error(f"Erro ao analisar funil: {str(e)}")
        else:
            st.warning("Por favor, forneça uma descrição do funil para análise.")

# Tab 4: Criação de E-mails
with tab4:
    st.header("Crie e-mails com o framework F4")
    
    with st.form("email_form"):
        offer = st.text_input("Produto ou Oferta", placeholder="Ex: Curso de Funis Perpétuos")
        audience = st.text_input("Público-alvo", placeholder="Ex: Designers que querem se tornar Funnel Builders")
        objective = st.text_input("Objetivo do e-mail", placeholder="Ex: Convidar para um webinar gratuito")
        
        submit_email = st.form_submit_button("Criar E-mail")
        
        if submit_email:
            if offer and audience and objective:
                with st.spinner("Criando seu e-mail..."):
                    try:
                        result = create_email(offer, audience, objective)
                        st.markdown(result["answer"])
                        
                        # Adiciona botão para copiar
                        st.download_button(
                            label="Baixar E-mail",
                            data=result["answer"],
                            file_name="email_f4.txt",
                            mime="text/plain"
                        )
                    
                    except Exception as e:
                        st.error(f"Erro ao criar e-mail: {str(e)}")
            else:
                st.warning("Por favor, preencha todos os campos.")

# Rodapé
st.markdown("---")
st.markdown("**Funnel Mastermind AI** | Desenvolvido por Glauco | v2.0.0")