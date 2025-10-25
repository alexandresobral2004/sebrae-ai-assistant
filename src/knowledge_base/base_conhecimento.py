from typing import List, Dict, Optional
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class BaseConhecimento:
    """Gerencia o armazenamento e recuperação de documentos usando ChromaDB."""
    
    def __init__(self, diretorio_persistencia: str = ".chromadb"):
        """
        Inicializa a base de conhecimento com ChromaDB.
        
        Args:
            diretorio_persistencia: Diretório para persistir o banco de dados vetorial
        """
        self.client = chromadb.PersistentClient(
            path=diretorio_persistencia
        )
        self.embedding_function = SentenceTransformerEmbeddingFunction(model_name='distiluse-base-multilingual-cased-v2')
        self.collection = self.client.get_or_create_collection(
            "documentos_sebrae",
            embedding_function=self.embedding_function
        )
        
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