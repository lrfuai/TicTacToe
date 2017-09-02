
import numpy as np
import sys
from copy import copy

winningArray=np.array([[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]])
pos_casilla = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]

ficha_0 = winningArray[0][0]        
row=pos_casilla[ficha_0][0]
col=pos_casilla[ficha_0][1]

print (self.__matriz[col][row])