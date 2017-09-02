
import numpy as np
import sys
from copy import copy

# 0 ->blank
# 1 --> 'x'
# 2-> 'o'
rows=3
cols=3
inf=9999999999
neg_inf=-9999999999
def printBoard(board):
    for j in range(0,rows):
        for i in range(0,cols):
            if board[i,j]==0:
                sys.stdout.write(' _ ')

            elif board[i,j]==1:
                sys.stdout.write(' X ')
            else:
                sys.stdout.write(' O ')
         
        print ('')
    
#for tic Tac Toe the heuris function will be evaluating the board position for each of the winning positions
heuristicTable=np.zeros((rows+1,cols+1))
numberOfWinningPositions=rows+cols+2 
for index in range(0,rows+1):
    heuristicTable[index,0]=10**index
    heuristicTable[0,index]=-10**index

winningArray=np.array([[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]])
#print 'the heuristicTable is ',heuristicTable
#print 'numberOfWinningPositions is ',numberOfWinningPositions
def utilityOfState(state):
    
    
    stateCopy=copy(state.ravel())
    heuristic=0
    #for i in range(0,numberOfWinningPositions):
    for i in range(0,cols):
        maxp=0
        minp=0
        for j in range(0, rows):
            if stateCopy[winningArray[i,j]]==2:
                maxp+=1
            elif stateCopy[winningArray[i,j]]==1:
                minp+=1
        
        #each iteration of the inner loop evalutes the objective function for each of the winning positions
        heuristic+=heuristicTable[maxp][minp]
    #print 'heuristic for state ',state,' is ',heuristic
    return heuristic

def minimax(state,alpha,beta,maximizing,depth,maxp,minp):
    
    if depth==0:
        return utilityOfState(state),state
    
    rowsLeft,columnsLeft=np.where(state==0)
    returnState=copy(state)
    if rowsLeft.shape[0]==0:
        return utilityOfState(state),returnState
        
    if maximizing==True:
        utility=neg_inf
        for i in range(0,rowsLeft.shape[0]):
            nextState=copy(state)
            nextState[rowsLeft[i],columnsLeft[i]]=maxp
            #print 'in max currently the Nextstate is ',nextState,'\n\n'
            Nutility,Nstate=minimax(nextState,alpha,beta,False,depth-1,maxp,minp)
            if Nutility > utility:
                utility=Nutility
                returnState=copy(nextState)
            if utility>alpha:
                alpha=utility
            if alpha >=beta :
                #print 'pruned'
                break;
        
        #print 'for max the best move is with utility ',utility,' n state ',returnState
        return utility,returnState

    else:
        utility=inf
        for i in range(0,rowsLeft.shape[0]):
            nextState=copy(state)
            nextState[rowsLeft[i],columnsLeft[i]]=minp
            #print 'in min currently the Nextstate is ',nextState,'\n\n'
            Nutility,Nstate=minimax(nextState,alpha,beta,True,depth-1,maxp,minp)
            if Nutility < utility:
                utility=Nutility
                returnState=copy(nextState)
            if utility< beta:
                beta=utility
            if alpha >=beta :
                #print 'pruned'
                break;
        return utility,returnState
        
def checkGameOver(state):
    stateCopy=copy(state)
    value=utilityOfState(stateCopy)
    print ("value",value)
    if value >=1000:
        return 1
    return -1