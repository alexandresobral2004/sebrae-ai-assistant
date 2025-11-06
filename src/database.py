"""
Configuração do banco de dados PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# URL do banco PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/sebrae_ai"
)

# Criar engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_size=10,
    max_overflow=20
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para models
Base = declarative_base()

# Dependency para FastAPI
def get_db():
    """Dependency que fornece sessão de banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
