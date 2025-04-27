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

        resgate_result = area_resgate(m)  # passa a instância mapeador

        if resgate_result == "resgate":
            middle()

        chegada_meio = middle()

        if chegada_meio == "sul":
            resgate()


