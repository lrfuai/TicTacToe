#!/usr/bin/env python
#Filename: tic-tac-toe.py
#Description: Tic-Tac-Toe two player game
import sys,random,time

from Game import Game
from PlayerParametrizado import Human
from PlayerParametrizado import AI

if __name__ == '__main__':
    game = Game()
    player1 = Human("O")
    player2 = AI("X",AI.EASY)
    #player2 = AI("X",AI.HARD)
    game.play( player1, player2)
