#!/usr/bin/env python3
"""
Teste rápido para verificar se as variáveis de ambiente estão sendo carregadas corretamente.
"""

import os
from dotenv import load_dotenv

def test_env_loading():
    print("🔍 Testando carregamento de variáveis de ambiente...")
    
    # Carrega o .env
    load_dotenv()
    
    # Verifica se a variável foi carregada
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        print(f"✅ OPENAI_API_KEY carregada: {api_key[:10]}...")
        return True
    else:
        print("❌ OPENAI_API_KEY não encontrada")
        return False

def test_assistant_import():
    print("\n🔍 Testando importação do assistente...")
    
    try:
        from src.assistant import AssistenteSebrae
        print("✅ AssistenteSebrae importado com sucesso")
        
        # Tenta inicializar
        assistente = AssistenteSebrae()
        print("✅ AssistenteSebrae inicializado com sucesso")
        
        # Testa uma consulta simples
        if assistente.client:
            print("✅ Cliente OpenAI configurado corretamente")
            return True
        else:
            print("❌ Cliente OpenAI não configurado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao importar/inicializar: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Teste de Diagnóstico - Variáveis de Ambiente")
    print("=" * 60)
    
    env_ok = test_env_loading()
    assistant_ok = test_assistant_import()
    
    print("\n" + "=" * 60)
    if env_ok and assistant_ok:
        print("🎉 Todos os testes passaram! O sistema deve funcionar.")
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")