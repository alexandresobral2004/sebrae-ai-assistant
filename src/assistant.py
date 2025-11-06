from typing import Optional, Dict, List
from .knowledge_base.base_conhecimento import BaseConhecimento
from .knowledge_base.processador_documentos import ProcessadorDocumentos
from .knowledge_base.gerenciador_consultores import GerenciadorConsultores
import openai
import os
import random
from datetime import datetime

# Configure a API Key do GitHub Copilot/OpenAI
# É uma boa prática usar variáveis de ambiente para chaves de API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AssistenteSebrae:
    def __init__(self, diretorio_base: str = ".chromadb", model_name: str = "gpt-3.5-turbo"):
        """
        Inicializa o Assistente Sebrae com sua identidade e base de conhecimento.

        Args:
            diretorio_base: Diretório para o banco de dados vetorial
            model_name: O nome do modelo OpenAI a ser usado (ex: 'gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo').
        """
        self.model_name = model_name
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        
        # Histórico de conversação (últimas 3 perguntas e respostas)
        self.historico_conversacao = []
        
        # PERSONA E MISSÃO PROFISSIONAL
        self.nome = "Consultor IA Sebrae"
        self.especialidade = "Especialista sênior em inteligência artificial e análise de dados"
        self.funcao_principal = "Consultor de Produtos e Serviços do Sebrae"
        self.missao = """Fornecer respostas precisas, práticas e atualizadas, ajudando os analistas Sebrae 
        a entender soluções do Sebrae, fichas técnicas (FT) e manuais de operacionalização da aplicação (MOA), 
        destacando melhores caminhos para que o analista possa contratar consultores e instrutores para o 
        atendimento às demandas."""
        
        # TOM E ESTILO
        self.tom_comunicacao = {
            "didatico": "Explique termos complexos de forma simples",
            "solicito": "Mostre-se pronto para ajudar",
            "profissional": "Use linguagem clara, objetiva e encorajadora",
            "analitico": "Demonstre expertise em IA e dados quando relevante"
        }
        
        # Inicializa componentes da base de conhecimento
        self.base_conhecimento = BaseConhecimento(diretorio_base)
        self.processador_documentos = ProcessadorDocumentos()
        
        # Gerenciador de consultores especializados
        self.gerenciador_consultores = GerenciadorConsultores()
    
    def _adicionar_ao_historico(self, pergunta: str, resposta: str):
        """
        Adiciona uma interação ao histórico, mantendo apenas as últimas 3.
        
        Args:
            pergunta: Pergunta do usuário
            resposta: Resposta do assistente
        """
        self.historico_conversacao.append({
            "pergunta": pergunta,
            "resposta": resposta,
            "timestamp": datetime.now().isoformat()
        })
        
        # Mantém apenas as últimas 3 interações
        if len(self.historico_conversacao) > 3:
            self.historico_conversacao = self.historico_conversacao[-3:]
    
    def _obter_contexto_historico(self) -> str:
        """
        Retorna o histórico de conversação formatado para contexto do LLM.
        
        Returns:
            String com o histórico formatado
        """
        if not self.historico_conversacao:
            return ""
        
        contexto = "\n\n**Histórico recente da conversa:**\n"
        for i, interacao in enumerate(self.historico_conversacao, 1):
            contexto += f"\nInteração {i}:\n"
            contexto += f"Usuário: {interacao['pergunta']}\n"
            contexto += f"Assistente: {interacao['resposta'][:200]}...\n"  # Resumo
        
        return contexto
    
    def _apresentacao_inicial(self) -> Dict[str, any]:
        """
        Retorna a apresentação inicial do assistente.
        
        Returns:
            Dict com mensagem de apresentação
        """
        hora_atual = datetime.now().hour
        
        if hora_atual < 12:
            periodo = "Bom dia"
        elif hora_atual < 18:
            periodo = "Boa tarde"
        else:
            periodo = "Boa noite"
        
        return {
            "resposta": f"""{periodo}! 👋

Sou o **Consultor IA Sebrae**, seu assistente especializado em empreendedorismo e soluções para pequenos negócios.

**Como posso ajudar você hoje?**

💡 Posso auxiliar com:
- Produtos e serviços do Sebrae
- Como abrir MEI, ME ou EPP
- Consultores especializados
- Cursos e capacitações
- Linhas de crédito e financiamento
- Gestão empresarial

**Faça sua pergunta e terei prazer em ajudar!** 😊""",
            "fontes": [],
            "consultores": [],
            "tipo_resposta": "apresentacao",
            "usou_base": False
        }
        
    def carregar_documentos(self, diretorio_docs: str):
        """
        Carrega documentos de um diretório para a base de conhecimento.

        Args:
            diretorio_docs: Caminho do diretório com os documentos
        """
        print("Processando documentos...")
        chunks = self.processador_documentos.processar_diretorio(diretorio_docs)
        if chunks:
            print(f"Adicionando {len(chunks)} chunks à base de conhecimento...")
            self.base_conhecimento.adicionar_documentos(chunks)
            print("Documentos carregados com sucesso!")
        else:
            print("Nenhum documento válido encontrado para processar.")
    
    def _analisar_consulta(self, consulta: str) -> Dict[str, str]:
        """
        Realiza análise Chain of Thought da consulta seguindo metodologia profissional.
        
        Args:
            consulta: A pergunta do usuário
            
        Returns:
            Dict com análise da consulta e estratégia de busca
        """
        # Análise da pergunta
        tipo_necessidade = "produto_sebrae"  # A, B ou C
        if any(palavra in consulta.lower() for palavra in ["como", "o que é", "conceito", "definição"]):
            tipo_necessidade = "conceito_negocio"
        elif any(palavra in consulta.lower() for palavra in ["tendência", "mercado", "futuro", "inovação"]):
            tipo_necessidade = "tendencia_mercado"
        
        # Estratégia de busca otimizada
        termos_busca = self._extrair_termos_relevantes(consulta)
        
        return {
            "tipo_necessidade": tipo_necessidade,
            "termos_busca": termos_busca,
            "estrategia": "base_interna_primeiro",
            "raciocinio": f"Analisando a consulta '{consulta}', identifico como {tipo_necessidade}. "
                         f"Vou iniciar pela base interna do Sebrae para garantir informações oficiais."
        }
    
    def _extrair_termos_relevantes(self, consulta: str) -> str:
        """
        Extrai e otimiza termos de busca da consulta.
        
        Args:
            consulta: Pergunta original
            
        Returns:
            String otimizada para busca
        """
        # Remove palavras irrelevantes e mantém termos-chave
        palavras_irrelevantes = {"como", "que", "qual", "onde", "quando", "por", "para", "um", "uma", "o", "a"}
        termos = [palavra.lower() for palavra in consulta.split() if palavra.lower() not in palavras_irrelevantes and len(palavra) > 2]
        return " ".join(termos)
    
    def classificar_intencao(self, consulta: str) -> Dict[str, any]:
        """
        Classifica a intenção da consulta do usuário para determinar se precisa
        consultar a base de dados ou se é uma interação casual/saudação.
        
        Args:
            consulta: Pergunta ou mensagem do usuário
            
        Returns:
            Dict com tipo de intenção, confiança e se deve buscar na base
        """
        consulta_lower = consulta.lower().strip()
        
        # 1. SAUDAÇÕES (não busca base, não indica consultores)
        saudacoes_exatas = [
            'oi', 'olá', 'ola', 'oie', 'opa', 'ei', 'hey', 'opa',
            'bom dia', 'boa tarde', 'boa noite', 'boa madrugada',
            'tudo bem', 'tudo bom', 'como vai', 'como você está',
            'e ai', 'e aí', 'beleza'
        ]
        
        # Saudação exata ou seguida apenas de pontuação/espaços
        for saudacao in saudacoes_exatas:
            if consulta_lower == saudacao or \
               consulta_lower.startswith(saudacao + ' ') or \
               consulta_lower.startswith(saudacao + '!') or \
               consulta_lower.startswith(saudacao + '?'):
                return {
                    'tipo': 'saudacao',
                    'confianca': 1.0,
                    'deve_buscar_base': False,
                    'deve_indicar_consultores': False,
                    'resposta_direta': self._responder_saudacao(consulta)
                }
        
        # 2. PERGUNTAS CASUAIS/AGRADECIMENTOS (não busca base, não indica consultores)
        padroes_casuais = [
            ('quem é você', 'quem e voce', 'quem vc é', 'quem vc e'),
            ('o que você faz', 'o que voce faz', 'o que vc faz'),
            ('qual seu nome', 'qual é seu nome', 'qual e seu nome'),
            ('como você se chama', 'como voce se chama'),
            ('obrigado', 'obrigada', 'valeu', 'vlw', 'muito obrigado'),
            ('tchau', 'até logo', 'ate logo', 'até mais', 'ate mais', 'falou'),
            ('pode me ajudar', 'me ajuda', 'preciso de ajuda', 'ajuda ai', 'ajuda aí'),
        ]
        
        for padroes in padroes_casuais:
            for padrao in padroes if isinstance(padroes, tuple) else [padroes]:
                if padrao in consulta_lower:
                    return {
                        'tipo': 'casual',
                        'confianca': 0.95,
                        'deve_buscar_base': False,
                        'deve_indicar_consultores': False,
                        'resposta_direta': self._responder_casual(consulta)
                    }
        
        # 3. PALAVRAS-CHAVE QUE INDICAM CONSULTA À BASE (busca base + consultores)
        palavras_base_conhecimento = [
            # Sebrae e serviços
            'sebrae', 'consultor', 'produto', 'serviço', 'servico', 'atendimento',
            # Tipos de empresa
            'mei', 'microempresa', 'micro empresa', 'pequena empresa', 'epp',
            'empreendedor', 'empresário', 'empresario',
            # Ações empresariais
            'como abrir', 'como criar', 'como fazer', 'como funciona', 'como registrar',
            'quero abrir', 'preciso abrir', 'vou abrir',
            # Documentação
            'documentação', 'documentacao', 'manual', 'ficha técnica', 'ficha tecnica',
            'moa', 'ft', 'procedimento',
            # Capacitação
            'curso', 'capacitação', 'capacitacao', 'treinamento', 'formação', 'formacao',
            'workshop', 'palestra', 'evento',
            # Consultoria
            'assessoria', 'consultoria', 'orientação', 'orientacao', 'ajuda especializada',
            # Aspectos legais/formais
            'cnpj', 'registro', 'alvará', 'alvara', 'licença', 'licenca',
            'documentos', 'burocracia', 'legalização', 'legalizacao',
            # Gestão empresarial
            'plano de negócio', 'plano de negocios', 'marketing', 'vendas',
            'financeiro', 'contabilidade', 'fiscal', 'tributário', 'tributario',
            # Crédito e financiamento
            'crédito', 'credito', 'empréstimo', 'emprestimo', 'financiamento',
            'capital', 'investimento', 'linha de crédito',
            # Inovação e tecnologia
            'inovação', 'inovacao', 'tecnologia', 'digital', 'transformação digital',
            'e-commerce', 'marketplace', 'redes sociais',
            # Setores
            'comércio', 'comercio', 'indústria', 'industria', 'serviços',
            'agricultura', 'agronegócio', 'agronegocio',
            # Gestão específica
            'estoque', 'fluxo de caixa', 'precificação', 'precificacao',
            'planejamento', 'estratégia', 'estrategia'
        ]
        
        # Conta quantas palavras-chave relevantes foram encontradas
        palavras_encontradas = sum(1 for palavra in palavras_base_conhecimento 
                                   if palavra in consulta_lower)
        
        # Se encontrou palavras relevantes = consulta à base + consultores
        if palavras_encontradas >= 1:
            return {
                'tipo': 'consulta_base',
                'confianca': min(0.7 + (palavras_encontradas * 0.1), 1.0),
                'deve_buscar_base': True,
                'deve_indicar_consultores': True,
                'palavras_encontradas': palavras_encontradas
            }
        
        # 4. PERGUNTAS GENÉRICAS com interrogação (tenta buscar, mas sem consultores)
        if '?' in consulta or any(palavra in consulta_lower for palavra in 
                                   ['como', 'qual', 'quais', 'onde', 'quando', 'por que', 'porque']):
            # Se a pergunta é muito curta (< 10 caracteres), provavelmente é casual
            if len(consulta.strip()) < 10:
                return {
                    'tipo': 'casual',
                    'confianca': 0.8,
                    'deve_buscar_base': False,
                    'deve_indicar_consultores': False,
                    'resposta_direta': self._responder_casual(consulta)
                }
            
            return {
                'tipo': 'informacao_geral',
                'confianca': 0.6,
                'deve_buscar_base': True,
                'deve_indicar_consultores': False,  # Pergunta genérica, sem consultores
                'nota': 'Pergunta genérica - consultará base mas sem indicar consultores'
            }
        
        # 5. PADRÃO (busca na base por segurança, sem consultores)
        return {
            'tipo': 'indefinido',
            'confianca': 0.4,
            'deve_buscar_base': True,
            'deve_indicar_consultores': False,
            'nota': 'Tipo indefinido - consultará base sem indicar consultores'
        }
    
    def _responder_saudacao(self, consulta: str) -> str:
        """Gera respostas personalizadas para saudações."""
        hora_atual = datetime.now().hour
        
        # Define saudação apropriada baseada no horário
        if hora_atual < 12:
            periodo = "Bom dia"
        elif hora_atual < 18:
            periodo = "Boa tarde"
        else:
            periodo = "Boa noite"
        
        saudacoes = [
            f"{periodo}! 👋 Sou o **Consultor IA Sebrae**, seu assistente especializado em empreendedorismo e soluções para pequenos negócios.",
            f"{periodo}! 😊 Seja bem-vindo! Sou o **Consultor IA Sebrae** e estou aqui para ajudar você!",
            f"{periodo}! Prazer em atendê-lo! Sou o **Consultor IA Sebrae**, especialista em soluções empresariais."
        ]
        
        introducao = random.choice(saudacoes)
        
        return f"""{introducao}

**Como posso te ajudar hoje?**

💡 Posso auxiliar com informações sobre:
- Produtos e serviços do Sebrae
- Orientações para abrir MEI ou empresa
- Consultores especializados
- Cursos e capacitações
- Financiamento e linhas de crédito
- Gestão empresarial e muito mais!

**Faça sua pergunta!** 🎯"""
    
    def _responder_casual(self, consulta: str) -> str:
        """Gera respostas para perguntas casuais sobre o assistente."""
        consulta_lower = consulta.lower()
        
        # Identifica o tipo de pergunta casual
        if any(palavra in consulta_lower for palavra in ['quem', 'nome', 'você é', 'voce e', 'vc é', 'vc e']):
            return """🤖 **Sobre mim:**

**Nome:** Consultor IA Sebrae

**Minha função:**
Sou um assistente inteligente especializado em ajudar analistas e empreendedores com informações do Sebrae.

**O que posso fazer:**
✅ Buscar informações em documentos oficiais do Sebrae
✅ Recomendar consultores especializados por área
✅ Explicar produtos, serviços e processos
✅ Orientar sobre MEI, microempresas e pequenos negócios
✅ Fornecer informações sobre cursos e capacitações

**Faça sua pergunta e vou buscar as melhores informações para você!** 😊"""
        
        if any(palavra in consulta_lower for palavra in ['obrigad', 'valeu', 'vlw']):
            return """De nada! 😊 Fico feliz em ajudar!

Se tiver mais dúvidas sobre o Sebrae, produtos, serviços ou consultores, **é só chamar!** 👋"""
        
        if any(palavra in consulta_lower for palavra in ['tchau', 'até logo', 'ate logo', 'até mais', 'ate mais', 'falou']):
            return """Até logo! 👋 

Estarei aqui sempre que precisar de informações do Sebrae. **Bom trabalho!** 🚀"""
        
        if any(palavra in consulta_lower for palavra in ['ajuda', 'ajudar', 'pode me', 'consegue']):
            return """📚 **Claro! Posso te ajudar sim!**

**Exemplos de perguntas que posso responder:**

🏢 **Sobre empresas:**
- "Como abrir uma MEI?"
- "Qual a diferença entre MEI e ME?"
- "Documentos necessários para abrir empresa"

📊 **Produtos e serviços:**
- "Quais produtos o Sebrae oferece?"
- "Como funciona o Sebrae Mais?"
- "Cursos disponíveis para empreendedores"

👨‍💼 **Consultores:**
- "Preciso de consultor em marketing digital"
- "Consultores especializados em finanças"
- "Quem pode me ajudar com redes sociais?"

💰 **Financiamento:**
- "Linhas de crédito para pequenas empresas"
- "Como obter financiamento pelo Sebrae?"

**Digite sua pergunta e eu busco as informações!** 🎯"""
        
        # Resposta genérica para outras perguntas casuais
        return """Olá! 😊 Estou aqui para ajudar com informações do Sebrae.

**Pode me perguntar sobre:**
- Produtos e serviços
- Como abrir empresas (MEI, ME, EPP)
- Consultores especializados
- Cursos e capacitações
- Financiamento e crédito

**Como posso te ajudar?** 💡"""
        
    def processar_consulta(self, consulta: str) -> Dict[str, Optional[str]]:
        """
        Processa consultas de forma conversacional e inteligente.
        O assistente decide automaticamente se deve buscar na base de dados ou responder diretamente.
        
        Args:
            consulta: A pergunta ou mensagem do usuário

        Returns:
            Dict[str, Optional[str]]: Resposta contendo texto, fontes e metadados
        """
        if not self.client:
            return {
                "resposta": "A chave de API do OpenAI não foi configurada. Verifique a variável de ambiente OPENAI_API_KEY.",
                "fontes": [],
                "palavras_chave": [],
                "raciocinio": "Erro de configuração"
            }

        consulta_limpa = consulta.strip()
        
        # Se consulta vazia, apresenta o assistente
        if not consulta_limpa:
            return self._apresentacao_inicial()
        
        # Classifica a intenção da consulta
        classificacao = self.classificar_intencao(consulta_limpa)
        
        # SAUDAÇÕES - responde diretamente
        if classificacao['tipo'] == 'saudacao':
            resposta = classificacao.get('resposta_direta', self._responder_saudacao(consulta_limpa))
            self._adicionar_ao_historico(consulta_limpa, resposta)
            return {
                "resposta": resposta,
                "fontes": [],
                "consultores": [],
                "tipo_resposta": "saudacao",
                "usou_base": False
            }
        
        # PERGUNTAS CASUAIS - responde diretamente
        if classificacao['tipo'] == 'casual':
            resposta = classificacao.get('resposta_direta', self._responder_casual(consulta_limpa))
            self._adicionar_ao_historico(consulta_limpa, resposta)
            return {
                "resposta": resposta,
                "fontes": [],
                "consultores": [],
                "tipo_resposta": "casual",
                "usou_base": False
            }
        
        # CONSULTAS À BASE - busca documentos + consultores
        if classificacao['deve_buscar_base']:
            resultado = self._processar_consulta_base_dados(consulta_limpa)
            self._adicionar_ao_historico(consulta_limpa, resultado.get('resposta', ''))
            return resultado
        
        # FALLBACK - resposta geral do LLM
        resultado = self._processar_consulta_llm_livre(consulta_limpa)
        self._adicionar_ao_historico(consulta_limpa, resultado.get('resposta', ''))
        return resultado
    
    def _processar_consulta_base_dados(self, consulta: str) -> Dict[str, Optional[str]]:
        """
        Processa consulta buscando na base de dados Sebrae e indicando consultores.
        
        Args:
            consulta: Pergunta do usuário
            
        Returns:
            Dict com resposta, fontes, consultores e metadados
        """
        print(f"📚 Buscando na base local Sebrae: '{consulta}'")
        
        # PASSO 1: Análise Chain of Thought da consulta
        analise = self._analisar_consulta(consulta)
        
        # PASSO 2: Busca prioritária na base interna (Regra de Ouro)
        resultados = self.base_conhecimento.buscar(analise["termos_busca"], num_resultados=8)
        
        # PASSO 3: Busca consultores especializados
        print("👨‍💼 Buscando consultores relacionados...")
        consultores_encontrados = self._buscar_consultores_relacionados(consulta, analise)
        
        if resultados:
            resposta_final = self._processar_resposta_base_interna(consulta, resultados, analise)
        else:
            # PASSO 4: Busca ampla como fallback
            resultados_amplos = self.base_conhecimento.buscar_ampla(consulta)
            if resultados_amplos:
                resposta_final = self._processar_resposta_busca_ampla(consulta, resultados_amplos, analise)
            else:
                # PASSO 5: Resposta quando não encontra informações
                resposta_final = {
                    "resposta": f"""Como Consultor IA do Sebrae, analisando sua consulta sobre '{consulta}', 
                    não encontrei informações específicas em nossa base de documentos oficial. 

                    📋 **Recomendação:** 
                    - Reformule a pergunta sendo mais específico
                    - Mencione se busca por um produto/serviço específico do Sebrae
                    - Indique o setor ou área de interesse

                    🎯 **Próximo Passo:**
                    Entre em contato com o atendimento Sebrae para consultas especializadas que possam não estar 
                    cobertas em nossos manuais técnicos.""",
                    "fontes": [],
                    "palavras_chave": [],
                    "raciocinio": analise["raciocinio"],
                    "estrategia_usada": "nenhuma_informacao_encontrada"
                }
        
        # Adiciona consultores à resposta se encontrados
        if consultores_encontrados:
            resposta_final["consultores"] = consultores_encontrados
        
        # Marca que usou a base de dados
        resposta_final["modo_consulta"] = "base_dados"
        resposta_final["usou_base"] = True
        
        return resposta_final
    
    def _processar_consulta_llm_livre(self, consulta: str) -> Dict[str, Optional[str]]:
        """
        Processa consulta usando o LLM com contexto do histórico de conversação.
        Responde como assistente de IA especializado em empreendedorismo.
        
        Args:
            consulta: Pergunta do usuário
            
        Returns:
            Dict com resposta do LLM e metadados
        """
        print(f"💬 Respondendo com IA: '{consulta}'")
        
        try:
            # Contexto do histórico
            contexto_historico = self._obter_contexto_historico()
            
            # Prompt para o LLM com contexto de empreendedorismo
            prompt_sistema = f"""Você é o Consultor IA Sebrae, um assistente especializado em empreendedorismo e pequenos negócios.

Seu papel é ajudar empreendedores com:
- Dicas práticas de gestão empresarial
- Orientações sobre marketing e vendas
- Estratégias de negócios
- Análise de ideias e oportunidades
- Informações gerais sobre empreendedorismo

Características da sua resposta:
- Seja didático e prático
- Use exemplos concretos quando possível
- Tom profissional mas acessível e amigável
- Forneça informações úteis e acionáveis
- Se a pergunta for sobre produtos/serviços específicos do Sebrae, mencione que você tem acesso à base oficial do Sebrae

{contexto_historico}

Responda à pergunta do usuário de forma completa, útil e considerando o contexto da conversa anterior (se houver)."""

            # Chama o modelo LLM
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": consulta}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            resposta_llm = response.choices[0].message.content
            
            return {
                "resposta": resposta_llm,
                "fontes": [],
                "consultores": [],
                "palavras_chave": [],
                "modo_consulta": "llm_livre",
                "usou_base": False,
                "raciocinio": "Resposta gerada pelo modelo de IA com contexto do histórico"
            }
            
        except Exception as e:
            print(f"❌ Erro ao processar com LLM: {str(e)}")
            return {
                "resposta": f"""Desculpe, ocorreu um erro ao processar sua pergunta no modo de conversa livre.

**Erro:** {str(e)}

**Sugestão:** Tente reformular sua pergunta ou use o modo 1 para consultar a base Sebrae:
`1 {consulta}`""",
                "fontes": [],
                "consultores": [],
                "erro": str(e)
            }
    
    def _buscar_consultores_relacionados(self, consulta: str, analise: Dict) -> List[Dict]:
        """
        Busca consultores especializados relacionados à consulta.
        
        Args:
            consulta: Pergunta original
            analise: Análise Chain of Thought
            
        Returns:
            Lista de consultores encontrados
        """
        try:
            # Extrai termos relevantes da consulta para buscar consultores
            termos_busca = analise.get("termos_busca", consulta)
            
            # Busca consultores relacionados
            consultores = self.gerenciador_consultores.buscar_consultores(termos_busca, limite=3)
            
            return consultores
            
        except Exception as e:
            # Log do erro mas não interrompe o fluxo principal
            print(f"Erro ao buscar consultores: {str(e)}")
            return []
    
    def _processar_resposta_base_interna(self, consulta: str, resultados: List[Dict], analise: Dict) -> Dict:
        """
        Processa resposta usando informações da base interna (Cenário A - Sucesso).
        
        Args:
            consulta: Pergunta original
            resultados: Resultados da busca interna
            analise: Análise Chain of Thought
            
        Returns:
            Dict com resposta baseada na base interna
        """
        # Organiza o contexto com identificação das fontes
        contextos_organizados = []
        fontes_unicas = set()
        
        for i, resultado in enumerate(resultados):
            fonte = resultado["metadados"]["fonte"]
            fontes_unicas.add(fonte)
            chunk_id = resultado["metadados"].get("chunk_id", "")
            
            contexto_formatado = f"""[DOCUMENTO OFICIAL SEBRAE {i+1}: {fonte} - Seção {chunk_id}]
{resultado["texto"]}
[FIM DO DOCUMENTO {i+1}]"""
            
            contextos_organizados.append(contexto_formatado)
        
        contexto_completo = "\n\n".join(contextos_organizados)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"""Você é o "{self.nome}" - {self.especialidade}.
                        
Sua função: {self.funcao_principal}
Missão: {self.missao}

TOM DE COMUNICAÇÃO:
- DIDÁTICO: Explique termos complexos de forma simples
- SOLÍCITO: Mostre-se pronto para ajudar
- PROFISSIONAL: Use linguagem clara, objetiva e encorajadora  
- ANALÍTICO: Demonstre expertise em IA e dados quando relevante

ESTRUTURA OBRIGATÓRIA DA RESPOSTA (SIGA ESTA ORDEM):

1. APRESENTAÇÃO E MISSÃO:
   - Inicie se apresentando como Consultor IA Sebrae
   - Reforce brevemente sua missão de ajudar os analistas

2. RESPOSTA À PERGUNTA:
   - Responda objetivamente à pergunta do usuário
   - Use informações dos documentos oficiais Sebrae encontrados
   - Seja claro, didático e completo
   - Cite especificamente as Fichas Técnicas (FTs) e MOAs quando aplicável

3. CONSULTORES ESPECIALIZADOS:
   - Esta seção será adicionada automaticamente pelo sistema
   - NÃO mencione consultores na sua resposta
   - O sistema incluirá automaticamente os consultores relacionados ao tema

4. DOCUMENTOS CONSULTADOS:
   - Esta seção será adicionada automaticamente pelo sistema
   - NÃO liste os documentos na sua resposta
   - O sistema incluirá automaticamente a lista de fontes com links

IMPORTANTE:
- Concentre-se APENAS nas seções 1 e 2
- NÃO crie seções de consultores ou documentos
- Seja objetivo e prático"""
                    },
                    {
                        "role": "user",
                        "content": f"""ANÁLISE INICIAL: {analise['raciocinio']}

CONTEXTO DOS DOCUMENTOS OFICIAIS SEBRAE:
{contexto_completo}

PERGUNTA DO ANALISTA: "{consulta}"

INSTRUÇÕES ESPECÍFICAS:
- Inicie com apresentação como Consultor IA Sebrae e sua missão
- Responda à pergunta de forma objetiva e completa
- Use informações de TODOS os documentos relevantes
- Cite as FTs e MOAs encontrados
- NÃO mencione consultores (será adicionado automaticamente)
- NÃO liste documentos (será adicionado automaticamente)

RESPOSTA PROFISSIONAL:"""
                    }
                ],
                max_tokens=2500,
                temperature=0.2  # Ainda mais preciso para informações oficiais
            )
            
            resposta_gerada = response.choices[0].message.content
            return {
                "resposta": resposta_gerada,
                "fontes": list(fontes_unicas),
                "palavras_chave": [],
                "num_documentos_consultados": len(fontes_unicas),
                "estrategia_usada": "base_interna_oficial",
                "raciocinio": analise["raciocinio"]
            }
            
        except Exception as e:
            return {
                "resposta": f"Erro ao processar informações da base oficial: {str(e)}",
                "fontes": [],
                "palavras_chave": [],
                "estrategia_usada": "erro_processamento"
            }
    
    def _processar_resposta_busca_ampla(self, consulta: str, resultados: List[Dict], analise: Dict) -> Dict:
        """
        Processa resposta usando busca ampla (Cenário B - Fallback).
        
        Args:
            consulta: Pergunta original
            resultados: Resultados da busca ampla
            analise: Análise Chain of Thought
            
        Returns:
            Dict com resposta baseada em busca ampla
        """
        if not resultados:
            return {
                "resposta": "Não foram encontradas informações relacionadas na base de conhecimento.",
                "fontes": [],
                "palavras_chave": [],
                "estrategia_usada": "busca_ampla_sem_resultados"
            }
        
        # Organiza contexto dos resultados amplos
        contextos = []
        fontes = set()
        
        for i, resultado in enumerate(resultados[:5]):  # Limita a 5 resultados
            fonte = resultado["metadados"]["fonte"]
            fontes.add(fonte)
            contextos.append(f"[DOCUMENTO PARCIAL {i+1}: {fonte}]\n{resultado['texto']}")
        
        contexto_amplo = "\n\n".join(contextos)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"""Você é o "{self.nome}" do Sebrae.
                        
SITUAÇÃO: A informação específica não foi encontrada em nossa base principal, 
mas encontramos algumas referências parciais em documentos.

INSTRUÇÕES:
- Seja transparente que a informação é limitada
- Use o que conseguiu encontrar de forma responsável
- Sugira próximos passos práticos
- Mantenha tom profissional e solícito"""
                    },
                    {
                        "role": "user",
                        "content": f"""ANÁLISE: {analise['raciocinio']}

A busca específica não retornou resultados completos, mas encontrei algumas referências parciais:

{contexto_amplo}

Pergunta: "{consulta}"

Responda baseado nas informações limitadas disponíveis, seja transparente sobre as limitações 
e forneça orientações práticas:"""
                    }
                ],
                max_tokens=1500,
                temperature=0.4
            )
            
            return {
                "resposta": response.choices[0].message.content,
                "fontes": list(fontes),
                "palavras_chave": [],
                "busca_ampla": True,
                "estrategia_usada": "busca_ampla_com_resultados_parciais",
                "raciocinio": analise["raciocinio"]
            }
            
        except Exception as e:
            return {
                "resposta": f"Erro ao processar busca ampla: {str(e)}",
                "fontes": [],
                "palavras_chave": [],
                "estrategia_usada": "erro_busca_ampla"
            }
    
    def _processar_resultados_amplos(self, consulta: str, resultados: List[Dict]) -> Dict[str, Optional[str]]:
        """
        Processa resultados de uma busca mais ampla quando a busca principal não retorna resultados.
        
        Args:
            consulta: A pergunta do usuário
            resultados: Lista de resultados da busca ampla
            
        Returns:
            Dict com resposta baseada nos resultados amplos
        """
        if not resultados:
            return {
                "resposta": "Não foram encontradas informações relacionadas na base de conhecimento.",
                "fontes": [],
                "palavras_chave": []
            }
        
        # Organiza contexto dos resultados amplos
        contextos = []
        fontes = set()
        
        for i, resultado in enumerate(resultados[:5]):  # Limita a 5 resultados
            fonte = resultado["metadados"]["fonte"]
            fontes.add(fonte)
            contextos.append(f"[DOCUMENTO {i+1}: {fonte}]\n{resultado['texto']}")
        
        contexto_amplo = "\n\n".join(contextos)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"Você é o '{self.nome}' do Sebrae. Analise o contexto fornecido e tente responder à pergunta, mesmo que as informações sejam parciais. Indique claramente quando as informações são limitadas e cite as fontes."
                    },
                    {
                        "role": "user",
                        "content": f"""Contexto parcial encontrado:
{contexto_amplo}

Pergunta: "{consulta}"

Responda baseado nas informações disponíveis, indicando quais documentos consultou e se as informações são limitadas:"""
                    }
                ],
                max_tokens=1500,
                temperature=0.4
            )
            
            return {
                "resposta": response.choices[0].message.content,
                "fontes": list(fontes),
                "palavras_chave": [],
                "busca_ampla": True
            }
            
        except Exception as e:
            return {
                "resposta": f"Erro ao processar busca ampla: {str(e)}",
                "fontes": [],
                "palavras_chave": []
            }
    
    def _buscar_internet(self, consulta: str) -> Optional[Dict[str, str]]:
        """
        Realiza busca na internet como fallback quando a informação não está na base local.
        
        Args:
            consulta: A pergunta do usuário
            
        Returns:
            Optional[Dict[str, str]]: Resultado da busca em fontes da internet
        """
        # Implementar integração com busca na internet aqui
        return None
    
    def formatar_resposta(self, resultado: Dict) -> str:
        """
        Formata resposta final seguindo padrões profissionais de transparência.
        """
        resposta = resultado.get("resposta", "")
        fontes = resultado.get("fontes", [])
        estrategia = resultado.get("estrategia_usada", "")
        raciocinio = resultado.get("raciocinio", "")
        consultores = resultado.get("consultores", [])
        
        # SEÇÃO 3: CONSULTORES ESPECIALIZADOS
        # Adiciona APENAS consultores relacionados ao tema buscado
        if consultores:
            resposta += "\n\n---\n"
            resposta += "## 👥 CONSULTORES ESPECIALIZADOS NO TEMA\n\n"
            resposta += "Com base no tema da sua consulta, identifiquei os seguintes consultores especializados:\n\n"
            
            for i, consultor in enumerate(consultores, 1):
                consultor_formatado = self.gerenciador_consultores.formatar_consultor(consultor)
                resposta += f"**Consultor {i}:**\n{consultor_formatado}\n\n"
            
            resposta += "💼 *Para contratar estes consultores, entre em contato diretamente através dos dados informados acima.*\n"
        
        # SEÇÃO 4: DOCUMENTOS CONSULTADOS E LINKS
        # Lista os documentos oficiais consultados com links para download
        if fontes:
            resposta += "\n\n---\n"
            resposta += "## � DOCUMENTOS CONSULTADOS\n\n"
            resposta += "As informações fornecidas foram extraídas dos seguintes documentos oficiais do Sebrae:\n\n"
            
            for i, fonte in enumerate(sorted(fontes), 1):
                # Remove extensão e formata nome do arquivo
                nome_arquivo = fonte
                
                # Cria link para download (ajustar path conforme necessário)
                # Assumindo estrutura: dados/documentos/categoria/arquivo.pdf
                link_download = f"/documentos/{fonte}"
                
                resposta += f"{i}. **{nome_arquivo}**\n"
                resposta += f"   📥 [Clique aqui para baixar]({link_download})\n\n"
            
            resposta += "\n� *Estes documentos contêm informações detalhadas sobre Fichas Técnicas (FT) e Manuais de Operacionalização (MOA).*\n"
        
        # Adiciona transparência sobre estratégia utilizada (rodapé)
        resposta += "\n\n---\n"
        
        if estrategia == "base_interna_oficial":
            resposta += "✅ *Resposta baseada em documentos oficiais Sebrae*\n"
        elif estrategia == "busca_ampla_com_resultados_parciais":
            resposta += "🔍 *Resposta baseada em busca ampla - informações parciais*\n"
        elif estrategia == "nenhuma_informacao_encontrada":
            resposta += "❓ *Informação não encontrada na base de conhecimento oficial*\n"
        
        # Rodapé com próximos passos
        if consultores or fontes:
            resposta += "\n✨ **Precisa de mais ajuda?** Posso fornecer informações adicionais sobre produtos e serviços do Sebrae."
        else:
            resposta += "\n💡 **Quer aprofundar?** Posso ajudar a conectar você com consultores especializados ou identificar cursos específicos do Sebrae para sua necessidade."
        
        return resposta