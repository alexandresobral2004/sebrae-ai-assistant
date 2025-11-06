# Estrutura de Resposta do Assistente Sebrae

## 📋 Ordem das Seções na Resposta

O assistente foi configurado para seguir **sempre** a seguinte sequência ao responder perguntas:

### 1️⃣ APRESENTAÇÃO E MISSÃO

- O assistente se apresenta como "Consultor IA Sebrae"
- Reforça brevemente sua missão de ajudar analistas Sebrae
- Tom profissional, solícito e didático

**Exemplo:**

```
Olá! Sou o Consultor IA Sebrae, especialista em produtos e serviços do Sebrae.
Minha missão é fornecer respostas precisas e práticas para ajudar você a entender
nossas soluções, fichas técnicas (FT) e manuais de operacionalização (MOA).
```

---

### 2️⃣ RESPOSTA À PERGUNTA

- Responde objetivamente à pergunta do usuário
- Utiliza informações dos documentos oficiais Sebrae
- Cita especificamente Fichas Técnicas (FTs) e MOAs quando aplicável
- Linguagem clara, didática e completa
- Cria referências aos arquivos consultados dentro da resposta

**Características:**

- ✅ Baseada em documentos oficiais
- ✅ Objetiva e prática
- ✅ Menciona FTs e MOAs relevantes
- ❌ NÃO lista consultores nesta seção
- ❌ NÃO lista documentos nesta seção

---

### 3️⃣ CONSULTORES ESPECIALIZADOS NO TEMA

**IMPORTANTE:** Esta seção aparece **SOMENTE** se houver consultores relacionados ao tema buscado.

- Lista **apenas** consultores especializados no tema da consulta
- Não exibe consultores sem vínculo com o assunto
- Fornece dados de contato completos
- Facilita a contratação de consultores

**Formato:**

```markdown
---
## 👥 CONSULTORES ESPECIALIZADOS NO TEMA

Com base no tema da sua consulta, identifiquei os seguintes consultores especializados:

**Consultor 1:**
Nome: João Silva
Especialidade: Marketing Digital
Área: Competitividade nos Negócios
Email: joao.silva@exemplo.com
Telefone: (11) 98765-4321

**Consultor 2:**
Nome: Maria Santos
Especialidade: Gestão Empresarial
...

💼 _Para contratar estes consultores, entre em contato diretamente através dos dados informados acima._
```

**Regras:**

- ✅ Somente consultores relacionados ao tema
- ✅ Máximo de 3 consultores mais relevantes
- ❌ Não exibir se não houver consultores relacionados
- ❌ Não incluir consultores genéricos

---

### 4️⃣ DOCUMENTOS CONSULTADOS E LINKS

Lista os documentos oficiais do Sebrae que foram consultados para gerar a resposta.

**Formato:**

```markdown
---

## 📚 DOCUMENTOS CONSULTADOS

As informações fornecidas foram extraídas dos seguintes documentos oficiais do Sebrae:

1. **FT_Marketing_Digital_2024.pdf** 📥 [Clique aqui para baixar](/documentos/FT_Marketing_Digital_2024.pdf)

2. **MOA_Gestao_Empresarial.docx** 📥 [Clique aqui para baixar](/documentos/MOA_Gestao_Empresarial.docx)

💡 _Estes documentos contêm informações detalhadas sobre Fichas Técnicas (FT) e Manuais de Operacionalização (MOA)._
```

**Características:**

- ✅ Lista todos os documentos utilizados
- ✅ Fornece link para download de cada documento
- ✅ Ordenada alfabeticamente
- ✅ Diferencia FTs de MOAs

---

## 🎯 Exemplo de Resposta Completa

```markdown
Olá! Sou o Consultor IA Sebrae, seu especialista em produtos e serviços do Sebrae. Minha missão é fornecer respostas precisas e práticas para ajudar você a encontrar as melhores soluções para seu negócio.

Com base nos documentos oficiais do Sebrae, encontrei as seguintes informações sobre marketing digital para pequenas empresas:

O Sebrae oferece a Ficha Técnica (FT) de Marketing Digital, que abrange estratégias completas para presença online de micro e pequenas empresas. Este produto inclui:

- Planejamento de presença digital
- Gestão de redes sociais
- Criação de conteúdo
- Análise de métricas

O Manual de Operacionalização (MOA) detalha como implementar cada etapa, incluindo ferramentas recomendadas e cronograma de implementação.

---

## 👥 CONSULTORES ESPECIALIZADOS NO TEMA

Com base no tema da sua consulta, identifiquei os seguintes consultores especializados:

**Consultor 1:** Nome: Carlos Eduardo Mendes Especialidade: Marketing Digital e E-commerce Área: Competitividade nos Negócios Email: carlos.mendes@consultoria.com Telefone: (11) 98765-4321 LinkedIn: linkedin.com/in/carloseduardomendes

💼 _Para contratar estes consultores, entre em contato diretamente através dos dados informados acima._

---

## 📚 DOCUMENTOS CONSULTADOS

As informações fornecidas foram extraídas dos seguintes documentos oficiais do Sebrae:

1. **FT_Marketing_Digital_PME_2024.pdf** 📥 [Clique aqui para baixar](/documentos/FT_Marketing_Digital_PME_2024.pdf)

2. **MOA_Marketing_Digital.docx** 📥 [Clique aqui para baixar](/documentos/MOA_Marketing_Digital.docx)

💡 _Estes documentos contêm informações detalhadas sobre Fichas Técnicas (FT) e Manuais de Operacionalização (MOA)._

---

✅ _Resposta baseada em documentos oficiais Sebrae_

✨ **Precisa de mais ajuda?** Posso fornecer informações adicionais sobre produtos e serviços do Sebrae.
```

---

## 🔧 Implementação Técnica

### Arquivo: `src/assistant.py`

1. **Prompt do Sistema** (`_processar_resposta_base_interna`)

   - Define a estrutura obrigatória
   - Instrui o LLM a focar apenas nas seções 1 e 2
   - Seções 3 e 4 são adicionadas automaticamente

2. **Formatação de Resposta** (`formatar_resposta`)

   - Recebe a resposta do LLM (seções 1 e 2)
   - Adiciona seção de consultores (se houver)
   - Adiciona seção de documentos (se houver)
   - Adiciona rodapé com transparência

3. **Busca de Consultores** (`_buscar_consultores_relacionados`)
   - Busca consultores especializados no tema
   - Filtra apenas consultores relevantes
   - Limita a 3 consultores mais relevantes

---

## ✅ Checklist de Qualidade

Ao verificar uma resposta, confirme que:

- [ ] Inicia com apresentação do Consultor IA Sebrae
- [ ] Responde objetivamente à pergunta
- [ ] Menciona FTs e MOAs quando aplicável
- [ ] Consultores listados são **apenas** os relacionados ao tema
- [ ] Documentos consultados estão listados com links
- [ ] Segue a ordem: Apresentação → Resposta → Consultores → Documentos
- [ ] Não há consultores sem vínculo com o tema
- [ ] Links de download estão corretos
- [ ] Tom profissional e solícito

---

## 📝 Notas de Desenvolvimento

**Data de Implementação:** 5 de novembro de 2025

**Versão:** 2.0

**Mudanças principais:**

- Reorganização da estrutura de resposta
- Separação clara entre conteúdo e metadados
- Filtro de consultores por relevância
- Links para download de documentos

**Próximos passos:**

- Implementar sistema de download real de documentos
- Adicionar cache de consultores
- Melhorar algoritmo de relevância de consultores
