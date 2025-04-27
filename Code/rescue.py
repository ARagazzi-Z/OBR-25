from imports import *
from gyro import *
from line import branco_dir_RGB, branco_esq_RGB, verde_dir_RGB, verde_esq_RGB, preto_dir_RGB, preto_esq_RGB
import math
import time

posicao_inicial = 0
    
# Modificação na função area_resgate para gravar a posição do robô no momento da entrada
def area_resgate(mapeador):
    lr, lg, lb = lscor.rgb()
    rr, rg, rb = rscor.rgb()
    lmedia = (lr + lg + lb) / 3
    rmedia = (rr + rg + rb) / 3

    if branco_esq_RGB() > lmedia > preto_esq_RGB() and branco_dir_RGB() > rmedia > preto_dir_RGB():
        # Registra a posição atual do robô como "entrada"
        mapeador.MAPA.append((mapeador.centro_x, mapeador.centro_y, 'entrada'))
        return "resgate"

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

def middle(mapeador):
    if area_resgate(mapeador) == "resgate":
        largura = ultras.distance() 
        if largura >= 910:  
            largura = 1200 
        elif largura < 910:
            largura = 900

        robot.straight(largura/2)
        gyro_turn(90) # virou para a direita para ver se tem parede
        if ultras.distance() < 50:
            gyro_turn(180)
            if largura == 1200:
                altura = 900
                robot.straight(altura/2) 


    # Simulação do deslocamento do robô da entrada até o centro
    deslocamento_x = 50   # distância percorrida em x (exemplo)
    deslocamento_y = 30   # distância percorrida em y (exemplo)
    
    # Calcula a nova posição (antes do ajuste) – essa é a posição atual do robô
    nova_pos_x = mapeador.centro_x + deslocamento_x
    nova_pos_y = mapeador.centro_y + deslocamento_y
    
    # Reescreve todas as coordenadas do mapa para que o novo centro seja (0, 0)
    nova_mapa = []
    for (x, y, tipo) in mapeador.MAPA:
         nova_mapa.append((x - nova_pos_x, y - nova_pos_y, tipo))
    mapeador.MAPA = nova_mapa

    # Define o novo centro como (0,0)
    mapeador.centro_x = 0
    mapeador.centro_y = 0

    # Agora, o ponto de entrada estará reescrito relativo ao novo centro;
    # por exemplo, se a entrada foi registrada originalmente em (0,0),
    # ela será atualizada para (-deslocamento_x, -deslocamento_y)
    print(f"Novo centro definido: (0,0). Entrada atualizada: ({-nova_pos_x}, {-nova_pos_y})")
    return "sul"


class Mapeador:
    def __init__(self, largura = 0, altura = 0, escala=10):
        self.largura = largura
        self.altura = altura
        self.escala = escala
        self.centro_x = 0
        self.centro_y = 0
        self.MAPA = []
        self.MARGEM_ERRO = 5

    # Distância esperada até a parede em um certo ângulo
    def dist_esperada(self, angulo_rad):
        dx = math.cos(angulo_rad)
        dy = math.sin(angulo_rad)

        if dx == 0:
            dx = 1e-6
        if dy == 0:
            dy = 1e-6

        if dx > 0:
            distancia_x = (self.largura/2 - self.centro_x) / dx
        else:
            distancia_x = (-self.largura/2 - self.centro_x) / dx

        if dy > 0:
            distancia_y = (self.altura/2 - self.centro_y) / dy
        else:
            distancia_y = (-self.altura/2 - self.centro_y) / dy

        return min(distancia_x, distancia_y)

    def radar(self):
        # Função principal para fazer o mapeamento
        for angulo in range(0, 360, 20):  # varre de 20 em 20 graus
            # Gira o robô e mede a distância
            gyro_turn(20) # -> Aqui giraria fisicamente
            time.sleep(0.1)  # pequena pausa para estabilizar
            distancia_real = self.medir_distancia()  # você implementa sua função de medir

            angulo_rad = math.radians(angulo)
            distancia_teorica = self.dist_esperada(angulo_rad) # calcula a distância esperada até a parede da localidade 

            # Decide o que é o objeto
            if distancia_real < distancia_teorica - self.MARGEM_ERRO:
                tipo = 'bolinha'
            elif distancia_real > distancia_teorica + self.MARGEM_ERRO:
                tipo = 'saida'  # pode ser saída ou entrada
            else:
                tipo = 'parede'

            # Calcula posição x, y do objeto detectado
            x = self.centro_x + math.cos(angulo_rad) * distancia_real
            y = self.centro_y + math.sin(angulo_rad) * distancia_real

            self.MAPA.append((x, y, tipo))

    def medir_distancia(self):
        dist_real = ultras.distance()
        return dist_real 

    # Função para desenhar o mapa
    def print_mapa(self):
        grid = [['.' for _ in range(self.largura // self.escala)] for _ in range(self.altura // self.escala)]

        centro_grid_x = (self.largura // self.escala) // 2
        centro_grid_y = (self.altura // self.escala) // 2
        grid[centro_grid_y][centro_grid_x] = 'R'  # Robô no centro

        for objeto in self.MAPA:
            x, y, tipo = objeto

            pos_x = int((x + self.largura/2) // self.escala)
            pos_y = int((self.altura/2 - y) // self.escala)

            if 0 <= pos_x < (self.largura // self.escala) and 0 <= pos_y < (self.altura // self.escala):
                if tipo == 'parede':
                    grid[pos_y][pos_x] = '#'
                elif tipo == 'bolinha':
                    grid[pos_y][pos_x] = 'O'
                elif tipo == 'saida':
                    grid[pos_y][pos_x] = 'S'
                elif tipo == 'entrada':
                    grid[pos_y][pos_x] = 'E'

        # Agora desenha no visor:
        ev3.screen.clear()

        tamanho_letra = 8  # cada caractere ocupa mais ou menos 8x8 pixels
        for i, linha in enumerate(grid):
            texto = ''.join(linha)
            ev3.screen.draw_text(0, i * tamanho_letra, texto)

    # Função para ir até uma posição 
    def resgate_vitimas(self, x_destino, y_destino):
        dx = x_destino - self.centro_x
        dy = y_destino - self.centro_y

        distancia = math.sqrt(dx**2 + dy**2)
        angulo = math.degrees(math.atan2(dy, dx))

        # Aqui você giraria até o ângulo certo e andaria até a distância certa
        gyro_turn(angulo)
        robot.straight(distancia)
        # Simulação de movimento
        print(f"Girando até {angulo:.2f} graus e andando {distancia:.2f} cm")


# Exemplo de uso
"""
m = Mapeador()
m.radar()
m.print_mapa()
"""
