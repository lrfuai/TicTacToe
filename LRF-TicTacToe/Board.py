import pygame;
import csv;
import logging;
from pygame.locals import *

BoardEmptySelector = "-"

class GameBoard:

    raw = []
    Board = None
    settings = None

    def __init__(self,settings):
        logging.info("Initializing Game Board")
        self.settings = settings
        self.raw = [ BoardEmptySelector for i in range(0,9) ]
        self.Board = BoardComposite()
        self.Board.Add(AsciiBoard())
        self.Board.Add(VisualBoard(settings))

    def print_board(self):
        '''Print the current game board'''
        self.Board.Draw()

    def freePositions(self):
        '''Get the list of available positions'''
        moves = []
        for i,v in enumerate(self.raw):
            if v== BoardEmptySelector:
                moves.append(i)
        return moves

    def Log(self, message):
        self.Board.Log(message)

    def Draw(self):
        logging.info("Refreshing Boards")
        self.Board.Draw(self.raw);

class BoardComposite:

    Boards = []


    def __init__(self):
        logging.info("Creating Board Composite")

    def Add(self, board) :
        self.Boards.append(board)

    def Log(self, message):
        for board in self.Boards:
            board.Log(message)

    def Draw(self, raw):
        for board in self.Boards:
            board.Draw(raw)

class VisualBoard :
    
    file = ""
    lastRaw = ["-","-","-","-","-","-","-","-"]
    lastMessage = ""
    
    def __init__(self,settings):
        logging.info("Creating Visual Board")
        self.file = settings.get("VisualBoard", "file")

    def Log(self, message):
        self.lastMessage = message
        self.__generateFile()

    def Draw(self,raw):
        self.lastRaw = raw
        self.__generateFile()
        

    def __generateFile(self):
        with open(self.file, "w+") as f:
            writer = csv.writer(f)
            writer.writerow(self.lastRaw)
            f.write(self.lastMessage.lstrip())

class AsciiBoard :

    def __init__(self):
        logging.info("Creating ASCII Board")

    def Log(self, message):
        print(message)

    def Draw(self,raw):
        print("\nCurrent board:")

        for j in range(0,9,3):
            for i in range(3):
                if raw[j+i] == BoardEmptySelector :
                    print("%d |" %(j+i)),
                else:
                    print("%s |" %raw[j+i]),
            print("\n"),

