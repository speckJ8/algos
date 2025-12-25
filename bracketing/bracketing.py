import random

type Bracket = (float, float, float)

def find_bracket(f: callable[[float], float], step: float=1e-2) -> Bracket:
    """
    Find a bracket for a unimodal function f (i.e. f has a single minimum)
    Returns a tuple (a, b, c), where a<b<c and f(a)>f(b) and f(c)>f(b)
    """
    a = random.uniform(-1000, 1000)
    b = a + step
    fa = f(a)
    fb = f(b)

    if fa == fb:
        return (a, (a+b)/2, b)
    elif fa < fb:
        t, ft = b, fb
        b, fb = a, fa
        a, fa = t, ft
        step = -step
    
    iter_count = 0
    while True:
        iter_count += 1
        c = b + step
        fc = f(c)
        if fc > fb:
            if c > b:
                return (a, b, c)
            else:
                return (c, b, a)
        if fc == fb:
            if c > b:
                return (b, (b+c)/2, c)
            else:
                return (c, (b+c)/2, b)
        a, fa = b, fb
        b, fb = c, fc


def quadratic_fit_search(f: callable[[float], float], bracket: Bracket=None, iterations=100) -> Bracket:
    """
    Find a bracket for a unimodal function by successively fitting a quadratic curve to potential brackets
    and improving the bracket interval size.
    """
    if bracket is None:
        bracket = find_bracket(f)
    
    for i in range(0, iterations):
        (a, b, c) = bracket
        fa, fb, fc = f(a), f(b), f(c)
        # minimum of the quadratic function fitting (a, f(a)), (b, f(b)) and (c, f(c))
        m = ((0.5*(fa*(b**2 - c**2) + fb*(c**2 - a**2) + fc*(a**2 - b**2)))/ \
                (fa*(b - c) + fb*(c - a) + fc*(a - b))) + 0.0
        fm = f(m)
        if fm > fb:
            if m > b:
                bracket = (m , b, c)
            if m < b:
                bracket = (a, b, m)
        elif fm < fb:
            if m > b:
                bracket = (b, m, c)
            if m < b:
                bracket = (a, m, b)
        else:
            # fm == fb must be the minimum of f
            return (a, b, c)
    
    return bracket
