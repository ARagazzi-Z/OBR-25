from imports import *
from gyro import *
from line import branco_dir_RGB, branco_esq_RGB, verde_dir_RGB, verde_esq_RGB, preto_dir_RGB, preto_esq_RGB

    
def resgate():
    lr, lg, lb = lscor.rgb()
    rr, rg, rb = rscor.rgb()

    lmedia = (lr + lg + lb) / 3
    rmedia = (rr + rg + rb) / 3

    if branco_esq_RGB() > lmedia > preto_esq_RGB():
        return "resgate1"
    elif branco_dir_RGB() > rmedia > preto_dir_RGB():
        return "resgate2"
    
def middle():
    robot.straight(450)
    gyro_90
    if ultras.distance() <= 50:
        gyro_180