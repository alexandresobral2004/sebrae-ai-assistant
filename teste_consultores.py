#!/usr/bin/env python3
"""
Teste da funcionalidade de busca de consultores especializados.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.knowledge_base.gerenciador_consultores import GerenciadorConsultores

def teste_gerenciador_consultores():
    """Testa o carregamento e busca de consultores."""
    
    print("🔍 TESTE: GERENCIADOR DE CONSULTORES SEBRAE")
    print("=" * 50)
    
    # Inicializar gerenciador
    print("\n1. Inicializando Gerenciador de Consultores...")
    gerenciador = GerenciadorConsultores()
    
    # Verificar estatísticas
    stats = gerenciador.obter_estatisticas()
    print(f"📊 Total de consultores carregados: {stats['total_consultores']}")
    print(f"📂 Total de áreas: {stats['total_areas']}")
    
    # Mostrar algumas áreas disponíveis
    print(f"\n📋 Algumas áreas disponíveis:")
    for i, area in enumerate(stats['areas_disponiveis'][:5], 1):
        print(f"   {i}. {area}")
    
    # Testes de busca
    casos_teste = [
        "marketing digital",
        "gestão financeira", 
        "tecnologia",
        "turismo",
        "sustentabilidade"
    ]
    
    print(f"\n🔍 TESTES DE BUSCA:")
    print("-" * 30)
    
    for termo in casos_teste:
        print(f"\n🎯 Buscando: '{termo}'")
        consultores = gerenciador.buscar_consultores(termo, limite=2)
        
        if consultores:
            print(f"✅ Encontrados {len(consultores)} consultores")
            for i, consultor in enumerate(consultores, 1):
                print(f"\n   Consultor {i}:")
                consultor_formatado = gerenciador.formatar_consultor(consultor)
                print("   " + consultor_formatado.replace("\n", "\n   "))
        else:
            print("❌ Nenhum consultor encontrado")
        
        print("-" * 30)

if __name__ == "__main__":
    teste_gerenciador_consultores()