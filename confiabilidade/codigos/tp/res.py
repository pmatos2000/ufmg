# coding: utf-8

import csv

class Res:
    def __init__(self, nome, total, total_falhas, menor, maior, media): 
        self.nome = nome
        self.total = total
        self.total_falhas = total_falhas
        self.ponc_falha = total_falhas/float(total) * 100
        self.menor = menor 
        self.maior = maior
        self.media = media
    
    def get_linha_cvs(self):
        return [str(self.nome),
                str(self.total),
                str(self.total_falhas),
                str(self.ponc_falha),
                str(self.menor),
                str(self.maior),
                str(self.media)]
        

def salva_lista_res(arquivo, res):
    arq = csv.writer(open(arquivo, "wb"))
    arq.writerow(["nome","total","total_falha","ponc_falha","menor","maior","media"])
    for r in res:
        arq.writerow(r.get_linha_cvs())
        