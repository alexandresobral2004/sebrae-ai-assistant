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