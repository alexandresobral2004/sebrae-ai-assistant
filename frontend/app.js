// ===================================
// SEBRAE AI ASSISTANT - JAVASCRIPT
// Lógica do Frontend Moderno com Autenticação
// ===================================

// === CONFIGURAÇÃO ===
const API_BASE = window.location.origin;
let SESSION_ID = null;
let currentUser = null;
let authToken = null;

// === ESTADO GLOBAL ===
let currentPage = 'home';
let chatHistory = [];
let selectedFiles = [];

// === INICIALIZAÇÃO ===
document.addEventListener('DOMContentLoaded', async () => {
  console.log('🚀 Inicializando Sebrae AI Assistant...');

  // Verificar autenticação
  if (!checkAuth()) {
    return; // Redireciona para login
  }

  // Carregar informações do usuário
  await loadUserInfo();

  // Configurar event listeners
  setupEventListeners();

  // Carregar status inicial
  await loadSystemStatus();

  // Carregar métricas
  await loadMetrics();

  // Carregar lista de documentos
  await loadDocuments();

  // Inicializar chat com saudação
  initializeChat();

  // Ocultar loading
  setTimeout(() => {
    document.getElementById('loading-overlay').classList.add('hidden');
  }, 1000);

  console.log('✅ Assistente pronto!');
});

// === AUTENTICAÇÃO ===
function checkAuth() {
  authToken = localStorage.getItem('token');

  if (!authToken) {
    console.log('❌ Usuário não autenticado, redirecionando...');
    window.location.href = '/login.html';
    return false;
  }

  return true;
}

async function loadUserInfo() {
  try {
    const response = await fetch(`${API_BASE}/api/auth/me`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login.html';
        return;
      }
      throw new Error('Erro ao carregar informações do usuário');
    }

    currentUser = await response.json();
    SESSION_ID = `user_${currentUser.id}`;

    // Atualizar UI com informações do usuário
    const userNameElement = document.getElementById('user-name');
    const userAvatarElement = document.getElementById('user-avatar');

    if (userNameElement) {
      userNameElement.textContent = currentUser.nome;
    }

    if (userAvatarElement && currentUser.google_picture) {
      userAvatarElement.src = currentUser.google_picture;
      userAvatarElement.style.display = 'block';
    }

    console.log('👤 Usuário logado:', currentUser.nome);

  } catch (error) {
    console.error('Erro ao carregar usuário:', error);
    showToast('Erro ao carregar informações do usuário', 'error');
  }
}

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = '/login.html';
}

