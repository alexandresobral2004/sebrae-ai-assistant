# 🤖 Consultor Sebrae IA

## Configuração da API OpenAI (GitHub Copilot)

### 🔑 Obtenção da Chave da API

Para usar este assistente, você precisa de uma chave da API OpenAI. Você pode obtê-la através do GitHub Copilot ou diretamente da OpenAI:

#### Opção 1: GitHub Copilot

1. Acesse [GitHub Copilot](https://github.com/features/copilot)
2. Se você tem uma assinatura ativa do GitHub Copilot, pode usar a API OpenAI
3. Acesse [OpenAI Platform](https://platform.openai.com/)
4. Crie uma conta ou faça login
5. Vá para "API Keys" e gere uma nova chave

#### Opção 2: Diretamente da OpenAI

1. Acesse [OpenAI Platform](https://platform.openai.com/)
2. Crie uma conta e configure o billing
3. Gere uma chave de API

### ⚙️ Configuração

1. **Configure a chave da API no arquivo `.env`:**

```bash
# Substitua "sua_chave_openai_aqui" pela sua chave real
OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxx"
```

2. **Instale as dependências:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Execute o assistente:**

```bash
# Interface web
streamlit run app.py

# Ou linha de comando
python3 main.py
```

### 🚀 Funcionalidades

- ✅ **Interface Web Profissional** com design do Sebrae
- ✅ **Processamento de Documentos** (PDF, DOCX, XLSX)
- ✅ **Sistema RAG** (Retrieval-Augmented Generation)
- ✅ **Chat Inteligente** baseado em OpenAI GPT
- ✅ **Base de Conhecimento Persistente** com ChromaDB
- ✅ **Busca Semântica** em documentos

### 📁 Estrutura de Documentos

Coloque seus documentos do Sebrae na pasta:

```
dados/documentos/
├── arquivo1.pdf
├── arquivo2.docx
└── arquivo3.xlsx
```

### 🔄 Modelos Disponíveis

O sistema suporta diferentes modelos OpenAI:

- `gpt-3.5-turbo` (padrão, mais rápido e econômico)
- `gpt-4` (mais preciso, mais caro)
- `gpt-4-turbo` (balance entre velocidade e precisão)

Para alterar o modelo, modifique o parâmetro `model_name` na inicialização do `AssistenteSebrae`.

### 💡 Dicas de Uso

1. **Primeira execução**: Clique em "Atualizar Base de Conhecimento" para processar os documentos
2. **Perguntas eficazes**: Seja específico sobre o que procura
3. **Contexto**: O assistente responde baseado nos documentos carregados

### 🔧 Troubleshooting

**Erro de API Key:**

- Verifique se a chave está correta no arquivo `.env`
- Confirme se a conta OpenAI tem créditos disponíveis

**Erro de importação:**

- Execute: `pip install openai python-dotenv streamlit`

**Documentos não carregados:**

- Verifique se os arquivos estão na pasta `dados/documentos`
- Formatos suportados: PDF, DOCX, XLSX

### 📊 Sistema RAG

O assistente usa um sistema RAG que:

1. **Indexa** documentos em embeddings semânticos
2. **Busca** trechos relevantes para cada pergunta
3. **Gera** respostas contextualizadas com OpenAI GPT
4. **Cita** as fontes dos documentos utilizados
