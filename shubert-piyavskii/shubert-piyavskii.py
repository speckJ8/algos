from dataclasses import dataclass
import math

type Bracket = (float, float, float)

@dataclass
class Solution:
    _index: int
    x: float
    fx: float
    sawtooth_value: float


def shubert_piyavskii(f: callable[[float], float], bracket: Bracket, l: float=10, e: float=1e-3) -> Solution:
    (a, _, b) = bracket
    middle = (a+b)/2
    fa, f_middle, fb = f(a), f(middle), f(b)
    points = [
        (a, fa),
        (middle, f_middle),
        (b, fb),
    ]

    if fa < f_middle and fa < fb:
        best = Solution(0, a, fa, -math.inf)
    elif f_middle < fb:
        best = Solution(1, middle, f_middle, -math.inf)
    else:
        best = Solution(2, b, fb, -math.inf)

    delta = math.inf
    while delta > e:
        print(f"GOOSE: current solution {best}")
        for i in range(0, len(points)-1):
            (left, f_left) = points[i]
            (right, f_right) = points[i+1]
            middle = ((f_left - f_right) + l*(right - left)) / 2*l
            f_middle = f(middle)
            sawtooth_y_middle = f_left - l*(left - middle)
            if f_middle < best.fx:
                best = Solution(i, middle, f_middle, sawtooth_y_middle)
        points.insert(best._index, (best.x, best.fx))
        delta = best.fx - best.sawtooth_value
        print(f"GOOSE: new delta {delta}")
    
    return best