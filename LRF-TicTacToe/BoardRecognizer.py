import cv2
import numpy as np
from matplotlib import pyplot as plt
import random
import time
import logging

class BoardNotMatchingCellNumber (Exception):
    pass

class BoardRecognizer:
    CellMinArea = None
    CellMaxArea = None
    ContentMinArea = None
    ContentMaxArea = None
    Debug = False


    def __init__(self, settings):
        logging.info("Initilizing Board Recognizer")
        
        self.CellMinArea = settings.getfloat("BoardDetector","CellMinArea")
        self.CellMaxArea = settings.getfloat("BoardDetector","CellMaxArea")
        self.ContentMinArea = settings.getfloat("BoardDetector","ContentMinArea")
        self.ContentMaxArea = settings.getfloat("BoardDetector","ContentMaxArea")
        self.Debug = settings.get("BoardDetector","Debug")

        logging.info("CellMinArea: " + str(self.CellMinArea))
        logging.info("CellMaxArea: " + str(self.CellMaxArea))
        logging.info("ContentMinArea: " + str(self.ContentMinArea))
        logging.info("ContentMaxArea: " + str(self.ContentMaxArea))
        logging.info("Debug: " + str(self.Debug))

    def __GetCountournsBetween(self, contours, areaFrom, areaTo):
        ret = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if( area > areaFrom and area < areaTo):
                approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                ret.append(approx)
        logging.info("Found " + str(len(ret)) + " Contourns between " + str(areaFrom) + " and " + str(areaTo))
        return ret

    def __ExtractContournsOnImage(self, contours, img):
        list = []
        for cnt in contours:
            hull = cv2.convexHull(cnt)
            area = cv2.contourArea(hull)
            P = cv2.arcLength(hull,True)

            x,y,w,h = cv2.boundingRect(hull)
            roi = img[y:y+h,x:x+w]
            list.append(roi)
        return list

    def __SaveContournsImages(self, contours, img, name):
        number = 0
        for imgCnt in self.__ExtractContournsOnImage(contours,img):
            cv2.imwrite("Imgs/"+str(name)+"-"+str(number)+".jpg",imgCnt)
            number = number +1


    def GetCells(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.imwrite("Imgs/Grayed.jpg",gray)
        cv2.imwrite("Imgs/Monochrome.jpg",thresh)
        cv2.drawContours(img, contours, -1, (0,255,0), 3)
        cv2.imwrite("Imgs/Contoruns.jpg",img)

        filteredBlocks = self.__GetCountournsBetween(contours, self.CellMinArea,self.CellMaxArea)
        if(self.Debug):
            self.__SaveContournsImages(filteredBlocks, img, "GetCells")
        return filteredBlocks

    def GetCellsImgs(self,img):
        return self.__ExtractContournsOnImage(self.GetCells(img), img)

    def GetContents(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        filteredChars = self.__GetCountournsBetween(contours, self.ContentMinArea,self.ContentMaxArea)
        if(self.Debug):
            self.__SaveContournsImages(filteredChars, img, "GetContent")
        return filteredChars

    def GetContentsImg(self, img):
        return self.__ExtractContournsOnImage(self.GetContents(img),img)
     
class Cell:
    Detector = None
    Img = None
    Key = None

    def __init__(self, detector, key):
        self.Detector = detector
        self.Key = key

    def isEmpty(self):
        return len (self.Detector.GetContents(self.Img)) == 0


class OpticalBoard:

    Cells = []
    Detector = None
    Camera = None
    RecognizeErrorSleep = None
    BufferFramesToDiscard = None

    def __init__ (self, settings):
        logging.info("Initilizing Optical Board")
        self.Detector = BoardRecognizer(settings)
        self.Camera = cv2.VideoCapture(settings.getint("OpticalBoard","CameraId"))
        self.RecognizeErrorSleep = settings.getfloat("OpticalBoard","RecognizeErrorSleep")
        self.BufferFramesToDiscard  = settings.getint("OpticalBoard","BufferFramesToDiscard")
        
        for pos in settings.get("OpticalBoard","Positions").split(","):
            self.Cells.append(Cell(self.Detector, pos))

    def __Update(self, img):
        cells = self.Detector.GetCellsImgs(img);
        logging.info("Searching For " + str(len(self.Cells)) + " Cells...")
        logging.info(str(len(cells)) + " Cells Recognized...")
        if(len(cells) == len(self.Cells)) :
            for i in range(0,len(self.Cells)) :
                self.Cells[i].Img = cells[i]
            logging.info("Done!")
        else :
            logging.info("Failed!")
            raise BoardNotMatchingCellNumber()
    
    def Recognize(self):
        logging.info("Start Recognition")
        cantDetect = True
        while(cantDetect):
            try:
                for i in range(0,self.BufferFramesToDiscard):
                    ret, frame = self.Camera.read()
                logging.info("Frame Stracted")
                cv2.imwrite("Imgs/frame.jpg",frame)
                self.__Update(frame)
                cantDetect = False;
            except BoardNotMatchingCellNumber:
                time.sleep(self.RecognizeErrorSleep)
                


if __name__ == '__main__':
    cap = cv2.VideoCapture(1)

    aBoard = OpticalBoard( (0,1,2,3,4,5,8,7,6) )

    while (True):
        cantDetect = True
        while(cantDetect):
            try:
                
                ret, frame = cap.read()
                ret, frame = cap.read()
                ret, frame = cap.read()
                ret, frame = cap.read()
                ret, frame = cap.read()

                aBoard.Update(frame)
                
                for aCell in aBoard.Cells :
                    if(aCell.isEmpty()):
                        print "La Celda " + str(aCell.Key) + " Esta Vacia"
                    else :
                        print "La Celda " + str(aCell.Key) + " Esta Ocupada"
                time.sleep(2)
                print chr(13)
            except BoardNotMatchingCellNumber:
               # time.sleep(.5)
                cantDetect = False;
        
        print "---------------------------------------------------"
        cantDetect = True
        time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
