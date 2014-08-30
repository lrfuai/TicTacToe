#envio serial
#Manejo de imagenes con pygame
#Ing Nestor Adrian Balich
#proyecto Brazo Robot - License Creative Common
#este material es GNU y debe referenciar al autor
#para python 2.7
# Junio de 2014 - Bs As LRF UAI


import os    
import sys
import serial
import pygame

from math import *
from time import time, sleep

P0 = 91
P1 = 130
P2 = 178
P3 = 130
P4 = 120
P5 = 120


def leerArchivo(sArchivo):
      f = open(sArchivo, "r")
      lineas=f.readlines()
      f.close
      return lineas

#posicion Cero#
##def PosicionCero1(s):   
##        comando = [255,2,G2]
##        s.write(comando)
##        sleep(1)
##        comando = [255,3,G3]
##        s.write(comando)
##        sleep(1)
##        comando = [255,4,G4]
##        s.write(comando)
##        sleep(1)
##        comando = [255,5,G5]
##        s.write(comando)
##        sleep(1)
        
def PosicionCero(s):
        vec = (90,134,180,140,122)
        PosicionarBrazo(s,vec)
        
def PosicionIntermedia(s):
        vec = (90,180,140,140,80)
        PosicionarBrazo(s,vec)

        
## FILA 1
def H1(s):
        vecFicha = (90,197,104,127,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,165,118,149,74)
        PosicionarBrazo(s,vec)
        Soltar(s)
    
def G1(s):
        vecFicha = (90,197,104,127,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,135,118,149,74)
        PosicionarBrazo(s,vec)
        Soltar(s)

     
def F1(s):
        vecFicha = (90,197,104,127,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,104,118,149,74)
        PosicionarBrazo(s,vec)
        Soltar(s)

## FILA 2
def H2(s):
        vecFicha = (90,178,86,93,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,158,99,117,74)
        PosicionarBrazo(s,vec)
        Soltar(s)
def G2(s):
        vecFicha = (90,178,86,93,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,135,99,117,74)
        PosicionarBrazo(s,vec)
        Soltar(s)
def F2(s):
        vecFicha = (90,178,86,93,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,113,99,117,74)
        PosicionarBrazo(s,vec)
        Soltar(s)
## FILA 3        
def H3(s):
        vecFicha = (90,168,63,52,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,150,74,75,74)
        PosicionarBrazo(s,vec)
        Soltar(s)

def G3(s):
        vecFicha = (90,168,63,52,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,135,74,75,65)
        PosicionarBrazo(s,vec)
        Soltar(s)

def F3(s):
        vecFicha = (90,168,63,52,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,118,74,75,74)
        PosicionarBrazo(s,vec)
        Soltar(s)

def Abrir(s):
        PosicionarMotor(s,0,P0,167)

def Cerrar(s):
        PosicionarMotor(s,0,P0,90)
        sleep(1)

def Agarrar(s):
      
        Abrir(s)
        PosicionarMotor(s,2,P2,P2-10)
        sleep(1)
        Cerrar(s)
        
def Soltar(s):
        PosicionarMotor(s,2,P2,P2-10)
        sleep(1)
        Abrir(s)


        
def PosicionarBrazo(s,vec):
        global P0,P1,P2,P3,P4,P5
        Subir(s)
        PosicionarMotor(s,0,P0,vec[0])
        PosicionarMotor(s,1,P1,vec[1])
        PosicionarMotor(s,3,P3,vec[3])
        PosicionarMotor(s,4,P4,vec[4])
        PosicionarMotor(s,2,P2,vec[2])
        
def jugada(posicion):
    #inicializar variables
    iCiclos = 0  
    sData = ['0','0','0']



   
    iport = 0
    s = serial.Serial(int(iport),9600)
    serial.timeout=1


    if posicion == '0':
          PosicionCero(s)
    elif posicion == 'H1':
             H1(s)
    elif posicion == 'H2':
             H2(s)
    elif posicion == 'H3':
             H3(s)    
    elif posicion == 'G1':
             G1(s)
    elif posicion == 'G2':
             G2(s)
    elif posicion == 'G3':
             G3(s)
    elif posicion == 'F1':
             F1(s)
    elif posicion == 'F2':
             F2(s)
    elif posicion == 'F3':
         F3(s)                 
    sleep(2)
    PosicionIntermedia(s)
    s.close()
    
        
def Subir(s):
        global P2
        PosicionarMotor(s,2,P2,130)
        
def Saludo(s):
        global P1,P2,P3,P4,P5
        PosicionarMotor(s,4,P3,90)
        PosicionarMotor(s,4,P3,120)
        PosicionarMotor(s,4,P3,160)
      
def PosicionarMotor(s,motor,g12,gX):
      global P1,P2,P3,P4,P5
    
##      print "motor " + str(motor) + ", " +str(g12) + ", " + str(gX)
      inc = g12        
      while inc != gX:
        if g12 < gX :
             inc = inc + 1
        else:
             inc = inc - 1
##        print inc    
        comando = [255,motor,inc]
        s.write(comando)
        sleep(0.02)

        if motor == 1:
              P1 = inc
        elif motor ==2:
              P2 = inc
        elif motor ==3:
              P3 = inc
        elif motor ==4:
              P4 = inc
        elif motor ==5:
              P5 = inc


