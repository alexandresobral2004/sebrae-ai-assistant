# 📝 Como Executar Prompts a partir de Arquivos .md

## 🎯 **VISÃO GERAL**

O sistema permite criar e executar prompts estruturados usando arquivos Markdown (`.md`), oferecendo uma forma organizada e reutilizável de trabalhar com templates de prompts.

---

## 🏗️ **ESTRUTURA DE UM ARQUIVO DE PROMPT**

### **Template Básico:**

```markdown
# 📝 Prompt Template: [Nome do Prompt]

## 🎯 OBJETIVO

Descrição do que o prompt faz

## 📋 VARIÁVEIS

- **{{variavel1}}**: Descrição da variável 1
- **{{variavel2}}**: Descrição da variável 2

## 🧠 PROMPT TEMPLATE
```

Seu prompt aqui com {{variavel1}} e {{variavel2}}.

[Estrutura do prompt...]

````

## 📝 EXEMPLO DE USO

### Input:
```json
{
  "variavel1": "valor1",
  "variavel2": "valor2"
}
````

````

---

## 🛠️ **MÉTODOS DE EXECUÇÃO**

### **1. 🚀 Método Simples (Sem Dependências)**

```python
def processar_prompt_markdown(arquivo_md: str, variaveis: dict) -> str:
    # Função já implementada em exemplo_simples_prompts.py
    pass

# Uso:
prompt_final = processar_prompt_markdown(
    "prompts/meu_prompt.md",
    {"variavel1": "valor1"}
)
````

### **2. 🧠 Método Avançado (Com GerenciadorPrompts)**

```python
from src.sistema_prompts import GerenciadorPrompts

# Inicializar
gerenciador = GerenciadorPrompts("prompts")

# Executar
prompt_final = gerenciador.executar_prompt(
    "nome_prompt",
    {"variavel1": "valor1"}
)
```

### **3. 🤖 Método Integrado (Com Assistente Sebrae)**

```python
from src.sistema_prompts import executar_prompt_com_assistente
from src.assistant import AssistenteSebrae

assistente = AssistenteSebrae()
gerenciador = GerenciadorPrompts("prompts")

resposta = executar_prompt_com_assistente(
    gerenciador, assistente, "nome_prompt", variaveis
)
```

---

## 📁 **EXEMPLOS PRÁTICOS**

### **Exemplo 1: Análise de Viabilidade**

**Arquivo:** `prompts/analise_viabilidade.md`

```markdown
# 📝 Prompt Template: Análise de Viabilidade

## 🎯 OBJETIVO

Analisar viabilidade de um empreendimento

## 📋 VARIÁVEIS

- **{{tipo_negocio}}**: Tipo de negócio
- **{{cidade}}**: Localização
- **{{investimento}}**: Valor do investimento

## 🧠 PROMPT TEMPLATE
```

Analise a viabilidade de abrir um {{tipo_negocio}} em {{cidade}} com investimento de {{investimento}}.

Forneça:

1. Análise de mercado
2. Projeção financeira
3. Riscos e oportunidades
4. Recomendações

```

```

**Execução:**

```python
valores = {
    "tipo_negocio": "padaria",
    "cidade": "São Paulo",
    "investimento": "R$ 50.000"
}

prompt = processar_prompt_markdown("prompts/analise_viabilidade.md", valores)
```

### **Exemplo 2: Plano de Marketing**

**Arquivo:** `prompts/plano_marketing.md`

```markdown
# 📝 Prompt Template: Plano de Marketing

## 🧠 PROMPT TEMPLATE
```

Crie um plano de marketing para {{empresa}} no setor {{setor}}, focando no público {{publico_alvo}} com orçamento de {{orcamento}}.

Inclua:

- Análise de mercado
- Estratégias de posicionamento
- Mix de marketing (4Ps)
- Cronograma de ações
- Métricas de sucesso

```

```

---

## 🔧 **FUNCIONALIDADES AVANÇADAS**

### **1. 📊 Listagem de Prompts Disponíveis**

```python
gerenciador = GerenciadorPrompts("prompts")
prompts = gerenciador.listar_prompts()
print(f"Prompts disponíveis: {prompts}")
```

### **2. 🔍 Verificação de Variáveis**

```python
variaveis = gerenciador.obter_variaveis_prompt("nome_prompt")
print(f"Variáveis necessárias: {variaveis}")
```

### **3. ✨ Criação Automática de Templates**

