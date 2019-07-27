
def normal_leven(str1, str2):
    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1
    matrix = [0 for n in range(len_str1 * len_str2)]
    for i in range(len_str1):
        matrix[i] = i
    for j in range(0, len(matrix), len_str1):
        if j % len_str1 == 0:
            matrix[j] = j // len_str1
    for i in range(1, len_str1):
        for j in range(1, len_str2):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[j * len_str1 + i] = min(matrix[(j - 1) * len_str1 + i] + 1,
                                           matrix[j * len_str1 + (i - 1)] + 1,
                                           matrix[(j - 1) * len_str1 + (i - 1)] + cost)
    leven_dist = str(matrix[-1]) + '/' + str(len_str1 - 1)

    return leven_dist

if __name__ == '__main__':
    w1 = 'there is a dog'
    w2 = 'there is dog'
    dist = normal_leven(w1, w2)
    print(dist)