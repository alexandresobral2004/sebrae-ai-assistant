# 📝 Prompt Template: Frontend Modernizado Sebrae

## 🎯 OBJETIVO

Desenvolver frontend moderno seguindo design system do Sebrae com busca prioritária local e fallback inteligente.

## 📋 VARIÁVEIS

- **{{tipo_interface}}**: Tipo de interface (dashboard, chat, upload, etc.)
- **{{funcionalidades}}**: Funcionalidades específicas a implementar
- **{{tema_visual}}**: Tema visual (cores Sebrae, moderno, responsivo)
- **{{prioridade_busca}}**: Sistema de busca (local_primeiro, fallback_internet)

## 🧠 PROMPT TEMPLATE

```
Você é um especialista em UI/UX e desenvolvimento frontend para o Sebrae. Crie uma interface {{tipo_interface}} moderna implementando {{funcionalidades}} com {{tema_visual}}.

REQUISITOS CRÍTICOS:
- Busca SEMPRE prioritária na base local ({{prioridade_busca}})
- Design system oficial do Sebrae:
  * Cores: #003366 (azul principal), #0066CC (azul secundário), #FF6B35 (laranja)
  * Tipografia: Roboto (fonte oficial)
  * Layout: Cards modernos com sombras suaves
  * Gradientes sutis e bordas arredondadas

FUNCIONALIDADES OBRIGATÓRIAS:

1. 🏠 **PÁGINA INICIAL**
   - Header com logo e identidade Sebrae
   - Cards interativos para escolha de funcionalidade
   - Métricas do sistema em tempo real
   - Navegação intuitiva

2. � **SISTEMA DE BUSCA PRIORITÁRIA**
   - PRIMEIRA busca na base local (CRÍTICO)
   - Avaliação de confiança (threshold 0.7)
   - Fallback para internet APENAS se necessário
   - Indicação transparente da fonte utilizada

3. 🤖 **INTERFACE DE CHAT**
   - Design moderno com mensagens em cards
   - Histórico persistente de conversas
   - Status de carregamento visual
   - Input com bordas e focus states

4. � **GERENCIAMENTO DE DOCUMENTOS**
   - Upload com drag & drop
   - Lista organizada de arquivos
   - Processamento automático
   - Métricas por tipo de arquivo

5. � **DASHBOARD**
   - Métricas em tempo real
   - Status do sistema
   - Contadores de uso
   - Indicadores visuais

IMPLEMENTAÇÃO TÉCNICA:
- Streamlit como framework base
- CSS customizado para design Sebrae
- Componentes reutilizáveis
- Responsividade mobile-first
- Performance otimizada

Desenvolva o código completo seguindo essas especificações.
```

## 📝 EXEMPLO DE USO

### Input:

```json
{
  "tipo_interface": "dashboard interativo",
  "funcionalidades": "chat IA, upload documentos, métricas tempo real",
  "tema_visual": "design system Sebrae oficial",
  "prioridade_busca": "base_local_primeiro_fallback_internet"
}
```

### Output Esperado:

```python
# Frontend modernizado com:
# - Design system Sebrae (cores, tipografia, layout)
# - Página inicial com cards de funcionalidades
# - Sistema de busca prioritária local CRÍTICO
# - Interface de chat modernizada
# - Upload de documentos intuitivo
# - Dashboard com métricas em tempo real
# - Navegação fluida entre páginas
# - Responsividade completa

# Arquivo: app_moderno.py
# Características: 26KB+ de código otimizado
```
