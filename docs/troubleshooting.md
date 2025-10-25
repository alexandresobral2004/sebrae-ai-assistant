# 🔧 Guia de Troubleshooting - Consultor IA Sebrae

Este guia contém soluções para os problemas mais comuns encontrados durante a instalação e uso do sistema.

---

## 🚨 **PROBLEMAS COMUNS E SOLUÇÕES**

### 1. 🔑 **Erro de API Key**

#### **Problema:**

```
ValueError: A chave de API do OpenAI não foi configurada
```

#### **Soluções:**

```bash
# 1. Verificar se o arquivo .env existe
ls -la .env

# 2. Verificar o conteúdo do .env
cat .env

# 3. Copiar do exemplo se necessário
cp .env.example .env

# 4. Editar com sua chave
nano .env
# Adicionar: OPENAI_API_KEY="sua-chave-real-aqui"

# 5. Reiniciar o aplicativo
streamlit run app.py
```

#### **Verificação:**

```python
import os
from dotenv import load_dotenv
load_dotenv()
print("API Key:", os.getenv("OPENAI_API_KEY")[:10] + "..." if os.getenv("OPENAI_API_KEY") else "NÃO ENCONTRADA")
```

---

### 2. 📚 **ChromaDB não carrega**

#### **Problema:**

```
RuntimeError: ChromaDB not initialized
```

#### **Soluções:**

```bash
# 1. Remover base corrompida
rm -rf .chromadb

# 2. Reinstalar ChromaDB
pip uninstall chromadb -y
pip install chromadb>=0.5.0

# 3. Reprocessar documentos
python -c "
from src.assistant import AssistenteSebrae
assistant = AssistenteSebrae()
assistant.carregar_documentos('dados/documentos')
"
```

---

### 3. 🔄 **Erro de Embeddings**

#### **Problema:**

```
TOKENIZERS_PARALLELISM warnings
```

#### **Soluções:**

```bash
# Método 1: Variável de ambiente
export TOKENIZERS_PARALLELISM=false
streamlit run app.py

# Método 2: No código
TOKENIZERS_PARALLELISM=false streamlit run app.py

# Método 3: Permanente (.bashrc/.zshrc)
echo 'export TOKENIZERS_PARALLELISM=false' >> ~/.zshrc
source ~/.zshrc
```

---

### 4. 📄 **Documentos não carregam**

#### **Problema:**

```
FileNotFoundError: dados/documentos not found
```

#### **Soluções:**

```bash
# 1. Verificar estrutura de pastas
ls -la dados/documentos/

# 2. Verificar permissões
chmod -R 755 dados/

# 3. Verificar tipos de arquivo
find dados/documentos/ -type f -name "*.pdf" | wc -l
find dados/documentos/ -type f -name "*.docx" | wc -l

# 4. Testar processamento individual
python -c "
from src.knowledge_base.processador_documentos import ProcessadorDocumentos
proc = ProcessadorDocumentos()
chunks = proc.processar_arquivo('dados/documentos/[arquivo-teste].pdf')
print(f'Chunks processados: {len(chunks)}')
"
```

---

### 5. 👥 **Consultores não aparecem**

#### **Problema:**

```
Total de consultores carregados: 0
```

#### **Soluções:**

```bash
# 1. Verificar pasta de consultores
ls -la dados/documentos/Consultores/

# 2. Verificar arquivos Excel
find dados/documentos/Consultores/ -name "*.xlsx" | head -5

# 3. Testar carregamento
python -c "
from src.knowledge_base.gerenciador_consultores import GerenciadorConsultores
gc = GerenciadorConsultores()
stats = gc.obter_estatisticas()
print(f'Consultores: {stats[\"total_consultores\"]}')
print(f'Áreas: {stats[\"total_areas\"]}')
"

# 4. Verificar dependência pandas
pip install pandas>=2.0.0
```

---

### 6. 🌐 **Streamlit não inicia**

#### **Problema:**

```
command not found: streamlit
```

#### **Soluções:**

```bash
# 1. Ativar ambiente virtual
source .venv/bin/activate

# 2. Verificar instalação
pip list | grep streamlit

# 3. Reinstalar se necessário
pip install streamlit>=1.35.0

# 4. Verificar versão Python
python --version  # Deve ser 3.9+

# 5. Executar diretamente
python -m streamlit run app.py
```

---

### 7. 🐌 **Performance lenta**

#### **Problema:**

Respostas muito demoradas (>10 segundos)

#### **Soluções:**

