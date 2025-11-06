"""
Sistema de autenticação com JWT e OAuth2
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

from src.database import get_db
from src.models import User, LoginHistory

load_dotenv()

# Configurações JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "sua-chave-secreta-super-segura-aqui-mude-em-producao")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 dias

# Configurações OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Context para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- SCHEMAS PYDANTIC ---

class UserCreate(BaseModel):
    """Schema para criar novo usuário."""
    email: EmailStr
    nome: str
    password: str
    empresa: Optional[str] = None
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    cargo: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

class UserLogin(BaseModel):
    """Schema para login."""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema de resposta de usuário."""
    id: int
    email: str
    nome: str
    empresa: Optional[str]
    telefone: Optional[str]
    cargo: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    google_picture: Optional[str]
    is_admin: bool
    email_verificado: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema de token JWT."""
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    """Dados extraídos do token."""
    email: Optional[str] = None

# --- FUNÇÕES DE AUTENTICAÇÃO ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera hash da senha."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria token JWT."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Autentica usuário com email e senha."""
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    
    if not user.hashed_password:  # Usuário Google sem senha
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Obtém usuário atual a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)
        
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.email).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Verifica se usuário está ativo."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Verifica se usuário é admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissões insuficientes"
        )
    return current_user

# --- FUNÇÕES AUXILIARES ---

def create_user(db: Session, user_data: UserCreate) -> User:
    """Cria novo usuário."""
    # Verifica se email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Cria usuário
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        email=user_data.email,
        nome=user_data.nome,
        hashed_password=hashed_password,
        empresa=user_data.empresa,
        telefone=user_data.telefone,
        cpf=user_data.cpf,
        cargo=user_data.cargo,
        cidade=user_data.cidade,
        estado=user_data.estado,
        email_verificado=False
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def create_or_update_google_user(
    db: Session,
    google_id: str,
    email: str,
    nome: str,
    picture: Optional[str] = None
) -> User:
    """Cria ou atualiza usuário do Google."""
    # Procura por google_id
    user = db.query(User).filter(User.google_id == google_id).first()
    
    if user:
        # Atualiza informações
        user.nome = nome
        user.google_picture = picture
        user.last_login = datetime.utcnow()
        user.email_verificado = True  # Email do Google é sempre verificado
    else:
        # Verifica se email já existe
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            # Vincula conta existente ao Google
            user.google_id = google_id
            user.google_picture = picture
            user.email_verificado = True
        else:
            # Cria novo usuário
            user = User(
                email=email,
                nome=nome,
                google_id=google_id,
                google_picture=picture,
                email_verificado=True,
                is_active=True
            )
            db.add(user)
    
    db.commit()
    db.refresh(user)
    
    return user

def register_login_attempt(
    db: Session,
    user_id: int,
    method: str,
    request: Request,
    success: bool = True
):
    """Registra tentativa de login no histórico."""
    login_record = LoginHistory(
        user_id=user_id,
        login_method=method,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        success=success
    )
    
    db.add(login_record)
    
    if success:
        # Atualiza last_login do usuário
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.last_login = datetime.utcnow()
    
    db.commit()
