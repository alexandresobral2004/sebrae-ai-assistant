#!/bin/bash

# Script para iniciar o servidor FastAPI do Sebrae AI Assistant

echo "🚀 Iniciando Servidor API Sebrae..."

# Ativar ambiente virtual
source .venv/bin/activate

# Iniciar servidor
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
