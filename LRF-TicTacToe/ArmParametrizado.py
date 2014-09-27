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

Position_Order = (0,3,1,2,4)
Position_Order_Inverse = (4,2,1,3,0)

Positions = {
      "0" : [[90,120,120,130,74],Position_Order_Inverse],
      "1" : [[90,95,120,125,64],Position_Order_Inverse],
      "2" : [[90,60,120,130,74],Position_Order_Inverse],
      "3" : [[90,110,89,85,64],(0,3,4,1,2)],
      "4" : [[90,90,89,85,64],(0,3,4,1,2)],
      "5" : [[90,70,89,85,64],(0,3,4,1,2)],
      "6" : [[90,105,60,30,54],Position_Order],
      "7" : [[90,90,60,35,54],Position_Order],
      "8" : [[90,70,60,40,60],Position_Order],
      "inicial" : [[90,90,100,50,78],Position_Order_Inverse],
      "Repositorio" : [[90,140,100,100,78],Position_Order_Inverse],
      "Intermedia" : [[90,90,70,60,78],Position_Order],
}



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
def transicionSuave(s,origin,posicion, orden = None):
    global Position_Last
    #if(Position_Last !=  origin[0]):
    #    transicionBrusca(s,origin[0])

    Position_Last = origin[0]
    last = origin[0];
    ready = False;
    if(orden == None):
        orden =posicion[1]

    for i in orden:
        newPos = last[i]
        while(posicion[0][i] != newPos):
            if(posicion[0][i] > newPos):
                newPos = newPos +IncementFactor[i];
            elif(posicion[0][i] < newPos):
                newPos = newPos-IncementFactor[i];
            moverArticulacion(s,i,newPos)
    Position_Last = posicion;

"""
movida generica para cualquier jugada
"""
def movida(s, posicion):
        global Position_Repository
        global Position_Order
        global Position_Last
        transicionSuave(s, Position_Last, Position_Repository)
        Agarrar(s)
        #transicionSuave(s, Position_Repository, Position_Transition)
        #transicionSuave(s, Position_Transition, Positions[posicion])
        transicionSuave(s, Position_Repository, Positions[posicion])
        Soltar(s)
        orden = None
        if(posicion in ("0","1","2")):
            orden = Position_Order
        transicionSuave(s, Positions[posicion], Position_Initial,orden)

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
    iport = 0
    s = serial.Serial(int(iport),9600)
    serial.timeout=1
    if(Position_Last == None):
        transicionBrusca(s,Position_Initial[0])
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
     for i in range(1,15):
        moverArticulacion(s,3,Position_Last[0][3]+i)
     Position_Last[0][3] = Position_Last[0][3]+15


def Subir(s):
     for i in range(1,15):
        moverArticulacion(s,3,Position_Last[0][3]-i)
     Position_Last[0][3] = Position_Last[0][3]-15


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
      iport = 0
      s = serial.Serial(int(iport),9600)
      serial.timeout=1
      transicionBrusca(s,Positions["0"])
      transicionSuave(s,Positions["0"], Positions["1"])
      transicionSuave(s,Positions["1"],Positions["2"])
      transicionSuave(s,Positions["2"],Positions["3"])
      transicionSuave(s,Positions["3"],Positions["4"])
      transicionSuave(s,Positions["4"],Positions["5"])
      transicionSuave(s,Positions["5"],Positions["6"])
      transicionSuave(s,Positions["6"],Positions["7"])
      transicionSuave(s,Positions["7"],Positions["8"])

if __name__ == '__main__':
      main()
      #TEST();