```python
# 1. Otimizar configurações (src/assistant.py)
class AssistenteSebrae:
    def __init__(self):
        # Reduzir documentos por busca
        self.num_documentos = 5  # Em vez de 8

        # Usar modelo mais rápido
        self.model_name = "gpt-3.5-turbo"

        # Reduzir tokens
        self.max_tokens = 1500

# 2. Limpar cache do ChromaDB
rm -rf .chromadb
# Reprocessar documentos

# 3. Verificar recursos do sistema
htop  # Ou Activity Monitor no Mac
```

---

### 8. 💾 **Erro de memória**

#### **Problema:**

```
MemoryError: Unable to allocate memory
```

#### **Soluções:**

```python
# 1. Processar documentos em lotes menores
# Em processador_documentos.py
def processar_em_lotes(self, documentos, tamanho_lote=10):
    for i in range(0, len(documentos), tamanho_lote):
        lote = documentos[i:i+tamanho_lote]
        # Processar lote

# 2. Configurar chunk size menor
chunk_size = 500  # Em vez de 1000
chunk_overlap = 50  # Em vez de 100

# 3. Usar modelo de embeddings menor
model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

---

## 🔍 **COMANDOS DE DEBUG**

### **Verificação Completa do Sistema**

```bash
#!/bin/bash
echo "=== DIAGNÓSTICO COMPLETO ==="

echo "1. Verificando Python..."
python --version

echo "2. Verificando ambiente virtual..."
which python

echo "3. Verificando dependências..."
pip list | grep -E "(streamlit|openai|chromadb|pandas)"

echo "4. Verificando arquivos de configuração..."
ls -la .env .env.example

echo "5. Verificando estrutura de dados..."
find dados/ -type f | wc -l

echo "6. Verificando ChromaDB..."
ls -la .chromadb/

echo "7. Testando importações..."
python -c "
try:
    from src.assistant import AssistenteSebrae
    print('✅ Importação OK')
except Exception as e:
    print(f'❌ Erro: {e}')
"

echo "8. Verificando API Key..."
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
print(f'API Key: {\"✅ Configurada\" if key else \"❌ Não encontrada\"}')
"
```

### **Teste Rápido de Funcionalidades**

```python
#!/usr/bin/env python3
"""Teste rápido de todas as funcionalidades"""

def teste_rapido():
    print("🧪 TESTE RÁPIDO DO SISTEMA")
    print("=" * 40)

    try:
        # 1. Teste de importação
        from src.assistant import AssistenteSebrae
        print("✅ 1. Importação: OK")

        # 2. Teste de inicialização
        assistant = AssistenteSebrae()
        print("✅ 2. Inicialização: OK")

        # 3. Teste de base de conhecimento
        stats_docs = len(assistant.base_conhecimento.collection.get()["documents"])
        print(f"✅ 3. Documentos carregados: {stats_docs}")

        # 4. Teste de consultores
        stats = assistant.gerenciador_consultores.obter_estatisticas()
        print(f"✅ 4. Consultores carregados: {stats['total_consultores']}")

        # 5. Teste de consulta simples
        resultado = assistant.processar_consulta("teste")
        print("✅ 5. Consulta de teste: OK")

        print("\n🎉 TODOS OS TESTES PASSARAM!")

    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    teste_rapido()
```

---

## 📞 **SUPORTE ADICIONAL**

### **Logs Detalhados**

```python
# Ativar logs detalhados (app.py)
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### **Monitoramento de Recursos**

```bash
# CPU e Memória
htop

# Espaço em disco
df -h

# Processos Python
ps aux | grep python

# Portas abertas
lsof -i :8501
```

### **Reset Completo**

```bash
#!/bin/bash
echo "🔄 RESET COMPLETO DO SISTEMA"

# 1. Parar aplicação
pkill -f streamlit

# 2. Limpar bases de dados
rm -rf .chromadb

# 3. Limpar cache Python
find . -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# 4. Recriar ambiente virtual
deactivate 2>/dev/null || true
rm -rf .venv
python -m venv .venv
source .venv/bin/activate

# 5. Reinstalar dependências
pip install -r requirements.txt

# 6. Reprocessar documentos
python -c "
from src.assistant import AssistenteSebrae
assistant = AssistenteSebrae()
assistant.carregar_documentos('dados/documentos')
"

# 7. Testar sistema
python teste_sistema_completo.py

echo "✅ Reset completo finalizado!"
```

---

## 🆘 **CONTATO PARA SUPORTE**

Se os problemas persistirem:

1. **📝 Crie um Issue** no GitHub com:

   - Descrição detalhada do problema
   - Mensagens de erro completas
   - Saída do comando de diagnóstico
   - Sistema operacional e versão Python

2. **📧 Inclua logs** relevantes:

   ```bash
   streamlit run app.py > logs.txt 2>&1
   ```

3. **🔍 Verifique Issues existentes** antes de criar novo

---

_Este guia é atualizado regularmente. Última atualização: 25/10/2025_
