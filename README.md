# 🎯 Consultor IA Sebrae - Sistema Inteligente de Apoio ao Empreendedorismo

<div align="center">
  <img src="https://img.shields.io/badge/Status-Operacional-brightgreen" />
  <img src="https://img.shields.io/badge/Tecnologia-OpenAI%20%2B%20ChromaDB-blue" />
  <img src="https://img.shields.io/badge/Interface-Streamlit-red" />
  <img src="https://img.shields.io/badge/Consultores-3.465%20Especialistas-orange" />
</div>

## 🚀 **VISÃO GERAL**

O **Consultor IA Sebrae** é um sistema completo de inteligência artificial que combina conhecimento oficial do Sebrae com busca inteligente de consultores especializados, oferecendo uma experiência única para empreendedores que buscam orientação profissional.

### ✨ **DIFERENCIAIS ÚNICOS**

- 🧠 **Chain of Thought Profissional**: Metodologia transparente de raciocínio
- 📚 **Base Oficial Sebrae**: 963 chunks de 50+ documentos oficiais
- 👥 **3.465 Consultores**: Busca automática de especialistas por área
- 🔍 **Busca Inteligente**: RAG avançado com fallback automático
- 💼 **Integração Completa**: Documentação + consultores em uma resposta

---

## 🎯 **FUNCIONALIDADES PRINCIPAIS**

### 1. 🧠 **METODOLOGIA CHAIN OF THOUGHT**

```
💭 Análise: [Categorização da consulta e estratégia escolhida]

[Resposta técnica baseada em documentos oficiais]

---
📚 Fontes consultadas:
1. FT_MEI_Abertura_Procedimentos.pdf
2. MOA_Gestao_Financeira_PME.pdf

👥 CONSULTORES ESPECIALIZADOS DISPONÍVEIS:
[Lista formatada de especialistas com contatos]

🎯 Resposta baseada em documentos oficiais Sebrae
```

### 2. � **SISTEMA RAG AVANÇADO**

- **Busca Principal**: 8 documentos simultâneos por consulta
- **Busca Fallback**: Busca ampla com termos alternativos
- **Base de Dados**: ChromaDB com embeddings multilíngues
- **Eliminação de Duplicatas**: Sistema inteligente de deduplicação

### 3. 👥 **BUSCA AUTOMÁTICA DE CONSULTORES**

- **Carregamento Automático**: 209 áreas de especialização
- **Correspondência Inteligente**: Por área, subárea e termos relevantes
- **Dados Completos**: Nome, contato, localização, especialidade
- **Formatação Profissional**: Layout otimizado para contratação

### 4. 🎨 **INTERFACE STREAMLIT PROFISSIONAL**

- **Design Sebrae**: Cores e identidade visual oficial
- **Chat Interativo**: Histórico de conversas persistente
- **Sidebar Informativa**: Estatísticas e documentos disponíveis
- **Responsividade**: Otimizado para desktop e mobile

### 5. 📝 **SISTEMA DE PROMPTS MARKDOWN**

- **Templates Reutilizáveis**: Prompts estruturados em arquivos `.md`
- **Variáveis Dinâmicas**: Sistema `{{variavel}}` para personalização
- **Biblioteca de Templates**: Análise de viabilidade, marketing, validação
- **Integração Completa**: Funciona com qualquer sistema de IA

---

## 🏗️ **ARQUITETURA TÉCNICA**

### **Stack Tecnológica**

```
Frontend:      Streamlit
LLM:          OpenAI GPT (API)
Vector DB:    ChromaDB
Embeddings:   SentenceTransformers (multilingual)
Docs:         PyPDF + python-docx + openpyxl
```

### **Estrutura do Projeto**

```
sebrae-ai-assistant/
├── 📱 app.py                           # Interface Streamlit
├── 🧠 src/
│   ├── assistant.py                    # Consultor IA principal
│   └── knowledge_base/
│       ├── base_conhecimento.py        # Sistema RAG
│       ├── processador_documentos.py   # Processamento PDFs/DOCs
│       └── gerenciador_consultores.py  # Busca de especialistas
├── 📚 dados/
│   └── documentos/
│       ├── [50+ PDFs e DOCs oficiais]
│       └── Consultores/
│           └── [209 planilhas Excel]
├── 📝 prompts/                         # Templates de prompts
│   ├── exemplo_prompt.md               # Análise de empreendimento
│   ├── analise_concorrencia.md         # Análise competitiva
│   ├── plano_marketing_digital.md      # Marketing digital
│   └── validacao_ideia_negocio.md      # Validação de ideias
├── ⚙️ .chromadb/                       # Base vetorial
├── 📋 requirements.txt                 # Dependências
└── 🔧 .env                            # Configurações
```

---

## ⚡ **GUIA DE INSTALAÇÃO**

### **1. Pré-requisitos**

```bash
Python 3.9+
Git
```

### **2. Clonagem e Setup**

