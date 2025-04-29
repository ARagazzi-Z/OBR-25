from imports import *
from gyro import *
from line import branco_dir_RGB, branco_esq_RGB, verde_dir_RGB, verde_esq_RGB, preto_dir_RGB, preto_esq_RGB
import math
import time

def area_resgate(mapeador):
    lr, lg, lb = lscor.rgb()
    rr, rg, rb = rscor.rgb()
    lmedia = (lr + lg + lb) / 3
    rmedia = (rr + rg + rb) / 3

    if branco_esq_RGB() > lmedia > preto_esq_RGB() and branco_dir_RGB() > rmedia > preto_dir_RGB():
        # Registra a posição atual do robô como "entrada"
        mapeador.MAPA.append((mapeador.centro_x, mapeador.centro_y, 'entrada'))
        return "resgate"

def triangulos(mapeador):
    # Pressupõe que o robô está no centro (0,0) e voltado para o norte.
    robot.straight(mapeador.largura / 2) # Avança até a parede norte.
    gyro_turn(90) # vira para leste
    robot.straight(-mapeador.altura / 2)
    # vai até o canto sudoeste
    gyro_turn(-90) # vira para norte
    robot.straight(-mapeador.largura)
    # vai até o canto sudeste
    gyro_turn(-90) # vira para oeste
    robot.straight(-mapeador.altura)
    # vai até o canto nordeste
    gyro_turn(-90) # vira para sul
    robot.straight(-mapeador.largura)
    # vai até o canto noroeste
    return "sair"

def saida():
    return 'saida com sucesso'

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

def atualizar_odometria(mapeador, distancia):
    # Usa o ângulo atual do gyro (em radianos) para integrar o deslocamento
    angulo_atual = math.radians(gyro.angle())
    mapeador.centro_x += distancia * math.cos(angulo_atual)
    mapeador.centro_y += distancia * math.sin(angulo_atual)
    """
    Odometria é um método utilizado para estimar a posição e orientação de um 
    objeto (geralmente um robô) em movimento, utilizando dados de sensores de movimento. 
    Em outras palavras, é uma forma de "calcular" a posição do objeto com base na 
    distância percorrida e na direção do movimento. 
    """

def middle(mapeador):
    if area_resgate(mapeador) == "resgate":
        largura_medida = ultras.distance()
        mapeador.largura = 1200 if largura_medida >= 910 else 900

        d = mapeador.largura / 2
        robot.straight(d) # vaiaté o meio da largura
        atualizar_odometria(mapeador, d) # atualiza a odometria em largura

        gyro_turn(90) # vira para calcular a direita

        dist_dir = ultras.distance()
        gyro_turn(180) # vira para calcular a esquerda
        dist_esq = ultras.distance()
        mapeador.altura = dist_dir + dist_esq

        centro_horizontal = (dist_dir + dist_esq) / 2
        if dist_dir < dist_esq:
            d2 = centro_horizontal - dist_dir
            robot.straight(d2)
            atualizar_odometria(mapeador, d2)
            gyro_turn(90) # vira para norte
        elif dist_esq < dist_dir:
            d2 = centro_horizontal - dist_esq
            robot.straight(-d2)
            atualizar_odometria(mapeador, -d2)
            gyro_turn(90) # vira para norte
        # Se as medições forem iguais, já está centralizado

    # Recalcula as coordenadas para que o novo centro seja (0,0)
    desloc_x = mapeador.centro_x
    desloc_y = mapeador.centro_y
    novo_mapa = []
    for (x, y, tipo) in mapeador.MAPA:
        novo_mapa.append((x - desloc_x, y - desloc_y, tipo))
    mapeador.MAPA = novo_mapa
    mapeador.centro_x = 0 # zera o centro 
    mapeador.centro_y = 0 # zera o centro

    """
               novo_mapa = []
       for (x, y, tipo) in mapeador.MAPA:
           novo_mapa.append((x - desloc_x, y - desloc_y, tipo))
       mapeador.MAPA = novo_mapa
    
           Essa parte faz:
                Desloca todo o mapa:
                    Para cada objeto no mapa, tira desloc_x e desloc_y da posição.
                    Isso ajusta todo o mapa como se o robô estivesse no (0,0) agora.
                    (É tipo: “o mundo se moveu para alinhar com o robô”.)
    """               

    # Busca o marcador da entrada e, se não existir, adiciona-o usando a última posição conhecida
    # Garante que a "entrada" esteja salva

    entrada_real = None
    for (x, y, tipo) in mapeador.MAPA:
        if tipo == 'entrada':
            entrada_real = (x, y)
            break
        # Procura no mapa se existe um marcador do tipo 'entrada'.
        # Se encontrar, salva a posição.
    if entrada_real is None:
        # Se não foi encontrado, salva a entrada com a posição calculada (inversa do DESLOC(deslocamento))
        # O deslocamento é negativo porque o robô se moveu para o centro
        entrada_real = (-desloc_x, -desloc_y)
        mapeador.MAPA.append((entrada_real[0], entrada_real[1], 'entrada'))
    print(f"Novo centro (0,0) configurado. Entrada salva no mapa: {entrada_real}. Dimensões - Largura: {mapeador.largura}, Altura: {mapeador.altura}")
    return "radar"

