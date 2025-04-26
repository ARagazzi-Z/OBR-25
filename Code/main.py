from imports import *
from line import *
from gyro import *
from rescue import *

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

        resgate_result = area_resgate()

        if resgate_result == "resgate1" and "resgate2":
            middle()

        chegada_meio = middle()

        if chegada_meio == "sul":
            resgate()

        
            