from typing import Optional, Dict, List
from .knowledge_base.base_conhecimento import BaseConhecimento
from .knowledge_base.processador_documentos import ProcessadorDocumentos
import google.generativeai as genai
import os

# Configure a API Key do Gemini
# É uma boa prática usar variáveis de ambiente para chaves de API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

class Assistente:
    def __init__(self, diretorio_base: str = ".chromadb"):
        """
        Inicializa o Assistente Sebrae com sua identidade e base de conhecimento.

        Args:
            diretorio_base: Diretório para o banco de dados vetorial
        """
        self.model = genai.GenerativeModel('gemini-pro') if GOOGLE_API_KEY else None
        self.nome = "Consultor Sebrae IA"
        self.missao = "Fornecer informações precisas e úteis sobre produtos, serviços e consultorias de negócios do Sebrae"
        
        # Inicializa componentes da base de conhecimento
        self.base_conhecimento = BaseConhecimento(diretorio_base)
        self.processador_documentos = ProcessadorDocumentos()
        
    def carregar_documentos(self, diretorio_docs: str, ignorar_arquivos: set = set()):
        """
        Carrega documentos de um diretório para a base de conhecimento.

        Args:
            diretorio_docs: Caminho do diretório com os documentos
            ignorar_arquivos: Um conjunto de caminhos de arquivos a serem ignorados.
        """
        print("Processando documentos...")
        chunks = self.processador_documentos.processar_diretorio(diretorio_docs, ignorar_arquivos=ignorar_arquivos)
        if not chunks:
            print("Nenhum documento novo para processar.")
            return
            
        print(f"Adicionando {len(chunks)} chunks à base de conhecimento...")
        self.base_conhecimento.adicionar_documentos(chunks)
        print("Documentos carregados com sucesso!")
        
    def processar_consulta(self, consulta: str) -> Dict[str, Optional[str]]:
        """
        Processa consultas do usuário seguindo a ordem de prioridade:
        1. Base de conhecimento local (RAG)
        2. Busca na internet (fallback)
        3. Resposta de não encontrado

        Args:
            consulta: A pergunta ou pedido do usuário

        Returns:
            Dict[str, Optional[str]]: Resposta contendo texto e fonte
        """
        if not self.model:
            return {
                "resposta": "A chave de API do Google não foi configurada. Verifique a variável de ambiente GOOGLE_API_KEY.",
                "fonte": None,
                "palavras_chave": []
            }

        # Primeira prioridade: Verificar base de conhecimento local
        resultados = self.base_conhecimento.buscar(consulta)
        if resultados:
            contexto = "\n---\n".join([r["texto"] for r in resultados])
            fonte = resultados[0]["metadados"]["fonte"]
            
            prompt = f"""
            Você é o '{self.nome}', um assistente de IA do Sebrae. Sua missão é: '{self.missao}'.
            Com base no contexto abaixo, responda à pergunta do usuário de forma clara, objetiva e amigável.
            
            Contexto dos documentos:
            ---
            {contexto}
            ---
            
            Pergunta do usuário: "{consulta}"
            
            Resposta:
            """
            resposta_gerada = self.model.generate_content(prompt).text
            return {
                "resposta": resposta_gerada,
                "fonte": fonte,
                "palavras_chave": [] # Pode ser gerado pelo Gemini também
            }
        
        # Segunda prioridade: Busca na internet
        resultado_internet = self._buscar_internet(consulta)
        if resultado_internet:
            return {
                "resposta": resultado_internet["resposta"],
                "fonte": None,
                "palavras_chave": []
            }
        
        # Terceira prioridade: Resposta de não encontrado
        return {
            "resposta": f"Não consegui encontrar informações ou produtos específicos sobre '{consulta}' em minha base de dados ou em fontes públicas no momento.",
            "fonte": None,
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
    
    def formatar_resposta(self, dados_resposta: Dict[str, Optional[str]]) -> str:
        """
        Formata a resposta final de acordo com as diretrizes de estilo.
        
        Args:
            dados_resposta: Dados da resposta incluindo texto e fonte
            
        Returns:
            str: Resposta formatada
        """
        resposta = dados_resposta["resposta"]
        fonte = dados_resposta.get("fonte")
        palavras_chave = dados_resposta.get("palavras_chave", [])
        
        texto_formatado = resposta
        
        # Adiciona palavras-chave se disponíveis
        if palavras_chave:
            texto_formatado += "\n\nPalavras-chave relacionadas: " + ", ".join(palavras_chave)
        
        # Adiciona citação da fonte se disponível
        if fonte:
            texto_formatado += f"\n\n(Fonte: [{fonte}])"
            
        return texto_formatado