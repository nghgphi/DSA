import cv2
import numpy as np
# from numpy.core.fromnumeric import size
from enum import Enum
import pytesseract

# phát hiện bảng caro
def detect_in_cell(img):
        try:
            contours, hierarchy =cv2.findContours(img, cv2.RETR_TREE ,cv2.CHAIN_APPROX_NONE)
            value = hierarchy.shape[1]
            for i in range(hierarchy.shape[1]):
                if hierarchy[0][i][2] == -1 and hierarchy[0][i][3] == -1:
                    value -= 1
            return value
        except TypeError:
            return 0
        except AttributeError:
            return 0
img = cv2.imread("data/caro3.jpg")
img = cv2.resize(img, (1200, 1200))
side = 80
k = 9

#  detect caro board
caroBoard = np.zeros((15, 15), dtype=np.uint8)

for i in range(15):
    for j in range(15):
        cell = img[side * i + k: side * (i+1) - k, side * j + k: side * (j+1) - k]

        imgGray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
        imgCanny = cv2.Canny(imgBlur, 100, 100)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        imgCanny = cv2.dilate(imgCanny, kernel= kernel, iterations= 1)

        caroBoard[i][j] = int(detect_in_cell(imgCanny))
        
print(caroBoard)
# row_temp = [caroBoard[4, 4 + k] for k in range(5)]
# print(type(row_temp))

# i = 1
# j = 1
# row_temp = [caroBoard[i, j + k] for k in range(5)]
# print(row_temp)
# print(np.any(row_temp = 2))


