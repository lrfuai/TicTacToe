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
P1 = 181
P2 = 141
P3 = 141
P4 = 81
P5 = 81


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
        vec = (90,180,140,140,80)
        PosicionInicial(s,0,vec[0])
        PosicionInicial(s,1,vec[1])
        PosicionInicial(s,3,vec[3])
        PosicionInicial(s,4,vec[4])
        PosicionInicial(s,2,vec[2])
        
def PosicionIntermedia(s):
        vec = (90,180,140,140,80)
        PosicionarBrazo(s,vec)

        
## FILA 1
def H1(s,lugar):
        vecFicha = (90,197,110,127,74)
        if lugar==2:
            vecFicha = (90,178,92,93,74)
        elif lugar == 3:
            vecFicha = (90,170,63,52,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,165,118,149,74)
        PosicionarBrazo(s,vec)
        Soltar(s)
    
def G1(s,lugar):
        vecFicha = (90,197,110,127,74)
        if lugar==2:
            vecFicha = (90,178,92,93,74)
        elif lugar == 3:
            vecFicha = (90,170,63,52,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,135,118,149,74)
        PosicionarBrazo(s,vec)
        Soltar(s)

     
def F1(s,lugar):
        vecFicha = (90,197,110,127,74)
        if lugar==2:
            vecFicha = (90,178,92,93,74)
        elif lugar == 3:
            vecFicha = (90,170,63,52,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,100,113,140,74)
        PosicionarBrazo(s,vec)
        Soltar(s)

## FILA 2
def H2(s,lugar):
        vecFicha = (90,178,92,93,74)
        if lugar==1:
            vecFicha = (90,197,110,127,74)
        elif lugar == 3:
            vecFicha = (90,170,63,52,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,158,99,117,74)
        PosicionarBrazo(s,vec)
        Soltar(s)
def G2(s,lugar):
        vecFicha = (90,178,92,93,74)
        if lugar==1:
            vecFicha = (90,197,110,127,74)
        elif lugar == 3:
            vecFicha = (90,170,63,52,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,135,99,117,74)
        PosicionarBrazo(s,vec)
        Soltar(s)
def F2(s,lugar):
        vecFicha = (90,178,92,93,74)
        if lugar==1:
            vecFicha = (90,197,110,127,74)
        elif lugar == 3:
            vecFicha = (90,170,63,52,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,109,94,108,74)
        PosicionarBrazo(s,vec)
        Soltar(s)
## FILA 3        
def H3(s,lugar):
        vecFicha = (90,170,63,52,74)
        if lugar==2:
            vecFicha = (90,178,92,93,74)
        elif lugar == 1:
            vecFicha = (90,197,110,127,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,150,74,75,74)
        PosicionarBrazo(s,vec)
        Soltar(s)

def G3(s,lugar):
        vecFicha = (90,170,63,52,74)
        if lugar==2:
            vecFicha = (90,178,92,93,74)
        elif lugar == 1:
            vecFicha = (90,197,110,127,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,135,74,75,74)
        PosicionarBrazo(s,vec)
        Soltar(s)

def F3(s,lugar):
        vecFicha = (90,170,63,52,74)
        if lugar==2:
            vecFicha = (90,178,92,93,74)
        elif lugar == 1:
            vecFicha = (90,197,110,127,74)
        PosicionarBrazo(s,vecFicha)
        Agarrar(s)
        vec = (90,114,69,66,74)
        PosicionarBrazo(s,vec)
        Soltar(s)

def Abrir(s):
        PosicionarMotor(s,0,P0,167)

def Cerrar(s):
        PosicionarMotor(s,0,P0,110)
        sleep(1)

def Agarrar(s):
      
        Abrir(s)
        PosicionarMotor(s,2,P2,P2-15)
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
        
def jugada(posicion,lugar):
    #inicializar variables
    iCiclos = 0  
    sData = ['0','0','0']



   
    iport = 0
    s = serial.Serial(int(iport),9600)
    serial.timeout=1


    if posicion == '0':
          PosicionCero(s)
    elif posicion == 'H1':
             H1(s,lugar)
    elif posicion == 'H2':
             H2(s,lugar)
    elif posicion == 'H3':
             H3(s,lugar)    
    elif posicion == 'G1':
             G1(s,lugar)
    elif posicion == 'G2':
             G2(s,lugar)
    elif posicion == 'G3':
             G3(s,lugar)
    elif posicion == 'F1':
             F1(s,lugar)
    elif posicion == 'F2':
             F2(s,lugar)
    elif posicion == 'F3':
         F3(s,lugar)                 
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

def PosicionInicial(s,motor,gX):
      global P1,P2,P3,P4,P5
      comando = [255,motor,gX]
      s.write(comando)
      sleep(0.02)
      
      if motor == 1:
              P1 = gX
      elif motor ==2:
              P2 = gX
      elif motor ==3:
              P3 = gX
      elif motor ==4:
              P4 = gX
      elif motor ==5:
              P5 = gX