```python
gerenciador.criar_prompt_template(
    nome="novo_prompt",
    objetivo="Objetivo do prompt",
    variaveis=["var1", "var2"],
    template="Template com {{var1}} e {{var2}}"
)
```

---

## 📚 **TEMPLATES PRONTOS**

### **1. Análise de Concorrência**

```markdown
## 🧠 PROMPT TEMPLATE
```

Faça uma análise da concorrência no setor {{setor}} em {{regiao}}.

Analise:

1. Principais concorrentes
2. Posicionamento de mercado
3. Preços praticados
4. Diferenciais competitivos
5. Oportunidades de mercado

Foque em empresas de porte {{porte_empresa}}.

```

```

### **2. Validação de Ideia de Negócio**

```markdown
## 🧠 PROMPT TEMPLATE
```

Valide a ideia de negócio: {{ideia_negocio}}.

Para o público {{publico_alvo}} na região {{regiao}}.

Avalie:

1. Viabilidade técnica
2. Viabilidade econômica
3. Aceitação do mercado
4. Recursos necessários
5. Cronograma de implementação

Dê uma nota de 1-10 e justifique.

```

```

---

## 🎯 **CASOS DE USO RECOMENDADOS**

### **📈 Para Consultoria:**

- Templates de análise setorial
- Modelos de plano de negócios
- Estruturas de diagnóstico empresarial

### **🎓 Para Educação:**

- Exercícios padronizados
- Estudos de caso estruturados
- Avaliações sistemáticas

### **🏢 Para Empresas:**

- Análises de projetos
- Relatórios executivos
- Planejamentos estratégicos

---

## ⚡ **DICAS DE BOAS PRÁTICAS**

### **1. 📝 Organização de Arquivos**

```
prompts/
├── analise/
│   ├── viabilidade.md
│   ├── concorrencia.md
│   └── mercado.md
├── planejamento/
│   ├── negocio.md
│   ├── marketing.md
│   └── financeiro.md
└── consultoria/
    ├── diagnostico.md
    └── recomendacoes.md
```

### **2. 🎯 Nomenclatura de Variáveis**

- Use nomes descritivos: `{{tipo_negocio}}` ✅
- Evite nomes genéricos: `{{var1}}` ❌
- Seja consistente: sempre `{{cidade}}`, não `{{local}}`

### **3. 📋 Estruturação de Templates**

- Inclua instruções claras
- Divida em seções numeradas
- Use emojis para organização visual
- Especifique o formato de resposta esperado

### **4. 🧪 Versionamento**

- `prompt_v1.md`, `prompt_v2.md`
- Ou use pastas: `v1/`, `v2/`
- Documente mudanças no próprio arquivo

---

## 🚀 **EXECUÇÃO RÁPIDA**

### **Comando de Linha**

```bash
# Executar exemplo simples
python3 exemplo_simples_prompts.py

# Executar com assistente (requer API configurada)
python3 exemplo_prompts.py
```

### **Código Mínimo**

```python
from exemplo_simples_prompts import processar_prompt_markdown

# Definir variáveis
variaveis = {"tipo_negocio": "restaurante", "cidade": "Rio de Janeiro"}

# Processar prompt
resultado = processar_prompt_markdown("prompts/meu_prompt.md", variaveis)

# Usar resultado com qualquer sistema de IA
print(resultado)
```

---

## 🔮 **INTEGRAÇÕES POSSÍVEIS**

### **1. OpenAI GPT**

```python
import openai
prompt = processar_prompt_markdown("prompt.md", variaveis)
resposta = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

### **2. Anthropic Claude**

```python
import anthropic
prompt = processar_prompt_markdown("prompt.md", variaveis)
# Usar com Claude API
```

### **3. Modelos Locais**

```python
# Ollama, LM Studio, etc.
prompt = processar_prompt_markdown("prompt.md", variaveis)
# Usar com modelo local
```

---

## 🎉 **CONCLUSÃO**

O sistema de prompts com arquivos `.md` oferece:

- ✅ **Reutilização**: Templates padronizados
- ✅ **Organização**: Estrutura clara e versionável
- ✅ **Flexibilidade**: Variáveis dinâmicas
- ✅ **Integração**: Compatible com qualquer sistema de IA
- ✅ **Manutenção**: Fácil edição e atualização

**Use para criar prompts profissionais, organizados e reutilizáveis no seu projeto Sebrae AI Assistant!** 🚀
