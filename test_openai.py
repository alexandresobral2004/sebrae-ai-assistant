#!/usr/bin/env python3
"""
Teste para verificar a configuração da API OpenAI.
"""

import os
from dotenv import load_dotenv

def test_openai_config():
    """Testa a configuração da API OpenAI."""
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY não encontrada no arquivo .env")
        print("   Configure sua chave da API OpenAI")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ Formato da chave API inválido")
        print("   A chave deve começar com 'sk-'")
        return False
    
    try:
        import openai
        
        client = openai.OpenAI(api_key=api_key)
        
        # Teste simples de conexão
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Diga apenas 'OK' se você está funcionando."}
            ],
            max_tokens=10
        )
        
        if response.choices[0].message.content.strip().upper() == "OK":
            print("✅ API OpenAI configurada e funcionando!")
            return True
        else:
            print("⚠️  API respondeu, mas não como esperado")
            return False
            
    except ImportError:
        print("❌ Biblioteca 'openai' não instalada")
        print("   Execute: pip install openai")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar API: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔑 Testando configuração da API OpenAI")
    print("=" * 50)
    
    if test_openai_config():
        print("\n🎉 Configuração OK! Pode executar o assistente.")
    else:
        print("\n❌ Configuração com problemas. Verifique acima.")