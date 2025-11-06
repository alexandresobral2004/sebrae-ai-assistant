# 📋 Sistema de Menu Interativo - Assistente Sebrae

## 🎯 Visão Geral

O Assistente Sebrae agora possui um **sistema de menu interativo** que permite ao usuário escolher explicitamente entre dois modos de consulta:

### Modo 1: 📚 Consulta à Base de Dados Sebrae

- **Como usar:** Digite `1` seguido da sua pergunta
- **Exemplo:** `1 Como abrir um MEI?`
- **Funcionalidades:**
  - ✅ Busca informações na base de documentos oficial do Sebrae
  - ✅ Consulta fichas técnicas (FT) e manuais (MOA)
  - ✅ **Indica consultores especializados relacionados**
  - ✅ Fornece fontes dos documentos utilizados
  - ✅ Resposta baseada em conteúdo oficial e validado

### Modo 2: 💬 Conversa Livre com IA

- **Como usar:** Digite `2` seguido da pergunta OU faça a pergunta diretamente
- **Exemplo:** `2 Dicas para aumentar vendas` ou apenas `Como fazer marketing?`
- **Funcionalidades:**
  - ✅ Resposta rápida usando o modelo LLM (GPT)
  - ✅ Orientações gerais sobre empreendedorismo
  - ✅ Dicas e análises sem buscar documentos
  - ❌ **NÃO indica consultores**
  - ❌ **NÃO busca na base de dados local**

---

## 🔧 Como Funciona Tecnicamente

### Fluxo de Processamento

```
Usuário digita pergunta
        ↓
┌───────────────────────────────────┐
│ Detector de Modo                  │
│ - Começa com "1 "? → Modo 1       │
│ - Começa com "2 "? → Modo 2       │
│ - Nenhum número? → Modo 2 (padrão)│
└───────────────────────────────────┘
        ↓
    ┌───┴───┐
    ↓       ↓
┌─────────────────────┐    ┌──────────────────────┐
│   MODO 1            │    │   MODO 2             │
│   Base de Dados     │    │   LLM Livre          │
├─────────────────────┤    ├──────────────────────┤
│ 1. Analisa consulta │    │ 1. Monta prompt      │
│ 2. Busca documentos │    │ 2. Chama LLM         │
│ 3. Busca consultores│    │ 3. Retorna resposta  │
│ 4. Gera resposta    │    │                      │
│    com fontes       │    │ • Sem fontes         │
└─────────────────────┘    │ • Sem consultores    │
                           └──────────────────────┘
```

### Implementação no Código

#### 1. Menu Principal (`_exibir_menu()`)

```python
def _exibir_menu(self) -> str:
    # Retorna texto formatado com opções
    # Mostra explicação de cada modo
    # Exemplos de uso
```

#### 2. Processador Principal (`processar_consulta()`)

```python
def processar_consulta(self, consulta: str):
    # Detecta se consulta começa com "1 " ou "2 "
    # Extrai pergunta removendo o número
    # Direciona para método apropriado
```

#### 3. Modo Base de Dados (`_processar_consulta_base_dados()`)

```python
def _processar_consulta_base_dados(self, consulta: str):
    # Analisa consulta (Chain of Thought)
    # Busca na base de conhecimento
    # Busca consultores relacionados (SEMPRE)
    # Monta resposta com fontes + consultores
```

#### 4. Modo LLM Livre (`_processar_consulta_llm_livre()`)

```python
def _processar_consulta_llm_livre(self, consulta: str):
    # Monta prompt de sistema
    # Chama OpenAI API
    # Retorna resposta sem fontes/consultores
    # Adiciona dica sobre modo 1
```

---

## 📝 Exemplos de Uso

### Exemplo 1: Consulta à Base Sebrae

```
Usuário: 1 Como abrir um MEI?

Sistema:
[Busca documentos oficiais]
[Busca consultores especializados em MEI]

Resposta:
"De acordo com os documentos do Sebrae (FT-1234)...
[Conteúdo da resposta]

📚 Fontes:
- Manual MEI 2024.pdf
- Guia Formalização.pdf

👨‍💼 Consultores Recomendados:
1. João Silva - Especialista em Formalização
2. Maria Santos - Consultora MEI
"
```

### Exemplo 2: Conversa Livre

```
Usuário: 2 Dicas para aumentar vendas

Sistema:
[Chama LLM diretamente, SEM buscar documentos]

Resposta:
"Aqui estão algumas dicas eficazes para aumentar suas vendas:
1. Conheça bem seu público-alvo...
2. Use redes sociais estrategicamente...
[...]

💡 Dica: Se você precisa de informações oficiais do Sebrae,
digite 1 antes da pergunta!"
```

### Exemplo 3: Pergunta Sem Número (Assume Modo 2)

```
Usuário: Como fazer marketing digital?

Sistema:
[Automaticamente usa Modo 2 - LLM Livre]

Resposta:
"Marketing digital é essencial para negócios modernos...
[Resposta gerada pelo LLM]

💡 Dica: Para consultar programas específicos do Sebrae sobre
marketing digital, digite: 1 Programas Sebrae marketing digital"
```

### Exemplo 4: Solicitação do Menu

```
Usuário: menu

Sistema:
╔══════════════════════════════════════════════════════════════╗
║          🤖 ASSISTENTE SEBRAE - MENU DE CONSULTA            ║
╚══════════════════════════════════════════════════════════════╝

[Exibe menu completo com opções]
```

---

## 🎨 Estrutura de Resposta

### Modo 1 (Base de Dados)

