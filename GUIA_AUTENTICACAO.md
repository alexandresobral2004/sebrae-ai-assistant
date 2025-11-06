http://127.0.0.1:8000/api/auth/google/callback# 🔐 Guia de Configuração - Sistema de Autenticação

## 📋 Visão Geral

Sistema completo de autenticação implementado com:

- ✅ **Google OAuth2** - Login com conta Google
- ✅ **Cadastro Tradicional** - Email, senha e informações complementares
- ✅ **JWT Tokens** - Autenticação stateless e segura
- ✅ **PostgreSQL** - Banco de dados robusto
- ✅ **Interface Copilot** - Design moderno e profissional

---

## 🗄️ 1. Configurar PostgreSQL

### Instalação

**macOS (com Homebrew):**

```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**

- Download: https://www.postgresql.org/download/windows/
- Instalar e iniciar serviço

### Criar Banco de Dados

```bash
# Conectar ao PostgreSQL
psql postgres

# Criar banco
CREATE DATABASE sebrae_ai;

# Criar usuário (opcional)
CREATE USER sebrae_user WITH PASSWORD 'sua_senha_segura';
GRANT ALL PRIVILEGES ON DATABASE sebrae_ai TO sebrae_user;

# Sair
\q
```

### Testar Conexão

```bash
psql -d sebrae_ai -U postgres
```

---

## 🔑 2. Configurar Google OAuth2

### Passo 1: Criar Projeto no Google Cloud

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Criar Projeto"**
3. Nomeie: `Sebrae AI Assistant`
4. Clique em **"Criar"**

### Passo 2: Habilitar Google+ API

1. No menu lateral: **APIs e Serviços** → **Biblioteca**
2. Pesquise: `Google+ API`
3. Clique em **"Ativar"**

### Passo 3: Criar Credenciais OAuth2

1. **APIs e Serviços** → **Credenciais**
2. Clique em **"Criar Credenciais"** → **"ID do cliente OAuth"**
3. Tipo de aplicativo: **"Aplicativo da Web"**
4. Nome: `Sebrae AI Web Client`

5. **Origens JavaScript autorizadas:**

   ```
   http://localhost:8000
   http://127.0.0.1:8000
   https://seu-dominio.com
   ```

6. **URIs de redirecionamento autorizados:**

   ```
   http://localhost:8000/api/auth/google/callback
   http://127.0.0.1:8000/api/auth/google/callback
   https://seu-dominio.com/api/auth/google/callback
   ```

7. Clique em **"Criar"**

8. **IMPORTANTE:** Copie o **Client ID** e **Client Secret**

### Passo 4: Configurar Tela de Consentimento

1. **APIs e Serviços** → **Tela de consentimento OAuth**
2. Tipo: **Externo** (para testes) ou **Interno** (apenas G Suite)
3. Preencha:
   - Nome do app: `Sebrae AI Assistant`
   - Email de suporte: seu-email@gmail.com
   - Logo (opcional)
   - Domínio da página inicial: `http://localhost:8000`
4. Escopos: `email`, `profile`, `openid`
5. Salvar

---

## ⚙️ 3. Configurar Variáveis de Ambiente

### Criar arquivo `.env`

```bash
cd /Users/alexandrerocha/sebrae-ai-assistant
nano .env
```

### Adicionar variáveis:

```bash
# OpenAI (já existente)
OPENAI_API_KEY=sua-chave-openai

# PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sebrae_ai

# JWT
JWT_SECRET_KEY=sua-chave-secreta-super-segura-mude-isto-em-producao-12345678

# Google OAuth2
GOOGLE_CLIENT_ID=seu-client-id-do-google.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-client-secret-do-google

# Configurações da Aplicação
AUTHLIB_INSECURE_TRANSPORT=1  # Apenas para desenvolvimento local
```

### Gerar JWT Secret Key Segura

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Copie o resultado e cole em `JWT_SECRET_KEY`.

---

## 📦 4. Instalar Dependências

### Instalar bibliotecas de autenticação:

```bash
cd /Users/alexandrerocha/sebrae-ai-assistant

# Instalar dependências de autenticação
pip3 install -r requirements_auth.txt

# OU instalar manualmente:
pip3 install python-jose[cryptography] passlib[bcrypt] python-multipart
pip3 install authlib httpx sqlalchemy psycopg2-binary alembic
pip3 install pydantic[email]
```

### Verificar instalação:

```bash
python3 -c "import sqlalchemy, authlib, passlib, jose; print('✅ Todas as dependências instaladas!')"
```

---

## 🚀 5. Inicializar Banco de Dados

### Criar tabelas automaticamente:

O sistema cria as tabelas automaticamente na primeira execução!

```bash
python3 api_server.py
```

Você verá no log:

```
INFO:     Started server process
INFO:     Waiting for application startup.
🚀 Inicializando Assistente IA Sebrae...
✅ Assistente IA Sebrae pronto!
```

### Verificar tabelas criadas:

```bash
psql -d sebrae_ai -U postgres

# Listar tabelas
\dt

# Você deve ver:
# users
# login_history
```

### Ver estrutura das tabelas:

```sql
\d users
\d login_history
```

---

## 🧪 6. Testar Sistema

### Teste 1: Iniciar Servidor

```bash
cd /Users/alexandrerocha/sebrae-ai-assistant
python3 api_server.py
```

### Teste 2: Acessar Frontend

Abra o navegador:

```
http://localhost:8000
```

Você deve ver a **página de login**.

### Teste 3: Cadastro Tradicional

1. Clique em **"Cadastre-se"**
2. Preencha o formulário:
   - Nome: Seu Nome
   - Email: seu@email.com
   - Senha: 123456 (mínimo 6 caracteres)
   - Empresa, cargo, etc. (opcional)
3. Clique em **"Criar conta"**
4. Você será redirecionado para o chat

### Teste 4: Login com Google

1. Na página de login, clique em **"Continuar com Google"**
2. Selecione sua conta Google
3. Autorize o aplicativo
4. Você será redirecionado para o chat

### Teste 5: Verificar Usuário no Banco

```bash
psql -d sebrae_ai -U postgres

SELECT id, email, nome, google_id, created_at FROM users;
```

---

## 🔒 7. Segurança em Produção

### ⚠️ IMPORTANTE: Antes de colocar em produção

1. **Alterar JWT Secret Key:**

   ```bash
   # Gerar nova chave forte
   python3 -c "import secrets; print(secrets.token_urlsafe(64))"
   ```

2. **Desabilitar AUTHLIB_INSECURE_TRANSPORT:**

   ```bash
   # Remover ou comentar no .env
   # AUTHLIB_INSECURE_TRANSPORT=1
   ```