// === FUNÇÕES AUXILIARES ===
function generateSessionId() {
  return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function formatTimestamp() {
  const now = new Date();
  return now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideOutRight 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// === NAVEGAÇÃO ===
function showPage(pageName) {
  // Ocultar todas as páginas
  document.querySelectorAll('.page').forEach(page => {
    page.classList.remove('active');
  });

  // Mostrar página selecionada
  const page = document.getElementById(`${pageName}-page`);
  if (page) {
    page.classList.add('active');
    currentPage = pageName;
  }
}

// === API CALLS ===
async function apiCall(endpoint, options = {}) {
  try {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    // Adicionar token de autenticação se disponível
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers,
      ...options
    });

    if (!response.ok) {
      // Se não autorizado, redirecionar para login
      if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login.html';
        return;
      }
      throw new Error(`API Error: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Call Error:', error);
    showToast(`Erro: ${error.message}`, 'error');
    throw error;
  }
}

// === STATUS DO SISTEMA ===
async function loadSystemStatus() {
  try {
    const status = await apiCall('/api/status');

    const statusText = document.getElementById('status-text');
    const statusDot = document.querySelector('.status-dot');

    if (status.status === 'online') {
      statusText.textContent = '🟢 Online';
      statusDot.classList.remove('offline');
    } else {
      statusText.textContent = '🔴 Offline';
      statusDot.classList.add('offline');
    }
  } catch (error) {
    console.error('Erro ao carregar status:', error);
  }
}

// === MÉTRICAS ===
async function loadMetrics() {
  try {
    const metrics = await apiCall('/api/metricas');

    document.getElementById('metric-docs').textContent = metrics.documentos_carregados;
    document.getElementById('metric-consultores').textContent = metrics.consultores_disponiveis.toLocaleString('pt-BR');
    document.getElementById('metric-consultas').textContent = metrics.consultas_hoje;

    // Animar números
    animateNumbers();
  } catch (error) {
    console.error('Erro ao carregar métricas:', error);
  }
}

function animateNumbers() {
  const metrics = document.querySelectorAll('.metric-number');
  metrics.forEach(metric => {
    const target = parseInt(metric.textContent.replace(/\D/g, ''));
    let current = 0;
    const increment = target / 50;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        metric.textContent = target.toLocaleString('pt-BR');
        clearInterval(timer);
      } else {
        metric.textContent = Math.floor(current).toLocaleString('pt-BR');
      }
    }, 20);
  });
}

// === CHAT ===
function initializeChat() {
  const saudacao = `Olá! 👋 Eu sou o **Assistente de Consultoria do Sebrae**, seu consultor especializado em inteligência artificial e análise de dados.

🎯 **Minha missão:** Ajudar analistas do Sebrae com informações precisas sobre produtos, serviços, fichas técnicas (FT) e manuais de operacionalização (MOA).

🔍 **Como funciono:**
- **Prioridade total** para nossa base local de documentos Sebrae
- Respostas rápidas e precisas baseadas em conhecimento oficial
- Fallback inteligente para informações complementares quando necessário

💡 **Posso ajudar com:**
- Soluções e produtos do Sebrae
- Fichas técnicas detalhadas
- Contratação de consultores e instrutores
- Estratégias para atendimento de demandas
- Orientações sobre empreendedorismo

**Qual é sua pergunta hoje?** Estou pronto para ajudar! 🚀`;

  addMessageToChat('assistant', saudacao);
}

async function sendMessage() {
  const input = document.getElementById('chat-input');
  const message = input.value.trim();

  if (!message) {
    showToast('Digite uma mensagem', 'warning');
    return;
  }

  // Adicionar mensagem do usuário
  addMessageToChat('user', message);

  // Limpar input
  input.value = '';

  // Desabilitar botão de envio
  const sendButton = document.getElementById('send-button');
  sendButton.disabled = true;
  sendButton.textContent = 'Pensando...';

  // Criar placeholder para resposta com animação de digitação
  const assistantMessageId = createTypingIndicator();

  try {
    // Chamar API com token de autenticação
    const response = await apiCall('/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        mensagem: message
      })
    });

    // Formatar resposta completa
    let respostaCompleta = response.resposta;

    // Adicionar consultores se houver
    if (response.consultores && response.consultores.length > 0) {
      respostaCompleta += '\n\n' + formatConsultores(response.consultores);
    }

    // Adicionar documentos se houver
    if (response.documentos && response.documentos.length > 0) {
      respostaCompleta += '\n\n' + formatDocumentos(response.documentos);
    }

    // Adicionar indicador de fonte
    if (response.usado_internet) {
      respostaCompleta += '\n\n🌐 **Informação complementar da internet incluída**';
    } else {
      respostaCompleta += '\n\n📚 **Resposta baseada na base local do Sebrae**';
    }

    // Remover indicador de digitação e adicionar resposta com efeito de digitação
    removeTypingIndicator(assistantMessageId);
    await typeMessage('assistant', respostaCompleta);

    // Atualizar métricas
    await loadMetrics();

  } catch (error) {
    removeTypingIndicator(assistantMessageId);
    addMessageToChat('assistant', '❌ Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.');
  } finally {
    // Reabilitar botão
    sendButton.disabled = false;
    sendButton.textContent = 'Enviar';

    // Focar no input
    input.focus();
  }
}

function addMessageToChat(role, content) {
  const messagesContainer = document.getElementById('chat-messages');
  const messageDiv = document.createElement('div');
  messageDiv.className = `chat-message message-${role}`;

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';

  const header = document.createElement('div');
  header.className = 'message-header';
  header.innerHTML = role === 'user' ? '👤 Você' : '🤖 Consultor IA';

  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';
  contentDiv.innerHTML = formatMessage(content);

  const meta = document.createElement('div');
  meta.className = 'message-meta';
  meta.textContent = formatTimestamp();

  bubble.appendChild(header);
  bubble.appendChild(contentDiv);
  bubble.appendChild(meta);
  messageDiv.appendChild(bubble);

  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Adicionar ao histórico
  chatHistory.push({ role, content, timestamp: new Date() });

  return messageDiv;
}

// === EFEITO DE DIGITAÇÃO ===
function createTypingIndicator() {
  const messagesContainer = document.getElementById('chat-messages');
  const messageDiv = document.createElement('div');
  const messageId = 'typing-' + Date.now();
  messageDiv.id = messageId;
  messageDiv.className = 'chat-message message-assistant';

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';

  const header = document.createElement('div');
  header.className = 'message-header';
  header.innerHTML = '🤖 Consultor IA';

  const typingIndicator = document.createElement('div');
  typingIndicator.className = 'typing-indicator';
  typingIndicator.innerHTML = '<span></span><span></span><span></span>';

  bubble.appendChild(header);
  bubble.appendChild(typingIndicator);
  messageDiv.appendChild(bubble);

  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  return messageId;
}

function removeTypingIndicator(messageId) {
  const indicator = document.getElementById(messageId);
  if (indicator) {
    indicator.remove();
  }
}

async function typeMessage(role, content) {
  const messagesContainer = document.getElementById('chat-messages');
  const messageDiv = document.createElement('div');
  messageDiv.className = `chat-message message-${role}`;

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';

  const header = document.createElement('div');
  header.className = 'message-header';
  header.innerHTML = role === 'user' ? '👤 Você' : '🤖 Consultor IA';

  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';

  const meta = document.createElement('div');
  meta.className = 'message-meta';
  meta.textContent = formatTimestamp();

  bubble.appendChild(header);
  bubble.appendChild(contentDiv);
  bubble.appendChild(meta);
  messageDiv.appendChild(bubble);

  messagesContainer.appendChild(messageDiv);

  // Dividir texto em linhas
  const lines = content.split('\n');

  // Velocidade de digitação (ms por caractere)
  const typingSpeed = 15;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let displayedText = '';

    // Digitar caractere por caractere
    for (let j = 0; j < line.length; j++) {
      displayedText += line[j];

      // Atualizar conteúdo com formatação
      let formattedContent = formatMessage(displayedText);

      // Adicionar linhas já completas antes desta
      if (i > 0) {
        const previousLines = lines.slice(0, i).join('\n');
        formattedContent = formatMessage(previousLines + '\n' + displayedText);
      }

      contentDiv.innerHTML = formattedContent;

      // Scroll automático
      messagesContainer.scrollTop = messagesContainer.scrollHeight;

      // Aguardar antes do próximo caractere
      await sleep(typingSpeed);
    }

    // Adicionar quebra de linha se não for a última linha
    if (i < lines.length - 1) {
      displayedText += '\n';
      await sleep(typingSpeed * 2);
    }
  }

  // Adicionar ao histórico
  chatHistory.push({ role, content, timestamp: new Date() });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function formatMessage(text) {
  // Converter markdown simples para HTML
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}

function formatConsultores(consultores) {
  let html = '---\n\n## 👥 CONSULTORES ESPECIALIZADOS ENCONTRADOS\n\n';

  consultores.forEach((consultor, index) => {
    html += `### 🔹 Consultor ${index + 1}\n\n`;

    if (consultor.nome) {
      html += `**👤 Nome:** ${consultor.nome}\n\n`;
    } else if (consultor.razao_social) {
      html += `**🏢 Empresa:** ${consultor.razao_social}\n\n`;
    }

    if (consultor.area_principal) {
      html += `**🎯 Área Principal:** ${consultor.area_principal}\n\n`;
    }

    if (consultor.subespecialidade) {
      html += `**📋 Subespecialidade:** ${consultor.subespecialidade}\n\n`;
    }

    if (consultor.cidade && consultor.estado) {
      html += `**📍 Localização:** ${consultor.cidade}, ${consultor.estado}\n\n`;
    }

    if (consultor.telefone) {
      html += `**📞 Telefone:** ${consultor.telefone}\n\n`;
    }

    if (consultor.email) {
      html += `**📧 Email:** ${consultor.email}\n\n`;
    }

    html += '\n';
  });

  html += '💡 **Como proceder:**\n';
  html += '1. Entre em contato diretamente com o consultor de sua preferência\n';
  html += '2. Mencione que encontrou o contato via sistema Sebrae\n';
  html += '3. Discuta suas necessidades específicas de consultoria\n';

  return html;
}