```json
{
  "resposta": "Texto da resposta...",
  "fontes": [
    {"titulo": "Manual MEI", "pagina": 5},
    {"titulo": "Guia Formalização", "pagina": 12}
  ],
  "consultores": [
    {
      "nome": "João Silva",
      "especialidade": "MEI e Formalização",
      "contato": "joao@example.com"
    }
  ],
  "palavras_chave": ["MEI", "formalização", "microempreendedor"],
  "modo_consulta": "base_dados",
  "usou_base": true
}
```

### Modo 2 (LLM Livre)

```json
{
  "resposta": "Texto da resposta do LLM...",
  "fontes": [],
  "consultores": [],
  "palavras_chave": [],
  "modo_consulta": "llm_livre",
  "usou_base": false,
  "raciocinio": "Resposta gerada pelo modelo de IA..."
}
```

---

## ⚙️ Configurações e Personalização

### Palavras-chave para Menu

O menu é exibido quando o usuário digita:

- `menu`
- `ajuda`
- `help`
- `opções` / `opcoes`
- String vazia

### Comportamento Padrão

- Se o usuário **não especificar modo** (não digitar 1 ou 2), o sistema assume **Modo 2 (LLM Livre)**
- Isso evita buscas desnecessárias na base para perguntas casuais

### Prompts do Sistema

**Modo 1 (Base de Dados):** Usa prompts Chain of Thought existentes **Modo 2 (LLM Livre):**

```python
prompt_sistema = """Você é um assistente de IA especializado em
empreendedorismo e negócios. Seja didático, prático e forneça
informações acionáveis..."""
```

---

## 🚀 Benefícios do Sistema de Menu

### Para o Usuário

✅ **Controle Total:** Escolhe explicitamente se quer dados oficiais ou resposta rápida  
✅ **Transparência:** Sabe exatamente qual fonte está sendo usada  
✅ **Eficiência:** Respostas rápidas para dúvidas gerais (Modo 2)  
✅ **Precisão:** Dados validados e consultores para demandas específicas (Modo 1)

### Para o Sistema

✅ **Performance:** Evita buscas caras quando não necessário  
✅ **Custos:** Reduz chamadas ao banco vetorial em perguntas casuais  
✅ **Clareza:** Logs mostram claramente qual modo foi usado  
✅ **Manutenibilidade:** Separação clara entre modos de operação

---

## 📊 Logs e Debugging

O sistema gera logs detalhados:

```
💬 MODO: Conversa Livre (usuário não especificou modo)
💬 Respondendo com LLM (sem buscar base): 'Como fazer marketing?'
```

```
📚 MODO: Consulta à Base de Dados Sebrae + Consultores
📚 Buscando na base de dados Sebrae: 'Como abrir um MEI?'
👨‍💼 Buscando consultores relacionados...
```

---

## 🔄 Fluxograma Completo

```
┌─────────────────────────────┐
│  Usuário envia mensagem     │
└──────────┬──────────────────┘
           ↓
    ┌──────────────┐
    │ Menu request?│
    │ (menu/ajuda) │
    └──┬───────┬───┘
       ↓ Sim   ↓ Não
  ┌─────────┐ ↓
  │ Exibe   │ ↓
  │ Menu    │ ↓
  └─────────┘ ↓
              ↓
       ┌──────────────┐
       │ Começa com 1?│
       └──┬───────┬───┘
    Sim ↓       ↓ Não
        ↓       ↓
        ↓   ┌──────────────┐
        ↓   │ Começa com 2?│
        ↓   └──┬───────┬───┘
        ↓ Sim ↓       ↓ Não (assume 2)
        ↓     ↓       ↓
  ┌──────────────┐ ┌─────────────┐
  │  MODO 1:     │ │  MODO 2:    │
  │  Base Dados  │ │  LLM Livre  │
  │  +Consultores│ │  Sem busca  │
  └──────┬───────┘ └──────┬──────┘
         ↓                ↓
         └────────┬───────┘
                  ↓
         ┌────────────────┐
         │ Retorna resposta│
         │ ao usuário      │
         └────────────────┘
```

---

## 🧪 Casos de Teste

### Teste 1: Menu

**Input:** `menu`  
**Esperado:** Exibe menu formatado com opções 1 e 2

### Teste 2: Modo 1 Completo

**Input:** `1 Como abrir um MEI?`  
**Esperado:**

- Busca documentos
- Busca consultores
- Retorna resposta com fontes e consultores

### Teste 3: Modo 1 Incompleto

**Input:** `1`  
**Esperado:** Pede para completar a pergunta

### Teste 4: Modo 2 Explícito

**Input:** `2 Dicas de vendas`  
**Esperado:** Resposta do LLM sem buscar base

### Teste 5: Modo 2 Implícito

**Input:** `Como fazer marketing?`  
**Esperado:** Resposta do LLM (assume modo 2)

### Teste 6: Modo 2 Incompleto

**Input:** `2`  
**Esperado:** Pede para completar a pergunta

---

## 📚 Arquivos Modificados

- `src/assistant.py` - Implementação completa do sistema de menu
  - `_exibir_menu()` - Novo método
  - `processar_consulta()` - Refatorado para detectar modo
  - `_processar_consulta_base_dados()` - Novo método (modo 1)
  - `_processar_consulta_llm_livre()` - Novo método (modo 2)

---

## 🎓 Conclusão

O sistema de menu traz **controle explícito** para o usuário, permitindo que ele escolha conscientemente entre:

1. **Informações oficiais validadas + consultores** (Modo 1)
2. **Resposta rápida de IA geral** (Modo 2)

Isso melhora a experiência do usuário, reduz custos de processamento e torna o sistema mais transparente e eficiente.
