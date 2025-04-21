#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

lm = Motor(Port.A) # motor da roda da esquerda
rm = Motor(Port.B) # motor da roda da direita
sm = Motor(Port.C) # motor do sensor
cm = Motor(Port.D) # motor da portão da caixa

gyro = GyroSensor(Port.S1)
ultras = UltrasonicSensor(Port.S2)
lscor = ColorSensor(Port.S3) # sensor de cor da esquerda
rscor = ColorSensor(Port.S4) # sensor de cor da direita

wd = 4 # wheel diameter
at = 5 # axle_track
robot = DriveBase(lm, rm, wd, at)
