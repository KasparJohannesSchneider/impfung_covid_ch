__all__ = ['sum_1_n', 'ltm', 'is_triangular']

import math
import scipy.special


def sum_1_n(n: int) -> int:
    """Calculates the sum from 1 to n.

    see https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF

    :rtype: int
    :param n: the integer to sum up to
    :return: sum from 1 to n
    """
    assert n >= 0, 'n must not be negative!'
    return int(n * (n + 1) / 2)


def ltm(n: int) -> int:
    """Returns the next lower triangular number to n or n if n is triangular.

    :param n: the number to get the next lower triangular number too
    :return: n if triangular else the next lower triangular number
    :rtype: int
    """
    assert n > 0, 'n must be greater than zero!'
    n += 1
    x1 = math.ceil((math.sqrt(8 * n + 1) - 1) /
                   2)
    return int(scipy.special.binom(x1, 2))


def is_triangular(n: int) -> bool:
    """Checks if a positive integer is triangular.

    :param n: the number to check
    :return: True if n is triangular else False
    :rtype: bool
    """
    if n <= 0:
        return False
    return n == ltm(n)
