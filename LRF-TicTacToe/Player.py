import Arm
import logging
from BoardRecognizer import OpticalBoard

class Human:
    '''Class for Human player'''
    BoardRecognizer = None

    def __init__(self,marker, settings):
        logging.info("Initializing a Human Player")
        self.BoardRecognizer = OpticalBoard(settings)
        self.marker = marker
        self.type = 'H'

    def __GetMovement(self,gameinstance):
        for pos in gameinstance.freePositions():
            if ( not self.BoardRecognizer.Cells[pos].isEmpty()):
                return pos
    
    def move(self, gameinstance):

        while True:
        
            self.BoardRecognizer.Recognize()

            m = self.__GetMovement(gameinstance)

            try:
                m = int(m)
            except:
                m = -1
        
            if m not in gameinstance.freePositions():
                print ("Invalid move. Retry")
            else:
                break
        #Arm.jugada(ARMMapper(m))
        logging.info("Human player ('" + self.marker + "') moves to '" + m + "' position.")
        gameinstance.mark(self.marker,m)

def ARMMapper(position):
        options = {0:"H1",1:"G1",2:"F1",3:"H2",4:"G2",5:"F2",6:"H3",7:"G3",8:"F3"}
        return options[position]
         
class AI:
    '''Class for Computer Player'''

    def __init__(self, marker):
        logging.info("Initializing an AI Player")
        self.marker = marker
        self.type = 'C'

        if self.marker == 'X':
            self.opponentmarker = 'O'
        else:
            self.opponentmarker = 'X'

    def move(self,gameinstance):
        move_position,score = self.maximized_move(gameinstance)
        Arm.jugada(ARMMapper(move_position))
        logging.info("AI player ('" + self.marker + "') moves to '" + move_position + "' position.")
        gameinstance.mark(self.marker,move_position)

    def maximized_move(self,gameinstance):
        ''' Find maximized move'''    
        logging.info("AI searching maximized Player")
        bestscore = None
        bestmove = None

        for m in gameinstance.freePositions():
            gameinstance.mark(self.marker,m)
        
            if gameinstance.is_gameover():
                score = self.get_score(gameinstance)
            else:
                move_position,score = self.minimized_move(gameinstance)
        
            gameinstance.revert_last_move()
            
            if bestscore == None or score > bestscore:
                bestscore = score
                bestmove = m

        return bestmove, bestscore

    def minimized_move(self,gameinstance):
        ''' Find the minimized move'''
        logging.info("AI searching minimized Player")
        bestscore = None
        bestmove = None

        for m in gameinstance.freePositions():
            gameinstance.mark(self.opponentmarker,m)
        
            if gameinstance.is_gameover():
                score = self.get_score(gameinstance)
            else:
                move_position,score = self.maximized_move(gameinstance)
        
            gameinstance.revert_last_move()
            
            if bestscore == None or score < bestscore:
                bestscore = score
                bestmove = m

        return bestmove, bestscore

    def get_score(self,gameinstance):
        if gameinstance.is_gameover():
            if gameinstance.winner  == self.marker:
                return 1 # Won
            elif gameinstance.winner == self.opponentmarker:
                return -1 # Opponent won
        return 0 # Draw

