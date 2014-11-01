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

Positions = {
      "0" : (90,120,118,130,74),
      "1" : (90,95,118,139,74),
      "2" : (90,70,113,130,74),
      "3" : (90,118,99,107,74),
      "4" : (90,95,99,107,74),
      "5" : (90,69,94,98,74),
      "6" : (90,110,74,65,74),
      "7" : (90,87,74,65,74),
      "8" : (90,74,69,56,74),
      "inicial" : (90,89,130,140,80),
      "Repositorio" : (95,140,100,100,70),
      "Intermedia" : (95,140,100,43,70),
}

Position_Order = (0,3,1,4,2)

Position_Initial = Positions["inicial"];
Position_Repository = Positions["Repositorio"];
Position_Transition = Positions["Intermedia"];

Position_Last  = None;
IncementFactor = (1,1,1,1,1);

"""
mueve una posicion una articulacion en particular
"""                
def moverArticulacion(s,motor,posicion):
      comando = [255,motor,posicion]
      s.write(comando)
      sleep(0.02)
"""
Transicion Brusca a una nueva posicion
""" 
def transicionBrusca(s,posicion):
    global Position_Last
    for i in Position_Order:
        moverArticulacion(s,i,posicion[i])
    Position_Last = posicion 



"""
Transicion Suave a una nueva posicion con un orden especifico
"""
def transicionSuave(s,origin,posicion,orden = Position_Order):
    global Position_Last
    if(Position_Last !=  origin):
        transicionBrusca(s,origin)
    
    Position_Last = origin
    last = origin;
    ready = False;
    for i in orden:
        newPos = last[i];
        while(posicion[i] != newPos):
            if(posicion[i] > newPos):
                newPos = newPos +IncementFactor[i];
            elif(posicion[i] < newPos):
                newPos = newPos-IncementFactor[i];
            moverArticulacion(s,i,newPos)
    Position_Last = posicion;

"""
movida generica para cualquier jugada
"""
def movida(s, posicion):
        global Position_Repository
        global Position_Last
        transicionSuave(s, Position_Last, Position_Repository)
        Agarrar(s)
        transicionSuave(s, Position_Repository, Position_Transition)
        transicionSuave(s, Position_Transition, Positions[posicion], reversed(Position_Order))
        Soltar(s)
        transicionSuave(s, Positions[posicion], Position_Initial, reversed(Position_Order))

"""
Realiza la jugada en el tablero
"""
def jugada(posicion):
    global Position_Last
    #Funcion que llama playerParametrizado.py#
    #inicializar variables
    iCiclos = 0  
    sData = ['0','0','0']
    
    #COM1 = 0#       
    iport = 2
    s = serial.Serial(int(iport),9600)
    serial.timeout=1
    if(Position_Last == None):
        transicionBrusca(s,Position_Initial)
        Position_Last = Position_Initial
    else:
        transicionSuave(s, Position_Last, Position_Initial)
    movida(s, posicion)
    s.close()

"""
Abre el Brazo
"""
def Abrir(s):
      moverArticulacion(s,0,167)
      sleep(1)

"""
Cierra el Brazo
"""
def Cerrar(s):
      moverArticulacion(s,0,90)
      sleep(1)
     

def Bajar(s):
     moverArticulacion(s,3,Position_Last[3]+18)
     sleep(1)

def Subir(s):
     moverArticulacion(s,3,Position_Last[3]-18)
     sleep(1)

"""
Agarra el Brazo
"""
def Agarrar(s):
      Abrir(s)
      Bajar(s)
      Cerrar(s)
      Subir(s)

"""
Suelta el Brazo
"""      
def Soltar(s):
      Bajar(s);
      Abrir(s)
      Subir(s)

def main():
    #Ingreso por teclado#    
    while True:
          data = raw_input("Ingrese posicion ")
          print data
          jugada(data.upper())
    s.close()

def TEST():
      iport = 2
      s = serial.Serial(int(iport),9600)
      serial.timeout=1
      transicionBrusca(s,Position_Initial)


if __name__ == '__main__':
      main()
      #TEST();