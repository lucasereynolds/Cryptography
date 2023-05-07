# Implementation of Shank's Algorithm
from math import ceil, sqrt


class Found(Exception): pass


def shanks(n: int, a: int, b: int) -> int:
    print("start")
    m = ceil(sqrt(n))

    # Create list l1 and sort on value of second element in tuple
    l1 = [(i, pow(a, i*m, n)) for i in range(1, m)]
    l1.sort(key=lambda x: x[1])

    # Create list l2 and sort on value of second element in tuple
    l2 = [(i, (b*pow(a, -i, n)) % n) for i in range(1, m)]
    l2.sort(key=lambda x: x[1])

    # Find pair (j,y) in l1 and (i,y) in l2
    try:
        for (j, val1) in l1:
            for (i, val2) in l2:
                if val1 == val2:
                    raise Found
    except Found:
        dlog = (m*j + i) % n
        print(str(b) + " = " + str(a) + "^" + str(dlog) + " (mod " + str(n) + ")")
        return dlog

    return 0


if __name__ == "__main__":
    # Compute the discrete logarithm of 525 to base 3 modulo 809
    res = shanks(809, 3, 525)

