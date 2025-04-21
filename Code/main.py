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

        resgate = resgate()

        if resgate == "resgate1" and "resgate2":
            middle()