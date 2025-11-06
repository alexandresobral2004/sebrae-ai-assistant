# 🔧 Como Corrigir o Erro "invalid_client: Unauthorized"

## ❌ Problema

Erro: `invalid_client: Unauthorized` ao tentar fazer login com Google

## ✅ Solução

### Passo 1: Acessar Google Cloud Console

1. Abra: https://console.cloud.google.com/apis/credentials
2. Faça login com sua conta Google (a mesma que criou as credenciais)

### Passo 2: Localizar suas Credenciais OAuth

1. Na página de **Credenciais**, procure por:
   - **Nome**: Algo como "Web client 1" ou o nome que você deu
   - **Client ID**: `503350985543-tadtui4e36tle9brp2rjgspd3kf679jt.apps.googleusercontent.com`
2. **CLIQUE** no nome do Client ID para editar

### Passo 3: Adicionar URL de Redirecionamento

Na tela de edição, você verá duas seções importantes:

#### A) Origens JavaScript autorizadas

Clique em **"+ ADICIONAR URI"** e adicione:

```
http://localhost:8000
```

#### B) URIs de redirecionamento autorizados

Clique em **"+ ADICIONAR URI"** e adicione EXATAMENTE esta URL:

```
http://localhost:8000/api/auth/google/callback
```

⚠️ **IMPORTANTE**:

- A URL deve ser EXATAMENTE como está acima
- Não pode ter barra `/` no final
- Deve começar com `http://` (não `https://`)
- O caminho deve ser `/api/auth/google/callback`

### Passo 4: Salvar

1. Clique no botão **"SALVAR"** no rodapé da página
2. Aguarde a confirmação de que foi salvo

### Passo 5: Aguardar Propagação (Opcional)

- As mudanças geralmente são instantâneas
- Em alguns casos, pode levar até 5 minutos para propagar

### Passo 6: Testar Novamente

1. Volte para: http://localhost:8000/login.html
2. Clique em "Continuar com Google"
3. Deve funcionar agora! 🎉

---

## 🔍 Verificação Visual

Quando você clicar para editar o Client ID, a tela deve mostrar algo assim:

```
Nome: [Seu nome do cliente]
ID do cliente: 503350985543-tadtui4e36tle9brp2rjgspd3kf679jt.apps.googleusercontent.com
Client Secret: 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

Origens JavaScript autorizadas:
  http://localhost:8000                    [botão X para remover]
  [+ ADICIONAR URI]

URIs de redirecionamento autorizados:
  http://localhost:8000/api/auth/google/callback    [botão X para remover]
  [+ ADICIONAR URI]
```

---

## 🆘 Se ainda não funcionar

### Opção 1: Criar novas credenciais

1. No Google Cloud Console, clique em **"+ CRIAR CREDENCIAIS"**
2. Selecione **"ID do cliente OAuth 2.0"**
3. Tipo: **"Aplicativo da Web"**
4. Nome: `Sebrae AI - Desenvolvimento Local`
5. Adicione as URLs acima
6. Copie o novo Client ID e Secret
7. Atualize no arquivo `.env`
8. Reinicie o servidor

### Opção 2: Verificar se o projeto Google Cloud está ativo

1. Verifique se o projeto no Google Cloud Console está ativo
2. Verifique se a **Google+ API** ou **Google Identity** estão habilitadas

### Opção 3: Verificar tela de consentimento OAuth

1. No menu lateral, vá em **"Tela de consentimento OAuth"**
2. Certifique-se de que está configurada
3. Adicione seu email como "Usuário de teste" se o app estiver em modo teste

---

## 📞 Precisa de Ajuda?

Se seguiu todos os passos e ainda não funcionar, verifique:

- [ ] URL de callback está EXATAMENTE como `http://localhost:8000/api/auth/google/callback`
- [ ] Clicou em SALVAR no Google Cloud Console
- [ ] Aguardou alguns segundos para propagação
- [ ] Limpou o cache do navegador (Ctrl+Shift+Del)
- [ ] Tentou em uma janela anônima
