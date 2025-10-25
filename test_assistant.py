#!/usr/bin/env python3
"""
Script de teste para verificar se o assistente está funcionando corretamente.
"""

import os
from dotenv import load_dotenv
from src.assistant import AssistenteSebrae

def test_assistant():
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verifica se a API key está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERRO: Variável OPENAI_API_KEY não encontrada no arquivo .env")
        print("   Configure sua chave da API OpenAI para usar com GitHub Copilot")
        return False
    
    try:
        # Testa inicialização do assistente
        print("🔄 Inicializando assistente...")
        assistente = AssistenteSebrae()
        print("✅ Assistente inicializado com sucesso!")
        
        # Verifica se há documentos para carregar
        diretorio_docs = "./dados/documentos"
        if os.path.exists(diretorio_docs):
            documentos = []
            for root, _, files in os.walk(diretorio_docs):
                for file in files:
                    if file.lower().endswith(('.pdf', '.docx', '.xlsx')):
                        documentos.append(file)
            
            if documentos:
                print(f"📁 Encontrados {len(documentos)} documentos para processar")
                print("🔄 Carregando documentos...")
                assistente.carregar_documentos(diretorio_docs)
                print("✅ Documentos carregados com sucesso!")
                
                # Testa uma consulta simples
                print("\n🔄 Testando consulta...")
                resposta = assistente.processar_consulta("O que é o Sebrae?")
                
                if resposta and resposta.get("resposta"):
                    print("✅ Consulta processada com sucesso!")
                    print(f"📝 Resposta: {resposta['resposta'][:100]}...")
                else:
                    print("❌ ERRO: Não foi possível processar a consulta")
                    return False
            else:
                print("⚠️  Nenhum documento encontrado para processar")
                print("   Coloque arquivos PDF, DOCX ou XLSX na pasta dados/documentos")
        else:
            print("⚠️  Diretório de documentos não encontrado")
            print("   Criando diretório dados/documentos...")
            os.makedirs(diretorio_docs, exist_ok=True)
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testando Assistente Sebrae IA")
    print("=" * 50)
    
    sucesso = test_assistant()
    
    print("\n" + "=" * 50)
    if sucesso:
        print("🎉 Todos os testes passaram! O assistente está funcionando.")
        print("💡 Agora você pode executar: streamlit run app.py")
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")