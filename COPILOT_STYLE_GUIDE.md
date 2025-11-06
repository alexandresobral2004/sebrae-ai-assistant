# 🎨 Guia de Estilo Microsoft Copilot - Sebrae AI Assistant

## 📋 Visão Geral

Interface redesenhada seguindo os padrões visuais do **Microsoft Copilot**, mantendo a identidade visual do Sebrae.

---

## 🎯 Características Principais

### 1. Design System

```css
/* Cores principais */
--copilot-primary: #0f6cbd; /* Azul Copilot */
--copilot-accent: #8b5cf6; /* Roxo acento */
--sebrae-blue: #006ec7; /* Azul Sebrae */
--sebrae-orange: #ff6b35; /* Laranja Sebrae */
```

### 2. Tipografia

- **Fonte Principal:** Segoe UI (Windows) / Inter (Fallback)
- **Pesos:** 400 (normal), 500 (medium), 600 (semibold), 700 (bold)
- **Tamanhos:** Sistema escalável de 0.75rem a 2rem

### 3. Espaçamento

Sistema baseado em múltiplos de 4px:

- `--space-xs`: 4px
- `--space-sm`: 8px
- `--space-md`: 16px
- `--space-lg`: 24px
- `--space-xl`: 32px
- `--space-2xl`: 48px

### 4. Bordas e Sombras

**Bordas arredondadas:**

- Pequeno: 4px
- Médio: 8px
- Grande: 12px
- Extra grande: 16px

**Sombras sutis:**

- XS: `0 1px 2px rgba(0,0,0,0.04)`
- SM: `0 2px 4px rgba(0,0,0,0.06)`
- MD: `0 4px 8px rgba(0,0,0,0.08)`
- LG: `0 8px 16px rgba(0,0,0,0.1)`

---

## 🎨 Componentes Principais

### Header

```css
.header {
  background: white;
  border-bottom: 1px solid #e1e1e1;
  position: sticky;
  top: 0;
  backdrop-filter: blur(10px);
}
```

**Características:**

- Fundo branco
- Borda inferior sutil
- Sticky no topo
- Efeito blur no background

### Chat Container

```css
.chat-container {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
}
```

**Layout:**

- Centralizado na página
- Largura máxima de 900px
- Cantos arredondados
- Sombra suave

### Mensagens

#### Mensagem do Usuário

```css
.message-user .message-body {
  background: linear-gradient(135deg, #006ec7, #0f6cbd);
  color: white;
  border-radius: 12px 12px 4px 12px;
}
```

#### Mensagem do Assistente

```css
.message-assistant .message-body {
  background: #f5f5f5;
  border: 1px solid #e1e1e1;
  border-radius: 12px 12px 12px 4px;
}
```

### Input de Chat

```css
.chat-input {
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  padding: 16px;
  transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-input:focus {
  border-color: #0f6cbd;
  box-shadow: 0 0 0 3px rgba(15, 108, 189, 0.1);
}
```

**Estados:**

- Normal: Borda cinza clara
- Focus: Borda azul + sombra sutil
- Hover: Transição suave

### Botões

#### Botão Primário

```css
.btn-primary {
  background: linear-gradient(135deg, #006ec7, #0f6cbd);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}
```

#### Botão Outline

```css
.btn-outline {
  background: transparent;
  border: 1px solid #e1e1e1;
  color: #242424;
}
```

#### Botão Enviar

```css
.btn-send {
  background: linear-gradient(135deg, #8b5cf6, #0f6cbd);
  color: white;
  font-weight: 600;
}
```

### Cards

```css
.feature-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e1e1e1;
  transition: all 250ms;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  border-color: #0f6cbd;
}
```

**Interação:**

- Hover: Eleva 4px + aumenta sombra
- Borda muda de cor no hover
- Transição suave de 250ms

---

## 🎭 Animações

### Mensagens

