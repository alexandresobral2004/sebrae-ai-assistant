#!/usr/bin/env python3
"""
Script para gerenciar a base de conhecimento do Assistente Sebrae
Permite adicionar, atualizar e verificar documentos sem recriar toda a base
"""

import os
import sys
from typing import List
from src.knowledge_base.base_conhecimento import BaseConhecimento
from src.knowledge_base.processador_documentos import ProcessadorDocumentos

# Cores para output no terminal
class Cores:
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    AZUL = '\033[94m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'

def exibir_menu():
    """Exibe o menu principal."""
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}╔═══════════════════════════════════════════════════════╗")
    print("║   GERENCIADOR DE BASE DE CONHECIMENTO SEBRAE       ║")
    print(f"╚═══════════════════════════════════════════════════════╝{Cores.RESET}\n")
    
    print("Escolha uma opção:\n")
    print(f"{Cores.VERDE}1.{Cores.RESET} 📚 Processar novos documentos (incremental)")
    print(f"{Cores.VERDE}2.{Cores.RESET} 📊 Ver estatísticas da base")
    print(f"{Cores.VERDE}3.{Cores.RESET} 🔍 Verificar arquivo específico")
    print(f"{Cores.VERDE}4.{Cores.RESET} ➕ Adicionar arquivo único")
    print(f"{Cores.VERDE}5.{Cores.RESET} 🗑️  Limpar base completamente")
    print(f"{Cores.VERDE}6.{Cores.RESET} 📋 Listar arquivos processados")
    print(f"{Cores.VERDE}0.{Cores.RESET} ❌ Sair\n")

def processar_diretorio_incremental(base: BaseConhecimento, processador: ProcessadorDocumentos, diretorio: str):
    """Processa todos os documentos no diretório de forma incremental."""
    print(f"\n{Cores.AZUL}📂 Processando diretório: {diretorio}{Cores.RESET}\n")
    
    if not os.path.exists(diretorio):
        print(f"{Cores.VERMELHO}❌ Diretório não encontrado!{Cores.RESET}")
        return
    
    novos = 0
    pulados = 0
    erros = 0
    
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            if file.endswith(('.pdf', '.docx', '.xlsx', '.txt', '.md')):
                file_path = os.path.join(root, file)
                
                # Verifica se já foi processado
                if base.arquivo_ja_processado(file_path):
                    print(f"{Cores.AMARELO}⏭️  Pulando: {file} (já processado){Cores.RESET}")
                    pulados += 1
                    continue
                
                try:
                    print(f"{Cores.AZUL}⏳ Processando: {file}...{Cores.RESET}", end=" ")
                    
                    # Processa o arquivo
                    chunks = processador.processar_arquivo(file_path)
                    
                    # Adiciona à base
                    base.adicionar_documentos_incrementalmente(chunks, file_path)
                    
                    print(f"{Cores.VERDE}✅ ({len(chunks)} chunks){Cores.RESET}")
                    novos += 1
                    
                except Exception as e:
                    print(f"{Cores.VERMELHO}❌ Erro: {str(e)}{Cores.RESET}")
                    erros += 1
    
    print(f"\n{Cores.NEGRITO}📊 Resultado:{Cores.RESET}")
    print(f"  {Cores.VERDE}✅ Novos processados: {novos}{Cores.RESET}")
    print(f"  {Cores.AMARELO}⏭️  Pulados: {pulados}{Cores.RESET}")
    print(f"  {Cores.VERMELHO}❌ Erros: {erros}{Cores.RESET}\n")

def exibir_estatisticas(base: BaseConhecimento):
    """Exibe estatísticas da base de conhecimento."""
    stats = base.obter_estatisticas()
    
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}📊 ESTATÍSTICAS DA BASE{Cores.RESET}\n")
    print(f"Total de chunks: {Cores.VERDE}{stats['total_chunks']}{Cores.RESET}")
    print(f"Total de arquivos: {Cores.VERDE}{stats['total_arquivos']}{Cores.RESET}\n")
    
    if stats['arquivos']:
        print(f"{Cores.NEGRITO}Arquivos processados:{Cores.RESET}\n")
        for idx, arquivo_info in enumerate(stats['arquivos'], 1):
            nome = os.path.basename(arquivo_info['caminho'])
            print(f"  {idx}. {nome}")
            print(f"     Data: {arquivo_info['data']}")
            print(f"     Chunks: {arquivo_info['chunks']}\n")
    else:
        print(f"{Cores.AMARELO}Nenhum arquivo processado ainda.{Cores.RESET}\n")

def verificar_arquivo(base: BaseConhecimento, caminho: str):
    """Verifica se um arquivo já foi processado."""
    if not os.path.exists(caminho):
        print(f"{Cores.VERMELHO}❌ Arquivo não encontrado: {caminho}{Cores.RESET}")
        return
    
    ja_processado = base.arquivo_ja_processado(caminho)
    nome = os.path.basename(caminho)
    
    if ja_processado:
        print(f"\n{Cores.VERDE}✅ Arquivo JÁ PROCESSADO: {nome}{Cores.RESET}")
        
        if caminho in base.documentos_processados:
            info = base.documentos_processados[caminho]
            print(f"   Data: {info.get('data_processamento', 'N/A')}")
            print(f"   Chunks: {info.get('num_chunks', 0)}")
            print(f"   Hash: {info.get('hash', 'N/A')[:16]}...\n")
    else:
        print(f"\n{Cores.AMARELO}⚠️  Arquivo NÃO PROCESSADO: {nome}{Cores.RESET}")
        print(f"   Execute a opção 1 ou 4 para processar este arquivo.\n")

