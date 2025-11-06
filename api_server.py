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
from datetime import datetime
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
    """Inicializa o assistente ao iniciar a API (sem carregar documentos)."""
    global assistente
    print("🚀 Inicializando Assistente IA Sebrae...")
    assistente = AssistenteSebrae()
    print("✅ Assistente IA Sebrae pronto!")
    print("💡 Documentos serão carregados automaticamente na primeira consulta")

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
    
    **Requer autenticação via token JWT.**
    """
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    # Carrega documentos na primeira consulta (lazy loading)
    carregar_documentos_se_necessario()
    
    try:
        # Processa consulta
        resultado = assistente.processar_consulta(message.mensagem)
        
        # Extrai informações da resposta
        resposta_texto = resultado.get("resposta", "")
        consultores = resultado.get("consultores", [])
        fontes = resultado.get("fontes", [])
        
        # Avalia confiança (simplificado)
        confianca = 0.8 if fontes else 0.5
        
        # Salva no histórico vinculado ao usuário
        session_id = f"user_{current_user.id}"
        if session_id not in conversas:
            conversas[session_id] = []
        
        conversas[session_id].append({
            "usuario": message.mensagem,
            "assistente": resposta_texto,
            "timestamp": datetime.now().isoformat(),
            "user_id": current_user.id,
            "user_email": current_user.email
        })
        
        return ChatResponse(
            resposta=resposta_texto,
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
    
    return {"mensagem": "Histórico limpo com sucesso"}

@app.post("/api/upload")
async def upload_documentos(files: List[UploadFile] = File(...)):
    """Faz upload de documentos para a base de conhecimento."""
    if not assistente:
        raise HTTPException(status_code=503, detail="Assistente não inicializado")
    
    os.makedirs(DIRETORIO_DOCS, exist_ok=True)
    
    documentos_salvos = []
    
    for file in files:
        # Valida extensão
        if not file.filename.endswith(('.pdf', '.docx', '.xlsx')):
            continue
        
        # Salva arquivo
        file_path = os.path.join(DIRETORIO_DOCS, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        documentos_salvos.append({
            "nome": file.filename,
            "tamanho": len(content),
            "tipo": file.filename.split('.')[-1]
        })
    
    # Recarrega documentos
    if documentos_salvos:
        global documentos_carregados
        assistente.carregar_documentos(DIRETORIO_DOCS)
        documentos_carregados = True  # Marca que documentos foram carregados
    
    return {
        "mensagem": f"{len(documentos_salvos)} documento(s) processado(s)",
        "documentos": documentos_salvos
    }

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
