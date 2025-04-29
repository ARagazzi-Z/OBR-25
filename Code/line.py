from imports import *
from gyro import gyro_180, gyro_90, gyro_90neg, gyro_10, gyro_10neg
from gyro import mgyro_10, mgyro_10neg

def line_REFLEC():

    p = 3
    # P (Proporcional): Multiplica o erro por kp para corrigir a direção.
    i = 0
    # I (Integral): Acumula pequenos erros ao longo do tempo.
    d = 6.5
    # D (Derivada): Reage a mudanças rápidas no erro para evitar oscilações.

    last_error = 0
    integral = 0

    while True:
        error = lscor.reflection() - rscor.reflection()
        P = error * p
        integral += error
        I = integral * i
        D = (error - last_error)* d
        turn = P + I + D 
        
        last_error = error #atualiza o erro
        speed = 30 

        robot.drive(speed, turn)

def verde1_REFLEC():
        
        count = 0
        bcount = 0
        tcount = 0
        xcount = 0

    # LEITURA DO VERDE
    # 1 VERDE
        # viu verde primeiro, sendo que está depois do preto **
        # viu verde primeiro, sendo que está antes do preto
        if (lscor.color() == Color.GREEN) != (rscor.color() == Color.GREEN):
            if lscor.color() == Color.GREEN:
                count += 1 
            elif rscor.color() == Color.GREEN:
                count += 1 
            else:
                count = 0
        else:
            count = 0

        if count == 3:
            if lscor.color() == Color.GREEN:
                    robot.straight(30)
                    gyro_90neg()
            elif rscor.color() == Color.GREEN:
                    robot.straight(30)
                    gyro_90()
                    count = 0

def beco_REFLEC():
     
        # beco sem saída
    if lscor.color() == Color.GREEN and rscor.color() == Color.GREEN:
        bcount += 1 
    else: 
        bcount = 0
        
    if bcount == 3:
        gyro_180()
        robot.straight(20)
    else:
        bcount = 0

def T_REFLEC():
            
        # INTERSEÇÃO onde não tem marcador verde
            # INTERSEÇÃO T 
        if (lscor.color() == Color.BLACK) and (rscor.color() == Color.WHITE):
            tcount += 1
        else:
            tcount = 0

        if (rscor.color() == Color.BLACK) and (lscor.color() == Color.WHITE):
            tcount += 1
        else:
            tcount = 0

        if tcount == 3:
            if (rscor.color() == Color.BLACK) and (lscor.color() == Color.WHITE):
                while lscor.color != Color.BLACK: 
                    mgyro_10()
                tcount = 0

            elif (lscor.color() == Color.BLACK) and (rscor.color() == Color.WHITE):
                while rscor.color != Color.BLACK: 
                    mgyro_10neg()
                tcount = 0

            else: 
                tcount = 0
        else:
            pass

def x_REFLEC():

            # INTERSEÇÃO X
        if (lscor.color() == Color.BLACK) and (rscor.color() == Color.BLACK):
            xcount += 1
        else:
            xcount = 0
        
        if xcount == 3:
            robot.straight(30)
        else:
            pass

def obstacle():
    robot.straight(-20)
    gyro_90()
    robot.straight(80)
    gyro_90neg()
    robot.straight(200)
    gyro_90neg()
    robot.straight(80)
    gyro_90()
    robot.straight(-50)

def line_RGB():
    
    kp = 0.8
    # P (Proporcional): Multiplica o erro por kp para corrigir a direção.
    ki = 0.01
    # I (Integral): Acumula pequenos erros ao longo do tempo.
    kd = 1.2
    # D (Derivada): Reage a mudanças rápidas no erro para evitar oscilações.

    last_error = 0
    integral = 0

    while True:
    
        # Lê os valores RGB dos sensores
        rgb_lscor = lscor.rgb()
        rgb_rscor = rscor.rgb()

        # Calcula o erro com base no vermelho (R)
        r_lscor,_,_ = rgb_lscor
        r_rscor,_,_ = rgb_rscor
        error = r_lscor - r_rscor

        # Calcula o valor integral e derivada para PID
        integral += error
        P = error * kp
        I = integral * ki
        D = (error - last_error)* kd
        turn = P + I + D 
        
        last_error = error #atualiza o erro
        speed = 30 

        lm.dc(speed + turn)
        rm.dc(speed - turn)

        wait(10)
        
        if ultras.distance() <= 50:
            return "obstacle"
        
        if verde_esq_RGB(lscor) and verde_dir_RGB(rscor):
            return "beco"

        if verde_esq_RGB(lscor) != verde_dir_RGB(rscor):
            return "verde1"
        
        if preto_esq_RGB() and branco_dir_RGB():
            return "TX na esquerda"

        if preto_dir_RGB() and branco_esq_RGB():
            return "TX na direita"
        
        if preto_esq_RGB() and preto_dir_RGB():
            return "X sem verde"
    
