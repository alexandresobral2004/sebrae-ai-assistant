# 🚀 GUIA RÁPIDO: Executar Prompts a partir de Arquivos .md

## ⚡ **RESUMO EXECUTIVO**

O sistema permite criar e executar prompts estruturados usando arquivos Markdown (`.md`) com variáveis dinâmicas, oferecendo templates reutilizáveis e organizados para o Consultor IA Sebrae.

---

## 🎯 **O QUE VOCÊ PODE FAZER**

### ✅ **Funcionalidades Principais**

- Criar templates de prompts em arquivos `.md`
- Usar variáveis dinâmicas com `{{variavel}}`
- Executar prompts com valores personalizados
- Integrar com qualquer sistema de IA
- Organizar biblioteca de prompts reutilizáveis

### ✅ **Templates Incluídos**

- 📊 **Análise de Viabilidade**: Avaliar empreendimentos
- 🏢 **Análise de Concorrência**: Mapear competidores
- 📱 **Plano Marketing Digital**: Estratégias online
- 💡 **Validação de Ideias**: Metodologia estruturada

---

## ⚡ **EXECUÇÃO RÁPIDA**

### **1. 🚀 Método Mais Simples**

```bash
# Execute o exemplo
cd /Users/alexandrerocha/sebrae-ai-assistant
python3 exemplo_simples_prompts.py
```

### **2. 🧠 Código Direto**

```python
from exemplo_simples_prompts import processar_prompt_markdown

# Definir variáveis
variaveis = {
    "tipo_negocio": "cafeteria",
    "cidade": "São Paulo",
    "investimento": "R$ 30.000"
}

# Processar prompt
resultado = processar_prompt_markdown("prompts/exemplo_prompt.md", variaveis)

# Usar com ChatGPT, Claude, ou qualquer IA
print(resultado)
```

---

## 📁 **ESTRUTURA DOS ARQUIVOS**

### **Template Básico:**

```markdown
# 📝 Prompt Template: Nome do Prompt

## 🎯 OBJETIVO

Descrição do que faz

## 📋 VARIÁVEIS

- **{{variavel1}}**: Descrição
- **{{variavel2}}**: Descrição

## 🧠 PROMPT TEMPLATE
```

Seu prompt aqui com {{variavel1}} e {{variavel2}}. [Estrutura detalhada...]

```

```

### **Localização:**

```
prompts/
├── exemplo_prompt.md           # Análise geral
├── analise_concorrencia.md     # Concorrência
├── plano_marketing_digital.md  # Marketing
└── validacao_ideia_negocio.md  # Validação
```

---

## 🎯 **CASOS DE USO PRÁTICOS**

### **1. 📊 Análise de Viabilidade**

```python
variaveis = {
    "tipo_negocio": "padaria artesanal",
    "localização": "Campinas",
    "investimento": "R$ 50.000",
    "publico_alvo": "classe média local"
}
```

### **2. 🏢 Análise de Concorrência**

```python
variaveis = {
    "setor": "alimentação saudável",
    "regiao": "São Paulo",
    "porte_empresa": "micro empresa"
}
```

### **3. 📱 Marketing Digital**

```python
variaveis = {
    "empresa": "Loja Virtual",
    "setor": "e-commerce",
    "publico_alvo": "jovens 20-35 anos",
    "orcamento": "R$ 3.000/mês",
    "objetivos": "aumentar vendas online"
}
```

---

## 🔧 **INTEGRAÇÃO COM IAs**

### **OpenAI ChatGPT:**

```python
import openai
prompt = processar_prompt_markdown("prompt.md", variaveis)
resposta = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

### **Assistente Sebrae (com API configurada):**

```python
from src.assistant import AssistenteSebrae
assistente = AssistenteSebrae()
resposta = assistente.processar_consulta(prompt)
```

### **Qualquer Sistema de IA:**

```python
# O prompt processado é uma string normal
# Use com Claude, Gemini, modelos locais, etc.
ai_response = seu_sistema_ia.gerar(prompt)
```

---

## 📚 **EXEMPLOS DE RESULTADOS**

### **Input:**

```python
variaveis = {"tipo_negocio": "lanchonete", "cidade": "Rio de Janeiro"}
```

### **Output Gerado:**

```
Você é um consultor especialista do Sebrae. Analise a viabilidade
de abrir um lanchonete na cidade de Rio de Janeiro...

1. 📊 ANÁLISE DE VIABILIDADE
   - Pontos fortes do mercado
   - Desafios identificados
   - Potencial de retorno

[Estrutura completa do prompt...]
```

---

## 🛠️ **PERSONALIZAÇÃO AVANÇADA**

### **Criar Novo Template:**

1. **Copie** um arquivo existente: `cp prompts/exemplo_prompt.md prompts/meu_prompt.md`
2. **Edite** as seções: OBJETIVO, VARIÁVEIS, PROMPT TEMPLATE
3. **Use** variáveis: `{{minha_variavel}}`
4. **Execute**: `processar_prompt_markdown("prompts/meu_prompt.md", variaveis)`

### **Sistema Completo (Opcional):**

```python
from src.sistema_prompts import GerenciadorPrompts

gerenciador = GerenciadorPrompts("prompts")
prompts = gerenciador.listar_prompts()
resultado = gerenciador.executar_prompt("nome_prompt", variaveis)
```

---

## 🎉 **BENEFÍCIOS**

### ✅ **Para Consultores:**

- Templates padronizados para análises
- Processo estruturado e replicável
- Economia de tempo na criação de prompts

### ✅ **Para Desenvolvedores:**

- Separação entre lógica e conteúdo
- Versionamento fácil dos prompts
- Reutilização em diferentes projetos

### ✅ **Para Empresas:**

- Metodologia consistente
- Qualidade padronizada
- Escalabilidade de processos

---

## 🚀 **PRÓXIMOS PASSOS**

1. **Execute** o exemplo: `python3 exemplo_simples_prompts.py`
2. **Explore** os templates na pasta `prompts/`
3. **Crie** seus próprios templates
4. **Integre** com seu sistema de IA preferido
5. **Documente** na pasta `docs/prompts_markdown.md`

---

<div align="center">

**🎯 Sistema de Prompts Markdown - Consultor Sebrae IA**  
_Transformando templates em inteligência aplicada_

**📁 Arquivos Relacionados:**

- `prompts/` - Templates prontos
- `exemplo_simples_prompts.py` - Código de execução
- `docs/prompts_markdown.md` - Documentação completa
- `src/sistema_prompts.py` - Sistema avançado

</div>
