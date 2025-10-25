#!/usr/bin/env python3
"""
Teste completo do sistema com busca de consultores integrada.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from src.assistant import AssistenteSebrae
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def teste_sistema_completo():
    """Testa o sistema completo com busca de consultores."""
    
    print("🎯 TESTE: SISTEMA COMPLETO COM CONSULTORES")
    print("=" * 60)
    
    # Inicializar assistente
    print("\n1. Inicializando Consultor IA Sebrae...")
    try:
        assistant = AssistenteSebrae()
        print("✅ Assistente inicializado com sucesso!")
        
        # Verificar consultores carregados
        stats = assistant.gerenciador_consultores.obter_estatisticas()
        print(f"📊 Consultores carregados: {stats['total_consultores']}")
        print(f"📂 Áreas disponíveis: {stats['total_areas']}")
        
    except Exception as e:
        print(f"❌ Erro na inicialização: {str(e)}")
        return
    
    # Casos de teste específicos
    casos_teste = [
        {
            "consulta": "Preciso de ajuda com turismo de aventura",
            "espera_consultores": True
        },
        {
            "consulta": "Como fazer marketing digital para minha empresa?",
            "espera_consultores": True
        },
        {
            "consulta": "Questões legais sobre direito civil",
            "espera_consultores": True
        }
    ]
    
    for i, caso in enumerate(casos_teste, 1):
        print(f"\n{i}. TESTE: {caso['consulta']}")
        print("-" * 50)
        
        try:
            # Processar consulta
            resultado = assistant.processar_consulta(caso["consulta"])
            
            # Formatar resposta
            resposta_formatada = assistant.formatar_resposta(resultado)
            
            print("RESPOSTA COMPLETA:")
            print(resposta_formatada)
            
            # Verificar se encontrou consultores
            consultores = resultado.get('consultores', [])
            if consultores:
                print(f"\n✅ Consultores encontrados: {len(consultores)}")
            else:
                print(f"\n⚠️ Nenhum consultor encontrado para este tema")
            
            print(f"\nESTRATÉGIA: {resultado.get('estrategia_usada', 'N/A')}")
            
            print("\n" + "="*60)
            
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            print("="*60)

if __name__ == "__main__":
    teste_sistema_completo()