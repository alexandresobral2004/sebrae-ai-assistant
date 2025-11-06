# 🧪 GUIA DE TESTE - Consultor Virtual Sebrae

## ✅ Sistema Implementado com Sucesso!

---

## 📋 O QUE FOI IMPLEMENTADO

✅ **Menu de saudação automático** - Quando usuário inicia conversa  
✅ **Modo 1** - Consulta à base de dados local + indicação de consultores  
✅ **Modo 2** - Conversa livre com IA (LLM)  
✅ **Detecção inteligente** - Sistema identifica modo automaticamente  
✅ **Interface web** - Totalmente integrado ao frontend existente

---

## 🎯 COMO TESTAR

### PASSO 1: Acessar a Aplicação

```
URL: http://localhost:8000/frontend/login.html
```

1. Abra seu navegador (Chrome, Firefox, Safari)
2. Cole a URL acima
3. Faça login com suas credenciais:
   - **Email:** seu email cadastrado
   - **Senha:** sua senha
   - Ou use **Login com Google**

### PASSO 2: Iniciar Chat

1. Após login, clique no botão **"💬 Iniciar Chat"**
2. Você será redirecionado para a tela de chat

### PASSO 3: Testar Menu Automático

Digite uma saudação simples para ver o menu:

```
Digite: Olá
```

**Resultado Esperado:**

```
╔══════════════════════════════════════════════════════════════╗
║       🤖 BEM-VINDO AO CONSULTOR VIRTUAL SEBRAE! 🤖         ║
╚══════════════════════════════════════════════════════════════╝

👋 Olá! Seja bem-vindo(a)!

[Menu completo com opções 1 e 2]
```

**✅ PASSOU** se o menu aparecer com as boas-vindas.

---

### PASSO 4: Testar Modo 1 (Base de Dados + Consultores)

#### Teste 4A: Formato com Enter

```
Digite: 1
[Aguarde resposta do sistema]

Digite: Como abrir um MEI?
```

**Resultado Esperado:**

- Sistema responde com informações da base de dados
- Lista de **consultores especializados** aparece
- Fontes dos documentos são mostradas

**Exemplo de resposta:**

```
📚 Com base nos documentos do Sebrae sobre MEI...

[Resposta detalhada]

👨‍💼 CONSULTORES RECOMENDADOS:
• João Silva - Microempreendedor Individual
• Maria Santos - Formalização de Negócios

📄 FONTES CONSULTADAS:
• Manual_MEI.pdf
• FT_Formalizacao.docx
```

#### Teste 4B: Formato Direto (uma linha)

```
Digite: 1 Quais cursos de marketing o Sebrae oferece?
```

**Resultado Esperado:**

- Mesma resposta do teste anterior
- Com consultores de marketing
- Com fontes dos documentos

**✅ PASSOU** se aparecerem:

- Resposta baseada nos documentos
- Lista de consultores
- Fontes consultadas

---

### PASSO 5: Testar Modo 2 (Conversa Livre com IA)

#### Teste 5A: Formato com Enter

```
Digite: 2
[Aguarde resposta do sistema]

Digite: Dicas para aumentar vendas no e-commerce
```

**Resultado Esperado:**

- Resposta gerada pela IA (não consulta documentos)
- Sem lista de consultores
- Sem fontes de documentos
- Dicas gerais e práticas

**Exemplo de resposta:**

```
💬 Aqui estão algumas estratégias para aumentar vendas no e-commerce:

1. **Otimize o SEO** do seu site para aparecer nas buscas
2. **Invista em anúncios** no Google e redes sociais
3. **Melhore a experiência** do usuário no site
...
```

#### Teste 5B: Formato Direto (uma linha)

```
Digite: 2 Como criar um plano de marketing digital?
```

**Resultado Esperado:**

- Resposta rápida da IA
- Orientações práticas
- Sem consulta à base local

**✅ PASSOU** se:

- Resposta for gerada rapidamente
- NÃO aparecer consultores
- NÃO aparecer fontes de documentos

---

### PASSO 6: Testar Comportamento Padrão (Sem Modo)

```
Digite: Quais são as tendências de mercado para 2025?
```

**Resultado Esperado:**

- Sistema assume **Modo 2** automaticamente
- Resposta da IA sem consultar base
- Nota informando que assumiu modo 2

**Exemplo:**

```
💬 As principais tendências de mercado para 2025 incluem...

[Resposta da IA]

_ℹ️ Nota: Como você não especificou o modo, respondi com
informações gerais. Para consultar documentos oficiais do
Sebrae, use o modo 1._
```

**✅ PASSOU** se assumir modo 2 e mostrar nota.

---

## 📊 CHECKLIST DE TESTES

### ✅ Testes Funcionais

- [ ] **Menu aparece** na primeira interação
- [ ] **Menu aparece** ao digitar saudação ("Olá", "Oi", etc.)
- [ ] **Modo 1** funciona com formato "1 [Enter] pergunta"
- [ ] **Modo 1** funciona com formato "1 pergunta" (uma linha)
- [ ] **Modo 1** retorna **consultores especializados**
- [ ] **Modo 1** retorna **fontes dos documentos**
- [ ] **Modo 2** funciona com formato "2 [Enter] pergunta"
- [ ] **Modo 2** funciona com formato "2 pergunta" (uma linha)
- [ ] **Modo 2** NÃO retorna consultores
- [ ] **Modo 2** NÃO retorna fontes
- [ ] **Sem modo** assume Modo 2 automaticamente
- [ ] **Histórico** mantém conversa entre mensagens