def adicionar_arquivo_unico(base: BaseConhecimento, processador: ProcessadorDocumentos, caminho: str):
    """Adiciona um único arquivo à base."""
    if not os.path.exists(caminho):
        print(f"{Cores.VERMELHO}❌ Arquivo não encontrado: {caminho}{Cores.RESET}")
        return
    
    nome = os.path.basename(caminho)
    
    if base.arquivo_ja_processado(caminho):
        print(f"{Cores.AMARELO}⚠️  Arquivo já foi processado anteriormente: {nome}{Cores.RESET}")
        resposta = input("Deseja reprocessar? (s/n): ").lower()
        if resposta != 's':
            print(f"{Cores.AZUL}Operação cancelada.{Cores.RESET}")
            return
    
    try:
        print(f"\n{Cores.AZUL}⏳ Processando: {nome}...{Cores.RESET}")
        
        # Processa o arquivo
        chunks = processador.processar_arquivo(caminho)
        
        # Adiciona à base (força reprocessamento removendo do controle antes)
        if caminho in base.documentos_processados:
            del base.documentos_processados[caminho]
        
        base.adicionar_documentos_incrementalmente(chunks, caminho)
        
        print(f"{Cores.VERDE}✅ Arquivo processado com sucesso!{Cores.RESET}")
        print(f"   Chunks gerados: {len(chunks)}\n")
        
    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro ao processar arquivo: {str(e)}{Cores.RESET}\n")

def limpar_base(base: BaseConhecimento):
    """Limpa completamente a base de conhecimento."""
    print(f"\n{Cores.VERMELHO}{Cores.NEGRITO}⚠️  ATENÇÃO: Esta operação irá apagar TODA a base de conhecimento!{Cores.RESET}")
    confirmacao = input("Digite 'CONFIRMAR' para prosseguir: ")
    
    if confirmacao != "CONFIRMAR":
        print(f"{Cores.AZUL}Operação cancelada.{Cores.RESET}")
        return
    
    try:
        base.limpar_base()
        print(f"{Cores.VERDE}✅ Base limpa com sucesso!{Cores.RESET}\n")
    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro ao limpar base: {str(e)}{Cores.RESET}\n")

def listar_arquivos_processados(base: BaseConhecimento):
    """Lista todos os arquivos que foram processados."""
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}📋 ARQUIVOS PROCESSADOS{Cores.RESET}\n")
    
    if not base.documentos_processados:
        print(f"{Cores.AMARELO}Nenhum arquivo processado ainda.{Cores.RESET}\n")
        return
    
    for idx, (caminho, info) in enumerate(base.documentos_processados.items(), 1):
        nome = os.path.basename(caminho)
        print(f"{idx}. {Cores.VERDE}{nome}{Cores.RESET}")
        print(f"   Caminho: {caminho}")
        print(f"   Data: {info.get('data_processamento', 'N/A')}")
        print(f"   Chunks: {info.get('num_chunks', 0)}")
        print()

def main():
    """Função principal do gerenciador."""
    # Configurações
    DIRETORIO_BASE = ".chromadb"
    DIRETORIO_DOCS = "./dados/documentos"
    
    # Inicializa componentes
    print(f"{Cores.AZUL}🔧 Inicializando base de conhecimento...{Cores.RESET}")
    base = BaseConhecimento(DIRETORIO_BASE)
    processador = ProcessadorDocumentos()
    print(f"{Cores.VERDE}✅ Pronto!{Cores.RESET}")
    
    while True:
        exibir_menu()
        opcao = input(f"{Cores.NEGRITO}Digite sua escolha: {Cores.RESET}")
        
        if opcao == "1":
            processar_diretorio_incremental(base, processador, DIRETORIO_DOCS)
            
        elif opcao == "2":
            exibir_estatisticas(base)
            
        elif opcao == "3":
            caminho = input("\nDigite o caminho do arquivo: ").strip()
            verificar_arquivo(base, caminho)
            
        elif opcao == "4":
            caminho = input("\nDigite o caminho do arquivo: ").strip()
            adicionar_arquivo_unico(base, processador, caminho)
            
        elif opcao == "5":
            limpar_base(base)
            
        elif opcao == "6":
            listar_arquivos_processados(base)
            
        elif opcao == "0":
            print(f"\n{Cores.AZUL}👋 Até logo!{Cores.RESET}\n")
            break
            
        else:
            print(f"\n{Cores.VERMELHO}❌ Opção inválida!{Cores.RESET}\n")
        
        input(f"\n{Cores.AMARELO}Pressione ENTER para continuar...{Cores.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Operação interrompida pelo usuário.{Cores.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro fatal: {str(e)}{Cores.RESET}\n")
        sys.exit(1)
