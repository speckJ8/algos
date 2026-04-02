import random
import math

def newton(f: callable[[float], float], f_: callable[[float], float], iterations: int=100) -> float:
    """
    Find local min (or max) of a function by using Newton's method.
    f is the target function, and f_ is its first derivative.
    """

    x = random.uniform(-1000, 1000)
    for i in range(0, iterations):
        fx, f_x = f(x), f_(x)
        if math.isclose(f_x, 0.0):
            break
        x = x - fx/f_x
    return x


def newton_min_dampened(f: callable[[float], float], f_: callable[[float], float], iterations: int=100) -> float:
    """
    Find local min of a function by using Newton's method. Modified version to avoid
    overshooting the minimum with large dislocations.
    f is the target function, and f_ is its first derivative.
    """

    x = random.uniform(-1000, 1000)
    d = 1
    for i in range(0, iterations):
        fx, f_x = f(x), f_(x)
        if math.isclose(f_x, 0.0):
            break
        x_next = x - d * (fx/f_x)
        while f(x) < f(x_next):
            fx, f_x = f(x), f_(x)
            if math.isclose(f_x, 0.0):
                break
            d = d/2
            x_next = x - d * (fx/f_x)
        x = x_next
    return x