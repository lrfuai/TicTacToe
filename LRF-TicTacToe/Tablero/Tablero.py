import pygame
from pygame.locals import *
import time
import sys

Pantalla=[700,500]
P0=[143,41]
P1=[286,41]
P2=[427,41]
P3=[143,185]
P4=[286,185]
P5=[427,185]
P6=[143,328]
P7=[286,328]
P8=[427,328]

PosList =[P0,P1,P2,P3,P4,P5,P6,P7,P8]
 
def load_image(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image

def load_imageo(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image

def load_imagex(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image

# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode(Pantalla)
    pygame.display.set_caption("LRF UAI: Programa de Ta-Te-Ti")
 
    background_image = load_image('Imagenes/Tateti tablero.jpg')
    background_O = load_imageo('Imagenes/Circulo.jpg')
    background_X = load_imagex('Imagenes/Cruz.jpg')
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        f = open('lista.txt','r')
        datos = f.readline()
     
        lista1 = datos.split(',')
        var = lista1
        screen.blit(background_image, (0, 0))
        if (var[0]=="O"):
                screen.blit(background_O,PosList[0])
        elif (var[0]=="X"):
                screen.blit(background_X,PosList[0])
        if (var[1]=="O"):
                screen.blit(background_O,PosList[1])
        elif (var[1]=="X"):
                screen.blit(background_X,PosList[1])
        if (var[2]=="O"):
                screen.blit(background_O,PosList[2])
        elif (var[2]=="X"):
                screen.blit(background_X,PosList[2])
        if (var[3]=="O"):
                screen.blit(background_O,PosList[3])
        elif (var[3]=="X"):
                screen.blit(background_X,PosList[3])
        if (var[4]=="O"):
                screen.blit(background_O,PosList[4])
        elif (var[4]=="X"):
                screen.blit(background_X,PosList[4])
        if (var[5]=="O"):
                screen.blit(background_O,PosList[5])
        elif (var[5]=="X"):
                screen.blit(background_X,PosList[5])
        if (var[6]=="O"):
                screen.blit(background_O,PosList[6])
        elif (var[6]=="X"):
                screen.blit(background_X,PosList[6])
        if (var[7]=="O"):
                screen.blit(background_O,PosList[7])
        elif (var[7]=="X"):
                screen.blit(background_X,PosList[7])
        if (var[8]=="O"):
                screen.blit(background_O,PosList[8])
        elif (var[8]=="X"):
                screen.blit(background_X,PosList[8])

        pygame.display.flip()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()
