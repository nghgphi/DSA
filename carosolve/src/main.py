import cv2
import numpy as np
from numpy.core.fromnumeric import diagonal, size
import pytesseract

# phát hiện bảng caro
def detectInCell(img):
        try:
            _, hierarchy =cv2.findContours(img, cv2.RETR_TREE ,cv2.CHAIN_APPROX_NONE)
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
# i = 4
# j = 7

caroBoard = np.zeros((15, 15), dtype=np.uint8)

for i in range(15):
    for j in range(15):
        cell = img[side * i + k: side * (i+1) - k, side * j + k: side * (j+1) - k]

        imgGray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
        imgCanny = cv2.Canny(imgBlur, 100, 100)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        imgCanny = cv2.dilate(imgCanny, kernel= kernel, iterations= 1)

        caroBoard[i][j] = int(detectInCell(imgCanny))
        


print(caroBoard)

# kiểm tra các điều kiện thắng thua
PATTERN_OPEN_THREE = np.array([
                        [0, 0, 4, 4, 4, 0, 0],
                        [0, 0, 4, 4, 4, 0, 2],
                        [2, 0, 4, 4, 4, 0, 0],
                        [0, 0, 4, 4, 0, 4, 0],
                        [2, 0, 4, 4, 0, 4, 0],
                        [0, 4, 4, 0, 4, 0, 2],
                        [0, 4, 4, 0, 4, 0, 0],
                        [0, 4, 4, 4, 0, 0, 2],
                        [0, 4, 4, 4, 0, 0, 0],
                        [0, 0, 0, 4, 4, 4, 0],
                        [2, 0, 0, 4, 4, 4, 0]
                    ])
def include_element(a):
        for k in range(len(PATTERN_OPEN_THREE)):
                if np.all(a == PATTERN_OPEN_THREE[k]):
                        return True
        return False
    
def have_4_consecutive(a):
    for i in range(len(a) - 3):
        if a[i] == a[i+1] and a[i] == a[i+2] and a[i] == a[i+3]:
            return True
    return False

def check_row_open_three(i, j):
    results = []
    if j <= 8:
        row_temp = np.array([caroBoard[i, j + k] for k in range(7)])

        if include_element(row_temp):
            for k in np.where(row_temp[1:6] == 0)[0]:
                    row_temp[k + 1] += 4
                    if have_4_consecutive(row_temp):
                        # row_temp[i] -= 4
                        results.append([i, j + k + 1])
                    row_temp[k + 1] -= 4
    return results
def check_column_open_three(i, j):
    results = []
    if i <= 8:
        column_temp = np.array([caroBoard[i + k, j] for k in range(7)])

        if include_element(column_temp):
            for k in np.where(column_temp[1:6] == 0)[0]:
                    column_temp[k + 1] += 4
                    if have_4_consecutive(column_temp):
                        # column_temp[i] -= 4
                        results.append([i + k + 1, j])
                    column_temp[k + 1] -= 4
    return results

def check_diag_1_open_three(i, j):
    # if i <= 8 and j <= 8:
        results = []
        diag_temp = np.array([caroBoard[i + k, j + k] for k in range(7)])

        if include_element(diag_temp):
            for k in np.where(diag_temp[1:6] == 0)[0]:
                    diag_temp[k + 1] += 4
                    if have_4_consecutive(diag_temp):
                        # diag_temp[k] -= 4
                        results.append([i + k + 1, j + k + 1])
                    diag_temp[k + 1] -= 4
        return results

def check_diag_2_open_three(i, j):# i <= 8 and j >= 6
        diag_temp = np.array([caroBoard[i + k, j - k] for k in range(7)])
        results = []
        if include_element(diag_temp):
            for k in np.where(diag_temp[1:6] == 0)[0]:
                    diag_temp[k + 1] += 4
                    if have_4_consecutive(diag_temp):
                        # diag_temp[k] -= 4
                        results.append([i + k + 1, j - k - 1])
                    diag_temp[k + 1] -= 4
        return results         
        


def check_row_four(i, j):
    if j <= 9:
 
        row_temp = np.array([caroBoard[i, j + k] for k in range(5)])
        if np.all(row_temp != 2) :
            equal_zero = np.where(np.array(row_temp) == 0)
            if size(equal_zero) == 1:
                return [i, j + equal_zero[0][0]]
        return [-1, -1]
    return [-1, -1]


def check_column_four(i, j):
    if i <= 9 :
        column_temp = np.array([caroBoard[i + k, j] for k in range(5)])
        
        if np.all(column_temp != 2):
            equal_zero = np.where(column_temp == 0)
            if size(equal_zero) == 1:
                return [i, j + equal_zero[0][0]]
        return [-1, -1]
    return [-1, -1]

