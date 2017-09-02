import cv2
import numpy as np

img = cv2.imread('tablero.jpg')
rows,cols,ch = img.shape

h=0
pts1 = np.float32([[65,55],[368,52],[28,387],[389,400]])
pts2 = np.float32([[0+h,0+h],[300+h,0+h],[0+h,300+h],[320+h,300+h]])
M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M,(640,480))

cv2.imshow('orignal', img)
cv2.imshow('perpectiva', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

# plt.subplot(121),plt.imshow(img),plt.title('Input')
# plt.subplot(122),plt.imshow(dst),plt.title('Output')
# dst.show()