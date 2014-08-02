import pygame;
from pygame.locals import *


BoardEmptySelector = "-"

class GameBoard:

    raw = []
    Board = None

    def __init__(self):
        self.raw = [ BoardEmptySelector for i in range(0,9) ]
        self.Board = BoardComposite()
        self.Board.Add(AsciiBoard())
        self.Board.Add(PygameBoard())

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
        self.Board.Draw(self.raw);

class BoardComposite:

    Boards = []

    def Add(self, board) :
        self.Boards.append(board)

    def Log(self, message):
        for board in self.Boards:
            board.Log(message)

    def Draw(self, raw):
        for board in self.Boards:
            board.Draw(raw)


class PygameBoard :
    
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((150,150))
        pygame.display.set_caption("Tris")
        font = pygame.font.SysFont("arial",30)

    def Log(self, message):
        pass

    def Draw(self,raw):
        pass

class AsciiBoard :

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