function formatDocumentos(documentos) {
  let html = '---\n\n## 📚 DOCUMENTOS CONSULTADOS\n\n';
  html += '*As informações acima foram extraídas dos seguintes documentos oficiais do Sebrae:*\n\n';

  documentos.forEach(doc => {
    const nome = doc.replace(/\.(pdf|docx|xlsx)$/i, '').replace(/_/g, ' ');
    const icone = getFileIcon(doc);

    html += `- ${icone} **${nome}**\n`;
    html += `  *Documento oficial do Sebrae - ${doc}*\n\n`;
  });

  html += '💾 **Para baixar os documentos:** Visite o portal oficial do Sebrae\n';
  html += '🔗 **Portal:** www.sebrae.com.br\n';

  return html;
}

function getFileIcon(filename) {
  const ext = filename.split('.').pop().toLowerCase();
  const icons = {
    'pdf': '📄',
    'docx': '📝',
    'doc': '📝',
    'xlsx': '📊',
    'xls': '📊'
  };
  return icons[ext] || '📄';
}

function clearChat() {
  if (confirm('Deseja realmente limpar o histórico de conversas?')) {
    chatHistory = [];
    document.getElementById('chat-messages').innerHTML = '';
    initializeChat();
    showToast('Histórico limpo! Nova conversa iniciada.', 'success');
  }
}

