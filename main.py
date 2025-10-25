import os
from dotenv import load_dotenv
from src.assistant import AssistenteSebrae # Corrigido o nome do módulo e da classe

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env

def main():
    # Inicializa o assistente
    assistente = AssistenteSebrae() # Instancia a classe com o nome correto
    
    # Define o diretório de documentos
    diretorio_docs = "./dados/documentos"
    
    # Verifica se o diretório existe
    if not os.path.exists(diretorio_docs):
        print(f"\nCriando diretório para documentos em: {diretorio_docs}")
        os.makedirs(diretorio_docs)
        print("\nPor favor, coloque seus documentos (PDF, DOCX, XLSX) no diretório 'dados/documentos' e execute novamente.")
        return
        
    # Verifica se há documentos no diretório
    documentos = [f for f in os.listdir(diretorio_docs) if f.lower().endswith(('.pdf', '.docx', '.xlsx'))]
    if not documentos:
        print("\nNenhum documento encontrado no diretório 'dados/documentos'.")
        print("Por favor, adicione documentos PDF, DOCX ou XLSX e execute novamente.")
        return
    
    print(f"\nEncontrados {len(documentos)} documentos para processar.")
    print("Iniciando carregamento e processamento dos documentos...")
    
    # Carrega os documentos
    assistente.carregar_documentos(diretorio_docs)
    
    print("\nAssistente pronto para responder suas perguntas!")
    print("Dica: Suas perguntas serão respondidas com informações dos documentos e palavras-chave relacionadas.")
    
    # Loop principal
    while True:
        # Obtém input do usuário
        consulta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        
        if consulta.lower() == 'sair':
            break
        
        # Processa a consulta
        dados_resposta = assistente.processar_consulta(consulta)
        
        # Formata e exibe a resposta
        resposta_formatada = assistente.formatar_resposta(dados_resposta)
        print("\nResposta:", resposta_formatada)

if __name__ == "__main__":
    main()