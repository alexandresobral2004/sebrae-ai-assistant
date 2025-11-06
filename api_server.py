"""
API Backend para o Assistente IA Sebrae
FastAPI server que expõe endpoints para o frontend HTML/CSS/JS
Com sistema de autenticação Google OAuth2 + Login tradicional
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import secrets

# Carrega variáveis de ambiente
load_dotenv()

# Importa o assistente existente
from src.assistant import AssistenteSebrae

# Importa autenticação
from src.auth import get_current_user, get_current_active_user
from src.auth_routes import router as auth_router
from src.models import User
from src.database import engine, Base

# Inicializa FastAPI
app = FastAPI(
    title="Sebrae AI Assistant API",
    description="API para o Assistente de Consultoria IA do Sebrae com Autenticação",
    version="3.0.0"
)

# Cria tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Inclui rotas de autenticação
app.include_router(auth_router)

# IMPORTANTE: SessionMiddleware é necessário para OAuth
# Gera uma chave secreta para sessões (em produção, usar variável de ambiente)
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", secrets.token_urlsafe(32))
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# Configuração CORS para permitir frontend acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretório de documentos
DIRETORIO_DOCS = "./dados/documentos"

# Inicializa o assistente globalmente
assistente = None

# Flag para controlar se documentos foram carregados
documentos_carregados = False

# Armazena histórico de conversas (em produção, usar banco de dados)
conversas = {}

# Armazena timestamps da última atividade de cada sessão
ultima_atividade = {}

# Configurações de sessão
TIMEOUT_SESSAO_MINUTOS = 5  # Tempo de inatividade para limpar sessão
MAX_MENSAGENS_CONTEXTO = 10  # Máximo de mensagens no contexto (evita estouro de tokens)

# Models Pydantic para validação
class ChatMessage(BaseModel):
    mensagem: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    resposta: str
    consultores: Optional[List[Dict]] = []
    documentos: Optional[List[str]] = []
    confianca: Optional[float] = 0.0
    fonte: str
    usado_internet: bool = False

class StatusResponse(BaseModel):
    status: str
    documentos_carregados: int
    documentos_em_memoria: bool  # Indica se documentos já foram carregados na memória
    consultores_disponiveis: int
    modelo: str

class DocumentoInfo(BaseModel):
    nome: str
    tipo: str
    tamanho: int

# --- ENDPOINTS ---

@app.on_event("startup")
async def startup_event():
    """Inicializa o assistente e carrega documentos em background."""
    global assistente, documentos_carregados
    print("🚀 Inicializando Assistente IA Sebrae...")
    assistente = AssistenteSebrae()
    print("✅ Assistente IA Sebrae pronto!")
    
    # Carrega documentos em background thread para não bloquear startup
    import threading
    def carregar_docs_background():
        global documentos_carregados
        if os.path.exists(DIRETORIO_DOCS):
            print("� Carregando documentos em background...")
            try:
                assistente.carregar_documentos(DIRETORIO_DOCS)
                documentos_carregados = True
                print("✅ Documentos carregados com sucesso!")
            except Exception as e:
                print(f"⚠️ Erro ao carregar documentos: {e}")
    
    threading.Thread(target=carregar_docs_background, daemon=True).start()
    print("💡 Carregamento de documentos iniciado em background...")

@app.get("/")
async def root():
    """Serve a página de login."""
    return FileResponse("frontend/login.html")

@app.get("/login.html")
async def login_page():
    """Serve a página de login."""
    return FileResponse("frontend/login.html")

@app.get("/register.html")
async def register_page():
    """Serve a página de registro."""
    return FileResponse("frontend/register.html")

@app.get("/chat.html")
async def chat_page():
    """Serve a página do chat (requer autenticação no frontend)."""
    return FileResponse("frontend/chat.html")

@app.get("/app.js")
async def app_js():
    """Serve o arquivo JavaScript do frontend."""
    return FileResponse("frontend/app.js", media_type="application/javascript")

@app.get("/styles.css")
async def styles_css():
    """Serve o arquivo CSS do frontend."""
    return FileResponse("frontend/styles.css", media_type="text/css")

@app.get("/static/design-tokens.css")
async def design_tokens_css():
    """Serve o arquivo CSS de design tokens."""
    return FileResponse("frontend/design-tokens.css", media_type="text/css")

@app.get("/static/copilot-style.css")
async def copilot_style_css():
    """Serve o arquivo CSS do estilo Copilot."""
    return FileResponse("frontend/copilot-style.css", media_type="text/css")

@app.get("/static/styles.css")
async def static_styles_css():
    """Serve o arquivo CSS principal via /static/."""
    return FileResponse("frontend/styles.css", media_type="text/css")

@app.get("/static/app.js")
async def static_app_js():
    """Serve o arquivo JavaScript via /static/."""
    return FileResponse("frontend/app.js", media_type="application/javascript")

def limpar_sessoes_inativas():
    """
    Limpa sessões que estão inativas há mais de TIMEOUT_SESSAO_MINUTOS.
    """
    global conversas, ultima_atividade
    agora = datetime.now()
    timeout = timedelta(minutes=TIMEOUT_SESSAO_MINUTOS)
    
    sessoes_para_remover = []
    
    for session_id, ultimo_acesso in list(ultima_atividade.items()):
        if agora - ultimo_acesso > timeout:
            sessoes_para_remover.append(session_id)
    
    for session_id in sessoes_para_remover:
        if session_id in conversas:
            print(f"🧹 Limpando sessão inativa: {session_id}")
            del conversas[session_id]
        if session_id in ultima_atividade:
            del ultima_atividade[session_id]
    
    return len(sessoes_para_remover)

def atualizar_atividade_sessao(session_id: str):
    """
    Atualiza o timestamp de última atividade da sessão.
    """
    global ultima_atividade
    ultima_atividade[session_id] = datetime.now()

def limitar_contexto_sessao(session_id: str):
    """
    Limita o número de mensagens no contexto para evitar estouro de tokens.
    Mantém apenas as MAX_MENSAGENS_CONTEXTO mais recentes.
    """
    global conversas
    
    if session_id in conversas and len(conversas[session_id]) > MAX_MENSAGENS_CONTEXTO:
        # Mantém apenas as mensagens mais recentes
        conversas[session_id] = conversas[session_id][-MAX_MENSAGENS_CONTEXTO:]
        print(f"⚠️ Contexto da sessão {session_id} limitado a {MAX_MENSAGENS_CONTEXTO} mensagens")
        return True
    return False

def obter_historico_formatado(session_id: str, limite: int = 5) -> str:
    """
    Retorna o histórico de conversas formatado para incluir no contexto do LLM.
    
    Args:
        session_id: ID da sessão
        limite: Número de mensagens recentes a incluir (padrão: 5)
        
    Returns:
        String formatada com o histórico
    """
    global conversas
    
    if session_id not in conversas or not conversas[session_id]:
        return ""
    
    # Pega as últimas N mensagens
    mensagens_recentes = conversas[session_id][-limite:]
    
    historico_formatado = "### HISTÓRICO DA CONVERSA (Mensagens anteriores):\n\n"
    
    for i, msg in enumerate(mensagens_recentes, 1):
        historico_formatado += f"**Mensagem {i}:**\n"
        historico_formatado += f"👤 Usuário: {msg['usuario']}\n"
        historico_formatado += f"🤖 Assistente: {msg['assistente'][:200]}...\n\n"  # Resumo
    
    historico_formatado += "### FIM DO HISTÓRICO\n\n"
    
    return historico_formatado

def carregar_documentos_se_necessario():
    """Carrega documentos sob demanda (lazy loading) apenas na primeira vez."""
    global documentos_carregados
    
    if not documentos_carregados and os.path.exists(DIRETORIO_DOCS):
        print("📚 Carregando documentos pela primeira vez...")
        try:
            assistente.carregar_documentos(DIRETORIO_DOCS)
            documentos_carregados = True
            print("✅ Documentos carregados com sucesso!")
        except Exception as e:
            print(f"⚠️ Erro ao carregar documentos: {e}")
            # Continua mesmo com erro - assistente pode responder sem documentos

@app.post("/api/carregar-documentos")
async def carregar_documentos_manual():
    """Endpoint para carregar/recarregar documentos manualmente."""
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    global documentos_carregados
    
    if not os.path.exists(DIRETORIO_DOCS):
        raise HTTPException(status_code=404, detail="Diretório de documentos não encontrado")
    
    try:
        print("📚 Carregando/recarregando documentos...")
        assistente.carregar_documentos(DIRETORIO_DOCS)
        documentos_carregados = True
        
        # Conta documentos carregados
        num_docs = 0
        for root, dirs, files in os.walk(DIRETORIO_DOCS):
            num_docs += len([f for f in files if f.endswith(('.pdf', '.docx', '.xlsx'))])
        
        return {
            "mensagem": "Documentos carregados com sucesso",
            "total_documentos": num_docs,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar documentos: {str(e)}")

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Retorna o status do sistema."""
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    # Conta documentos no diretório
    num_docs = 0
    if os.path.exists(DIRETORIO_DOCS):
        for root, dirs, files in os.walk(DIRETORIO_DOCS):
            num_docs += len([f for f in files if f.endswith(('.pdf', '.docx', '.xlsx'))])
    
    return StatusResponse(
        status="online",
        documentos_carregados=num_docs,
        documentos_em_memoria=documentos_carregados,  # Indica se já foram processados
        consultores_disponiveis=3465,  # Da base de consultores
        modelo=assistente.model_name
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    current_user: User = Depends(get_current_active_user)
):
    """
    Processa uma mensagem do usuário e retorna resposta do assistente.
    
    **Com memória de conversação e timeout de inatividade.**
    **Com sistema de menu: 1 = Base de Dados, 2 = LLM Livre**
    **Requer autenticação via token JWT.**
    """
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    # REMOVIDO: Não bloqueia mais esperando documentos
    # A função carregar_documentos_se_necessario() foi removida daqui
    # Os documentos são carregados em background no startup
    
    # Define session_id baseado no usuário
    session_id = f"user_{current_user.id}"
    
    # Limpa sessões inativas globalmente
    sessoes_limpas = limpar_sessoes_inativas()
    if sessoes_limpas > 0:
        print(f"🧹 {sessoes_limpas} sessão(ões) inativa(s) removida(s)")
    
    # Atualiza timestamp de atividade da sessão atual
    atualizar_atividade_sessao(session_id)
    
    # Verifica se precisa limitar o contexto
    contexto_foi_limitado = limitar_contexto_sessao(session_id)
    
    # **NOVO: Verifica se é a primeira interação do usuário**
    primeira_interacao = session_id not in conversas or len(conversas.get(session_id, [])) == 0
    
    # Se for a primeira interação E a mensagem for uma saudação genérica, exibe o menu
    saudacoes = ['oi', 'olá', 'ola', 'hey', 'hi', 'hello', 'bom dia', 'boa tarde', 'boa noite']
    mensagem_lower = message.mensagem.strip().lower()
    
    if primeira_interacao and (mensagem_lower in saudacoes or len(mensagem_lower) < 10):
        # Força exibição do menu enviando string vazia para o assistente
        resultado = assistente.processar_consulta("")
        
        return ChatResponse(
            resposta=resultado.get("resposta", ""),
            consultores=[],
            documentos=[],
            confianca=1.0,
            fonte="menu",
            usado_internet=False
        )
    
    try:
        # Obtém histórico formatado para incluir no contexto
        historico_contexto = obter_historico_formatado(session_id, limite=5)
        
        # Monta a consulta com contexto histórico
        consulta_com_contexto = message.mensagem
        if historico_contexto:
            consulta_com_contexto = f"""{historico_contexto}

### NOVA PERGUNTA DO USUÁRIO:
{message.mensagem}

**INSTRUÇÕES:**
- Considere o histórico acima ao responder
- Se a pergunta se referir a algo mencionado anteriormente ("isso", "aquilo", "a anterior"), use o contexto
- Mantenha a coerência com respostas anteriores
- Se for um novo assunto, responda normalmente
"""
        
        # Processa consulta com contexto
        resultado = assistente.processar_consulta(consulta_com_contexto)
        
        # Extrai informações da resposta
        resposta_texto = resultado.get("resposta", "")
        consultores = resultado.get("consultores", [])
        fontes = resultado.get("fontes", [])
        
        # Avalia confiança (simplificado)
        confianca = 0.8 if fontes else 0.5
        
        # Inicializa histórico se não existir
        if session_id not in conversas:
            conversas[session_id] = []
        
        # Salva no histórico vinculado ao usuário
        conversas[session_id].append({
            "usuario": message.mensagem,  # Salva pergunta original (sem contexto)
            "assistente": resposta_texto,
            "timestamp": datetime.now().isoformat(),
            "user_id": current_user.id,
            "user_email": current_user.email,
            "contexto_limitado": contexto_foi_limitado  # Flag se contexto foi resetado
        })
        
        # Adiciona aviso se o contexto foi limitado
        aviso_contexto = ""
        if contexto_foi_limitado:
            aviso_contexto = f"\n\n_ℹ️ Nota: O histórico da conversa foi limitado às últimas {MAX_MENSAGENS_CONTEXTO} mensagens para otimizar o desempenho._"
        
        return ChatResponse(
            resposta=resposta_texto + aviso_contexto,
            consultores=consultores,
            documentos=fontes,
            confianca=confianca,
            fonte="base_local",
            usado_internet=False
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar consulta: {str(e)}")

@app.get("/api/historico")
async def get_historico(current_user: User = Depends(get_current_active_user)):
    """Retorna o histórico de conversas do usuário autenticado."""
    session_id = f"user_{current_user.id}"
    
    if session_id not in conversas:
        return {"historico": []}
    
    return {"historico": conversas[session_id]}

@app.delete("/api/historico")
async def limpar_historico(current_user: User = Depends(get_current_active_user)):
    """Limpa o histórico do usuário autenticado."""
    session_id = f"user_{current_user.id}"
    
    if session_id in conversas:
        conversas[session_id] = []
    
    if session_id in ultima_atividade:
        del ultima_atividade[session_id]
    
    return {"mensagem": "Histórico limpo com sucesso"}

@app.get("/api/sessao/status")
async def status_sessao(current_user: User = Depends(get_current_active_user)):
    """
    Retorna informações sobre a sessão atual do usuário.
    """
    session_id = f"user_{current_user.id}"
    
    # Verifica se há histórico
    num_mensagens = len(conversas.get(session_id, []))
    
    # Calcula tempo desde última atividade
    ultima_msg = None
    tempo_inativo = None
    sessao_ativa = session_id in ultima_atividade
    
    if sessao_ativa:
        ultimo_acesso = ultima_atividade[session_id]
        tempo_inativo_segundos = (datetime.now() - ultimo_acesso).total_seconds()
        tempo_inativo = int(tempo_inativo_segundos / 60)  # em minutos
        
        if num_mensagens > 0:
            ultima_msg = conversas[session_id][-1]["timestamp"]
    
    return {
        "session_id": session_id,
        "ativa": sessao_ativa,
        "num_mensagens": num_mensagens,
        "tempo_inativo_minutos": tempo_inativo,
        "timeout_minutos": TIMEOUT_SESSAO_MINUTOS,
        "max_mensagens_contexto": MAX_MENSAGENS_CONTEXTO,
        "contexto_sera_limitado": num_mensagens >= MAX_MENSAGENS_CONTEXTO,
        "ultima_mensagem": ultima_msg
    }

@app.post("/api/sessao/renovar")
async def renovar_sessao(current_user: User = Depends(get_current_active_user)):
    """
    Renova a sessão do usuário (atualiza timestamp de atividade).
    """
    session_id = f"user_{current_user.id}"
    atualizar_atividade_sessao(session_id)
    
    return {
        "mensagem": "Sessão renovada com sucesso",
        "session_id": session_id,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/upload")
async def upload_documentos(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Faz upload de documentos para a base de conhecimento de forma INCREMENTAL.
    Apenas processa arquivos novos ou modificados.
    
    Requer autenticação.
    """
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    os.makedirs(DIRETORIO_DOCS, exist_ok=True)
    
    documentos_salvos = []
    documentos_pulados = []
    
    for file in files:
        # Valida extensão
        if not file.filename.endswith(('.pdf', '.docx', '.xlsx', '.txt', '.md')):
            continue
        
        # Salva arquivo
        file_path = os.path.join(DIRETORIO_DOCS, file.filename)
        
        # Verifica se arquivo já existe e não foi modificado
        if assistente.base_conhecimento.arquivo_ja_processado(file_path):
            documentos_pulados.append({
                "nome": file.filename,
                "motivo": "Já processado anteriormente"
            })
            continue
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        documentos_salvos.append({
            "nome": file.filename,
            "tamanho": len(content),
            "tipo": file.filename.split('.')[-1],
            "caminho": file_path
        })
    
    # Processa APENAS os novos documentos
    documentos_adicionados = 0
    if documentos_salvos:
        from src.knowledge_base.processador_documentos import ProcessadorDocumentos
        processador = ProcessadorDocumentos()
        
        for doc_info in documentos_salvos:
            try:
                # Processa o documento
                chunks = processador.processar_arquivo(doc_info["caminho"])
                
                # Adiciona incrementalmente (verifica hash internamente)
                assistente.base_conhecimento.adicionar_documentos_incrementalmente(
                    chunks,
                    caminho_arquivo=doc_info["caminho"]
                )
                documentos_adicionados += 1
                
            except Exception as e:
                print(f"❌ Erro ao processar {doc_info['nome']}: {e}")
                doc_info["erro"] = str(e)
    
    return {
        "mensagem": f"{documentos_adicionados} novo(s) documento(s) processado(s)",
        "novos": documentos_salvos,
        "pulados": documentos_pulados,
        "total_novos": len(documentos_salvos),
        "total_pulados": len(documentos_pulados)
    }

@app.post("/api/base/processar-diretorio")
async def processar_diretorio_incremental(
    current_user: User = Depends(get_current_active_user)
):
    """
    Processa todos os documentos no diretório de forma INCREMENTAL.
    Apenas adiciona arquivos novos ou modificados.
    
    Requer autenticação (apenas admins).
    """
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem processar diretórios")
    
    if not os.path.exists(DIRETORIO_DOCS):
        raise HTTPException(status_code=404, detail="Diretório de documentos não encontrado")
    
    from src.knowledge_base.processador_documentos import ProcessadorDocumentos
    processador = ProcessadorDocumentos()
    
    arquivos_processados = []
    arquivos_pulados = []
    erros = []
    
    # Varre todos os arquivos no diretório
    for root, dirs, files in os.walk(DIRETORIO_DOCS):
        for file in files:
            if file.endswith(('.pdf', '.docx', '.xlsx', '.txt', '.md')):
                file_path = os.path.join(root, file)
                
                # Verifica se já foi processado
                if assistente.base_conhecimento.arquivo_ja_processado(file_path):
                    arquivos_pulados.append({
                        "arquivo": file,
                        "caminho": file_path
                    })
                    continue
                
                try:
                    # Processa o arquivo
                    chunks = processador.processar_arquivo(file_path)
                    
                    # Adiciona à base
                    assistente.base_conhecimento.adicionar_documentos_incrementalmente(
                        chunks,
                        caminho_arquivo=file_path
                    )
                    
                    arquivos_processados.append({
                        "arquivo": file,
                        "chunks": len(chunks),
                        "caminho": file_path
                    })
                    
                except Exception as e:
                    print(f"❌ Erro ao processar {file}: {e}")
                    erros.append({
                        "arquivo": file,
                        "erro": str(e)
                    })
    
    return {
        "mensagem": f"Processamento incremental concluído",
        "novos_processados": len(arquivos_processados),
        "pulados": len(arquivos_pulados),
        "erros": len(erros),
        "detalhes": {
            "processados": arquivos_processados,
            "pulados": arquivos_pulados,
            "erros": erros
        }
    }

@app.get("/api/base/estatisticas")
async def obter_estatisticas_base(
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna estatísticas detalhadas da base de conhecimento.
    
    Requer autenticação.
    """
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    stats = assistente.base_conhecimento.obter_estatisticas()
    
    return {
        "total_chunks": stats["total_chunks"],
        "total_arquivos": stats["total_arquivos"],
        "arquivos": stats["arquivos"],
        "ultima_atualizacao": max(
            [a["data"] for a in stats["arquivos"]] + ["N/A"]
        ) if stats["arquivos"] else "N/A"
    }

@app.delete("/api/base/limpar")
async def limpar_base_conhecimento(
    current_user: User = Depends(get_current_active_user)
):
    """
    LIMPA COMPLETAMENTE a base de conhecimento.
    ⚠️ ATENÇÃO: Esta operação é irreversível!
    
    Requer autenticação de administrador.
    """
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem limpar a base")
    
    try:
        assistente.base_conhecimento.limpar_base()
        
        return {
            "mensagem": "Base de conhecimento limpa com sucesso",
            "aviso": "Todos os documentos foram removidos da base. Processe novamente para reconstruir."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar base: {str(e)}")

@app.delete("/api/base/arquivo/{nome_arquivo}")
async def remover_arquivo_base(
    nome_arquivo: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove um arquivo específico do controle da base de conhecimento.
    
    Requer autenticação de administrador.
    """
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem remover arquivos")
    
    # Busca o arquivo no diretório
    file_path = None
    for root, dirs, files in os.walk(DIRETORIO_DOCS):
        if nome_arquivo in files:
            file_path = os.path.join(root, nome_arquivo)
            break
    
    if not file_path:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    try:
        assistente.base_conhecimento.remover_arquivo(file_path)
        
        return {
            "mensagem": f"Arquivo '{nome_arquivo}' removido do controle",
            "aviso": "Para remover completamente, limpe e reconstrua a base sem este arquivo"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover arquivo: {str(e)}")

@app.get("/api/documentos")
async def listar_documentos():
    """Lista todos os documentos na base de conhecimento."""
    if not os.path.exists(DIRETORIO_DOCS):
        return {"documentos": []}
    
    documentos = []
    
    for root, dirs, files in os.walk(DIRETORIO_DOCS):
        for file in files:
            if file.endswith(('.pdf', '.docx', '.xlsx')):
                file_path = os.path.join(root, file)
                tamanho = os.path.getsize(file_path)
                
                documentos.append({
                    "nome": file,
                    "tipo": file.split('.')[-1],
                    "tamanho": tamanho,
                    "pasta": os.path.basename(root)
                })
    
    return {"documentos": documentos, "total": len(documentos)}

@app.get("/api/metricas")
async def get_metricas():
    """Retorna métricas do sistema."""
    num_docs = 0
    if os.path.exists(DIRETORIO_DOCS):
        for root, dirs, files in os.walk(DIRETORIO_DOCS):
            num_docs += len([f for f in files if f.endswith(('.pdf', '.docx', '.xlsx'))])
    
    total_conversas = sum(len(conv) for conv in conversas.values())
    
    return {
        "documentos_carregados": num_docs,
        "consultores_disponiveis": 3465,
        "consultas_hoje": total_conversas,
        "sessoes_ativas": len(conversas)
    }

@app.get("/health")
async def health_check():
    """Health check para monitoramento."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "assistente_ativo": assistente is not None
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando Servidor API Sebrae...")
    print("📍 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
