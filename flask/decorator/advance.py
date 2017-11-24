# 高级用法

import time
import functools


def decorator_with_params():
    def log_cost_time(prefix=">>"):
        def inner_dec(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                begin = time.time()
                try:
                    return f(*args, **kwargs)
                finally:
                    print("{} func {} cost {}".format(prefix, f.__name__, time.time() - begin))
            return wrapped
        return inner_dec

    @log_cost_time("==>")
    def test(a, *, b):
        time.sleep(0.1)
        return a + b

    print(test(1, b=3))

    # 等价表示法
    def test2(a, *, b):
        time.sleep(0.1)
        return a + b

    decorator_f = log_cost_time("==>")
    test2 = decorator_f(test2)
    print(test2(2, b=2))


if __name__ == "__main__":
    decorator_with_params()
