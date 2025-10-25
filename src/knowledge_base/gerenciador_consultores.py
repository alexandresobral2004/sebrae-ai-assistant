"""
Módulo para gerenciar e buscar consultores especializados do Sebrae.
"""

import pandas as pd
import os
from typing import List, Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class GerenciadorConsultores:
    """
    Classe responsável por carregar e buscar consultores especializados
    na base de dados do Sebrae.
    """
    
    def __init__(self, caminho_consultores: str = None):
        """
        Inicializa o gerenciador de consultores.
        
        Args:
            caminho_consultores: Caminho para a pasta de consultores
        """
        if caminho_consultores is None:
            # Caminho correto: vai de src/knowledge_base para a raiz, depois para dados/documentos/Consultores
            caminho_consultores = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "dados", "documentos", "Consultores"
            )
        
        self.caminho_consultores = Path(caminho_consultores)
        self.consultores_carregados = {}
        self._carregar_consultores()
    
    def _carregar_consultores(self):
        """
        Carrega todos os arquivos de consultores da pasta.
        """
        if not self.caminho_consultores.exists():
            logger.warning(f"Pasta de consultores não encontrada: {self.caminho_consultores}")
            return
        
        logger.info("Carregando consultores...")
        
        arquivos_encontrados = list(self.caminho_consultores.glob("*.xlsx"))
        
        for arquivo in arquivos_encontrados:
            try:
                # Extrai a área de especialização do nome do arquivo
                nome_arquivo = arquivo.stem
                partes = nome_arquivo.split("_")
                
                if len(partes) >= 2:
                    area_principal = partes[0]
                    subespecialidade = "_".join(partes[1:])
                else:
                    area_principal = nome_arquivo
                    subespecialidade = ""
                
                # Carrega os dados do Excel
                df = pd.read_excel(arquivo)
                
                # Processa os dados dos consultores
                consultores_arquivo = self._processar_dados_excel(df, area_principal, subespecialidade)
                
                if consultores_arquivo:
                    chave_area = f"{area_principal}_{subespecialidade}".lower()
                    self.consultores_carregados[chave_area] = {
                        'area_principal': area_principal.replace('_', ' '),
                        'subespecialidade': subespecialidade.replace('_', ' '),
                        'consultores': consultores_arquivo,
                        'arquivo_origem': arquivo.name
                    }
                    
            except Exception as e:
                logger.error(f"Erro ao carregar arquivo {arquivo.name}: {str(e)}")
        
        logger.info(f"Carregados {len(self.consultores_carregados)} grupos de consultores")
    
    def _processar_dados_excel(self, df: pd.DataFrame, area: str, subespecialidade: str) -> List[Dict]:
        """
        Processa os dados do DataFrame do Excel e extrai informações dos consultores.
        
        Args:
            df: DataFrame com dados dos consultores
            area: Área principal de atuação
            subespecialidade: Subespecialidade
            
        Returns:
            Lista de dicionários com dados dos consultores
        """
        consultores = []
        
        # Mapeia possíveis nomes de colunas (considerando variações)
        mapeamento_colunas = {
            'nome': ['nome', 'consultor', 'nome_consultor', 'nome do consultor', 'equipe técnica', 'equipe_tecnica'],
            'email': ['email', 'e-mail', 'e_mail', 'correio', 'e-mail 01'],
            'telefone': ['telefone', 'fone', 'celular', 'contato', 'telefone 01', 'telefone do profissional'],
            'cidade': ['cidade', 'localidade', 'municipio', 'município'],
            'estado': ['estado', 'uf', 'regiao', 'região'],
            'razao_social': ['razao social', 'razão social', 'empresa'],
            'cnpj': ['cnpj'],
            'area_empresa': ['área da empresa', 'area da empresa'],
            'subarea_empresa': ['subárea da empresa', 'subarea da empresa'],
            'natureza_servico': ['natureza da prestação de serviço', 'natureza servico'],
            'endereco': ['rua', 'endereço', 'endereco'],
            'bairro': ['bairro'],
            'cep': ['cep'],
            'escritorio_regional': ['escritório regional', 'escritorio regional'],
            'representante_legal': ['nome do representante legal', 'representante legal']
        }
        
        # Identifica as colunas disponíveis
        colunas_encontradas = {}
        df_columns_lower = [col.lower() for col in df.columns]
        
        for campo, possiveis_nomes in mapeamento_colunas.items():
            for possivel_nome in possiveis_nomes:
                if possivel_nome in df_columns_lower:
                    indice = df_columns_lower.index(possivel_nome)
                    colunas_encontradas[campo] = df.columns[indice]
                    break
        
        # Processa cada linha do DataFrame
        for idx, row in df.iterrows():
            try:
                # Verifica se a linha tem dados válidos
                if pd.isna(row).all():
                    continue
                
                consultor = {
                    'area_principal': area.replace('_', ' '),
                    'subespecialidade': subespecialidade.replace('_', ' '),
                }
                
                # Extrai dados das colunas identificadas
                for campo, coluna in colunas_encontradas.items():
                    valor = row[coluna]
                    if pd.notna(valor):
                        consultor[campo] = str(valor).strip()
                
                # Verifica se tem pelo menos nome/equipe técnica ou razão social
                if consultor.get('nome') or consultor.get('razao_social'):
                    consultores.append(consultor)
                    
            except Exception as e:
                logger.warning(f"Erro ao processar linha {idx}: {str(e)}")
                continue
        
        return consultores
    
    def buscar_consultores(self, termo_busca: str, limite: int = 5) -> List[Dict]:
        """
        Busca consultores relacionados ao termo de busca.
        
        Args:
            termo_busca: Termo para buscar consultores
            limite: Número máximo de consultores a retornar
            
        Returns:
            Lista de consultores encontrados
        """
        termo_busca = termo_busca.lower()
        consultores_encontrados = []
        
        # Busca em todas as áreas carregadas
        for chave_area, dados_area in self.consultores_carregados.items():
            # Verifica se o termo está na área principal ou subespecialidade
            area_principal = dados_area['area_principal'].lower()
            subespecialidade = dados_area['subespecialidade'].lower()
            
            relevancia = 0
            
            # Calcula relevância baseada na correspondência
            if termo_busca in area_principal:
                relevancia += 3
            if termo_busca in subespecialidade:
                relevancia += 2
            
            # Busca por palavras-chave específicas
            palavras_termo = termo_busca.split()
            for palavra in palavras_termo:
                if len(palavra) > 2:  # Ignora palavras muito pequenas
                    if palavra in area_principal:
                        relevancia += 1
                    if palavra in subespecialidade:
                        relevancia += 1
            
            # Se encontrou relevância, adiciona os consultores
            if relevancia > 0:
                for consultor in dados_area['consultores']:
                    consultor_completo = consultor.copy()
                    consultor_completo['relevancia'] = relevancia
                    consultor_completo['arquivo_origem'] = dados_area['arquivo_origem']
                    consultores_encontrados.append(consultor_completo)
        
        # Ordena por relevância e limita o resultado
        consultores_encontrados.sort(key=lambda x: x['relevancia'], reverse=True)
        return consultores_encontrados[:limite]
    
    def buscar_por_area(self, area: str) -> List[Dict]:
        """
        Busca consultores por área específica.
        
        Args:
            area: Nome da área para buscar
            
        Returns:
            Lista de consultores da área
        """
        area_normalizada = area.lower().replace(' ', '_')
        consultores_area = []
        
        for chave_area, dados_area in self.consultores_carregados.items():
            if area_normalizada in chave_area:
                for consultor in dados_area['consultores']:
                    consultor_completo = consultor.copy()
                    consultor_completo['arquivo_origem'] = dados_area['arquivo_origem']
                    consultores_area.append(consultor_completo)
        
        return consultores_area
    
    def formatar_consultor(self, consultor: Dict) -> str:
        """
        Formata os dados de um consultor para exibição.
        
        Args:
            consultor: Dicionários com dados do consultor
            
        Returns:
            String formatada com dados do consultor
        """
        formatacao = []
        
        # Nome/Empresa
        if consultor.get('nome'):
            formatacao.append(f"👤 **{consultor['nome']}**")
        elif consultor.get('razao_social'):
            formatacao.append(f"🏢 **{consultor['razao_social']}**")
        
        # Área de especialização
        if consultor.get('area_principal'):
            area_completa = consultor['area_principal']
            if consultor.get('subespecialidade'):
                area_completa += f" - {consultor['subespecialidade']}"
            formatacao.append(f"🎯 **Especialidade:** {area_completa}")
        
        # Área da empresa se disponível
        if consultor.get('area_empresa'):
            area_info = consultor['area_empresa']
            if consultor.get('subarea_empresa'):
                area_info += f" - {consultor['subarea_empresa']}"
            formatacao.append(f"🏭 **Área de Atuação:** {area_info}")
        
        # Contatos
        contatos = []
        if consultor.get('email'):
            contatos.append(f"📧 {consultor['email']}")
        if consultor.get('telefone'):
            contatos.append(f"📱 {consultor['telefone']}")
        
        if contatos:
            formatacao.append(f"📞 **Contato:** {' | '.join(contatos)}")
        
        # Localização
        localizacao = []
        if consultor.get('cidade'):
            localizacao.append(consultor['cidade'])
        if consultor.get('estado'):
            localizacao.append(consultor['estado'])
        
        if localizacao:
            formatacao.append(f"📍 **Localização:** {' - '.join(localizacao)}")
        
        # Escritório Regional
        if consultor.get('escritorio_regional'):
            formatacao.append(f"� **Escritório Regional:** {consultor['escritorio_regional']}")
        
        # Natureza do serviço
        if consultor.get('natureza_servico'):
            formatacao.append(f"⚙️ **Serviços:** {consultor['natureza_servico']}")
        
        # Representante Legal
        if consultor.get('representante_legal'):
            formatacao.append(f"👔 **Representante:** {consultor['representante_legal']}")
        
        return "\n".join(formatacao)
    
    def obter_estatisticas(self) -> Dict:
        """
        Retorna estatísticas sobre os consultores carregados.
        
        Returns:
            Dicionário com estatísticas
        """
        total_consultores = sum(len(dados['consultores']) for dados in self.consultores_carregados.values())
        total_areas = len(self.consultores_carregados)
        
        areas_disponiveis = []
        for dados in self.consultores_carregados.values():
            area_nome = dados['area_principal']
            if dados['subespecialidade']:
                area_nome += f" - {dados['subespecialidade']}"
            areas_disponiveis.append(area_nome)
        
        return {
            'total_consultores': total_consultores,
            'total_areas': total_areas,
            'areas_disponiveis': sorted(areas_disponiveis)
        }