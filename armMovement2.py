#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Robotica
#
# Created:     12/11/2016
# Copyright:   (c) Robotica 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys
import serial
import pygame
import cv2
import numpy as np
import configparser
import logging

from math import *
from time import time, sleep

def nothing(x) :
      pass

# Comentarios:
# 0: pinza 80-150
# 1: base 45-150
# 2: brazo-eje1:  60-120
# 3: brazo-eje2:
# 4: brazo-eje3: 70-135
# El orden, es el orden de ejes que va a ejecutar
# Las posiciones estan ordenadas

class ArmPosition :
    pos = []
    order = ()

    def __init__ (self, p, o) :
        self.pos = p
        self.order = o

class ArmInterface :
    __serial = None
    __connected = False
    __lastPos = None

    __minLimits = []
    __maxLimits = []

    __serialPath = None

    def __init__ (self, serialPath) :
        logging.info("Initilizing Arm Interface")   
        self.__minLimits = [ 70,  35,  55, 40,  30]
        self.__maxLimits = [145, 150, 110, 90, 110]
        self.__serialPath = serialPath

    def connect(self) :
        ##self.__serialPath = "/dev/ttyUSB0"
        self.__serialPath = "COM7"        
        self.__serial = serial.Serial(self.__serialPath, 9600)
        self.__serial.timeout = 1
        self.__connected = True

    def disconnect(self) :
        self.__connected = False
        self.__serial.close()

    def isConnected(self) :
        return self.__connected

    def move(self,numArt,pos):
        if self.__connected == True :
            if self.__maxLimits[numArt] < pos :
                pos = self.__maxLimits[numArt]
                print ("Limite maximo en art " , str(numArt) , " limitado a: " , str(pos))

            if self.__minLimits[numArt] > pos :
                pos = self.__minLimits[numArt]
                print ("Limite minimo en art " , str(numArt) , " limitado a: " , str(pos))

            comando = [255, numArt, pos]
            self.__serial.write(comando)
            sleep(0.02)
        else :
            print ("Arm not connected!")

    def moveSudden(self, pos) :
        if self.__connected == True :
            order = [0,3,1,2,4]
            for i in order:
                self.move(i, pos[i])

            self.__lastPos = pos
        else :
            print ("Arm not connected!")


    def moveSoft(self, pos, order) :
        if self.__lastPos != None and self.__connected:
            incementFactor = (1,1,1,1,1);
            for i in order:
                newPos = self.__lastPos[i]
                while(pos[i] != newPos):
                    if(pos[i] > newPos):
                        newPos = newPos + incementFactor[i];
                    elif(pos[i] < newPos):
                        newPos = newPos - incementFactor[i];

                    self.move(i,newPos)
            self.__lastPos = pos;
        elif self.__lastPos == None :
            print ("Arm need to be initialized with a sudden position.")
        else :
            print ("Arm not connected!")