def check_cross_left_right_four(i, j):
    if i <= 9 and j <= 9:
        diagonal_temp = np.array([caroBoard[i + k, j + k] for k in range(5)])
        if np.all(diagonal_temp != 2):
            equal_zero = np.where(diagonal_temp == 0)
            if size(equal_zero) == 1:
                return [i + equal_zero[0][0], j + equal_zero[0][0]]

    return [-1, -1]

def check_cross_right_left_four(i, j):
    if i <= 9 and j >= 4:
        diagonal_temp = np.array([caroBoard[i + k, j - k] for k in range(5)])
        if np.all(diagonal_temp != 2):
            equal_zero = np.where(diagonal_temp == 0)
            if size(equal_zero) == 1:
                return [i + equal_zero[0][0], j + equal_zero[0][0]]
        return [-1, -1]
    return [-1 , -1 ]


print('Player is 2')
print('Vi tri nuoc don la: ')
result_list_four = []
result_list_three = []
for i in range(15):
    for j in range(15):
        result_list_four = [
                        check_row_four(i, j),
                        check_column_four(i, j),
                        check_cross_left_right_four(i, j),
                        check_cross_right_left_four(i, j)
                ]
        row_three = check_row_open_three(i, j)
        column_three = check_column_open_three(i, j)
        if len(row_three) > 0:
            for k in range(len(row_three)):
                result_list_three.append(row_three[k])

        if len(column_three) > 0:
            for k in range(len(column_three)):
                result_list_three.append(column_three[k])
        
        if i <= 8 and j <= 8:
            diag_1_three = check_diag_1_open_three(i, j)
            if len(diag_1_three) > 0:
                for k in range(len(diag_1_three)):
                    result_list_three.append(diag_1_three[k])
        if i <= 8 and j >= 6:
            diag_2_three = check_diag_2_open_three(i, j)
            if len(diag_2_three) > 0:
                for k in range(len(diag_2_three)):
                    result_list_three.append(diag_2_three[k])

        
        for k in range(len(result_list_four)):
            if result_list_four[k] != [-1, -1]:
                print(result_list_four[k])

res = []
seen = set()

print('Vi tri nuoc doi la: ')
for x in result_list_three:
    x_set = frozenset(x)
    if x_set not in seen:
        res.append(x)
        seen.add(x_set)
print(res)
        # for k in range(len(result_list_three)):
        #     if len(result_list_three[k]) != 0:
        #         print(result_list_three[k])
    #     print(result_list, end= " ")
    #     print('\n')
    # print('\n')

        




# def CheckDoubleRow(i, j):

#     if j == 1:
#         # rowTemp = np.array([caroBoard[i][j-2], caroBoard[i][j-1], caroBoard[i][j], caroBoard[i][j+1], caroBoard[i][j+2], caroBoard[i][j+3],caroBoard[i][j+4]])
#         visited = np.array(caroBoard[i][j:j+3])
#         unvisited = np.array([caroBoard[i][j-1], caroBoard[i][j+3], caroBoard[i][j+4]])
#         if all(visited == 2) and all(unvisited == 0):
#             return (2, i, j+3)
#         if all(visited == 4) and all(unvisited == 0):
#             return (4, i, j+3)

    # if j > 1:
    #     visited = np.array(caroBoard[i][j:j+3])
    #     unvisited = np.array([caroBoard[i][j-2], caroBoard[i][j-1], caroBoard[i][j+3], caroBoard[i][j+4]])
    #     if all(visited == 2) and all(unvisited == 0):
    #         return (2, i, j-1)
    #     if all(visited == 2) and all(np.array([caroBoard[i][j-2], caroBoard[i][j-1], caroBoard[i][j+3]]) == 0) and caroBoard[i][j+4] == 4:
    #         return (2, i, j-1)
    #     if all(visited == 2) and all(np.array([caroBoard[i][j+4], caroBoard[i][j-1], caroBoard[i][j+3]]) == 0) and caroBoard[i][j-1] == 4:
    #         return (2, i, j+3)
    # if j > 0 and caroBoard[i][j] == 2 and caroBoard[i][j+1] == 2 and caroBoard[i][j+2] == 2:
    #         result_1 = []
    #         if j > 1:
    #             rowTemp = np.array([caroBoard[i][j-2], caroBoard[i][j-1], caroBoard[i][j+3], caroBoard[i][j+4]])
    #             equalFour = np.array([rowTemp == 4])
    #             if (not equalFour[1]) and (not equalFour[2]) and equalFour[0]:
    #                     result_1.append([2, i, j-1])
    #             if (not equalFour[1]) and (not equalFour[2]) and equalFour[3]:
    #                     result_1.append([2, i, j+4])
    #             if len(result_1) > 0:
    #                 return result_1
    #             else:
    #                 return (-1, -1, -1)
    #         if j == 1:
    #             rowTemp = np.array([caroBoard[i][j-1], caroBoard[i][j+3], caroBoard[i][j+4]])
    #             equalZero = np.where(rowTemp != 0)
    #             if len(equalZero) != 0:
    #                 return (-1, -1, -1)
    #             else:
    #                 return (2, i, j+3)
        # if caroBoard[i][j] == 2 and caroBoard[i][j+1] == 2 and caroBoard[i][j+2] == 2:
        #     result_1 = []
        #     if j > 1:
        #         rowTemp = np.array([caroBoard[i][j-2], caroBoard[i][j-1], caroBoard[i][j+3], caroBoard[i][j+4]])
        #         equalFour = np.array([rowTemp == 4])
        #         if (not equalFour[1]) and (not equalFour[2]) and equalFour[0]:
        #                 result_1.append([2, i, j-1])
        #         if (not equalFour[1]) and (not equalFour[2]) and equalFour[3]:
        #                 result_1.append([2, i, j+4])
        #         if len(result_1) > 0:
        #             return result_1
        #         else:
        #             return (-1, -1, -1)
        #     if j == 1:
        #         rowTemp = np.array([caroBoard[i][j-1], caroBoard[i][j+3], caroBoard[i][j+4]])
        #         equalZero = np.where(rowTemp != 0)
        #         if len(equalZero) != 0:
        #             return (-1, -1, -1)
        #         else:
        #             return (2, i, j+3)



                    


                





