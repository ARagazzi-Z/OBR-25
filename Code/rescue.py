from imports import *
from gyro import *
from line import branco_dir_RGB, branco_esq_RGB, verde_dir_RGB, verde_esq_RGB, preto_dir_RGB, preto_esq_RGB

posicao_inicial = 0
    
def area_resgate():
    lr, lg, lb = lscor.rgb()
    rr, rg, rb = rscor.rgb()

    lmedia = (lr + lg + lb) / 3
    rmedia = (rr + rg + rb) / 3

    if branco_esq_RGB() > lmedia > preto_esq_RGB():
        return "resgate1"
    elif branco_dir_RGB() > rmedia > preto_dir_RGB():
        return "resgate2"

def triangulos():
    pass

def saida():
    pass

def detec_parede():
    gyro.reset_angle()
    posicao_inicial = lm.angle()  # pega o ângulo inicial do motor esquerdo

    robot.straight(70)  # tenta andar pra frente
    wait(500) 

    posicao_final = lm.angle()  # pega o ângulo final
    static_gauge()
    if abs(posicao_final - posicao_inicial) < 7:
        robot.stop()
        return True
    else:
        return False

def vitima_morta(lscor):
    r, g, b = lscor.rgb()
    return r < 30 and g < 30 and b < 30

def vitima_viva(lscor):
    r, g, b = lscor.rgb()
    media = (r + g + b) / 3
    return media > 60 and abs(r - g) < 10 and abs(g - b) < 10 and abs(r - b) < 10 # Essas três checagens garantem que as cores estejam bem próximas umas das outras.
    #  Isso é típico de cores como o prata, onde não há dominância de vermelho, verde ou azul — todos têm valores parecidos.

def detec_vitima(distance, victim_status):
    """
    Executa a sequência de manobras para resgatar a vítima.
    victim_status: "morta" ou "viva"
    """
    robot.straight(-50)
    gyro_180()
    robot.straight(-70)  # aproxima da vítima
    if victim_status == "morta":
        gyro_10() # ajeita a posição para a bolinha entrar no lado da caixa
        cm.angle(35) # abre o portao para vitima morta ()
        robot.straight(-70) # entra a bolinha na caixa
        cm.angle(-35) # fecha o portão
        robot.straight(50)
        gyro_10neg()
    elif victim_status == "viva":
        gyro_10neg() # ajeita a posição para a bolinha entrar no lado da caixa
        cm.angle(-35) # abre o portao para vitimas vivas ()
        robot.straight(-70) # entra a bolinha na caixa
        cm.angle(35) # fecha o portão
        robot.straight(50)
        gyro_10()
    else:
        robot.straight(-distance + 50)
        gyro_10()

def resgate():
    count = 0
    ball = 0
    while count < 36: # PRIMEIRA TENTATIVA
        gyro_10()
        wait(100)
        count += 1

        if ultras.distance() <= 40: # distancia para detectar a bolinha 
            distance = ultras.distance()
            robot.straight(distance - 50)

            # Verificando a vítima
            if vitima_morta():
                # Realizando os movimentos quando a vítima é morta
                detec_vitima(distance, "morta")
                ball += 1
                if ball == 3:
                    break
            elif vitima_viva():
                # Realizando os movimentos quando a vítima é viva
                detec_vitima(distance, "viva")
                ball += 1
                if ball == 3:
                    break
            else: # Caso não haja vítima, retorna à posição inicial
                robot.straight(-distance)
                gyro_10()
        else:
            # Caso não detecte a bolinha na distância estabelecida, passa para o próximo movimento
            pass    

    if ball == 3:
        triangulos()
        saida()
    elif count == 36 and ball < 3:
        if ultras.distance() > 45: # se for 120
            robot.straight(35) # ficar a 40 cm da borda do de 120 (45 + 35 = 80 => 120 - 80 = 40) 
            count = 0
            while count < 36: # SEGUNDA TENTATIVA => SE FOR 120 CM
                gyro_10()
                wait(100)
                count += 1
                if ultras.distance() <= 35: # distancia para detectar a bolinha 
                    distance = ultras.distance()
                    robot.straight(ultras.distance() - 50)
                    # Verificando a vítima novamente
                    if vitima_morta():
                        detec_vitima(distance, "morta")
                        ball += 1
                        if ball == 3:
                            break
                    elif vitima_viva():
                        detec_vitima(distance, "viva")
                        ball += 1
                        if ball == 3:
                            break
                    else:
                        robot.straight(-distance)
                        gyro_10()
                else:
                    pass    
        else:
            gyro_90neg()
            if ultras.distance() > 45: # se for 120
                robot.straight(35) # ficar a 40 cm da borda do de 120 (45 + 35 = 80 => 120 - 80 = 40) 
                count = 0
                while count < 36:
                    gyro_10()
                    wait(100)
                    count += 1
                    if ultras.distance() <= 35: # distancia para detectar a bolinha 
                        distance = ultras.distance()
                        robot.straight(ultras.distance() - 50)
                        # Verificando a vítima novamente
                        if vitima_morta():
                            detec_vitima(distance, "morta")
                            ball += 1
                            if ball == 3:
                                break
                        elif vitima_viva():
                            detec_vitima(distance, "viva")
                            ball += 1
                            if ball == 3:
                                break
                        else:
                            robot.straight(-distance)
                            gyro_10()
                    else:
                        pass    

                if ball == 3:
                    triangulos()
                    saida()
                elif count == 36 and ball < 3:
                    triangulos()
                    saida()

            else:
                gyro_180
                if ultras.distance() > 45: # se for 120
                    robot.straight(35) # ficar a 40 cm da borda do de 120 (45 + 35 = 80 => 120 - 80 = 40) 
                    count = 0
                    while count < 36:
                        gyro_10()
                        wait(100)
                        count += 1
                        if ultras.distance() <= 35: # distancia para detectar a bolinha 
                            distance = ultras.distance()
                            robot.straight(ultras.distance() - 50)
                            # Verificando a vítima novamente
                            if vitima_morta():
                                detec_vitima(distance, "morta")
                                ball += 1
                                if ball == 3:
                                    break
                            elif vitima_viva():
                                detec_vitima(distance, "viva")
                                ball += 1
                                if ball == 3:
                                    break
                            else:
                                robot.straight(-distance)
                                gyro_10()
                        else:
                            pass    

                    if ball == 3:
                        triangulos()
                        saida()
                    elif count == 36 and ball < 3:
                        triangulos()
                        saida()
                else:
                    triangulos()
                    saida()

def middle():
    robot.straight(450)
    gyro_90() # vira para direita
    right = ultras.distance()
    gyro_180() # vira para esquerda
    left = ultras.distance()
    gyro.reset_angle() # reseta o ângulo do giroscópio
    if right < left:
        robot.straight(left)
        if detec_parede():
            robot.straight(-450)
            sm.angle(90) # ativa o sensor de cor para vitimas
            return "sul"
        else:
            robot.straight(-450)
            sm.angle(90) # ativa o sensor de cor para vitimas
            return "sul"
    elif right > left:
        gyro_180()
        gyro.reset_angle() # reseta o ângulo do giroscópio
        robot.straight(right)
        if detec_parede():
            robot.straight(-450)
            sm.angle(90) # ativa o sensor de cor para vitimas
            return "sul"
        else: 
            robot.straight(-450)
            sm.angle(90) # ativa o sensor de cor para vitimas
            return "sul"
    else:
        sm.angle(90)
        return "sul"


