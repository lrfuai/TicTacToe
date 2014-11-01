#!/usr/bin/env python
#Filename: tic-tac-toe.py
#Description: Tic-Tac-Toe two player game
import sys,random,time, ConfigParser, logging

from Game import Game
from Player import Human
from Player import AI

import logging

if __name__ == '__main__':
    
    settings = ConfigParser.ConfigParser()
    settings.read('config.ini')

    logging.basicConfig(
        filename=settings.get("Log","File"),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    game = Game(settings)
    player1 = Human(settings.get("Main","PlayerOne"),settings)
    player2 = AI(settings.get("Main","PlayerTwo"))
    game.play( player1, player2)