# dự đoán khả năng thắng thua
# print('Assume player is X')
# for i in range(15):
#     for j in range(15):
#         # xử lý nước đôi 
#         if j == 1:
#         # rowTemp = np.array([caroBoard[i][j-2], caroBoard[i][j-1], caroBoard[i][j], caroBoard[i][j+1], caroBoard[i][j+2], caroBoard[i][j+3],caroBoard[i][j+4]])
#             visited = np.array(caroBoard[i][j:j+3])
#             unvisited = np.array([caroBoard[i][j-1], caroBoard[i][j+3], caroBoard[i][j+4]])
#             if all(visited == 2) and all(unvisited == 0):

#                 return (2, i, j+3)
#             if all(visited == 4) and all(unvisited == 0):
#                 return (4, i, j+3)

#         if j > 1:
#             visited = np.array(caroBoard[i][j:j+3])
#             unvisited = np.array([caroBoard[i][j-2], caroBoard[i][j-1], caroBoard[i][j+3], caroBoard[i][j+4]])
#             if all(visited == 2) and all(unvisited == 0):
#                 return (2, i, j-1)
#             if all(visited == 2) and all(np.array([caroBoard[i][j-2], caroBoard[i][j-1], caroBoard[i][j+3]]) == 0) and caroBoard[i][j+4] == 4:
#                 return (2, i, j-1)
#             if all(visited == 2) and all(np.array([caroBoard[i][j+4], caroBoard[i][j-1], caroBoard[i][j+3]]) == 0) and caroBoard[i][j-1] == 4:
#                 return (2, i, j+3)

#         #xử lý cột:
#         # a_1, b_1, c_1 = zip(checkColumn(i, j))
#         # if a_1 == 2:
#         #     print('Player can win at: (', b_1, ', ', c_1, ')')
#         # if a_1 == 4:
#         #     print('Player can lose at: (', b_1, ', ', c_1, ')')

#         # # xử lý hàng:  
#         result = CheckCrossUtoDandLtoR(i, j)
#         if result[0] == 2:
#             print('Player can win at: (', result[1], ', ', result[2], ')')
#         if result[0] == 4:
#             print('Player can lose at: (', result[1], ', ', result[2], ')')
#         else:
#             pass

#         # a_3, b_3, c_3 = checkCrossU2DandL2R(i, j)
#         # a_4, b_4, c_4 = checkCrossU2DandR2L(i, j)

#         # if a_3 == 2:
#         #     print('Player can win at: (', b_3, ', ', c_3, ')')
#         # if a_3 == 4:
#         #     print('Player can lose at: (', b_3, ', ', c_3, ')')

#         # if a_4 == 2:
#         #     print('Player can win at: (', b_4, ', ', c_4, ')')
#         # if a_4 == 4:
#         #     print('Player can lose at: (', b_4, ', ', c_4, ')')


# cv2.imshow('a', img)

# print(caroBoard)
cv2.waitKey(0)