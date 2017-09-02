import numpy as np
import cv2

cam = None
updateRef = False

def updateRef() :
        updateRef = True

def detectar_borde() : 
		# Cargamos la imagen
		
		ret_val, original = cam.read(1)
		#original = cv2.imread("imagen/tablero.jpg")
		cv2.imshow("original", original)
		 
		# Convertimos a escala de grises
		gris = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
		 
		# Aplicar suavizado Gaussiano
		gauss = cv2.GaussianBlur(gris, (5,5), 0)
		 
		cv2.imshow("suavizado", gauss)
		 
		# Detectamos los bordes con Canny
		canny = cv2.Canny(gauss, 50, 150)
		 
		cv2.imshow("canny", canny)
		 
		# Buscamos los contornos
		(_, contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		 
		# Mostramos el número de monedas por consola
		print("He encontrado {} objetos".format(len(contornos)))
		 
		cv2.drawContours(original,contornos,-1,(0,0,255), 2)
		cv2.imshow("contornos", original)
		 
		cv2.waitKey(0)

if __name__ == '__main__':

    #camDet = CamDetection(None, 1, 15)  # numero de camara 0 o 1 y cantidad de repeticiones de imagen 15
    cam = cv2.VideoCapture(1)

    while True:
        #try:
        key = cv2.waitKey(1) & 0xFF

        if key == 27 :
            break
        elif key == 115 :
            updateRef()

        detectar_borde()
        #except cv2.error as e:
        #    print ("Error")
        #    break
        #except ValueError:
        #    print ("Error 2")
        #    break

    cv2.destroyAllWindows()