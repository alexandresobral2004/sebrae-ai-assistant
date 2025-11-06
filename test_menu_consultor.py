"""
Script de teste para o sistema de menu do Consultor Virtual Sebrae
Testa os 3 cenários principais:
1. Primeira interação (deve exibir menu)
2. Consulta à base de dados (modo 1)
3. Conversa livre com LLM (modo 2)
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.assistant import AssistenteSebrae
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def print_separator():
    print("\n" + "="*80 + "\n")

def test_menu_sistema():
    """Testa o sistema de menu do Consultor Virtual"""
    
    print("🧪 INICIANDO TESTES DO CONSULTOR VIRTUAL SEBRAE\n")
    
    # Inicializa o assistente
    print("📦 Inicializando assistente...")
    assistente = AssistenteSebrae()
    
    # Carrega documentos
    print("📚 Carregando documentos da base de conhecimento...")
    diretorio_docs = "./dados/documentos"
    
    if os.path.exists(diretorio_docs):
        assistente.carregar_documentos(diretorio_docs)
        print("✅ Documentos carregados com sucesso!\n")
    else:
        print(f"⚠️ Diretório {diretorio_docs} não encontrado. Continuando sem documentos...\n")
    
    print_separator()
    
    # ========================
    # TESTE 1: Primeira Interação (Menu)
    # ========================
    print("📋 TESTE 1: Primeira Interação - Deve exibir o menu")
    print("-" * 80)
    print("Usuário envia: (string vazia para simular primeira interação)")
    
    resultado1 = assistente.processar_consulta("")
    print(resultado1["resposta"])
    
    print_separator()
    
    # ========================
    # TESTE 2: Modo 1 - Consulta Base de Dados
    # ========================
    print("📋 TESTE 2: Modo 1 - Consulta à Base de Dados Sebrae")
    print("-" * 80)
    print("Usuário digita: 1")
    
    resultado2 = assistente.processar_consulta("1")
    print(resultado2["resposta"])
    
    print("\n" + "-" * 80)
    print("Usuário digita: Como abrir um MEI?")
    
    resultado3 = assistente.processar_consulta("1 Como abrir um MEI?")
    print(resultado3["resposta"])
    
    # Exibe consultores encontrados
    if resultado3.get("consultores"):
        print("\n👨‍💼 CONSULTORES RECOMENDADOS:")
        for consultor in resultado3["consultores"][:3]:
            print(f"  • {consultor.get('nome', 'N/A')} - {consultor.get('especialidade', 'N/A')}")
    
    # Exibe fontes
    if resultado3.get("fontes"):
        print("\n📄 FONTES CONSULTADAS:")
        for fonte in resultado3["fontes"][:3]:
            print(f"  • {fonte}")
    
    print_separator()
    
    # ========================
    # TESTE 3: Modo 2 - Conversa Livre com LLM
    # ========================
    print("📋 TESTE 3: Modo 2 - Conversa Livre com Inteligência Artificial")
    print("-" * 80)
    print("Usuário digita: 2")
    
    resultado4 = assistente.processar_consulta("2")
    print(resultado4["resposta"])
    
    print("\n" + "-" * 80)
    print("Usuário digita: Dicas para aumentar vendas no e-commerce")
    
    resultado5 = assistente.processar_consulta("2 Dicas para aumentar vendas no e-commerce")
    print(resultado5["resposta"])
    
    print_separator()
    
    # ========================
    # TESTE 4: Consulta sem especificar modo (deve usar modo 2)
    # ========================
    print("📋 TESTE 4: Consulta sem especificar modo (deve assumir modo 2)")
    print("-" * 80)
    print("Usuário digita: Como fazer marketing digital eficaz?")
    
    resultado6 = assistente.processar_consulta("Como fazer marketing digital eficaz?")
    print(resultado6["resposta"])
    
    print_separator()
    
    # ========================
    # TESTE 5: Saudação (deve exibir menu)
    # ========================
    print("📋 TESTE 5: Saudação inicial (deve exibir menu)")
    print("-" * 80)
    print("Usuário digita: Olá")
    
    resultado7 = assistente.processar_consulta("olá")
    print(resultado7["resposta"])
    
    print_separator()
    
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("\n📊 RESUMO:")
    print(f"  • Teste 1 (Menu): {'✅ PASSOU' if 'BEM-VINDO' in resultado1['resposta'] else '❌ FALHOU'}")
    print(f"  • Teste 2 (Modo 1 - Apenas '1'): {'✅ PASSOU' if 'selecionado' in resultado2['resposta'] else '❌ FALHOU'}")
    print(f"  • Teste 3 (Modo 1 - Consulta): {'✅ PASSOU' if resultado3['resposta'] else '❌ FALHOU'}")
    print(f"  • Teste 4 (Modo 2 - Apenas '2'): {'✅ PASSOU' if 'selecionado' in resultado4['resposta'] else '❌ FALHOU'}")
    print(f"  • Teste 5 (Modo 2 - Consulta): {'✅ PASSOU' if resultado5['resposta'] else '❌ FALHOU'}")
    print(f"  • Teste 6 (Sem modo): {'✅ PASSOU' if resultado6['resposta'] else '❌ FALHOU'}")
    print(f"  • Teste 7 (Saudação): {'✅ PASSOU' if 'BEM-VINDO' in resultado7['resposta'] else '❌ FALHOU'}")

if __name__ == "__main__":
    test_menu_sistema()
