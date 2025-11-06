"""
Rotas de autenticação e gerenciamento de usuários
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from datetime import timedelta
import os

from src.database import get_db
from src.auth import (
    UserCreate, UserLogin, UserResponse, Token,
    authenticate_user, create_access_token, create_user,
    create_or_update_google_user, register_login_attempt,
    get_current_user, get_current_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.models import User

# Configuração OAuth
config = Config(environ=os.environ)
oauth = OAuth(config)

# Validar credenciais do Google
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    print("⚠️ AVISO: Credenciais do Google OAuth não configuradas!")
    print(f"   GOOGLE_CLIENT_ID: {'✓' if GOOGLE_CLIENT_ID else '✗'}")
    print(f"   GOOGLE_CLIENT_SECRET: {'✓' if GOOGLE_CLIENT_SECRET else '✗'}")
else:
    print("✅ Google OAuth configurado")
    print(f"   Client ID: {GOOGLE_CLIENT_ID[:20]}...")

# Configurar Google OAuth
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account',  # Sempre mostra seleção de conta
    }
)

# Router
router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

# --- ENDPOINTS DE REGISTRO E LOGIN ---

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Registra novo usuário com email e senha.
    
    - **email**: Email único do usuário
    - **nome**: Nome completo
    - **password**: Senha (mínimo 6 caracteres)
    - **empresa**: Empresa (opcional)
    - **telefone**: Telefone (opcional)
    - **cpf**: CPF (opcional)
    - **cargo**: Cargo (opcional)
    - **cidade**: Cidade (opcional)
    - **estado**: Estado - UF (opcional)
    """
    # Validações básicas
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha deve ter no mínimo 6 caracteres"
        )
    
    # Cria usuário
    user = create_user(db, user_data)
    
    # Registra login
    register_login_attempt(db, user.id, "password", request, success=True)
    
    # Cria token
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Login com email e senha.
    
    Retorna token JWT para autenticação nas próximas requisições.
    """
    user = authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Registra login bem-sucedido
    register_login_attempt(db, user.id, "password", request, success=True)
    
    # Cria token
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

# --- ENDPOINTS GOOGLE OAUTH ---

@router.get("/google/login")
async def google_login(request: Request):
    """
    Inicia fluxo de login com Google OAuth2.
    
    Redireciona para página de consentimento do Google.
    """
    try:
        # Constrói a URL de callback manualmente
        redirect_uri = str(request.base_url) + "api/auth/google/callback"
        
        # Log detalhado para debug
        print(f"🔐 Iniciando OAuth Google")
        print(f"   Base URL: {request.base_url}")
        print(f"   Redirect URI: {redirect_uri}")
        print(f"   Client ID: {GOOGLE_CLIENT_ID[:30]}...")
        print(f"   Client Secret: {GOOGLE_CLIENT_SECRET[:20]}...")
        
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        print(f"❌ Erro no Google Login: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao iniciar login com Google: {str(e)}"
        )

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Callback do Google OAuth2.
    
    Processa retorno do Google e cria/atualiza usuário.
    """
    try:
        # Obtém token do Google
        token = await oauth.google.authorize_access_token(request)
        
        # Obtém informações do usuário
        user_info = token.get('userinfo')
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível obter informações do Google"
            )
        
        # Extrai dados
        google_id = user_info.get('sub')
        email = user_info.get('email')
        nome = user_info.get('name', email.split('@')[0])
        picture = user_info.get('picture')
        
        if not google_id or not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados incompletos do Google"
            )
        
        # Cria ou atualiza usuário
        user = create_or_update_google_user(
            db=db,
            google_id=google_id,
            email=email,
            nome=nome,
            picture=picture
        )
        
        # Registra login
        register_login_attempt(db, user.id, "google", request, success=True)
        
        # Cria token JWT
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Redireciona para frontend com token
        return RedirectResponse(
            url=f"/?token={access_token}",
            status_code=status.HTTP_302_FOUND
        )
        
    except Exception as e:
        # Em caso de erro, redireciona para login com mensagem
        error_message = str(e)
        return RedirectResponse(
            url=f"/login.html?error={error_message}",
            status_code=status.HTTP_302_FOUND
        )

# --- ENDPOINTS DE USUÁRIO ---

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Retorna informações do usuário autenticado.
    
    Requer autenticação via token JWT.
    """
    return UserResponse.model_validate(current_user)

@router.put("/me", response_model=UserResponse)
async def update_me(
    nome: str = None,
    empresa: str = None,
    telefone: str = None,
    cargo: str = None,
    cidade: str = None,
    estado: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza informações do usuário autenticado.
    """
    if nome:
        current_user.nome = nome
    if empresa:
        current_user.empresa = empresa
    if telefone:
        current_user.telefone = telefone
    if cargo:
        current_user.cargo = cargo
    if cidade:
        current_user.cidade = cidade
    if estado:
        current_user.estado = estado
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.model_validate(current_user)

@router.post("/logout")
async def logout():
    """
    Logout (client-side apenas - invalidar token no frontend).
    """
    return {"message": "Logout realizado com sucesso"}

# --- ENDPOINTS ADMIN ---

@router.get("/users", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os usuários (apenas admin).
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.model_validate(user) for user in users]

@router.put("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Ativa/desativa usuário (apenas admin).
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    user.is_active = not user.is_active
    db.commit()
    
    return {
        "message": f"Usuário {'ativado' if user.is_active else 'desativado'}",
        "user": UserResponse.model_validate(user)
    }
