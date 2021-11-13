import numpy as np 
import cv2
import pytesseract
import math
from function import *
import os

path_folder = r'dataset1\\'
path_result = r'sudoku_result\\'

for path in os.listdir(path_folder):


    image = cv2.imread(path_folder + path)

    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)

    imgCanny = cv2.Canny(imgGray, 50, 200, None, 3)

    imgTheshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)


    imgContours = image.copy()

    width = 450
    height = 450


    contours, hierarchy = cv2.findContours(imgTheshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    biggest, maxArea = biggest_contours(contours)

    # cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)

    if biggest.size != 0:

        biggest = reOrder(biggest)

        # print(biggest)

        # print(biggest.shape)

        cv2.drawContours(imgContours, biggest, -1, (255,0,0), 5)

        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0],[width, 0], [0, height],[width, height]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        imgWrap = cv2.warpPerspective(image, matrix, (width, height))



    # cv2.imshow('a', imgWrap)
        wrapGray = cv2.cvtColor(imgWrap, cv2.COLOR_BGR2GRAY)

        wrapBlur = cv2.GaussianBlur(wrapGray, (5, 5), 1)

        wrapCanny = cv2.Canny(wrapGray, 50, 200, None, 3)

        wrapTheshold = cv2.adaptiveThreshold(wrapBlur, 255, 1, 1, 3, 3)

        print(imgWrap.shape)

        #chia bảng sudoku
        sudoku = np.zeros((9,9), np.uint8)

        size = imgWrap.shape[0]//9

        for i in range(9):

            for j in range(9):

                cell = imgWrap[size*i+6:size*(i+1)-6, size*j + 6:size*(j+1) - 6]
                cellGray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

                cellBlur = cv2.GaussianBlur(cellGray, (5, 5), 1)

                cellCanny = cv2.Canny(cellGray, 50, 200, None, 3)

                cellTheshold = cv2.adaptiveThreshold(cellBlur, 255, 1, 1, 3, 3)
                
                
                pytesseract.pytesseract.tesseract_cmd= r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
                try:
                    text = pytesseract.image_to_string(cellTheshold,config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
                    sudoku[i][j] = int(text)
                except ValueError:
                    sudoku[i][j] = 0

            # print('\n')
        sudokuCopy = sudoku.copy()
        solve(sudoku)
        # print(sudoku)
        # cv2.imshow('a', wrapTheshold)
        # print(sudokuCopy)

        for i in range(9):

            for j in range(9):

                cell = imgWrap[size*i + 6:size*(i+1) - 6, size*j + 6:size*(j+1) - 6]
                cellGray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

                cellBlur = cv2.GaussianBlur(cellGray, (5, 5), 1)

                cellCanny = cv2.Canny(cellGray, 50, 200, None, 3)

                cellTheshold = cv2.adaptiveThreshold(cellBlur, 255, 1, 1, 11, 2)

                # if np.sum(cellTheshold) < 38*38*14:
                if sudokuCopy[i][j] == 0:

                    cv2.putText(imgWrap, str(sudoku[i][j]), (size*j + 20,size*(i+1) - 20), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)

        cv2.imwrite(path_result + path, imgWrap)


