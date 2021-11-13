import numpy as np 
import cv2


def biggest_contours(contours): 

    biggest = np.array([])
    x, y, w, h = 0, 0, 0, 0
    maxArea = 0

    for i in contours:
        area = cv2.contourArea(i)

        if area > 50:

            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)

            if area > maxArea and len(approx) == 4:

                biggest = approx
                maxArea = area
         
    # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)

    return biggest, maxArea

        

def reOrder(points):
    
    points = points.reshape((4,2))
    pointsNew = np.zeros((4,1,2), dtype= np.int32)

    pointsNew[0] = points[np.argmin(points.sum(1))]
    pointsNew[3] = points[np.argmax(points.sum(1))]

    diff = np.diff(points, axis= 1)

    pointsNew[1] = points[np.argmin(diff)]
    pointsNew[2] = points[np.argmax(diff)]
    
    return pointsNew

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0
    return False

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False
    return True

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None




   