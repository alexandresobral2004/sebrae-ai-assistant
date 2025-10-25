#!/usr/bin/env python3
"""
Teste básico para verificar se o código está funcionando.
"""

import os
import sys

def test_basic_imports():
    """Testa imports básicos."""
    try:
        print("🔄 Testando imports básicos...")
        
        # Testa import do streamlit
        import streamlit
        print("✅ Streamlit importado com sucesso")
        
        # Testa se o arquivo .env existe
        if os.path.exists(".env"):
            print("✅ Arquivo .env encontrado")
        else:
            print("❌ Arquivo .env não encontrado")
            return False
        
        # Testa se a estrutura do projeto está correta
        if os.path.exists("src/assistant.py"):
            print("✅ Arquivo src/assistant.py encontrado")
        else:
            print("❌ Arquivo src/assistant.py não encontrado")
            return False
            
        if os.path.exists("src/knowledge_base/base_conhecimento.py"):
            print("✅ Arquivo base_conhecimento.py encontrado")
        else:
            print("❌ Arquivo base_conhecimento.py não encontrado")
            return False
        
        # Verifica se há documentos
        docs_dir = "dados/documentos"
        if os.path.exists(docs_dir):
            docs = [f for f in os.listdir(docs_dir) if f.endswith(('.pdf', '.docx', '.xlsx'))]
            if docs:
                print(f"✅ Encontrados {len(docs)} documentos para processar")
            else:
                print("⚠️  Nenhum documento encontrado em dados/documentos")
        else:
            print("⚠️  Diretório dados/documentos não existe")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_streamlit_app():
    """Verifica se o app.py pode ser carregado."""
    try:
        print("\n🔄 Verificando sintaxe do app.py...")
        
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Compila o código para verificar sintaxe
        compile(content, "app.py", "exec")
        print("✅ Sintaxe do app.py está correta")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Erro de sintaxe em app.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar app.py: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Teste Básico do Assistente Sebrae IA")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_streamlit_app
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Resultado: {passed}/{len(tests)} testes passaram")
    
    if passed == len(tests):
        print("🎉 Testes básicos passaram!")
        print("💡 Para executar o app: streamlit run app.py")
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")