```css
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message {
  animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Loading Spinner

```css
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-spinner {
  animation: spin 0.8s linear infinite;
}
```

### Status Indicator

```css
@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.status-dot {
  animation: pulse 2s ease-in-out infinite;
}
```

---

## 📱 Responsividade

### Breakpoints

```css
/* Mobile */
@media (max-width: 768px) {
  .chat-container {
    height: calc(100vh - 250px);
    border-radius: 0;
  }

  .features-section {
    grid-template-columns: 1fr;
  }
}
```

### Ajustes Mobile

- Chat ocupa altura total
- Cards empilham verticalmente
- Input e botão em coluna
- Header simplificado

---

## 🎨 Paleta de Cores Completa

### Cores Principais

```css
Copilot Blue:    #0F6CBD  /* Primário */
Copilot Accent:  #8B5CF6  /* Destaques */
Sebrae Blue:     #006EC7  /* Identidade */
Sebrae Orange:   #FF6B35  /* Secundário */
```

### Cores de Estado

```css
Success:  #107C10  /* Verde */
Warning:  #F7630C  /* Laranja */
Error:    #D13438  /* Vermelho */
```

### Cores Neutras

```css
Surface Primary:    #FFFFFF  /* Fundo cards */
Surface Secondary:  #F5F5F5  /* Fundo páginas */
Surface Tertiary:   #E8E8E8  /* Fundo elementos */
Border:             #E1E1E1  /* Bordas */
Divider:            #EDEBE9  /* Separadores */
```

### Cores de Texto

```css
Text Primary:    #242424  /* Texto principal */
Text Secondary:  #605E5C  /* Texto secundário */
Text Tertiary:   #8A8886  /* Texto terciário */
Text Inverse:    #FFFFFF  /* Texto em fundos escuros */
```

---

## 🔧 Customização

### Alterar Cor Primária

```css
:root {
  --copilot-primary: #0f6cbd; /* Altere aqui */
  --copilot-primary-hover: #115ea3;
}
```

### Alterar Espaçamentos

```css
:root {
  --space-md: 16px; /* Padrão */
  --space-md: 20px; /* Aumentar */
}
```

### Alterar Fonte

```css
:root {
  --font-family: "Inter", sans-serif; /* Padrão */
  --font-family: "Roboto", sans-serif; /* Alternativa */
}
```

### Alterar Bordas

```css
:root {
  --radius-md: 8px; /* Padrão */
  --radius-md: 12px; /* Mais arredondado */
  --radius-md: 4px; /* Mais reto */
}
```

---

## 📊 Hierarquia Visual

### Níveis de Importância

```
1. Botão Primário (Gradiente azul)
   ↓
2. Texto em destaque (Azul Copilot)
   ↓
3. Texto normal (Cinza escuro)
   ↓
4. Texto secundário (Cinza médio)
   ↓
5. Texto terciário (Cinza claro)
```

### Elevação (Z-index)

```css
Tooltip:         1070
Popover:         1060
Modal:           1050
Modal Backdrop:  1040
Fixed:           1030
Sticky:          1020
Dropdown:        1000
```

---

## 🎯 Checklist de Qualidade

Ao criar novos componentes, verifique:

- [ ] Usa variáveis CSS (não valores hardcoded)
- [ ] Tem estados hover/focus/active
- [ ] É responsivo (mobile-first)
- [ ] Tem transições suaves (250ms)
- [ ] Usa sombras sutis
- [ ] Bordas arredondadas apropriadas
- [ ] Cores acessíveis (contraste WCAG AA)
- [ ] Tipografia escalável (rem/em)

---

## 💡 Dicas de UX

### 1. **Feedback Visual**

- Sempre mostre hover states
- Use transições suaves
- Indique elementos clicáveis

### 2. **Espaçamento**

- Respire! Use espaçamento generoso
- Mantenha consistência
- Use grid/flexbox

### 3. **Hierarquia**

- Tamanhos de fonte claros
- Pesos de fonte apropriados
- Cores com contraste adequado

### 4. **Performance**

- Use transform para animações
- Evite layout shifts
- Otimize sombras e blur

---

## 🔄 Migração do Estilo Antigo

### Para voltar ao estilo anterior:

**Edite `frontend/index.html`:**

```html
<!-- Comentar Copilot Style -->
<!-- <link rel="stylesheet" href="/static/copilot-style.css"> -->

<!-- Descomentar estilo original -->
<link
  rel="stylesheet"
  href="/static/styles.css"
/>
```

### Para usar os dois estilos:

```html
<!-- Ambos (Copilot sobrescreve) -->
<link
  rel="stylesheet"
  href="/static/styles.css"
/>
<link
  rel="stylesheet"
  href="/static/copilot-style.css"
/>
```

---

## 📚 Recursos Adicionais

### Inspiração

- [Microsoft Copilot](https://copilot.microsoft.com)
- [Fluent UI](https://developer.microsoft.com/en-us/fluentui)
- [Material Design 3](https://m3.material.io/)

### Ferramentas

- [Coolors](https://coolors.co/) - Paleta de cores
- [CSS Gradient](https://cssgradient.io/) - Gradientes
- [Box Shadows](https://box-shadow.dev/) - Sombras CSS
- [Cubic Bezier](https://cubic-bezier.com/) - Curvas de animação

---

## ✅ Resultado Final

**Interface moderna, limpa e profissional:**

- ✓ Inspirada no Microsoft Copilot
- ✓ Mantém identidade visual Sebrae
- ✓ Totalmente responsiva
- ✓ Acessível e performática
- ✓ Fácil de manter e customizar

---

**Data de criação:** 5 de novembro de 2025  
**Versão:** 1.0  
**Autor:** Copilot AI Assistant
