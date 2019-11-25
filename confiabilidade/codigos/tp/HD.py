

import datetime 

class HD:
    def __init__(self, serial, modelo, capacidade, data_ini):
        self.serial = serial
        self.modelo = modelo
        self.data_ini = datetime.datetime.strptime(data_ini,'%Y-%m-%d')
        self.data_fim = None
        self.capacidade = capacidade
        self.falha = False;
        self.dias_falha = 0;
        
        
    def __repr__(self):
        r = "HD(serial: {0}, modelo: {1}, Tam: {2}, Ini: {3}, Fim: {4}, Falha: {5}, Dias: {6})"
        return r.format(self.serial,
                        self.modelo,
                        self.capacidade,
                        self.data_ini.strftime("%Y-%m-%d"),
                        None if (self.data_fim is None) else self.data_fim.strftime("%Y-%m-%d"),
                        self.falha,
                        self.dias_falha)
        
    def get_serial(self):
        return self.serial
    
    def get_modelo(self):
        return self.modelo
    
    def get_data_ini(self):
        return self.data_ini
    
    def get_data_fim(self):
        return self.data_fim
    
    def get_falha(self):
        return  self.falha
    
    def get_capacidade(self):
        return self.capacidade
    
    def get_dias_falhas(self):
        return self.dias_falha
    
    def setDataFim(self, data_fim):
        self.data_fim =  datetime.datetime.strptime(data_fim,'%Y-%m-%d')
        self.dias_falha = (self.data_fim - self.data_ini).days
        self.falha = True
