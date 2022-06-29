import time

def loop_solution(c, n):
    """n x c =
    = c + c + c + ...
    :param c:
    :param n:
    :return:
    """
    total = 0
    for i in range(n):
        total += c
        # print(i)
    return total


def recursive_solution(c, n):
    """n x c =
    = (n - 1) x c + c
    = ((n - 2) x c + c) + c
    = ...
    :param c:
    :param n:
    :return:
    """
    # print(n)
    if n == 1:
        return c
    else:
        return recursive_solution(c, n-1) + c


def tail_recursive_solution(c, n, r=0):
    # print(n, r)
    if n == 1:
        return c + r
    else:
        return tail_recursive_solution(c, n-1, c+r)


def good_solution(c, n):
    """
    :param c:
    :param n:
    :return:
    """
    return c * n


def evaluate_time(sol, title):
    c = 1
    n = 500

    print(title)
    time_start = time.time()
    r = sol(c, n)
    time_end = time.time()
    print('result: {}'.format(r))
    print('execution time: {}\n'.format(time_end - time_start))


if __name__ == '__main__':
    evaluate_time(good_solution, 'Good')
    evaluate_time(loop_solution, 'Loop')
    evaluate_time(recursive_solution, 'Recursive')
    evaluate_time(tail_recursive_solution, 'Tail Recursive')
