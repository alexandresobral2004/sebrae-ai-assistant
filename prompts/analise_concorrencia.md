# 📝 Prompt Template: Análise de Concorrência

## 🎯 OBJETIVO

Analisar concorrência e posicionamento de mercado para um empreendimento

## 📋 VARIÁVEIS

- **{{setor}}**: Setor de atuação (ex: alimentação, varejo, serviços)
- **{{regiao}}**: Região/cidade para análise
- **{{porte_empresa}}**: Porte da empresa (micro, pequena, média)

## 🧠 PROMPT TEMPLATE

```
Você é um consultor especialista do Sebrae em análise competitiva. Faça uma análise completa da concorrência no setor {{setor}} na região {{regiao}} para uma empresa de porte {{porte_empresa}}.

Com base nos documentos oficiais do Sebrae, forneça:

1. 🏢 **MAPEAMENTO DOS CONCORRENTES**
   - Principais players do mercado
   - Participação de mercado estimada
   - Localização dos concorrentes

2. 💰 **ANÁLISE DE PREÇOS**
   - Faixa de preços praticada no mercado
   - Estratégias de precificação observadas
   - Oportunidades de posicionamento

3. 🎯 **POSICIONAMENTO COMPETITIVO**
   - Diferenciais dos principais concorrentes
   - Gaps identificados no mercado
   - Oportunidades de nicho

4. 📊 **ANÁLISE SWOT COMPETITIVA**
   - Forças dos concorrentes
   - Fraquezas identificadas
   - Oportunidades de entrada
   - Ameaças do setor

5. 📈 **ESTRATÉGIAS RECOMENDADAS**
   - Como se diferenciar no mercado
   - Propostas de valor únicas
   - Estratégias de entrada

6. 👥 **CONSULTORES ESPECIALIZADOS**
   - Busque consultores especialistas em análise competitiva
   - Inclua dados de contato completos

Baseie todas as análises nos documentos oficiais do Sebrae e cite as fontes utilizadas.
```

## 📝 EXEMPLO DE USO

### Input:

```json
{
  "setor": "alimentação saudável",
  "regiao": "São Paulo - Zona Sul",
  "porte_empresa": "micro empresa"
}
```

### Output Esperado:

```
💭 Análise: Mapeamento competitivo - setor alimentação saudável

[Análise detalhada da concorrência no setor...]

📚 Fontes consultadas:
1. Estudo Setorial - Alimentação Saudável.pdf
2. Guia de Análise Competitiva.pdf

👥 CONSULTORES ESPECIALIZADOS:
[Lista de consultores especializados]
```
