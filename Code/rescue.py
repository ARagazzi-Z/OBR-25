from imports import *
from gyro import *
from line import branco_dir_RGB, branco_esq_RGB, verde_dir_RGB, verde_esq_RGB, preto_dir_RGB, preto_esq_RGB

    
def area_resgate():
    lr, lg, lb = lscor.rgb()
    rr, rg, rb = rscor.rgb()

    lmedia = (lr + lg + lb) / 3
    rmedia = (rr + rg + rb) / 3

    if branco_esq_RGB() > lmedia > preto_esq_RGB():
        return "resgate1"
    elif branco_dir_RGB() > rmedia > preto_dir_RGB():
        return "resgate2"

def vitima_morta(lscor):
    r, g, b = lscor.rgb()
    return r < 30 and g < 30 and g < 30

def vitima_viva(lscor):
    r, g, b = lscor.rgb()
    media = (r + g + b) / 3
    return media > 60 and abs(r - g) < 10 and abs(g - b) < 10 and abs(r - b) < 10 # Essas três checagens garantem que as cores estejam bem próximas umas das outras.
#  Isso é típico de cores como o prata, onde não há dominância de vermelho, verde ou azul — todos têm valores parecidos.

def resgate():
    count = 0
    ball = 0
    while count < 36:
        gyro_10()
        wait(100)
        if ultras.distance() < 40 : # distancia para detectar a bolinha 
            robot.straight(ultras.distance() - 50)
            if vitima_morta():
                robot.straight(-50)
                gyro_180()
                robot.straight(-70) # estará bem próximo da vítima
                gyro_10()
                robot.straight(-50)
                ball += 1
            elif vitima_viva():
                robot.straight(-50)
                gyro_180()
                robot.straight(-70) # estará bem próximo da vítima
                gyro_10neg()
                robot.straight(-50)
                ball += 1
        
        count += 1
    if ball == 3:

    

def middle():
    robot.straight(450)
    gyro_90 # vira para direita
    if ultras.distance() <= 50: # se for na direita 
        gyro_180()
        robot.straight(450)
    elif ultras.distance() >50:
        robot.straight(450)
        cm.angle(90) # ativa o sensor de cor para vitimas