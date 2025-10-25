#!/usr/bin/env python3
"""
Teste do Consultor IA Sebrae com metodologia Chain of Thought profissional.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.assistant import AssistenteSebrae
import logging

# Configurar logging para ver o fluxo
logging.basicConfig(level=logging.INFO)

def teste_metodologia_profissional():
    """Testa a nova metodologia profissional Chain of Thought."""
    
    print("🎯 TESTE: CONSULTOR IA SEBRAE - METODOLOGIA PROFISSIONAL")
    print("=" * 70)
    
    # Inicializar assistente
    print("\n1. Inicializando Consultor IA Sebrae...")
    assistant = AssistenteSebrae()
    
    # Casos de teste profissionais
    casos_teste = [
        {
            "consulta": "Como abrir um MEI para uma loja de roupas?",
            "esperado": "Resposta oficial com FTs específicas"
        },
        {
            "consulta": "Quais são os benefícios do CNAE para comércio eletrônico?",
            "esperado": "Informações técnicas específicas"
        },
        {
            "consulta": "Como funciona machine learning para negócios?",
            "esperado": "Expertise em IA + informações Sebrae se disponível"
        }
    ]
    
    for i, caso in enumerate(casos_teste, 1):
        print(f"\n{i}. TESTE: {caso['consulta']}")
        print("-" * 50)
        
        try:
            resultado = assistant.processar_consulta(caso["consulta"])
            resposta_formatada = assistant.formatar_resposta(resultado)
            
            print("RESPOSTA PROFISSIONAL:")
            print(resposta_formatada)
            
            print(f"\nESTRATÉGIA UTILIZADA: {resultado.get('estrategia_usada', 'N/A')}")
            print(f"DOCUMENTOS CONSULTADOS: {resultado.get('num_documentos_consultados', 0)}")
            
            if resultado.get('raciocinio'):
                print(f"CHAIN OF THOUGHT: ✓ Presente")
            
            print("\n" + "="*70)
            
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            print("="*70)

if __name__ == "__main__":
    teste_metodologia_profissional()