// === UPLOAD DE DOCUMENTOS ===
function setupEventListeners() {
  // Logout
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', logout);
  }

  // Enter no chat
  const chatInput = document.getElementById('chat-input');
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Upload de arquivos
  const fileInput = document.getElementById('file-input');
  fileInput.addEventListener('change', handleFileSelect);

  const uploadArea = document.getElementById('upload-area');
  uploadArea.addEventListener('dragover', handleDragOver);
  uploadArea.addEventListener('dragleave', handleDragLeave);
  uploadArea.addEventListener('drop', handleDrop);
}

function handleFileSelect(e) {
  const files = Array.from(e.target.files);
  addFilesToList(files);
}

function handleDragOver(e) {
  e.preventDefault();
  e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
  e.currentTarget.classList.remove('drag-over');
}

function handleDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');

  const files = Array.from(e.dataTransfer.files);
  addFilesToList(files);
}

function addFilesToList(files) {
  const validExtensions = ['.pdf', '.docx', '.xlsx'];
  const validFiles = files.filter(file => {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    return validExtensions.includes(ext);
  });

  if (validFiles.length === 0) {
    showToast('Apenas arquivos PDF, DOCX e XLSX são aceitos', 'warning');
    return;
  }

  selectedFiles = [...selectedFiles, ...validFiles];
  displaySelectedFiles();

  document.getElementById('upload-button').style.display = 'block';
}

function displaySelectedFiles() {
  const container = document.getElementById('selected-files');
  container.innerHTML = '';

  selectedFiles.forEach((file, index) => {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';

    const fileInfo = document.createElement('div');
    fileInfo.className = 'file-info';
    fileInfo.innerHTML = `
            ${getFileIcon(file.name)}
            <span>${file.name}</span>
            <span style="color: var(--cinza-escuro); font-size: 0.9rem;">(${(file.size / 1024).toFixed(1)} KB)</span>
        `;

    const removeBtn = document.createElement('span');
    removeBtn.className = 'file-remove';
    removeBtn.textContent = '✕';
    removeBtn.onclick = () => removeFile(index);

    fileItem.appendChild(fileInfo);
    fileItem.appendChild(removeBtn);
    container.appendChild(fileItem);
  });
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  displaySelectedFiles();

  if (selectedFiles.length === 0) {
    document.getElementById('upload-button').style.display = 'none';
  }
}

async function uploadFiles() {
  if (selectedFiles.length === 0) {
    showToast('Selecione arquivos para fazer upload', 'warning');
    return;
  }

  const uploadButton = document.getElementById('upload-button');
  uploadButton.disabled = true;
  uploadButton.textContent = '⏳ Processando...';

  try {
    const formData = new FormData();
    selectedFiles.forEach(file => {
      formData.append('files', file);
    });

    const response = await fetch(`${API_BASE}/api/upload`, {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    showToast(`${result.mensagem}`, 'success');

    // Limpar seleção
    selectedFiles = [];
    document.getElementById('selected-files').innerHTML = '';
    document.getElementById('file-input').value = '';
    uploadButton.style.display = 'none';

    // Recarregar documentos e métricas
    await loadDocuments();
    await loadMetrics();

  } catch (error) {
    showToast('Erro ao fazer upload dos documentos', 'error');
  } finally {
    uploadButton.disabled = false;
    uploadButton.textContent = '🚀 Processar Documentos';
  }
}

// === LISTA DE DOCUMENTOS ===
async function loadDocuments() {
  try {
    const response = await apiCall('/api/documentos');
    const container = document.getElementById('documents-list');

    if (response.documentos.length === 0) {
      container.innerHTML = '<p style="text-align: center; color: var(--cinza-escuro);">Nenhum documento carregado ainda.</p>';
      return;
    }

    container.innerHTML = '';

    response.documentos.forEach(doc => {
      const docItem = document.createElement('div');
      docItem.className = 'document-item';
      docItem.innerHTML = `
                <div>
                    ${getFileIcon(doc.nome)}
                    <strong>${doc.nome}</strong>
                    <span style="color: var(--cinza-escuro); font-size: 0.9rem; margin-left: 10px;">
                        ${(doc.tamanho / 1024).toFixed(1)} KB - ${doc.pasta}
                    </span>
                </div>
            `;
      container.appendChild(docItem);
    });

  } catch (error) {
    console.error('Erro ao carregar documentos:', error);
  }
}
