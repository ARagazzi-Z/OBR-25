from imports import *
from line import *
from gyro import *
from rescue import *
from rescue import Mapeador  # importar a classe Mapeador

m = Mapeador()  # instância para armazenar a posição

def main():
    while True:
        evento = line_RGB()

        if evento == "obstacle":
            obstacle()

        if evento == "beco":
            beco_sem_saida()

        if evento == "verde1":
            verde1_RGB()
        
        if evento == "TX na direita":
            TX_dir_RGB()

        if evento == "TX na esquerda":
            TX_esq_RGB()

        if evento == "X sem verde":
            X_preto_RGB()

        resgate_result = area_resgate(m)  # passa a instância mapeador

        if resgate_result == "resgate":
            middle()

        m = Mapeador

        if middle() == "radar":
            m.radar()

        if m.radar() == 'detecção das vitimas':
            m.condensar_objeto()

        if m.condensar_objeto() == 'resgate das vitimas':
            m.resgatar_vitima()

        if m.resgatar_vitima() == 'resgate das vitimas concluído':
            triangulos()

        if triangulos() == 'sair':
            saida()

        if saida() == 'saida com sucesso':
            print("Saída com sucesso!")
            
        