3. **Usar HTTPS:**

   - Obter certificado SSL (Let's Encrypt)
   - Configurar Nginx/Apache como proxy reverso

4. **Atualizar URLs no Google Cloud:**

   - Adicionar domínio real em "Origens autorizadas"
   - Adicionar callback HTTPS em "URIs de redirecionamento"

5. **Configurar CORS corretamente:**

   ```python
   # Em api_server.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://seu-dominio.com"],  # Não usar "*"
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "DELETE"],
       allow_headers=["*"],
   )
   ```

6. **Senha do PostgreSQL:**

   - Criar senha forte para usuário do banco
   - Não usar usuário `postgres` em produção

7. **Rate Limiting:**
   - Implementar limite de requisições por IP
   - Prevenir ataques de força bruta

---

## 🛠️ 8. Comandos Úteis

### Reiniciar PostgreSQL

**macOS:**

```bash
brew services restart postgresql@15
```

**Ubuntu/Debian:**

```bash
sudo systemctl restart postgresql
```

### Ver logs do PostgreSQL

**macOS:**

```bash
tail -f /usr/local/var/log/postgresql@15.log
```

**Ubuntu/Debian:**

```bash
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Backup do Banco

```bash
pg_dump -U postgres sebrae_ai > backup_sebrae_ai.sql
```

### Restaurar Backup

```bash
psql -U postgres sebrae_ai < backup_sebrae_ai.sql
```

### Resetar Banco (CUIDADO!)

```bash
psql -U postgres -c "DROP DATABASE sebrae_ai;"
psql -U postgres -c "CREATE DATABASE sebrae_ai;"
python3 api_server.py  # Recria tabelas
```

---

## 📊 9. Estrutura do Banco de Dados

### Tabela: `users`

| Campo              | Tipo        | Descrição                     |
| ------------------ | ----------- | ----------------------------- |
| `id`               | Integer     | Primary Key (auto-increment)  |
| `email`            | String(255) | Email único (required)        |
| `nome`             | String(255) | Nome completo (required)      |
| `hashed_password`  | String(255) | Senha hash (null para Google) |
| `empresa`          | String(255) | Empresa (opcional)            |
| `telefone`         | String(50)  | Telefone (opcional)           |
| `cpf`              | String(14)  | CPF (opcional)                |
| `cargo`            | String(100) | Cargo (opcional)              |
| `cidade`           | String(100) | Cidade (opcional)             |
| `estado`           | String(2)   | UF (opcional)                 |
| `google_id`        | String(255) | ID do Google (único)          |
| `google_picture`   | String(500) | URL da foto do Google         |
| `is_active`        | Boolean     | Usuário ativo?                |
| `is_admin`         | Boolean     | É administrador?              |
| `email_verificado` | Boolean     | Email verificado?             |
| `created_at`       | DateTime    | Data de criação               |
| `updated_at`       | DateTime    | Última atualização            |
| `last_login`       | DateTime    | Último login                  |

### Tabela: `login_history`

| Campo          | Tipo       | Descrição               |
| -------------- | ---------- | ----------------------- |
| `id`           | Integer    | Primary Key             |
| `user_id`      | Integer    | ID do usuário           |
| `login_method` | String(50) | 'google' ou 'password'  |
| `ip_address`   | String(50) | IP do cliente           |
| `user_agent`   | Text       | User Agent do navegador |
| `success`      | Boolean    | Login bem-sucedido?     |
| `timestamp`    | DateTime   | Data/hora do login      |

---

## 🐛 10. Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'sqlalchemy'"

```bash
pip3 install -r requirements_auth.txt
```

### Erro: "connection to server failed"

PostgreSQL não está rodando:

```bash
brew services start postgresql@15  # macOS
sudo systemctl start postgresql    # Linux
```

### Erro: "FATAL: database 'sebrae_ai' does not exist"

Criar banco:

```bash
psql postgres -c "CREATE DATABASE sebrae_ai;"
```

### Erro: Google OAuth "redirect_uri_mismatch"

1. Verificar se a URL de callback está correta no Google Cloud Console
2. URL deve ser EXATAMENTE: `http://localhost:8000/api/auth/google/callback`
3. Incluir tanto `localhost` quanto `127.0.0.1`

### Erro: "401 Unauthorized" no chat

Token expirou ou inválido:

1. Fazer logout
2. Fazer login novamente
3. Verificar se `JWT_SECRET_KEY` não mudou

### Usuários não aparecem no banco

Verificar conexão:

```bash
psql -d sebrae_ai -U postgres
SELECT * FROM users;
```

---

## 📚 11. Endpoints da API

### Autenticação

| Método | Endpoint                    | Descrição              | Auth |
| ------ | --------------------------- | ---------------------- | ---- |
| POST   | `/api/auth/register`        | Criar nova conta       | ❌   |
| POST   | `/api/auth/login`           | Login com email/senha  | ❌   |
| GET    | `/api/auth/google/login`    | Iniciar login Google   | ❌   |
| GET    | `/api/auth/google/callback` | Callback Google OAuth  | ❌   |
| GET    | `/api/auth/me`              | Dados do usuário atual | ✅   |
| PUT    | `/api/auth/me`              | Atualizar perfil       | ✅   |
| POST   | `/api/auth/logout`          | Logout                 | ✅   |

### Chat (Requerem Autenticação)

| Método | Endpoint         | Descrição        | Auth |
| ------ | ---------------- | ---------------- | ---- |
| POST   | `/api/chat`      | Enviar mensagem  | ✅   |
| GET    | `/api/historico` | Ver histórico    | ✅   |
| DELETE | `/api/historico` | Limpar histórico | ✅   |

### Admin (Apenas Administradores)

| Método | Endpoint                             | Descrição        | Auth     |
| ------ | ------------------------------------ | ---------------- | -------- |
| GET    | `/api/auth/users`                    | Listar usuários  | ✅ Admin |
| PUT    | `/api/auth/users/{id}/toggle-active` | Ativar/desativar | ✅ Admin |

---

## ✅ Checklist de Configuração

- [ ] PostgreSQL instalado e rodando
- [ ] Banco `sebrae_ai` criado
- [ ] Projeto criado no Google Cloud Console
- [ ] Google+ API habilitada
- [ ] Credenciais OAuth2 criadas
- [ ] URIs de redirecionamento configuradas
- [ ] Arquivo `.env` criado
- [ ] `DATABASE_URL` configurada
- [ ] `GOOGLE_CLIENT_ID` configurada
- [ ] `GOOGLE_CLIENT_SECRET` configurada
- [ ] `JWT_SECRET_KEY` gerada e configurada
- [ ] Dependências instaladas (`requirements_auth.txt`)
- [ ] Servidor iniciado com sucesso
- [ ] Cadastro tradicional testado
- [ ] Login com Google testado
- [ ] Usuários aparecendo no banco

---

## 🎓 Próximos Passos

1. **Customizar Design:**

   - Editar `frontend/login.html`
   - Editar `frontend/register.html`
   - Ajustar cores em `copilot-style.css`

2. **Adicionar Features:**

   - Recuperação de senha
   - Verificação de email
   - Autenticação de dois fatores
   - Upload de avatar

3. **Melhorar Segurança:**

   - Rate limiting
   - Captcha no cadastro
   - Validação de senha forte
   - Logs de auditoria

4. **Deploy em Produção:**
   - Configurar HTTPS
   - Usar variáveis de ambiente seguras
   - Configurar backup automático
   - Monitoramento e alertas

---

**Data de criação:** 5 de novembro de 2025  
**Versão:** 1.0  
**Autor:** Copilot AI Assistant
