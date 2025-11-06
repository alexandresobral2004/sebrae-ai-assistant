from typing import List, Dict, Optional
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import json
import os
from datetime import datetime
import hashlib

class BaseConhecimento:
    """Gerencia o armazenamento e recuperação de documentos usando ChromaDB."""
    
    def __init__(self, diretorio_persistencia: str = ".chromadb"):
        """
        Inicializa a base de conhecimento com ChromaDB.
        
        Args:
            diretorio_persistencia: Diretório para persistir o banco de dados vetorial
        """
        self.diretorio_persistencia = diretorio_persistencia
        self.client = chromadb.PersistentClient(
            path=diretorio_persistencia
        )
        self.embedding_function = SentenceTransformerEmbeddingFunction(model_name='distiluse-base-multilingual-cased-v2')
        self.collection = self.client.get_or_create_collection(
            "documentos_sebrae",
            embedding_function=self.embedding_function
        )
        
        # Arquivo de controle de documentos processados
        self.arquivo_controle = os.path.join(diretorio_persistencia, "documentos_processados.json")
        self.documentos_processados = self._carregar_controle()
        
    def adicionar_documentos(self, documentos: List[Dict[str, any]]):
        """
        Adiciona chunks de documentos à base de conhecimento.
        
        Args:
            documentos: Lista de chunks de documentos com metadados
        """
        import hashlib

        textos = [doc["texto"] for doc in documentos]
        metadados = [doc["metadados"] for doc in documentos]
        
        # Gera IDs únicos para cada chunk usando um hash do caminho e do ID do chunk
        ids = [
            hashlib.sha256(
                f"{meta['caminho']}_{meta['chunk_id']}".encode()
            ).hexdigest()
            for meta in metadados
        ]
        
        self.collection.add(
            documents=textos,
            metadatas=metadados,
            ids=ids
        )
    
    def buscar(self, consulta: str, num_resultados: int = 3) -> List[Dict]:
        """
        Busca documentos relevantes na base de conhecimento.
        
        Args:
            consulta: A consulta de busca
            num_resultados: Número de resultados a retornar
            
        Returns:
            Lista de documentos relevantes com metadados
        """
        resultados = self.collection.query(
            query_texts=[consulta],
            n_results=num_resultados
        )
        
        documentos = []
        for i in range(len(resultados['documents'][0])):
            documentos.append({
                "texto": resultados['documents'][0][i],
                "metadados": resultados['metadatas'][0][i],
                "distancia": resultados['distances'][0][i]
            })
        
        return documentos
    
    def buscar_por_palavras_chave(self, palavras_chave: List[str], num_resultados: int = 3) -> List[Dict]:
        """
        Busca documentos por palavras-chave específicas.
        
        Args:
            palavras_chave: Lista de palavras-chave para buscar
            num_resultados: Número de resultados a retornar
            
        Returns:
            Lista de documentos relevantes com metadados
        """
        where_clause = {
            "$or": [
                {"palavras_chave": {"$contains": palavra}}
                for palavra in palavras_chave
            ]
        }
        
        resultados = self.collection.query(
            query_texts=palavras_chave,
            where=where_clause,
            n_results=num_resultados
        )
        
        documentos = []
        for i in range(len(resultados['documents'][0])):
            documentos.append({
                "texto": resultados['documents'][0][i],
                "metadados": resultados['metadatas'][0][i],
                "distancia": resultados['distances'][0][i]
            })
        
        return documentos
    
    def buscar_ampla(self, consulta: str, num_resultados: int = 10) -> List[Dict]:
        """
        Realiza uma busca mais ampla usando diferentes estratégias quando a busca principal falha.
        
        Args:
            consulta: A consulta de busca
            num_resultados: Número de resultados a retornar
            
        Returns:
            Lista de documentos relevantes encontrados em busca ampla
        """
        # Tenta busca com termos individuais da consulta
        termos = consulta.lower().split()
        termos_relevantes = [termo for termo in termos if len(termo) > 3]
        
        todos_resultados = []
        ids_vistos = set()
        
        # Busca por cada termo relevante individualmente
        for termo in termos_relevantes[:3]:  # Limita a 3 termos para evitar muitas consultas
            try:
                resultados = self.collection.query(
                    query_texts=[termo],
                    n_results=5
                )
                
                for i in range(len(resultados['documents'][0])):
                    doc_id = f"{resultados['metadatas'][0][i]['fonte']}_{resultados['metadatas'][0][i]['chunk_id']}"
                    
                    if doc_id not in ids_vistos:
                        todos_resultados.append({
                            "texto": resultados['documents'][0][i],
                            "metadados": resultados['metadatas'][0][i],
                            "distancia": resultados['distances'][0][i],
                            "termo_busca": termo
                        })
                        ids_vistos.add(doc_id)
                        
            except Exception as e:
                print(f"Erro na busca ampla com termo '{termo}': {e}")
                continue
        
        # Ordena por relevância (menor distância = mais relevante)
        todos_resultados.sort(key=lambda x: x["distancia"])
        
        return todos_resultados[:num_resultados]
    
    def _carregar_controle(self) -> Dict:
        """
        Carrega o arquivo de controle de documentos já processados.
        
        Returns:
            Dicionário com informações dos documentos processados
        """
        if os.path.exists(self.arquivo_controle):
            try:
                with open(self.arquivo_controle, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Erro ao carregar controle: {e}")
                return {}
        return {}
    
    def _salvar_controle(self):
        """
        Salva o arquivo de controle de documentos processados.
        """
        try:
            os.makedirs(self.diretorio_persistencia, exist_ok=True)
            with open(self.arquivo_controle, 'w', encoding='utf-8') as f:
                json.dump(self.documentos_processados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erro ao salvar controle: {e}")
    
    def _calcular_hash_arquivo(self, caminho_arquivo: str) -> str:
        """
        Calcula hash MD5 de um arquivo para detectar modificações.
        
        Args:
            caminho_arquivo: Caminho do arquivo
            
        Returns:
            Hash MD5 do arquivo
        """
        hash_md5 = hashlib.md5()
        try:
            with open(caminho_arquivo, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"❌ Erro ao calcular hash de {caminho_arquivo}: {e}")
            return ""
    
    def arquivo_ja_processado(self, caminho_arquivo: str) -> bool:
        """
        Verifica se um arquivo já foi processado e não foi modificado.
        
        Args:
            caminho_arquivo: Caminho do arquivo a verificar
            
        Returns:
            True se o arquivo já foi processado e não foi modificado
        """
        if caminho_arquivo not in self.documentos_processados:
            return False
        
        # Verifica se o arquivo ainda existe
        if not os.path.exists(caminho_arquivo):
            return False
        
        # Verifica se o hash mudou (arquivo foi modificado)
        hash_atual = self._calcular_hash_arquivo(caminho_arquivo)
        hash_salvo = self.documentos_processados[caminho_arquivo].get("hash", "")
        
        return hash_atual == hash_salvo
    
    def marcar_arquivo_processado(self, caminho_arquivo: str, num_chunks: int = 0):
        """
        Marca um arquivo como processado no controle.
        
        Args:
            caminho_arquivo: Caminho do arquivo processado
            num_chunks: Número de chunks gerados do arquivo
        """
        self.documentos_processados[caminho_arquivo] = {
            "hash": self._calcular_hash_arquivo(caminho_arquivo),
            "data_processamento": datetime.now().isoformat(),
            "num_chunks": num_chunks
        }
        self._salvar_controle()
    
    def adicionar_documentos_incrementalmente(self, documentos: List[Dict[str, any]], caminho_arquivo: str = None):
        """
        Adiciona documentos de forma incremental, verificando se já foram processados.
        
        Args:
            documentos: Lista de chunks de documentos com metadados
            caminho_arquivo: Caminho do arquivo de origem (opcional)
        """
        # Se foi fornecido um caminho e o arquivo já foi processado, pula
        if caminho_arquivo and self.arquivo_ja_processado(caminho_arquivo):
            print(f"⏭️ Arquivo já processado: {os.path.basename(caminho_arquivo)}")
            return
        
        # Adiciona os documentos
        self.adicionar_documentos(documentos)
        
        # Marca como processado se foi fornecido o caminho
        if caminho_arquivo:
            self.marcar_arquivo_processado(caminho_arquivo, len(documentos))
            print(f"✅ Arquivo processado: {os.path.basename(caminho_arquivo)} ({len(documentos)} chunks)")
    
    def obter_estatisticas(self) -> Dict:
        """
        Obtém estatísticas da base de conhecimento.
        
        Returns:
            Dicionário com estatísticas
        """
        total_documentos = self.collection.count()
        arquivos_processados = len(self.documentos_processados)
        
        return {
            "total_chunks": total_documentos,
            "total_arquivos": arquivos_processados,
            "arquivos": [
                {
                    "caminho": caminho,
                    "data": info.get("data_processamento", "N/A"),
                    "chunks": info.get("num_chunks", 0)
                }
                for caminho, info in self.documentos_processados.items()
            ]
        }
    
    def limpar_base(self):
        """
        Limpa completamente a base de dados e o controle.
        ⚠️ CUIDADO: Esta operação é irreversível!
        """
        try:
            # Deleta a coleção
            self.client.delete_collection("documentos_sebrae")
            
            # Recria a coleção
            self.collection = self.client.get_or_create_collection(
                "documentos_sebrae",
                embedding_function=self.embedding_function
            )
            
            # Limpa o controle
            self.documentos_processados = {}
            self._salvar_controle()
            
            print("✅ Base de conhecimento limpa com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao limpar base: {e}")
    
    def remover_arquivo(self, caminho_arquivo: str):
        """
        Remove um arquivo específico da base de dados.
        
        Args:
            caminho_arquivo: Caminho do arquivo a remover
        """
        try:
            # Remove do controle
            if caminho_arquivo in self.documentos_processados:
                del self.documentos_processados[caminho_arquivo]
                self._salvar_controle()
                
                # Nota: ChromaDB não tem uma maneira fácil de deletar por metadados
                # Seria necessário reprocessar toda a base excluindo este arquivo
                print(f"⚠️ Arquivo removido do controle: {caminho_arquivo}")
                print("   Para remover completamente, reconstrua a base sem este arquivo")
            else:
                print(f"❌ Arquivo não encontrado no controle: {caminho_arquivo}")
                
        except Exception as e:
            print(f"❌ Erro ao remover arquivo: {e}")