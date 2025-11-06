"""
Models SQLAlchemy para usuários e autenticação
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from src.database import Base
from datetime import datetime

class User(Base):
    """Model de usuário."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nome = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Null para login Google
    
    # Informações adicionais
    empresa = Column(String(255), nullable=True)
    telefone = Column(String(50), nullable=True)
    cpf = Column(String(14), nullable=True)
    cargo = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    
    # Autenticação Google
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    google_picture = Column(String(500), nullable=True)
    
    # Status e permissões
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    email_verificado = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', nome='{self.nome}')>"


class LoginHistory(Base):
    """Histórico de logins para auditoria."""
    __tablename__ = "login_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    login_method = Column(String(50), nullable=False)  # 'google' ou 'password'
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    success = Column(Boolean, default=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<LoginHistory(user_id={self.user_id}, method='{self.login_method}')>"