```bash
# Clonar repositório
git clone [seu-repositorio]
cd sebrae-ai-assistant

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### **3. Configuração da API**

Crie o arquivo `.env`:

```env
# Chave da API OpenAI
OPENAI_API_KEY="sua-chave-openai-aqui"
```

### **4. Primeira Execução**

```bash
# Processar documentos (primeira vez)
python -c "
from src.assistant import AssistenteSebrae
assistant = AssistenteSebrae()
assistant.carregar_documentos('dados/documentos')
"

# Executar aplicação
streamlit run app.py
```

**🌐 Acesso:** http://localhost:8501

---

## 💡 **EXEMPLOS DE USO**

### **Consulta Típica:**

**Usuário:** "Como abrir um MEI para uma loja de roupas?"

**Sistema:**

```
💭 Análise: Produto Sebrae - procedimentos oficiais

Com base nos documentos oficiais do Sebrae, para abrir um MEI
para loja de roupas você deve...

---
📚 Fontes consultadas:
1. FT_MEI_Procedimentos_Abertura.pdf

👥 CONSULTORES ESPECIALIZADOS:
👤 Maria Silva - Consultora MEI
📞 (11) 99999-9999 | 📧 maria@consultoria.com
📍 São Paulo - SP

🎯 Resposta baseada em documentos oficiais Sebrae
```

---

## 📊 **ESPECIFICAÇÕES TÉCNICAS**

### **Performance**

| Métrica                    | Valor |
| -------------------------- | ----- |
| 📄 Documentos Processados  | 50+   |
| 🧩 Chunks Vetorizados      | 963   |
| 👥 Consultores Carregados  | 3.465 |
| 📂 Áreas de Especialização | 209   |
| ⚡ Tempo Médio Resposta    | 2-4s  |
| 🔍 Documentos por Busca    | 8     |

### **Capacidades do Sistema**

- ✅ **Busca Semântica**: Compreensão de contexto e intenção
- ✅ **Fallback Inteligente**: Múltiplas estratégias de busca
- ✅ **Transparência Total**: Fontes e estratégias explícitas
- ✅ **Integração Consultores**: Busca automática por especialização
- ✅ **Persistência**: Histórico de conversas salvo
- ✅ **Escalabilidade**: Suporte a milhares de documentos

---

## 🔧 **CONFIGURAÇÕES AVANÇADAS**

### **Parâmetros do Sistema**

```python
# src/assistant.py
class AssistenteSebrae:
    model_name = "gpt-3.5-turbo"          # Modelo LLM
    temperature_oficial = 0.2              # Precisão para docs oficiais
    temperature_fallback = 0.4             # Criatividade para busca ampla
    max_tokens = 2500                      # Limite de resposta
    num_documentos_busca = 8               # Documentos por consulta
    limite_consultores = 3                 # Consultores por resposta
```

### **Personalização da Interface**

```python
# app.py - Cores Sebrae
st.markdown("""
<style>
.stApp { background-color: #f8f9fa; }
.main-header { color: #1e3a8a; }
.sidebar .sidebar-content { background-color: #3b82f6; }
</style>
""", unsafe_allow_html=True)
```

---

## 🚀 **ROADMAP DE DESENVOLVIMENTO**

### **✅ Versão 1.0 - Atual**

- [x] Sistema RAG com base oficial Sebrae
- [x] Interface Streamlit profissional
- [x] Busca automática de consultores
- [x] Chain of Thought methodology

### **🔄 Versão 1.1 - Em Planejamento**

- [ ] Sistema de feedback de usuários
- [ ] Métricas de satisfação
- [ ] Cache de consultas frequentes
- [ ] API REST para integração

### **🎯 Versão 2.0 - Futuro**

- [ ] Agendamento direto de consultores
- [ ] Sistema de avaliações
- [ ] Integração com CRM Sebrae
- [ ] App mobile dedicado

---

## 👥 **CONTRIBUIÇÕES**

### **Como Contribuir**

1. **Fork** do repositório
2. **Clone** sua fork
3. **Crie** uma branch: `git checkout -b feature/nova-funcionalidade`
4. **Commit** suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
5. **Push** para a branch: `git push origin feature/nova-funcionalidade`
6. **Abra** um Pull Request

### **Padrões de Código**

- Python 3.9+ com type hints
- Docstrings em português
- Formatação com black
- Testes unitários obrigatórios

---

## 📞 **SUPORTE E CONTATO**

### **Documentação Técnica**

- 📖 [Wiki do Projeto](./docs/)
- 🔧 [Guia de Troubleshooting](./docs/troubleshooting.md)
- 🎯 [Exemplos Avançados](./docs/examples.md)

### **Comunidade**

- 💬 Issues do GitHub para bugs
- 💡 Discussions para ideias
- 📧 Contato direto para parcerias

---

## 📜 **LICENÇA**

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">

**🎯 Consultor IA Sebrae**  
_Transformando conhecimento em oportunidades_

[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-red)](https://streamlit.io/) [![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT-blue)](https://openai.com/) [![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-green)](https://www.trychroma.com/)

_Desenvolvido com 💙 para o ecossistema empreendedor brasileiro_

</div>
