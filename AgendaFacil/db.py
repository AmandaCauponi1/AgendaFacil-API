import csv
import os

def ler(nome_arquivo):
    caminho = f'data/{nome_arquivo}.csv'
    if not os.path.exists(caminho):
        return []
    
    with open(caminho, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        return list(leitor)

def salvar(nome_arquivo, dados):
    caminho = f'data/{nome_arquivo}.csv'
    arquivo_existe = os.path.exists(caminho)
    colunas = list(dados.keys())
    
    with open(caminho, mode='a', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        if not arquivo_existe:
            escritor.writeheader()
        escritor.writerow(dados)

def atualizar_arquivo(nome_arquivo, lista_completa):
    caminho = f'data/{nome_arquivo}.csv'
    
    if not lista_completa:
        open(caminho, 'w').close()
        return

    colunas = list(lista_completa[0].keys())
    
    with open(caminho, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(lista_completa)