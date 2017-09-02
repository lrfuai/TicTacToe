import cv2
import numpy as np

class Matrix3x3:
    def __init__(self):
        self.m = []
        for item in range(3):
            self.m.append(["-","-","-"])

class CamListener :
    def onDetectPiece(self, x, y) :
        raise NotImplementedError( "Should have implemented this" ) 



class CamDetection :
    __cam = None
    __haveSubt = False
    __updateRef = False
    __listener = None
    __debounceCount = None
    __debounceAmount = 0
    __imgMatriz = 0

    #equ = cv2.norm(gray)
    __vpos_y = [80,240,400]
    __vpos_x = [100,260,420]

    def __init__ (self, listener, numCam, debounceAmount) :
        self.__cam = cv2.VideoCapture(numCam)
     
        #self.__cam.set(15, 0)
        #self.__cam.set(16, 100)
        #self.__cam.set(11, 50)

        self.__listener = listener
        m = Matrix3x3()
        self.__debounceCount = m.m        
        self.__debounceAmount = debounceAmount

    def updateRef(self) :
        self.__updateRef = True

    # pinta una matriz con la posiciones en la imagen de fondo    
    def pintar_fichas(self, matriz): 

        for row in range(3) :
            for col in range(3) :
                x= self.__vpos_x[row]
                y = self.__vpos_y[col]
                if (matriz[col][row] == "x"):            
                    cv2.rectangle(self.__imgMatriz,(x-30,y-30),(x+30,y+30),(255,0,0),2)
                elif (matriz[col][row] == "o"):    
                    cv2.circle(self.__imgMatriz,(x,y), 30, (0,255,0), 2)

        cv2.imshow('matriz', self.__imgMatriz)


    def process(self, key, showImage) :
        ret_val, img = self.__cam.read(1)
        #webcam = cv2.VideoCapture(1)
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)

        img = cv2.transpose(img)
        img = cv2.flip(img, 0)

        #define tipo de letra para el texto en patalla
        font = cv2.FONT_HERSHEY_SIMPLEX

        #equ = cv2.norm(gray)
        vpos_y = [80,240,400]
        vpos_x = [100,260,420]

        m = Matrix3x3()
        debounceTemp = m.m

        if self.__updateRef == True :  #con letra s graba imagenes de referencia
            self.__updateRef = False
            print("Actualizando imagen de referencia !")
            for pos_y in vpos_y:
                for pos_x in vpos_x:
                    #cv2.circle(img,(pos_x,pos_y), 80, (0,255,255), 1)
                    cv2.rectangle(img,(pos_x-80,pos_y-80),(pos_x+80,pos_y+80),(0,255,0),2)

                    #arma nombre del archivo de las imagenes de referencia   
                    sFile =  str(pos_y) + '_' + str(pos_x)
                    #agrega nombre del archivo en la imagen
                    cv2.putText(img,str(sFile),(pos_x-40,pos_y+70), font, 0.4,(255,255,255),1,cv2.LINE_AA)
                    #extrae el area de la imagen
                    ext_img = img[pos_y-80:pos_y+80, pos_x-80:pos_x+80] #gray[y1:y2, x1:x2]
                    #guarda la imagen final
                    cv2.imwrite( 'imagen/'+ sFile + '_T.png',ext_img)
                    self.__haveSubt = True
                    #print(sFile)

                    #cv2.line(gray,(0,0),(511,511),(255,0,0),5) #con -1 es todo de un solo color

        for pos_y in vpos_y:
            for pos_x in vpos_x:
                #cv2.circle(img,(pos_x,pos_y), 80, (0,255,255), 1)
                cv2.rectangle(img,(pos_x-80,pos_y-80),(pos_x+80,pos_y+80),(0,255,0),2)

                #arma nombre del archivo    
                sFile =  str(pos_y) + '_' + str(pos_x) 
                #agrega nombre del archivo en la imagen
                cv2.putText(img,str(sFile),(pos_x-40,pos_y+70), font, 0.4,(255,255,255),1,cv2.LINE_AA)
                #extrae el area de la imagen
                ext_img = img[pos_y-80:pos_y+80, pos_x-80:pos_x+80] #gray[y1:y2, x1:x2]
                #guarda la imagen final
                cv2.imwrite( 'imagen/' + sFile + '.png',ext_img)                
                #print(sFile)

                # cv2.rectangle(gray,(384,0),(510,128),(0,255,0),2s)

        if(showImage == True) :
            img_contorno = img.copy()

        if self.__haveSubt == True :
            for pos_y in vpos_y:
                for pos_x in vpos_x:
                    #arma nombre del archivo    
                    sFile =  str(pos_y) + '_' + str(pos_x) 

                    #Cargamos las dos imagenes para hacer las diferencias
                    diff1 = cv2.imread('imagen//'+ sFile +'.png')       
                    diff2 = cv2.imread('imagen//'+ sFile +'_T.png')

                    # Aplicamos suavizado para eliminar ruido
                    diff1 = cv2.GaussianBlur(diff1, (21, 21),0)
                    diff2 = cv2.GaussianBlur(diff2, (21, 21),0)

                    #Calculamos la diferencia absoluta de las dos imagenes
                    resta = cv2.absdiff(diff1, diff2)

                    # Aplicamos un umbral
                    umbral = cv2.threshold(resta, 25, 255, cv2.THRESH_BINARY)[1]
                    # Dilatamos el umbral para tapar agujeros
                    umbral = cv2.dilate(umbral, None, iterations=2)

                    # Copiamos el umbral para detectar los contornos
                    imagen_gris= umbral.copy()

                    # Convertimos en escala de grises para buscar los contornos
                    imagen_gris = cv2.cvtColor(imagen_gris, cv2.COLOR_BGR2GRAY)  

                    # Aplicamos suavizado para eliminar ruido
                    imagen_gris = cv2.GaussianBlur(imagen_gris, (21, 21),0)

                    # Buscamos los contornos
                    im, contornos, hierarchy = cv2.findContours(imagen_gris,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                    #Miramos cada uno de los contornos y, si no es ruido, dibujamos su Bounding Box sobre la imagen original
                    for c in contornos:                   
                        if cv2.contourArea(c) < 25000 and  cv2.contourArea(c) > 8000  :
                            posicion_x,posicion_y,ancho,alto = cv2.boundingRect(c) #Guardamos las dimensiones de la Bounding Box
                            cv2.rectangle(diff1,(posicion_x,posicion_y),(posicion_x+ancho,posicion_y+alto),(0,255,0),1) #Dibujamos la bounding box sobre diff1
                            #print ('Diferencia en: '+sFile)
                            #print(cv2.contourArea(c)) 


                            #pinta el circulo de la ficha detectada
                            if(showImage == True) :
                                cv2.circle(img_contorno,(pos_x,pos_y), 30, (0,255,255), 2)                                
                                

                            #vpos_y = [80,240,400]
                            #vpos_x = [100,260,420]
                            #nuevo sistema de deteccion y carga en matriz nestro 01-07-2017
                            for row in range(3) :
                                for col in range(3) :
                                    if (pos_x==vpos_x[row]):
                                       if (pos_y==vpos_y[col]):                                    
                                            debounceTemp[col][row]="o" # alamacena la ficha reconocida
                                       #     print (row,col,debounceTemp)
                            # if (pos_y==80):
                            #    if (pos_x==100):
                            #       debounceTemp[0][0]=1
                            #    elif (pos_x==260):
                            #       debounceTemp[0][1]=1
                            #    elif (pos_x==420):
                            #       debounceTemp[0][2]=1   

                               
                            # pieceX = pos_x - (vpos_x[0] - 80) #sistema mateo no funciona
                            # pieceY = pos_y - (vpos_y[0] - 80)
                            # pieceX = int(round(pieceX / 160))
                            # pieceY = int(round(pieceY / 160))
                            # debounceTemp[pieceX][pieceY] = 1
                            

                            

                #rimg=cv2.flip(img_contorno,0) #voltear horizontal
                #rimg=cv2.flip(rimg,1) #voltear vertial

        for x in range(3) :
            for y in range(3) :
                #cuenta la coincidencias
                if debounceTemp[x][y] == "o" :
                     self.__debounceCount[x][y] += 1             
                else :
                     self.__debounceCount[x][y] = 0


                #print(self.__debounceCount[x][y] , self.__debounceAmount )
                if self.__debounceCount[x][y] == self.__debounceAmount :
                    if self.__listener != None :
                        self.__listener.onDetectPiece(x, y)
                    else :
                        print("Pieza detectada en la posición %d - %d  " % (x, y))
                    
       


        if(showImage == True) :    
            cv2.imshow('contorno', img_contorno)  #muetra la ficha detectada
            self.__imgMatriz = img.copy()  #copia en la imagen global que usara pintarficha
            #self.pintar_fichas(debounceTemp) #prueba pintarficha

# Module test!
if __name__ == '__main__':

    camDet = CamDetection(None, 1, 15)  # numero de camara 0 o 1 y cantidad de repeticiones de imagen 15

    while True:
        #try:
        key = cv2.waitKey(1) & 0xFF

        if key == 27 :
            break
        elif key == 115 :
            camDet.updateRef()

        camDet.process(key, True)
        #except cv2.error as e:
        #    print ("Error")
        #    break
        #except ValueError:
        #    print ("Error 2")
        #    break

    cv2.destroyAllWindows()