class ArmMovement :
    __settings = configparser.ConfigParser()

    __armInterface = None

    __initial = None

    __transition_with_object = None

    __transition_without_object = None

    __getPiece = []
    __dropPiece = []

    def __init__ (self, serialPath) :
        logging.info("Initilizing Arm")
        self.__settings = configparser.ConfigParser()
        self.__settings.read('armConfig.ini')

        self.__armInterface = ArmInterface(serialPath)

        self.__initial = self.__loadPosAndOrder("inicial")
        self.__transition_with_object = self.__loadPosAndOrder("transicion_con_objeto")
        self.__transition_without_object = self.__loadPosAndOrder("transicion_sin_objeto")

        for i in range(1, 5) :
            self.__getPiece.append(self.__loadPosAndOrder("agarrar_pieza_" + str(i)))

        for i in range(1, 10) :
            self.__dropPiece.append(self.__loadPosAndOrder("dejar_pieza_" + str(i)))



    def __loadPosAndOrder(self, name) :
        pos = self.__loadPosition(name)
        order = self.__loadOrder(name)
        return ArmPosition(pos, order)

    def __loadPosition(self, name) :
        return list(map(int, self.__settings.get(name,"posiciones").split(',')))

    def __loadOrder(self, name) :
        return list(map(int, self.__settings.get(name,"orden").split(',')))

    def __goToTransitionPos(self) :
        print ("not implemented")

    def goToPosFast(self, pos) :
        self.__armInterface.connect()
        self.__armInterface.moveSudden(pos)
        self.__armInterface.disconnect()

    def goToPosSlow(self, pos, order) :
        self.__armInterface.connect()
        self.__armInterface.moveSoft(pos, order)
        self.__armInterface.disconnect()

    def getPiece(self, pieceNumber) :
        logging.info("Getting piece: " + str(pieceNumber))
        print ("Obteniendo ficha " , str(pieceNumber))
        self.__armInterface.connect()
        self.__armInterface.moveSudden(self.__transition_without_object.pos)
        self.__armInterface.moveSoft(self.__getPiece[pieceNumber-1].pos, self.__getPiece[pieceNumber-1].order)
        self.__armInterface.moveSoft(self.__transition_with_object.pos, self.__transition_with_object.order)
        self.__armInterface.disconnect()
        print ("Listo!")

    def dropPieceOnBlock(self, blockNumber) :
        logging.info("Dropping piece on: " + str(blockNumber))
        print ("Dejando ficha en bloque: " , str(blockNumber))
        self.__armInterface.connect()
        self.__armInterface.moveSoft(self.__transition_with_object.pos, self.__transition_with_object.order)
        self.__armInterface.moveSoft(self.__dropPiece[blockNumber-1].pos, self.__dropPiece[blockNumber-1].order)
        self.__armInterface.moveSoft(self.__transition_without_object.pos, self.__transition_without_object.order)
        self.__armInterface.disconnect()
        print ("Listo!")

    def getPieceAndDropOnBlock(self, pieceNumber, blockNumber) :
        self.getPiece(pieceNumber)
        self.dropPieceOnBlock(blockNumber)

# Module Test!
if __name__ == '__main__':
    cv2.namedWindow("test")
    cv2.createTrackbar("pos0", "test", 145, 200, nothing)
    cv2.createTrackbar("pos1", "test", 94, 200, nothing)
    cv2.createTrackbar("pos2", "test", 85, 200, nothing)
    cv2.createTrackbar("pos3", "test", 46, 200, nothing)
    cv2.createTrackbar("pos4", "test", 78, 200, nothing)

    arm = ArmMovement(0)
    print ("Q,W,E,R = Agarrar piezas.")
    print ("1,2,3,4,5,6,7,8,9 dejar piezas.")
    print ("TAB mover suave, SPACE mover rapido.")

    while True :
        key = cv2.waitKey(1) & 0xFF

        pos1 = int(cv2.getTrackbarPos('pos0', 'test'))
        pos2 = int(cv2.getTrackbarPos('pos1', 'test'))
        pos3 = int(cv2.getTrackbarPos('pos2', 'test'))
        pos4 = int(cv2.getTrackbarPos('pos3', 'test'))
        pos5 = int(cv2.getTrackbarPos('pos4', 'test'))

        if key == 27 : # ESC
            print ("Exit")
            break;
        elif key == 32 : # SPACE
            pos = [pos1,pos2,pos3,pos4,pos5]
            arm.goToPosFast(pos)
        elif key == 9 : # TAB
            pos = [pos1,pos2,pos3,pos4,pos5]
            order = (0,3,1,2,4)
            arm.goToPosSlow(pos, order)
        elif key == ord('q') :
            arm.getPiece(1)
        elif key == ord('w') :
            arm.getPiece(2)
        elif key == ord('e') :
            arm.getPiece(3)
        elif key == ord('r') :
            arm.getPiece(4)
        elif key == ord('1') :
            arm.dropPieceOnBlock(1)
        elif key == ord('2') :
            arm.dropPieceOnBlock(2)
        elif key == ord('3') :
            arm.dropPieceOnBlock(3)
        elif key == ord('4') :
            arm.dropPieceOnBlock(4)
        elif key == ord('5') :
            arm.dropPieceOnBlock(5)
        elif key == ord('6') :
            arm.dropPieceOnBlock(6)
        elif key == ord('7') :
            arm.dropPieceOnBlock(7)
        elif key == ord('8') :
            arm.dropPieceOnBlock(8)
        elif key == ord('9') :
            arm.dropPieceOnBlock(9)


    cv2.destroyAllWindows()
