# 📝 Prompt Template: Validação de Ideia de Negócio

## 🎯 OBJETIVO

Validar uma ideia de negócio usando metodologia estruturada do Sebrae

## 📋 VARIÁVEIS

- **{{ideia_negocio}}**: Descrição da ideia de negócio
- **{{publico_alvo}}**: Público-alvo pretendido
- **{{regiao}}**: Região de atuação
- **{{investimento_inicial}}**: Investimento inicial estimado
- **{{experiencia_empreendedor}}**: Experiência prévia do empreendedor

## 🧠 PROMPT TEMPLATE

```
Você é um consultor especialista do Sebrae em validação de negócios. Valide a seguinte ideia de negócio: {{ideia_negocio}}.

Contexto:
- Público-alvo: {{publico_alvo}}
- Região: {{regiao}}
- Investimento inicial: {{investimento_inicial}}
- Experiência do empreendedor: {{experiencia_empreendedor}}

Com base na metodologia de validação do Sebrae, analise:

1. 🎯 **VALIDAÇÃO DE MERCADO**
   - Existe demanda real para {{ideia_negocio}}?
   - Tamanho do mercado na {{regiao}}
   - Tendências do setor
   - Sazonalidade do negócio

2. 👥 **VALIDAÇÃO DE PÚBLICO**
   - O {{publico_alvo}} realmente compraria?
   - Poder de compra do público
   - Comportamento de consumo
   - Canais de acesso ao público

3. 💰 **VIABILIDADE FINANCEIRA**
   - O {{investimento_inicial}} é adequado?
   - Projeção de receitas
   - Estrutura de custos
   - Ponto de equilíbrio estimado

4. 🏢 **VIABILIDADE OPERACIONAL**
   - Complexidade de implementação
   - Recursos necessários
   - Fornecedores disponíveis
   - Aspectos legais e regulatórios

5. 🏆 **VANTAGEM COMPETITIVA**
   - Diferenciais da ideia
   - Barreiras de entrada
   - Sustentabilidade da vantagem
   - Escalabilidade do negócio

6. 👨‍💼 **ADEQUAÇÃO AO PERFIL EMPREENDEDOR**
   - Compatibilidade com {{experiencia_empreendedor}}
   - Competências necessárias
   - Gap de conhecimento
   - Tempo de dedicação necessário

7. ⚠️ **RISCOS IDENTIFICADOS**
   - Principais riscos do negócio
   - Fatores críticos de sucesso
   - Planos de contingência

8. 📊 **NOTA FINAL E RECOMENDAÇÃO**
   - Nota de 1 a 10 para viabilidade
   - Recomendação: Seguir/Ajustar/Abandonar
   - Próximos passos sugeridos

9. 👥 **CONSULTORES ESPECIALIZADOS**
   - Busque consultores especialistas no setor
   - Incluir mentores e especialistas em validação

Base toda a análise nos materiais oficiais do Sebrae sobre validação de negócios e cite as fontes.
```

## 📝 EXEMPLO DE USO

### Input:

```json
{
  "ideia_negocio": "aplicativo de delivery de produtos orgânicos",
  "publico_alvo": "famílias preocupadas com alimentação saudável, classe A/B",
  "regiao": "Brasília - DF",
  "investimento_inicial": "R$ 80.000",
  "experiencia_empreendedor": "formação em TI, sem experiência em food service"
}
```

### Output Esperado:

```
💭 Análise: Validação de negócio - delivery de orgânicos

[Validação estruturada da ideia de negócio...]

📊 NOTA FINAL: 7,5/10
✅ RECOMENDAÇÃO: Seguir com ajustes no modelo

📚 Fontes consultadas:
1. Metodologia de Validação de Negócios.pdf
2. Estudo sobre Food Service Digital.pdf

👥 CONSULTORES ESPECIALIZADOS:
[Consultores em tecnologia e food service]
```
