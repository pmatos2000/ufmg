# coding: utf-8
# Realiza o pré processamento dos dados


import os
import HD
import csv



def get_caminhos(pasta):
    """
        Descrição:
            Retorna uma lista com todos os caminhos para os aquivos do diretorio (pasta) no formato csv
        Parâmetro:
            pasta:
                Diretorio onde está os arquivos
        Utilização:
            get_caminhos(dir)
    """
    arquivos = os.listdir(pasta)
    arquivos = [arq for arq in arquivos if arq.lower().endswith(".csv")]
    arquivos.sort()
    caminhos = [pasta + cam for cam in arquivos]
    return caminhos
    
def busca_dados(dados, serial):
    for d in dados:
        if d.get_serial() == serial:
            return d
    return None
    
    
def processa(caminhos):
    dados = []
    for caminho in caminhos:
        print(caminho)
        arq =  csv.DictReader(open(caminho))
        for l in arq:
            serial = l["serial_number"]
            falha = (l['failure'] == '1')
            d = busca_dados(dados, serial)        
            if (d is None): # Novo HD
                if falha == False:
                    modelo = l["model"]
                    data_ini = l["date"]
                    capacidade = l["capacity_bytes"]
                    hd = HD.HD(serial = serial, modelo = modelo, capacidade = capacidade, data_ini = data_ini)
                    dados.append(hd)
            elif falha == True : # Atualiza a data do erro
                data_fim = l["date"]
                d.setDataFim(data_fim = data_fim)
    return dados
            

def pre(pasta):
    caminhos = get_caminhos(pasta)
    return processa(caminhos)
        
def salva_pre(pasta, dados):
    arq_saida = pasta + "pre.csv"
    arq = csv.writer(open(arq_saida, "wb"))
    arq.writerow(["serial","modelo","capacidade","data__ini","data_fim","falha","dias_falha"])
    for d in dados:
        serial = d.get_serial()
        modelo = d.get_modelo()
        capacidade = d.get_capacidade()
        data_ini = d.get_data_ini().strftime("%Y-%m-%d")
        data_fim = "" if (d.get_data_fim() is None) else (d.get_data_fim().strftime("%Y-%m-%d"))
        falha = "1" if (d.get_falha()) else "0"
        dias_falhas = str(d.get_dias_falhas())
        arq.writerow([serial,modelo,capacidade,data_ini,data_fim,falha,dias_falhas])
    
        
        
    
        
def main():
    dir_entrada = "./../base de dados/dados/"
    dir_saida = './../base de dados/pre/'
    dados = pre(pasta = dir_entrada)
    salva_pre(pasta = dir_saida, dados = dados)
    
# Descomente para executar     
# main()