"""
Em Python, o "f" antes das aspas indica uma f-string (string formatada). 
Essa funcionalidade, disponível a partir do Python 3.6, permite inserir 
valores de variáveis ou expressões diretamente dentro da string, usando chaves { }.
"""

class Mapeador:
    def __init__(self, largura = 0, altura = 0, escala=10):
        self.largura = largura
        self.altura = altura
        self.escala = escala
        self.centro_x = 0
        self.centro_y = 0
        self.MAPA = []
        self.MARGEM_ERRO = 20  # margem de erro para a detecção de objetos
        # Inicializa o mapa com a largura e altura dadas, e o centro na origem (0,0)

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

    def medir_distancia(self):
        dist_real = ultras.distance()
        return dist_real 
    
    def radar(self):
        # Função principal para fazer o mapeamento
        for angulo in range(0, 360, 10):  # varre de 10 em 10 graus
            # Gira o robô e mede a distância
            gyro_turn(10) # -> Aqui giraria fisicamente
            time.sleep(0.1)  # pequena pausa para estabilizar
            distancia_real = self.medir_distancia()  # você implementa sua função de medir

            angulo_rad = math.radians(angulo)
            distancia_teorica = self.dist_esperada(angulo_rad) # calcula a distância esperada até a parede da localidade 

            # Decide o que é o objeto
            if distancia_real < distancia_teorica - self.MARGEM_ERRO:
                tipo = 'vitima' # pode ser uma vitima morta ou viva
            elif distancia_real > distancia_teorica + self.MARGEM_ERRO:
                tipo = 'saida'  # pode ser saída ou entrada
            else:
                tipo = 'parede'

            # Calcula posição x, y do objeto detectado
            x = self.centro_x + math.cos(angulo_rad) * distancia_real
            y = self.centro_y + math.sin(angulo_rad) * distancia_real

            self.MAPA.append((x, y, tipo))
            return 'detecção das vitimas'
        
    def condensar_objeto(self, x, y, tipo):
        # Verifica se o tipo é 'entrada', 'saida' ou 'vitima'
        if tipo in ['entrada', 'saida', 'vitima']:
            # Procura por objetos similares dentro de uma distância de 10mm
            similar = [obj for obj in self.MAPA if obj[2] == tipo and abs(obj[0] - x) < 10 and abs(obj[1] - y) < 10]

        # self.MAPA: A lista que armazena todos os objetos do mapa. Cada objeto é representado por uma tupla no formato (x, y, tipo)
            # - obj[0] é a coordenada X,
            # - obj[1] é a coordenada Y, e
            # - obj[2] é o tipo do objeto (entrada, saida, vitima, parede).

            if similar:
                # Se encontrar objetos similares próximos, calcula a posição média
                media_x = sum(obj[0] for obj in similar) / len(similar)
                media_y = sum(obj[1] for obj in similar) / len(similar)

                # sum(obj[0] for obj in similar): Soma as coordenadas X de todos os objetos na lista similar.
                # sum(obj[1] for obj in similar): Soma as coordenadas Y de todos os objetos na lista similar.
                # len(similar): Retorna o número de objetos na lista similar (quantos objetos estão próximos).
               # media_x e media_y: São as médias das coordenadas X e Y dos objetos encontrados. 
            # Ao calcular essas médias, o código "mescla" os objetos, representando todos como um único objeto no centro dessas posições.
            
                    # Remove os objetos antigos
                self.MAPA = [obj for obj in self.MAPA if obj not in similar]
                # Isso é feito com uma list comprehension, onde ele cria uma nova lista que não inclui os objetos que estão em similar. 
                    # Ou seja, os objetos que estavam muito próximos e foram agrupados na posição média são retirados do mapa.

                # Adiciona o novo objeto com a posição média calculada
                self.MAPA.append((media_x, media_y, tipo))
            else:
                # Se não encontrar objetos similares próximos, adiciona o objeto normalmente
                self.MAPA.append((x, y, tipo))
        else:
            # Para tipos de objetos diferentes (como 'parede'), adiciona diretamente sem cálculo de média
            self.MAPA.append((x, y, tipo))
        return 'resgate das vitimas'
    
    # Função para ir até uma posição 
    def resgate_vitimas(self):
        # Seleciona vítimas do mapa (supondo que vítimas estejam marcadas como 'vitima')
        vitimas = [(x, y) for (x, y, tipo) in self.MAPA if tipo == 'vitima']
        for i in range(3):
            if not vitimas:
                print("Nenhuma vítima encontrada.")
                break
            # Encontra a vítima mais próxima do centro (0,0)
            vitima_mais_proxima = min(vitimas, key=lambda p: p[0]**2 + p[1]**2)
            distancia = math.sqrt(vitima_mais_proxima[0]**2 + vitima_mais_proxima[1]**2)
            angulo_para_vitima = math.degrees(math.atan2(vitima_mais_proxima[1], vitima_mais_proxima[0]))

            """ 
                Explicação da Matemática e Palavras-Chave:

                1. O cálculo da vítima mais próxima:       
                - Linha: 
                    vitima_mais_proxima = min(vitimas, key=lambda p: p[0]**2 + p[1]**2)
                - Aqui, a função min é usada com uma função lambda para calcular o quadrado da distância 
                    (p[0]**2 + p[1]**2) de cada ponto em 'vitimas' em relação à origem (0, 0).
                - Usar o quadrado da distância elimina a necessidade de calcular a raiz quadrada, otimizando 
                    a comparação.

                2. O cálculo da distância real:
                - Linha: 
                    distancia = math.sqrt(vitima_mais_proxima[0]**2 + vitima_mais_proxima[1]**2)
                - Calcula a distância euclidiana real (a raiz quadrada da soma dos quadrados) para a vítima mais próxima.

                3. O cálculo do ângulo:
                - Linha: 
                    angulo_para_vitima = math.degrees(math.atan2(vitima_mais_proxima[1], vitima_mais_proxima[0]))
                - Primeiro, math.atan2 é usado para calcular o ângulo em radianos considerando o sinal dos 
                    componentes (isso garante o ângulo correto no quadrante apropriado).
                - Depois, math.degrees converte esse ângulo de radianos para graus, facilitando a interpretação.

                Palavras-Chave e Funções:
                - min: Função que retorna o menor elemento de uma sequência, podendo utilizar uma função 'key' para 
                personalizar a comparação.
                - lambda: Cria funções anônimas de forma concisa.
                - **: Operador de exponenciação em Python.
                - math.sqrt: Calcula a raiz quadrada.
                - math.atan2: Retorna o arco cujo tangente é y/x, considerando o sinal de ambos os argumentos.
                - math.degrees: Converte um ângulo de radianos para graus.
            
                
            A expressão lambda é usada para definir uma função inline que calcula o valor de comparação para cada elemento na lista "vitimas". 
            No exemplo, cada "p" é um ponto (uma tupla com coordenadas) e a lambda retorna p[0]² + p[1]², ou seja, a distância ao quadrado da origem. 
            Dessa forma, a função min usa esse valor para determinar qual é o ponto mais próximo.
            
            Usar uma lambda nesse contexto permite evitar a criação de uma função nomeada separadamente, tornando o código mais conciso e direto.
            
            """

            # Vai até a vítima
            gyro_turn(angulo_para_vitima)
            robot.straight(distancia)
            print(f"Vítima resgatada em {vitima_mais_proxima}")
            
            # Remove a vítima do mapa
            self.MAPA = [item for item in self.MAPA 
                         if not (item[2]=='vitima' and abs(item[0]-vitima_mais_proxima[0])<1e-6 and abs(item[1]-vitima_mais_proxima[1])<1e-6)]
            """
            Para cada item, ela mantém o item somente se a condição dentro de not (negação) for falsa. Ou seja, ela está removendo o item que atende a condição.

                Condição do if:
                A condição é:

                item[2] == 'vitima': O terceiro elemento do item deve ser a string 'vitima'.
                abs(item[0] - vitima_mais_proxima[0]) < 1e-6: A diferença entre as coordenadas x (primeiro elemento dos itens) deve ser menor que 1e-6, indicando que os valores são praticamente iguais.
                abs(item[1] - vitima_mais_proxima[1]) < 1e-6: Similarmente, a diferença entre as coordenadas y deve ser inferior a 1e-6.
                Uso de not:
                Ao colocar not na frente da condição, a list comprehension exclui (remove) o item que atende a todos esses três critérios, mantendo todos os demais.

                Função abs:
                A referência à função abs, cuja assinatura é definida como:

                #       def abs(x: SupportsAbs[_T], /) -> _T: ...

                indica que ela calcula o valor absoluto de uma expressão. Assim, as verificações: 
                abs(item[0] - vitima_mais_proxima[0]) e abs(item[1] - vitima_mais_proxima[1]) 
                garantem que mesmo variações muito pequenas (menores que 1e-6) sejam consideradas equivalentes.

            Resumindo, este código remove da lista self.MAPA o item que representa a vítima mais próxima 
            (com as coordenadas praticamente idênticas) para evitar, por exemplo, múltiplas contagens da mesma vítima ou para atualizar o estado do mapa de resgate.
            """
            # Retorna ao centro (0,0)
            angulo_retorno = math.degrees(math.atan2(-vitima_mais_proxima[1], -vitima_mais_proxima[0]))
            gyro_turn(angulo_retorno)
            robot.straight(distancia)
            
            # Alinha o robô para o norte
            gyro_turn(0)
            
            # Atualiza a lista de vítimas remanescentes
            vitimas = [(x, y) for (x, y, tipo) in self.MAPA if tipo == 'vitima']
        print("Resgate de vítimas concluído.")
        return 'resgate das vitimas concluído'
    
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
                elif tipo == 'vitima':
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



# Exemplo de uso
"""
m = Mapeador()
m.radar()
m.print_mapa()
"""
