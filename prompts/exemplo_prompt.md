# 📝 Prompt Template: Análise de Empreendimento

## 🎯 OBJETIVO

Analisar viabilidade de um empreendimento com base nos documentos Sebrae

## 📋 VARIÁVEIS

- **{{tipo_negocio}}**: Tipo de negócio (ex: restaurante, loja, serviços)
- **{{localização}}**: Cidade/região do empreendimento
- **{{investimento}}**: Valor aproximado de investimento
- **{{publico_alvo}}**: Público-alvo principal

## 🧠 PROMPT TEMPLATE

```
Você é um consultor especialista do Sebrae. Analise a viabilidade de abrir um {{tipo_negocio}} na cidade de {{localização}} com investimento de aproximadamente {{investimento}}, focando no público {{publico_alvo}}.

Com base nos documentos oficiais do Sebrae, forneça:

1. 📊 **ANÁLISE DE VIABILIDADE**
   - Pontos fortes do mercado
   - Desafios identificados
   - Potencial de retorno

2. 📋 **REQUISITOS LEGAIS**
   - Documentação necessária
   - Licenças e autorizações
   - Aspectos tributários

3. 💰 **PLANEJAMENTO FINANCEIRO**
   - Estrutura de custos
   - Projeção de receitas
   - Capital de giro necessário

4. 📈 **ESTRATÉGIAS DE MARKETING**
   - Posicionamento no mercado
   - Canais de divulgação
   - Diferenciação competitiva

5. 👥 **CONSULTORES ESPECIALIZADOS**
   - Busque consultores especializados na área
   - Inclua dados de contato completos

Baseie todas as recomendações nos documentos oficiais do Sebrae e cite as fontes utilizadas.
```

## 📝 EXEMPLO DE USO

### Input:

```json
{
  "tipo_negocio": "padaria artesanal",
  "localização": "São Paulo",
  "investimento": "R$ 50.000",
  "publico_alvo": "classe média local"
}
```

### Output Esperado:

```
💭 Análise: Empreendimento alimentício - padaria artesanal

Com base nos documentos oficiais do Sebrae sobre negócios alimentícios...

[Resposta estruturada seguindo o template]
```