### ✅ Testes de UX

- [ ] **Menu** é claro e fácil de entender
- [ ] **Instruções** de uso são visíveis
- [ ] **Respostas** aparecem formatadas corretamente
- [ ] **Consultores** aparecem com nome e especialidade
- [ ] **Fontes** aparecem com nome do arquivo

---

## 🔍 EXEMPLOS DE PERGUNTAS PARA TESTAR

### Para Modo 1 (Base de Dados):

```
1 Como abrir um MEI?
1 Quais são os cursos de empreendedorismo do Sebrae?
1 Como contratar um consultor do Sebrae?
1 O que é o Sebraetec?
1 Quais são as linhas de crédito disponíveis?
1 Como fazer o registro de marca?
```

### Para Modo 2 (Conversa Livre):

```
2 Dicas para aumentar vendas online
2 Como melhorar meu atendimento ao cliente?
2 Estratégias de marketing digital eficazes
2 Como fazer uma boa gestão financeira?
2 Ideias de negócio para 2025
2 Como validar uma ideia de negócio?
```

---

## 🎯 RESULTADOS ESPERADOS POR MODO

### Modo 1 (Base de Dados):

```
✅ Resposta baseada em documentos oficiais
✅ Lista de consultores especializados:
   👨‍💼 Nome do Consultor - Especialidade
✅ Fontes consultadas:
   📄 Nome_do_Arquivo.pdf
✅ Tempo de resposta: 5-10 segundos
```

### Modo 2 (Conversa Livre):

```
✅ Resposta gerada pela IA
❌ SEM consultores
❌ SEM fontes de documentos
✅ Tempo de resposta: 2-5 segundos
✅ Dicas práticas e orientações gerais
```

---

## 🐛 POSSÍVEIS PROBLEMAS E SOLUÇÕES

### Problema 1: Menu não aparece

**Sintoma:** Ao digitar "Olá", não aparece o menu

**Solução:**

1. Limpe o histórico do chat
2. Faça logout e login novamente
3. Verifique se o servidor está rodando

### Problema 2: Consultores não aparecem no Modo 1

**Sintoma:** Modo 1 responde mas sem consultores

**Solução:**

1. Verifique se digitou "1" no início
2. Aguarde alguns segundos para processar
3. Tente uma pergunta mais específica

### Problema 3: Resposta muito lenta

**Sintoma:** Sistema demora muito para responder

**Solução:**

- Modo 1 é mais lento (busca documentos)
- Modo 2 é mais rápido (IA direta)
- Aguarde até 15 segundos no Modo 1

### Problema 4: Erro de API

**Sintoma:** Mensagem "API não configurada"

**Solução:**

1. Verifique arquivo `.env`
2. Confirme que `OPENAI_API_KEY` está preenchida
3. Reinicie o servidor

---

## 📸 SCREENSHOTS ESPERADOS

### Tela 1: Menu Inicial

```
[Caixa de chat com menu formatado]
- Header com título
- Descrição do assistente
- Box com opção 1 (azul)
- Box com opção 2 (verde)
- Instruções de uso
```

### Tela 2: Resposta Modo 1

```
[Caixa de chat]
- Resposta textual
- Seção "Consultores Recomendados" com lista
- Seção "Fontes Consultadas" com arquivos
```

### Tela 3: Resposta Modo 2

```
[Caixa de chat]
- Resposta textual da IA
- Sem consultores
- Sem fontes
```

---

## ✅ CRITÉRIOS DE SUCESSO

O sistema está **100% funcional** se:

1. ✅ Menu aparece automaticamente na primeira interação
2. ✅ Modo 1 busca na base E retorna consultores
3. ✅ Modo 2 responde via IA sem buscar base
4. ✅ Sistema distingue claramente entre os dois modos
5. ✅ Instruções são claras e fáceis de seguir
6. ✅ Respostas são formatadas corretamente
7. ✅ Histórico mantém contexto da conversa

---

## 🚀 STATUS DO SERVIDOR

**Servidor:** ✅ ONLINE  
**Porta:** 8000  
**Documentos:** 421 arquivos  
**Consultores:** 3.465 registros  
**Modelo IA:** GPT-3.5-Turbo

**URLs:**

- Login: http://localhost:8000/frontend/login.html
- Chat: http://localhost:8000/frontend/chat.html
- API: http://localhost:8000/docs

---

## 📞 PRECISA DE AJUDA?

Se encontrar algum problema:

1. Verifique os logs do servidor: `tail -f server.log`
2. Teste o endpoint direto: `curl http://localhost:8000/api/status`
3. Reinicie o servidor se necessário
4. Limpe o cache do navegador

---

**Data:** 6 de novembro de 2025  
**Status:** ✅ SISTEMA PRONTO PARA TESTE  
**Versão:** 3.0.0 - Menu Interativo

🎯 **Boa sorte nos testes!**
