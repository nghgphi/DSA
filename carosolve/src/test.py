import numpy as np

def include_element(a):
        for k in range(len(PATTERN_OPEN_THREE)):
                if np.all(test == PATTERN_OPEN_THREE[k]):
                        return True
        return False



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
                    ], dtype= np.uint8)

column_temp = np.array([0, 0, 4, 4, 4, 0, 0])

def have_4_consecutive(a):
    for i in range(len(a) - 3):
        if a[i] == a[i+1] and a[i] == a[i+2] and a[i] == a[i+3]:
            return True
    return False

results = []
# print(np.where(column_temp[1:6] == 0)[0])
for k in np.where(column_temp[1:6] == 0)[0]:
        print(k)
        column_temp[k + 1] += 4
        if have_4_consecutive(column_temp):
                results.append([k + 1])
        column_temp[k + 1] -= 4

print(results)