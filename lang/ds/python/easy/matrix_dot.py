def mat_dot(matrix1, matrix2):
    m = len(matrix1)
    n = len(matrix1[0])
    l = len(matrix2[0])
    if len(matrix1[0]) != len(matrix2):
        raise RuntimeError('matrix1[m n]!= matrix2[n l]')

    matrix3 = []
    for i in range(m):
        tmp_list = []
        for k in range(l):
            tmp = 0
            for j in range(n):
                tmp += matrix1[i][j] * matrix2[j][k]
            tmp_list.append(tmp)
        matrix3.append(tmp_list)
    return matrix3


def mat_dot2(matrix1, matrix2):
    m = len(matrix1)
    n = len(matrix1[0])
    l = len(matrix2[0])
    if len(matrix1[0]) != len(matrix2):
        raise RuntimeError('matrix1[m n]!= matrix2[n l]')

    matrix3 = []
    for i in range(m):
        tmp_list = []
        for k in range(l):
            tmp_list.append(sum([matrix1[i][j] * matrix2[j][k] for j in range(n)]))
        matrix3.append(tmp_list)
    return matrix3


def mat_dot3(matrix1, matrix2):
    m = len(matrix1)
    n = len(matrix1[0])
    l = len(matrix2[0])
    if len(matrix1[0]) != len(matrix2):
        raise RuntimeError('matrix1[m n]!= matrix2[n l]')

    matrix3 = []
    for i in range(m):
        matrix3.append([sum([matrix1[i][j] * matrix2[j][k] for j in range(n)]) for k in range(l)])
    return matrix3


def mat_dot4(matrix1, matrix2):
    m = len(matrix1)
    n = len(matrix1[0])
    l = len(matrix2[0])
    if len(matrix1[0]) != len(matrix2):
        raise RuntimeError('matrix1[m n]!= matrix2[n l]')

    matrix3 = [[sum([matrix1[i][j] * matrix2[j][k] for j in range(n)]) for k in range(l)] for i in range(m)]
    return matrix3


if __name__ == '__main__':
    m = 4
    n = 2
    l = 3

    a = [[j + i * n for j in range(n)] for i in range(m)]
    # print(a)
    """matrix a
    0  1
    2  3
    4  5
    6  7
    """
    # print(a[1][0])
    # print(len(a), len(a[0]))

    b = [[i + j for j in range(l)] for i in range(n)]
    # print(b)
    """matrix b
    0  1  2
    1  2  3
    """
    # print(len(b), len(b[0]))

    c = mat_dot(a, b)
    print(c)

    c = mat_dot2(a, b)
    print(c)

    c = mat_dot3(a, b)
    print(c)

    c = mat_dot4(a, b)
    print(c)
