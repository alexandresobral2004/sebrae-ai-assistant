# 🤖 Consultor Sebrae IA

Um assistente virtual especializado em fornecer informações sobre produtos, serviços e consultorias de negócios do Sebrae, com interface web profissional.

## Características

### 🎭 Identidade

- Nome: "Consultor Sebrae IA"
- Missão: Fornecer informações precisas e úteis sobre produtos, serviços e consultorias de negócios do Sebrae

### 🗣️ Tom e Estilo

- Profissional e Solícito
- Didático
- Focado no Sebrae

### 🧠 Sistema de Processamento de Informação

O assistente opera com um sistema de conhecimento híbrido, seguindo uma ordem estrita de prioridade:

1. **Busca na Base de Conhecimento Local (RAG)**

   - Fonte primária e mais confiável
   - Utiliza documentos internos do Sebrae
   - Cita fontes usando o formato: `(Fonte: [nome_do_arquivo.pdf])`

2. **Busca na Internet (Fallback)**

   - Utilizada apenas quando a informação não está na base local
   - Busca informações gerais sobre o Sebrae e conceitos de negócios

3. **Regra de Recusa**
   - Caso a informação não seja encontrada em nenhuma fonte, o assistente informa claramente
   - Evita adivinhações ou informações imprecisas

## Estrutura do Projeto

```
sebrae-ai-assistant/
├── src/
│   └── assistant.py      # Implementação principal do assistente
├── README.md            # Documentação do projeto
└── requirements.txt     # Dependências do projeto
```

## Desenvolvimento

O projeto está estruturado para implementar um assistente virtual que:

- Mantém uma identidade profissional e consistente
- Processa informações de forma hierárquica e confiável
- Fornece respostas claras e bem fundamentadas
- Cita fontes quando apropriado