def branco_dir_RGB(rscor):
    r, g, b = rscor.rgb()
    media = (r + g + b) / 3
    if media > 60:
        return True
    else:
        return False

def branco_esq_RGB(lscor):
    r, g, b = lscor.rgb()
    media = (r + g + b) / 3
    if media > 60:
        return True
    else:
       return False

def preto_esq_RGB(lscor):
    r, g, b = lscor.rgb()
    media = (r + g + b) / 3
    return media < 20
            # NÃO É NECESSÁRIO USAR COMO ARGUMENTO O SENSOR NESSE CASO

def preto_dir_RGB(rscor):
    r, g, b = rscor.rgb()
    media = (r + g + b) / 3
    return media < 20
            # NÃO É NECESSÁRIO USAR COMO ARGUMENTO O SENSOR NESSE CASO

"""
Função para detectar se a cor verde está presente no valor RGB fornecido.

Argumento:
    rgb: Tupla com os valores RGB lidos do sensor de cor.
    
Retorno:
    True se a cor dominante for verde, False caso contrário.
"""

    # Lógica para identificar o verde:
    # O valor de "g" (verde) deve ser maior que o de "r" (vermelho) e "b" (azul),
    # e o valor de verde (g) deve ser suficientemente alto para garantir que é verde.


    # Desempacota os valores RGB

# Lógica para identificar o verde na esquerda:
def verde_esq_RGB(lscor):

    r, g, b = lscor.rgb()

    return g > 50 and g > r + 10 and g > b + 10
            # NÃO É NECESSÁRIO USAR COMO ARGUMENTO O SENSOR NESSE CASO

# Lógica para identificar o verde na direita:
def verde_dir_RGB(rscor):

    r, g, b = rscor.rgb()

    return g > 50 and g > r + 10 and g > b + 10
            # NÃO É NECESSÁRIO USAR COMO ARGUMENTO O SENSOR NESSE CASO

def beco_sem_saida(lscor, rscor):
        robot.straight(20) #se o verde é antes ou depois da interseção
        if preto_dir_RGB(rscor) and preto_esq_RGB(lscor):
            gyro_180()
            robot.straight(50)
        else:
            pass
            # NÃO É NECESSÁRIO USAR COMO ARGUMENTO O SENSOR NESSE CASO

def verde1_RGB():
    verde_dir = verde_dir_RGB()
    verde_esq = verde_esq_RGB()

    robot.straight(30) # se o verde é antes ou depois da interseção
    if preto_esq_RGB() and branco_dir_RGB(): # se o verde é na esq
        gyro_90neg()
    elif preto_dir_RGB() and branco_esq_RGB(): # se o verde é na dir
        gyro_90()
    elif preto_esq_RGB() and preto_dir_RGB(): # se é interseção de +
        if verde_dir:
            gyro_90()
        elif verde_esq:
           gyro_90()
    else:
        robot.straight(-30)

def TX_dir_RGB():
        turn = 0
        gyro.reset_angle(0)
        while not preto_esq_RGB() == True:
            gyro_10()
            wait(10)
        turn = gyro.angle()
        if abs(turn) < 90:
            robot.turn(turn * (-1))
        elif abs(turn) >= 90:
            turn = turn - 90
            robot.turn(turn)

def TX_esq_RGB():
    if preto_esq_RGB() and branco_dir_RGB():    
        turn = 0
        gyro.reset_angle(0)
        while not preto_esq_RGB() == True:
            gyro_10neg()
            wait(10)
        turn = gyro.angle()
        if abs(turn) < 90:
            robot.turn(turn * (-1))
        elif abs(turn) >= 90:
            turn = abs(turn) - 90
            robot.turn(turn)

def X_preto_RGB():
    if preto_esq_RGB() and preto_dir_RGB():
        robot.straight(30)
