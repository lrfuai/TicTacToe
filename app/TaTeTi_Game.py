#from camDetection import *
from camDetection_Canny import *
from armMovement import *
from TaTeTi_Logic_2 import *

# Config parameters!
camNum = 1
debounceAmount = 10 # Veces que se necesita comprobar que hay algo
cycleTime = 0.1 # Segundos que dura cada ciclo
#serialPath = "/dev/ttyUSB0" # Linux
activarRobot = False
serialPath = "COM7" # Puerto serie de Windows


class TaTeTi :

	__robotTurn = False
	__camDet = None
	__armMov = None
	__Logic = None
	#__board = np.zeros((rows,cols))
	__pieceToGet = 1


	def __init__(self) :
		self.__camDet = CamDetection(self, camNum, debounceAmount)
		self.__armMov = ArmMovement(serialPath)
		self.__Logic = TaTeTi_Logic_2()
		#for i in range(3):
		#	self.__board.append([0,0,0])

	def onDetectPiece(self, x, y) :
		#if(self.__board[x][y] == 0) :


			
			print("Pieza detectada en %d - %d  " % (x, y))

			
			

			#print (self.__Logic.get_ficha (x,y))
			if (self.__Logic.get_ficha (x,y)=="o"):
				print("Pieza ya reconocida")
			else:	
				print ("Movio el humano")
				self.__Logic.put_ficha (x,y,"o")
				self.__Logic.print_matriz_texto()
				self.__camDet.pintar_fichas(self.__Logic.get_matriz())								

				if(self.__Logic.check_ganador("o")): 
					print ("GANO EL HUMANO")
				else:
					print ("Movio el robot")
					self.__Logic.mueve_robot()
					self.__Logic.print_matriz_texto()
					self.__camDet.pintar_fichas(self.__Logic.get_matriz())
					
					if(self.__Logic.check_ganador("x")): 
						print ("GANO EL ROBOT")	
					

			if activarRobot :
				print ("Moviendo brazo robot")
				# # Dejamos la pieza
				# if(self.__pieceToGet < 5) :	
				# 	self.__armMov.getPiece(self.__pieceToGet)
				# 	if self.__board[0][0] != state[0][0] :
				# 		self.__armMov.dropPieceOnBlock(7)

				# 	elif self.__board[0][1] != state[0][1] :
				# 		self.__armMov.dropPieceOnBlock(8)

				# 	elif self.__board[0][2] != state[0][2] :
				# 		self.__armMov.dropPieceOnBlock(9)

				# 	elif self.__board[1][0] != state[1][0] :
				# 		self.__armMov.dropPieceOnBlock(4)

				# 	elif self.__board[1][1] != state[1][1] :
				# 		self.__armMov.dropPieceOnBlock(5)

				# 	elif self.__board[1][2] != state[1][2] :
				# 		self.__armMov.dropPieceOnBlock(6)

				# 	elif self.__board[2][0] != state[2][0] :
				# 		self.__armMov.dropPieceOnBlock(1)

				# 	elif self.__board[2][1] != state[2][1] :
				# 		self.__armMov.dropPieceOnBlock(2)

				# 	elif self.__board[2][2] != state[2][2] :
				# 		self.__armMov.dropPieceOnBlock(3)

			# self.__pieceToGet += 1

			# value=checkGameOver(self.__board)
			# if value==1:
			# 	print ("Gano el robot segui participando!!!")
			# else :
			# 	self.__camDet.updateRef()

	def run(self) :
		while True :
			key = cv2.waitKey(1) & 0xFF
			if key == 27 :
				break
			elif key == 115 :  #inicializa al presionar s
				#self.__board = np.zeros((rows,cols))
				
				self.__camDet.updateRef()
				#self.__pieceToGet = 1
				self.__Logic.init_matriz()

			self.__camDet.process(key, True)

			sleep(cycleTime)


if __name__ == '__main__' :
	game = TaTeTi()
	print ("presiona la tecla S para comenzar!")

	game.run()