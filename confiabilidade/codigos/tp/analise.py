# coding: utf-8

import HD
import res
import csv
import numpy
import math
import matplotlib.pyplot as plt

def get_dados(caminho = "./../base de dados/pre/pre.csv"):
    dados  = []
    arq =  csv.DictReader(open(caminho,"rb"))
    for l in arq:
        serial = l["serial"]
        modelo = l["modelo"]
        capacidade = l["capacidade"]
        data_ini = l["data_ini"]
        d = HD.HD(serial = serial, modelo = modelo, capacidade = capacidade, data_ini = data_ini)
        falha = l["falha"]
        if falha == "1":
            data_fim = l["data_fim"]
            d.set_data_fim(data_fim)
        dados.append(d)
    return dados


def get_modelos_dados(dados):
    modelos = []
    for d in dados:
        modelo = d.get_modelo()
        if  not (modelo in modelos):
            modelos.append(modelo)
    modelos.sort()
    return modelos;

def analisa_dados(dados):
    dados_falhas = filter(lambda d: d.get_falha(), dados)
    total = len(dados)
    total_falhas = len(dados_falhas)
    dias_falhas = [d.get_dias_falhas() for d in dados_falhas]
    media_dias_falhas = numpy.median(dias_falhas)
    r = "Total: {0}, falhas: {1} - {2}%, Media de dias entre falhas: {3}"
    r = r.format(total, total_falhas, 100 * total_falhas/float(total), media_dias_falhas)
    print(r)


def get_dic_modelo_marca(caminho = "./../base de dados/pre/map.csv"):
    arq =  csv.DictReader(open(caminho))
    dic_modelo_marca = dict()
    for l in arq:
        modelo = l["modelo"]
        marca = l["marca"]
        dic_modelo_marca[modelo] = marca
    return dic_modelo_marca
    

def gera_vetor_r_real(dados, total_ini,  total_dias):
    r_real = [total_ini] # Salva o total de HD ao longo do tempo
    for i in range(1, total_dias):
        falhas = [d for d in dados if d.get_dias_falhas() == i]
        sobreviveram = r_real[i-1] - len(falhas)
        r_real.append(sobreviveram)
    return r_real
                
        
        
    
def calcula_confiabilidade_exp(dados, pre_fixo, caminho):
    total_dias = 366
    dias  = numpy.arange(total_dias)
    dados_falhas = [d for d in dados if d.get_falha()]
    dias_falhas = [d.get_dias_falhas() for d in dados_falhas]
    total_ini = len(dias_falhas)
    r_real =  gera_vetor_r_real(dados = dados_falhas, total_ini = total_ini, total_dias = total_dias)
    media = numpy.median(dias_falhas)
    #print(media)
    R = lambda t: total_ini * math.exp(-t/media)
    R_vec = numpy.vectorize(R)
    r_calc = R_vec(dias)
    plt.clf()
    plt.plot(dias, r_calc, "b", label = "Estimado - $\lambda$ = " + str(1/media))
    plt.plot(dias, r_real, "r", label = "Dados")
    plt.legend(loc="upper right")
    #plt.show()
    plt.savefig(caminho  + pre_fixo + "_exp.eps", format="eps")

    
    
def analise_modelos(dados, modelos, caminho =  "./../base de dados/saida/"):
    resultados = []
    for m in modelos:
        dados_filtro = [d for d in dados if d.get_modelo() == m]
        dados_falhas = [d for d in dados_filtro if d.get_falha()]
        dias_falhas = [d.get_dias_falhas() for d in dados_falhas]
        nome = m
        total = len(dados_filtro)
        total_falhas = len(dados_falhas)
        menor = min(dias_falhas) if (total_falhas > 0) else 0
        maior = max(dias_falhas) if (total_falhas > 0) else 0
        media = numpy.median(dias_falhas) if (total_falhas > 0) else 0
        r = res.Res(nome = nome, total = total, total_falhas = total_falhas, menor = menor, maior = maior, media = media)
        resultados.append(r)
        
        #Para valores maiores que 30 estima a confiabilidade
        if total_falhas >= 30:
            calcula_confiabilidade_exp(dados = dados_filtro, pre_fixo = nome, caminho = caminho)
        
    res.salva_lista_res(caminho + "modelos.csv", resultados)
    
   
def analise_marcas(dados, modelos, dic, caminho =  "./../base de dados/saida/"):
    resultados = []
    marcas = dic.values()
    marcas = set(marcas) # Remove valores duplicadoss     
    for m in marcas:
        dados_filtro = [d for d in dados if dic[d.get_modelo()] == m]
        dados_falhas = [d for d in dados_filtro if d.get_falha()]
        dias_falhas = [d.get_dias_falhas() for d in dados_falhas]
        nome = m
        total = len(dados_filtro)
        total_falhas = len(dados_falhas)
        menor = min(dias_falhas) if (total_falhas > 0) else 0
        maior = max(dias_falhas) if (total_falhas > 0) else 0
        media = numpy.median(dias_falhas) if (total_falhas > 0) else 0
        r = res.Res(nome = nome, total = total, total_falhas = total_falhas, menor = menor, maior = maior, media = media)
        resultados.append(r)
    res.salva_lista_res(caminho + "marcas.csv", resultados)
    
def analise_capacidades(dados, capacidades, caminho =  "./../base de dados/saida/"):
    resultados = []
    for c in capacidades:
        dados_filtro = [d for d in dados if d.get_capacidade() == c]
        dados_falhas = [d for d in dados_filtro if d.get_falha()]
        dias_falhas = [d.get_dias_falhas() for d in dados_falhas]
        nome = c
        total = len(dados_filtro)
        total_falhas = len(dados_falhas)
        menor = min(dias_falhas) if (total_falhas > 0) else 0
        maior = max(dias_falhas) if (total_falhas > 0) else 0
        media = numpy.median(dias_falhas) if (total_falhas > 0) else 0
        r = res.Res(nome = nome, total = total, total_falhas = total_falhas, menor = menor, maior = maior, media = media)
        resultados.append(r)
    res.salva_lista_res(caminho + "capacidades.csv", resultados)
    

def get_capacidades_dados(dados):
    capacidades = []
    for d in dados:
        cap = d.get_capacidade()
        if  not (cap in capacidades):
            capacidades.append(cap)
    capacidades.sort()
    return capacidades;

def main():
    dados = get_dados()
    modelos = get_modelos_dados(dados = dados)
    dic = get_dic_modelo_marca()
    capacidades = get_capacidades_dados(dados)
    analise_modelos(dados =  dados, modelos = modelos)
    #analise_marcas(dados = dados, modelos = modelos , dic = dic)
    #analise_capacidades(dados = dados, capacidades = capacidades)

main()

