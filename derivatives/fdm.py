import random

def finite_diff_derivative_forward(f: callable[[float], float], delta: float=1e-9) -> callable[[float], float]:
    return lambda x: (f(x + delta) - f(x))/delta

def finite_diff_derivative_central(f: callable[[float], float], delta: float=1e-9) -> callable[[float], float]:
    return lambda x: (f(x + delta/2) - f(x - delta/2))/delta

def eval_fdm(f: callable[[float], float], f_: callable[[float], float], delta: float=1e-9):
    avg_forward_err = 0
    avg_central_err = 0
    f_f = finite_diff_derivative_forward(f)
    f_c = finite_diff_derivative_central(f)
    for i in range(1, 1001):
        x = random.uniform(-1000, 1000)
        forward_error = abs((f_f(x) - f_(x))/f_(x))
        central_error = abs((f_c(x) - f_(x))/f_(x))
        avg_forward_err = ((i-1)/i)*avg_forward_err + forward_error/i
        avg_central_err = ((i-1)/i)*avg_central_err + central_error/i
    return (avg_forward_err, avg_central_err)