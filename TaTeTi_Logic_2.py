
import numpy as np
import sys
from copy import copy

class TaTeTi_Logic_2:
# 0 ->blank
# 1 --> 'x'
# 2-> 'o'
    
    __matriz = []#np.array([["-", "-", "-"],["-", "-", "-"],["-", "-", "-"]])

    def __init__ (self):
        self.__matriz= [["-", "-", "-"],["-", "-", "-"],["-", "-", "-"]]

    def init_matriz( self):
        self.__matriz= [["-", "-", "-"],["-", "-", "-"],["-", "-", "-"]]
        #print (self.__matriz)

    def put_ficha( self,col,row,pieza):
        self.__matriz[col][row]=pieza

    def get_ficha(self,col,row ):
        return self.__matriz[col][row]

    def get_matriz(self ):
        return self.__matriz

    def print_matriz_texto(self):
        print (self.__matriz[0])
        print (self.__matriz[1])
        print (self.__matriz[2])
        
    def mueve_robot(self):
        for row in range(3):
            for col in range(3):
                if self.__matriz[col][row] != "o":
                    if self.__matriz[col][row] != "x":
                        self.__matriz[col][row] = "x"
                        return


    

    def check_ganador(self,ficha):
        winningArray=np.array([[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]])
        pos_casilla = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]

        for nro_winn in range(8):
            ref_ficha = winningArray[nro_winn][0]        
            row=pos_casilla[ref_ficha][0]
            col=pos_casilla[ref_ficha][1]
            val_ficha_0 = self.__matriz[row][col]

            ref_ficha = winningArray[nro_winn][1]        
            row=pos_casilla[ref_ficha][0]
            col=pos_casilla[ref_ficha][1]
            val_ficha_1 = self.__matriz[row][col]

            ref_ficha = winningArray[nro_winn][2]        
            row=pos_casilla[ref_ficha][0]
            col=pos_casilla[ref_ficha][1]
            val_ficha_2 = self.__matriz[row][col]

            print ("pieza ...... ",val_ficha_0,val_ficha_1,val_ficha_2)

            if ((val_ficha_0 == ficha) and (val_ficha_1 == ficha) and (val_ficha_2 == ficha) ):
                return True
            
            


     #   for nro_casilla in range(9):
     #       print (pos_casilla [nro_casilla])
    #print 'the heuristicTable is ',heuristicTable
    #print 'numberOfWinningPositions is ',numberOfWinningPositions

