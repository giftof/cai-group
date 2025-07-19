def to_int(s: str) -> int:
    return int(s)


def to_float(s: str) -> float:
    return float(s)


def float_to_int(a: float) -> int:
    try:
        int(a)
    except:
        raise ValueError('overflow?')


def power(n: float, e: int) -> float:
    r = 1
    for _ in range(0, e):
        r *= n
    return r

def foo():
    try:
        a = to_float('999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999')
        b = to_int('10')
        v = power(a, b)
        v2 = float_to_int(v)
    except ValueError as e:
        print(e)
    else:
        print(v2)
    
if __name__ == '__main__':
    foo()