"""
0: pass
1: wall
2: gone
"""

MAZE = [[0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]]
#
# MAZE = [
#     [0, 0, 0, 0],
#     [0, 0, 1, 0],
#     [1, 0, 1, 0],
#     [1, 0, 0, 0],
# ]

X_START = 0
Y_START = 0
X_END = len(MAZE) - 1
Y_END = len(MAZE[0]) - 1
PASSING_PATH = [[1 for _ in range(Y_END + 1)] for _ in range(X_END + 1)]
CORRECT_PATH = [[1 for _ in range(Y_END + 1)] for _ in range(X_END + 1)]

# pri nt(X_START, Y_START)
# print(X_END, Y_END)
# print(MAZE[X_START][Y_START])
# print(MAZE[X_END][Y_END])
# print(MAZE)
# print(PATH)


# recursive
def find_path1(x, y):
    if x is X_END and y is Y_END:
        MAZE[x][y] = 2
        show_path(MAZE)
        return True

    if x < X_START or x > X_END or y < Y_START or y > Y_END:
        return False

    if MAZE[x][y] == 1 or MAZE[x][y] == 2:
        return False

    if MAZE[x][y] == 0:
        MAZE[x][y] = 2

    show_path(MAZE)

    if find_path1(x - 1, y) or find_path1(x + 1, y) or find_path1(x, y - 1) or find_path1(x, y + 1):
        return True

    return False


# recursive
def find_path2(x, y):
    if x is X_END and y is Y_END:
        CORRECT_PATH[x][y] = 2
        show_path(CORRECT_PATH)
        return True

    if MAZE[x][y] == 1 or PASSING_PATH[x][y] == 2:
        return False

    PASSING_PATH[x][y] = 2

    if x > X_START:
        if find_path2(x - 1, y):
            CORRECT_PATH[x][y] = 2
            show_path(CORRECT_PATH)
            return True

    if x < X_END:
        if find_path2(x + 1, y):
            CORRECT_PATH[x][y] = 2
            show_path(CORRECT_PATH)
            return True

    if y > Y_START:
        if find_path2(x, y - 1):
            CORRECT_PATH[x][y] = 2
            show_path(CORRECT_PATH)
            return True

    if y < Y_END:
        if find_path2(x, y + 1):
            CORRECT_PATH[x][y] = 2
            show_path(CORRECT_PATH)
            return True

    return False


# stack
def find_path3(x, y):
    path_stack = []
    passing_path_stack = []
    is_exist = False

    while True:
        if MAZE[x][y] == 0 and not (x, y) in passing_path_stack:
            passing_path_stack.append((x, y))

            if not (x, y) in path_stack:
                path_stack.append((x, y))

        if x is X_END and y is Y_END:
            is_exist = True
            break

        if x < X_END and MAZE[x+1][y] == 0 and not(x+1, y) in passing_path_stack:
            x += 1
            continue

        if x > X_START and MAZE[x-1][y] == 0 and not(x-1, y) in passing_path_stack:
            x -= 1
            continue

        if y < Y_END and MAZE[x][y+1] == 0 and not(x, y+1) in passing_path_stack:
            y += 1
            continue

        if y > Y_START and MAZE[x][y-1] == 0 and not(x, y-1) in passing_path_stack:
            y -= 1
            continue

        if MAZE[x][y] == 0 and (x, y) in passing_path_stack:
            x, y = path_stack.pop()
            continue

        break

    print(path_stack)
    return is_exist


# queue
def find_path4(x, y):
    path_queue = [(x, y)]
    passing_path_queue = []
    is_exist = False

    while True:
        tmp_queue = []

        for x, y in path_queue:
            if MAZE[x][y] == 0 and not (x, y) in passing_path_queue:
                passing_path_queue.append((x, y))

            if x is X_END and y is Y_END:
                is_exist = True
                break

            if x < X_END and MAZE[x+1][y] == 0 and not(x+1, y) in passing_path_queue and not (x+1, y) in tmp_queue:
                x += 1
                tmp_queue.append((x, y))

            if x > X_START and MAZE[x-1][y] == 0 and not(x-1, y) in passing_path_queue and not (x-1, y) in tmp_queue:
                x -= 1
                tmp_queue.append((x, y))

            if y < Y_END and MAZE[x][y+1] == 0 and not(x, y+1) in passing_path_queue and not (x, y+1) in tmp_queue:
                y += 1
                tmp_queue.append((x, y))

            if y > Y_START and MAZE[x][y-1] == 0 and not(x, y-1) in passing_path_queue and not (x, y-1) in tmp_queue:
                y -= 1
                tmp_queue.append((x, y))

        if tmp_queue == [] or is_exist is True:
            break

        path_queue = tmp_queue

    print(passing_path_queue)

    return is_exist


def show_path(path):
    for j in path:
        for i in j:
            print(i, end=' ')
        print()
    print()


if __name__ == '__main__':
    # print(find_path2(0, 0))
    # print(find_path1(0, 0))
    # print(find_path3(0, 0))
    print(find_path4(0, 0))
