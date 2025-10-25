#!/usr/bin/env python3
"""
Teste do sistema melhorado de busca e resposta.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_improved_system():
    """Testa o sistema melhorado."""
    try:
        from src.assistant import AssistenteSebrae
        
        print("🔍 Testando sistema melhorado...")
        assistente = AssistenteSebrae()
        
        # Testa uma consulta
        print("\n📝 Testando consulta: 'Como fazer um plano de marketing?'")
        resultado = assistente.processar_consulta("Como fazer um plano de marketing?")
        
        print(f"\n✅ Resposta gerada!")
        print(f"📊 Documentos consultados: {resultado.get('num_documentos_consultados', 0)}")
        print(f"📚 Fontes: {len(resultado.get('fontes', []))}")
        
        resposta_formatada = assistente.formatar_resposta(resultado)
        print(f"\n📄 Resposta formatada: {len(resposta_formatada)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Teste do Sistema Melhorado")
    print("=" * 50)
    
    if test_improved_system():
        print("\n🎉 Sistema melhorado funcionando!")
    else:
        print("\n❌ Problema no sistema melhorado.")