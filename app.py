import streamlit as st
import os
from typing import Dict
from dotenv import load_dotenv
import json

# Carrega as variáveis de ambiente do arquivo .env ANTES de importar o assistente
load_dotenv()

# Agora importa o assistente após carregar as variáveis de ambiente
from src.assistant import AssistenteSebrae

# Define o diretório de documentos globalmente
DIRETORIO_DOCS = "./dados/documentos"

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Consultor Sebrae IA",
    page_icon=":robot_face:",
    layout="wide"
)

# --- CORES E ESTILOS ---
SEBRAE_AZUL = "#006EC7"
SEBRAE_CINZA_CLARO = "#F5F5F5"
SEBRAE_CINZA_ESCURO = "#E0E0E0"
TEXTO_COR = "#333333"

st.markdown(f"""
<style>
    /* Reset e Cores Base */
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background-color: {SEBRAE_CINZA_CLARO};
    }}

    /* --- BARRA LATERAL --- */
    .css-1d391kg {{
        background-color: #FFFFFF !important;
        border-right: 1px solid {SEBRAE_CINZA_ESCURO};
    }}

    .sidebar-content h2 {{
        color: {SEBRAE_AZUL};
        font-size: 1.8rem;
        font-weight: 700;
        padding: 1rem 0;
        border-bottom: 2px solid {SEBRAE_AZUL};
    }}

    .stButton button {{
        background-color: {SEBRAE_AZUL};
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s ease;
    }}

    .stButton button:hover {{
        background-color: #0056a0; /* Azul um pouco mais escuro */
        transform: translateY(-2px);
    }}

    /* --- ÁREA DE CHAT --- */
    .chat-container {{
        padding: 1rem;
    }}

    .user-message {{
        background-color: {SEBRAE_AZUL};
        color: white;
        border-radius: 12px 12px 0 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        max-width: 70%;
        margin-left: auto;
    }}

    .assistant-message {{
        background-color: #FFFFFF;
        color: {TEXTO_COR};
        border-radius: 12px 12px 12px 0;
        padding: 1rem;
        margin-bottom: 1rem;
        max-width: 70%;
        margin-right: auto;
        border: 1px solid {SEBRAE_CINZA_ESCURO};
    }}
    
    .stTextInput > div > div > input {{
        background-color: #FFFFFF;
        color: {TEXTO_COR};
        border: 1px solid {SEBRAE_CINZA_ESCURO};
        border-radius: 8px;
    }}

</style>
""", unsafe_allow_html=True)


# --- FUNÇÕES DO ASSISTENTE E DOCUMENTOS ---

def inicializar_assistente():
    """Inicializa o assistente e o armazena no estado da sessão."""
    if 'assistente_sebrae' not in st.session_state:
        with st.spinner("Carregando o assistente..."):
            st.session_state.assistente_sebrae = AssistenteSebrae()

def nova_conversa():
    """Limpa o histórico de conversas para iniciar uma nova."""
    st.session_state.historico = []

def atualizar_base_conhecimento(assistente: AssistenteSebrae):
    """Verifica novos documentos e atualiza a base de conhecimento."""
    if not os.path.exists(DIRETORIO_DOCS):
        os.makedirs(DIRETORIO_DOCS)
        st.info("Diretório 'dados/documentos' criado. Adicione seus arquivos lá.")
        return

    documentos_no_diretorio = {os.path.join(root, f) 
                               for root, _, files in os.walk(DIRETORIO_DOCS) 
                               for f in files 
                               if f.lower().endswith(('.pdf', '.docx', '.xlsx'))}
    
    try:
        with open("documentos_processados.json", "r") as f:
            processados = set(json.load(f))
    except FileNotFoundError:
        processados = set()

    novos_documentos = documentos_no_diretorio - processados
    
    if not novos_documentos:
        st.success("A base de conhecimento já está atualizada.")
        return

    with st.spinner(f"Processando {len(novos_documentos)} novo(s) documento(s)..."):
        assistente.carregar_documentos(DIRETORIO_DOCS)
    
    processados.update(novos_documentos)
    with open("documentos_processados.json", "w") as f:
        json.dump(list(processados), f)
    
    st.success(f"{len(novos_documentos)} novo(s) documento(s) processado(s) com sucesso!")

def listar_documentos_carregados():
    """Lista todos os documentos carregados na base de conhecimento."""
    try:
        with open("documentos_processados.json", "r") as f:
            documentos = json.load(f)
            return [os.path.basename(doc) for doc in documentos]
    except FileNotFoundError:
        return []


# --- INTERFACE PRINCIPAL ---

def main():
    """Função principal que renderiza a interface do Streamlit."""
    
    inicializar_assistente()

    if 'historico' not in st.session_state:
        st.session_state.historico = []

    # --- BARRA LATERAL ---
    with st.sidebar:
        st.title("Consultor Sebrae IA")
        
        if st.button("Nova Conversa"):
            nova_conversa()
            st.rerun()

        if st.button("Atualizar Base de Conhecimento"):
            atualizar_base_conhecimento(st.session_state.assistente_sebrae)

        st.markdown("---")
        st.markdown("### Documentos Carregados")
        
        documentos = listar_documentos_carregados()
        if documentos:
            for doc in documentos:
                st.text(f"• {doc}")
        else:
            st.info("Nenhum documento carregado")

        st.markdown("---")
        st.markdown("### Sobre")
        st.info(
            "Este é um assistente de IA treinado para responder perguntas sobre os "
            "documentos do Sebrae. Ele utiliza uma base de conhecimento para "
            "fornecer respostas precisas e contextuais."
        )

    # --- TELA PRINCIPAL ---
    st.markdown(f"<h1 style='color: {SEBRAE_AZUL};'>Consultor Sebrae IA</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # --- HISTÓRICO DA CONVERSA ---
    chat_container = st.container()
    with chat_container:
        for item in st.session_state.historico:
            if item["role"] == "user":
                st.markdown(f"<div class='user-message'>**Você:** {item['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='assistant-message'>**Assistente:** {item['content']}</div>", unsafe_allow_html=True)

    # --- CAMPO DE ENTRADA ---
    prompt = st.chat_input("Digite sua pergunta...")

    if prompt:
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.historico.append({"role": "user", "content": prompt})
        
        # Processa a pergunta e obtém a resposta do assistente
        with st.spinner("Pensando..."):
            resposta_dados = st.session_state.assistente_sebrae.processar_consulta(prompt)
            resposta_formatada = st.session_state.assistente_sebrae.formatar_resposta(resposta_dados)

        # Adiciona a resposta do assistente ao histórico
        st.session_state.historico.append({"role": "assistant", "content": resposta_formatada})
        
        # Força o rerender para exibir a nova conversa
        st.rerun()


if __name__ == "__main__":
    main()