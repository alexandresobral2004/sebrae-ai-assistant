# 📝 Prompt Template: Plano de Marketing Digital

## 🎯 OBJETIVO

Criar um plano de marketing digital completo baseado nas melhores práticas do Sebrae

## 📋 VARIÁVEIS

- **{{empresa}}**: Nome da empresa
- **{{setor}}**: Setor de atuação
- **{{publico_alvo}}**: Descrição do público-alvo
- **{{orcamento}}**: Orçamento disponível para marketing
- **{{objetivos}}**: Objetivos de marketing (vendas, brand awareness, etc.)

## 🧠 PROMPT TEMPLATE

```
Você é um especialista em marketing digital do Sebrae. Crie um plano de marketing digital completo para {{empresa}}, uma empresa do setor {{setor}}, focando no público {{publico_alvo}} com orçamento de {{orcamento}} para alcançar os objetivos: {{objetivos}}.

Com base nos documentos oficiais do Sebrae sobre marketing digital, estruture:

1. 📊 **ANÁLISE SITUACIONAL**
   - Análise do mercado digital no setor
   - Posicionamento atual da empresa
   - Oportunidades digitais identificadas

2. 🎯 **DEFINIÇÃO DE PERSONAS**
   - Perfil detalhado do público {{publico_alvo}}
   - Comportamento digital das personas
   - Jornada do cliente digital

3. 📱 **ESTRATÉGIA DE PRESENÇA DIGITAL**
   - Website/e-commerce recomendado
   - Redes sociais prioritárias
   - Outros canais digitais relevantes

4. 📝 **ESTRATÉGIA DE CONTEÚDO**
   - Tipos de conteúdo para cada canal
   - Calendário editorial sugerido
   - Temas e formatos recomendados

5. 💰 **DISTRIBUIÇÃO DO ORÇAMENTO {{orcamento}}**
   - Alocação por canal/estratégia
   - Investimento em mídia paga
   - Custos com ferramentas e recursos

6. 📈 **MÉTRICAS E KPIs**
   - Indicadores de performance
   - Metas mensais e trimestrais
   - Ferramentas de monitoramento

7. 📅 **CRONOGRAMA DE IMPLEMENTAÇÃO**
   - Fases de implementação (90 dias)
   - Marcos importantes
   - Responsabilidades e prazos

8. 👥 **CONSULTORES ESPECIALIZADOS**
   - Busque especialistas em marketing digital
   - Inclua consultores em redes sociais e e-commerce

Base todas as recomendações nos materiais oficiais do Sebrae sobre marketing digital e cite as fontes.
```

## 📝 EXEMPLO DE USO

### Input:

```json
{
  "empresa": "Doces da Vovó",
  "setor": "alimentação artesanal",
  "publico_alvo": "mulheres de 25-45 anos, classe B/C",
  "orcamento": "R$ 2.000/mês",
  "objetivos": "aumentar vendas online em 30% e fortalecer marca"
}
```

### Output Esperado:

```
💭 Análise: Marketing Digital - setor alimentação artesanal

[Plano completo de marketing digital estruturado...]

📚 Fontes consultadas:
1. Guia de Marketing Digital para PMEs.pdf
2. E-commerce para Pequenos Negócios.pdf

👥 CONSULTORES ESPECIALIZADOS:
[Consultores em marketing digital e redes sociais]
```
