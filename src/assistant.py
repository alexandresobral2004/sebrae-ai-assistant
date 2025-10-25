from typing import Optional, Dict, List
from .knowledge_base.base_conhecimento import BaseConhecimento
from .knowledge_base.processador_documentos import ProcessadorDocumentos
from .knowledge_base.gerenciador_consultores import GerenciadorConsultores
import openai
import os

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
        
    def processar_consulta(self, consulta: str) -> Dict[str, Optional[str]]:
        """
        Processa consultas seguindo metodologia Chain of Thought profissional:
        1. Análise da pergunta
        2. Busca prioritária na base interna
        3. Busca ampla como fallback
        4. Resposta estruturada com transparência de fonte

        Args:
            consulta: A pergunta ou pedido do usuário

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

        # PASSO 1: Análise Chain of Thought da consulta
        analise = self._analisar_consulta(consulta)
        
        # PASSO 2: Busca prioritária na base interna (Regra de Ouro)
        resultados = self.base_conhecimento.buscar(analise["termos_busca"], num_resultados=8)
        
        # PASSO 3: Busca consultores especializados relacionados
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
        
        return resposta_final
    
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

DIRETRIZES DE RESPOSTA:
1. TRANSPARÊNCIA DE FONTE: Seja explícito que está usando documentos oficiais Sebrae
2. EXPERTISE EM IA: Quando relevante, adicione insights sobre IA/dados
3. AÇÃO PRÁTICA: Finalize com recomendação ou próximo passo
4. FOCO EM PRODUTOS/SERVIÇOS: Destaque FTs, MOAs e oportunidades de consultoria"""
                    },
                    {
                        "role": "user",
                        "content": f"""ANÁLISE INICIAL: {analise['raciocinio']}

CONTEXTO DOS DOCUMENTOS OFICIAIS SEBRAE:
{contexto_completo}

PERGUNTA DO ANALISTA: "{consulta}"

INSTRUÇÕES ESPECÍFICAS:
- Inicie mencionando que encontrou informações em documentos oficiais Sebrae
- Use informações de TODOS os documentos relevantes  
- Cite especificamente as Fichas Técnicas (FTs) e MOAs encontrados
- Combine informações complementares
- Destaque oportunidades para contratação de consultores/instrutores
- Finalize com recomendação prática

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
        
        # Adiciona raciocínio Chain of Thought se disponível
        if raciocinio:
            resposta = f"💭 **Análise:** {raciocinio}\n\n{resposta}"
        
        # Adiciona seção de fontes se houver documentos consultados
        if fontes:
            resposta += "\n\n---\n"
            resposta += "📚 **Fontes consultadas:**\n"
            for i, fonte in enumerate(sorted(fontes), 1):
                resposta += f"{i}. {fonte}\n"
        
        # Adiciona seção de consultores especializados se encontrados
        if consultores:
            resposta += "\n\n---\n"
            resposta += "👥 **CONSULTORES ESPECIALIZADOS DISPONÍVEIS:**\n\n"
            
            for i, consultor in enumerate(consultores, 1):
                consultor_formatado = self.gerenciador_consultores.formatar_consultor(consultor)
                resposta += f"**Consultor {i}:**\n{consultor_formatado}\n\n"
            
            resposta += "💼 *Para contratar estes consultores, entre em contato diretamente através dos dados informados acima.*"
        
        # Adiciona transparência sobre estratégia utilizada
        if estrategia == "base_interna_oficial":
            resposta += "\n� *Resposta baseada em documentos oficiais Sebrae*"
        elif estrategia == "busca_ampla_com_resultados_parciais":
            resposta += "\n🔍 *Resposta baseada em busca ampla - informações parciais*"
        elif estrategia == "nenhuma_informacao_encontrada":
            resposta += "\n❓ *Informação não encontrada na base de conhecimento oficial*"
        
        # Rodapé profissional padrão
        resposta += "\n\n---\n"
        if consultores:
            resposta += "✨ **Próximos passos:** Além dos consultores indicados acima, posso ajudar a identificar cursos específicos do Sebrae para sua necessidade."
        else:
            resposta += "💡 **Quer aprofundar?** Posso ajudar a conectar você com consultores especializados ou identificar cursos específicos do Sebrae para sua necessidade."
        
        return resposta