# 🔑 Como Configurar a Chave OpenAI

## ✅ Status Atual

- ✅ Biblioteca OpenAI instalada com sucesso
- ✅ Sistema processou 963 chunks de 50+ documentos
- ⚠️ Chave da API precisa ser configurada

## 🔧 Configuração da Chave

### 1. Obter Chave OpenAI

**Opção A: Via GitHub Copilot (Recomendado)**

- Se você tem GitHub Copilot ativo, pode usar a API OpenAI
- Acesse: https://platform.openai.com/
- Faça login com sua conta
- Vá em "API Keys" e gere uma nova chave

**Opção B: Diretamente da OpenAI**

- Acesse: https://platform.openai.com/
- Crie uma conta e configure billing
- Gere uma chave de API

### 2. Configurar no Projeto

Edite o arquivo `.env` e substitua:

```bash
# ANTES:
OPENAI_API_KEY="sua_chave_openai_aqui"

# DEPOIS (com sua chave real):
OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Importante:** A chave deve começar com `sk-`

### 3. Testar Configuração

```bash
python3 test_openai.py
```

### 4. Executar o Sistema

```bash
streamlit run app.py
```

## 🎯 O que já está funcionando:

- ✅ Interface Streamlit carregada
- ✅ Base de conhecimento com 963 chunks processados
- ✅ 50+ documentos do Sebrae indexados
- ✅ Sistema RAG configurado
- ✅ ChromaDB funcionando

## 📱 URL do Sistema

O Streamlit já está rodando em:

- **Local:** http://localhost:8506
- **Rede:** http://10.0.0.54:8506

## 🔍 Próximos Passos

1. Configure a chave OpenAI no arquivo `.env`
2. Teste com `python3 test_openai.py`
3. Acesse http://localhost:8506
4. Faça perguntas sobre os documentos do Sebrae!

## 💡 Dica

O sistema já processou todos os documentos automaticamente. Assim que você configurar a chave da API, poderá fazer perguntas como:

- "O que é gestão de vendas?"
- "Como fazer um plano de marketing?"
- "Quais são as boas práticas de segurança?"
