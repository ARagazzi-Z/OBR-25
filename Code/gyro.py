from imports import *


# ref é a referência, o valor que quer chegar
# A EQUAÇÃO: Erro = [leitura do sensor] - [ref] 
def gyro_straight():
        
    kp = -1.7
    ki = 0.01
    kd = -10

    integral = 0
    last_error = 0
    while True:
        ref = 0 # andar reto
        error = gyro.angle() - ref
        P = error * kp
        integral += error
        I = integral * ki
        D = (error - last_error)* kd
        turn = P + I + D 
        
        last_error = error #atualiza o erro

        robot.drive(30, turn)

def fw_10():
    while True:
        ref = 10 
        error = gyro.angle() - ref
        P = error * kp
        integral += error
        I = integral * ki
        D = (error - last_error)* kd
        turn = P + I + D 
        
        last_error = error #atualiza o erro

        robot.drive(30, turn)

def fw_10neg():
    while True:
        ref = -10 
        error = gyro.angle() - ref
        P = error * kp
        integral += error
        I = integral * ki
        D = (error - last_error)* kd
        turn = P + I + D 
        
        last_error = error #atualiza o erro

        robot.drive(30, turn)

KP = -0.6
KI = -0.01
KD = -4
integral = 0
last_error = 0

def gyro_180():  
    while True:
        ref = 180
        error = gyro.angle() - ref
        P = error * KP
        integral += error
        I = integral * KI
        D = (error - last_error)* KD
        turn = P + I + D 
            
        lturn = turn * 1
        rturn = turn * -1
        last_error = error #atualiza o erro

        ref = abs(ref) # tornando a referencia um numero absoluto 
        # tornando o angulo lido pelo gyro um numero absoluto
        # isso torna mais fácil a certificação.

        while not abs(gyro.angle())>= ref:
            robot.stop() # para permitir que os motores atuem separadamente
            lm.run(lturn)
            rm.run(rturn)
        robot.stop()
        lm.brake()
        rm.brake()

# ref é a referência, o valor que quer chegar
# A EQUAÇÃO: Erro = [leitura do sensor] - [ref] 
def gyro_90():  
    while True:
        ref = 90 
        error = gyro.angle() - ref
        P = error * KP
        integral += error
        I = integral * KI
        D = (error - last_error)* KD
        turn = P + I + D 
        
        lturn = turn * 1
        rturn = turn * -1
        last_error = error #atualiza o erro

        ref = abs(ref) # tornando a referencia um numero absoluto 
        # tornando o angulo lido pelo gyro um numero absoluto
        # isso torna mais fácil a certificação.

        while not abs(gyro.angle())>= ref:
            robot.stop() # para permitir que os motores atuem separadamente
            lm.run(lturn)
            rm.run(rturn)
        robot.stop()
        lm.brake()
        rm.brake()
        
def gyro_90neg():  
    while True:
        ref = -90 
        error = gyro.angle() - ref
        P = error * KP
        integral += error
        I = integral * KI
        D = (error - last_error)* KD
        turn = P + I + D 
        
        lturn = turn * 1
        rturn = turn * -1
        last_error = error #atualiza o erro

        ref = abs(ref) # tornando a referencia um numero absoluto 
        # tornando o angulo lido pelo gyro um numero absoluto
        # isso torna mais fácil a certificação.

        while not abs(gyro.angle())>= ref:
            robot.stop() # para permitir que os motores atuem separadamente
            lm.run(lturn)
            rm.run(rturn)
        robot.stop()
        lm.brake()
        rm.brake()

def gyro_10neg():  
    while True:
        ref = -10
        error = gyro.angle() - ref
        P = error * KP
        integral += error
        I = integral * KI
        D = (error - last_error)* KD
        turn = P + I + D 
        
        lturn = turn * 1
        rturn = turn * -1
        last_error = error #atualiza o erro

        ref = abs(ref) # tornando a referencia um numero absoluto 
        # tornando o angulo lido pelo gyro um numero absoluto
        # isso torna mais fácil a certificação.

        while not abs(gyro.angle())>= ref:
            robot.stop() # para permitir que os motores atuem separadamente
            lm.run(lturn)
            rm.run(rturn)
        robot.stop()
        lm.brake()
        rm.brake()

def gyro_10():  
    while True:
        ref = 10
        error = gyro.angle() - ref
        P = error * KP
        integral += error
        I = integral * KI
        D = (error - last_error)* KD
        turn = P + I + D 
        
        lturn = turn * 1
        rturn = turn * -1
        last_error = error #atualiza o erro

        ref = abs(ref) # tornando a referencia um numero absoluto 
        # tornando o angulo lido pelo gyro um numero absoluto
        # isso torna mais fácil a certificação.

        while not abs(gyro.angle())>= ref:
            robot.stop() # para permitir que os motores atuem separadamente
            lm.run(lturn)
            rm.run(rturn)
        robot.stop()
        lm.brake()
        rm.brake()


#CALIBRATION OF THE GYRO TO PREVENT DYNAMIC DRIFT
#Change from speed() (deg/sec) to angle() (deg) or from angle to speed.
def dynam_gauge():
    gyro.reset_angle(0)
    gyro.speed()
    wait(1000)
    gyro.angle()
    wait(1000)
    gyro.reset_angle(0)

#CALIBRATION OF THE GYRO TO PREVENT STATIC DRIFT
#Calculates the difference between the reference(that the robot should have gone) and the drift (the wrong drift)
ref = 0 # the robot should have gone at that moment
def static_gauge():
    drift = ref - gyro.angle()
    gyro.reset_angle(drift) 
#CALIBRAR COM ELE TOTALMENTE PARADO 

#SEMPRE CALIBRAR O GYRO AO BATER EM UMA PAREDE PARA EVITAR O *DRIFT ESTÁTICO*
#A CALIBRAÇÃO DO DRIFT DINÂMICO PODE SER FEITO AO INÍCIO DO ROUND

def scor_reflection_data():
    x = lscor.reflection()
    y = rscor.reflection()

    ev3.screen.print('esquerda:')(x)
    ev3.screen.print('direita:')(y)

# Escreve na tela a quantidade de luz refletida que cada sensor está vendo