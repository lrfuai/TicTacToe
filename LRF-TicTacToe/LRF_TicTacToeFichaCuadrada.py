#!/usr/bin/env python
#Filename: tic-tac-toe.py
#Description: Tic-Tac-Toe two player game
import sys,random,time

from Game import Game
from PlayerCuadrada import Human
from PlayerCuadrada import AI

if __name__ == '__main__':
    game = Game()
    player1 = Human("X")
    player2 = AI("O")
    game.play( player1, player2)
