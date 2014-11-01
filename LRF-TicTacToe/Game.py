import Board
from Board import GameBoard

class Game:
    settings = None

    def __init__(self, settings):
        '''Initialize parameters - the game board, moves stack and winner'''
        self.settings = settings
        #self.board = [ '-' for i in range(0,9) ]
        self.Board = GameBoard(settings)
        self.lastmoves = []
        self.winner = None

    def freePositions(self):
        return self.Board.freePositions()

    def mark(self,marker,pos):
        '''Mark a position with marker X or O'''

        self.Board.raw[pos] = marker
        self.lastmoves.append(pos)

    def revert_last_move(self):
        '''Reset the last move'''

        self.Board.raw[self.lastmoves.pop()] = Board.BoardEmptySelector
        self.winner = None

    def is_gameover(self):
        '''Test whether game has ended'''

        win_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6),(1,4,7),(2,5,8), (0,4,8), (2,4,6)]

        for i,j,k in win_positions:
            if self.Board.raw[i] == self.Board.raw[j] == self.Board.raw[k] and self.Board.raw[i] != '-':
                self.winner = self.Board.raw[i]
                return True

        if Board.BoardEmptySelector not in self.Board.raw :
            self.winner = Board.BoardEmptySelector
            return True

        return False

    def play(self,player1,player2):
        '''Execute the game play with players'''

        self.p1 = player1
        self.p2 = player2
    
        for i in range(9):

            self.Board.Draw()
            
            if i%2==0:
                if self.p1.type == 'H':
                    self.Board.Log("[Human's Move]")
                else:
                    self.Board.Log("[Computer's Move]")

                self.p1.move(self)
            else:
                if self.p2.type == 'H':
                    self.Board.Log("[Human's Move]")
                else:
                    self.Board.Log("[Computer's Move]")

                self.p2.move(self)

            if self.is_gameover():
                if self.winner == '-':
                    self.Board.Log("Game over with Draw")
                else:
                    self.Board.Log("Winner : %s" %self.winner)
                return
