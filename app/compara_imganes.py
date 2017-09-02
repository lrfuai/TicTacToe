import cv2
import numpy as np

while True:

        key = cv2.waitKey(100)
        print (key)    
        if key == 32 : # SPACE
            mask = np.int16(img.copy())
            haveSubt = True
        elif key == 27 :
            break # Break on ESC    

        #Cargamos las dos imagenes para hacer las diferencias
        diff1 = cv2.imread('imagen//80_100.png')
        diff2 = cv2.imread('imagen//80_100_T.png')

        gris = cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY)
        # Aplicar suavizado Gaussiano
        gauss = cv2.GaussianBlur(gris, (5,5), 0)         
        cv2.imshow("suavizado", gauss)

        diff1 = cv2.GaussianBlur(gauss, (5, 5), 0)
        diff2 = cv2.GaussianBlur(diff2, (51, 51), 0)

        #Calculamos la diferencia absoluta de las dos imagenes
        resta = cv2.absdiff(diff1, diff2)

        # Aplicamos un umbral
        umbral = cv2.threshold(resta, 25, 255, cv2.THRESH_BINARY)[1]

        # Dilatamos el umbral para tapar agujeros
        umbral = cv2.dilate(umbral, None, iterations=2)
        
        # Copiamos el umbral para detectar los contornos
        imagen_gris= umbral.copy()

        #Buscamos los contornos
        imagen_gris = cv2.cvtColor(imagen_gris, cv2.COLOR_BGR2GRAY)   
        im, contornos, hierarchy = cv2.findContours(imagen_gris,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
 
         
        #Miramos cada uno de los contornos y, si no es ruido, dibujamos su Bounding Box sobre la imagen original
        for c in contornos:
            if cv2.contourArea(c) < 500:
                posicion_x,posicion_y,ancho,alto = cv2.boundingRect(c) #Guardamos las dimensiones de la Bounding Box
                cv2.rectangle(diff1,(posicion_x,posicion_y),(posicion_x+ancho,posicion_y+alto),(0,0,255),2) #Dibujamos la bounding box sobre diff1
        
        cv2.imshow('Imagen1', diff1)
        cv2.imshow('Imagen2', diff2)
        cv2.imshow('Diferencias detectadas', imagen_gris)

cv2.destroyAllWindows()