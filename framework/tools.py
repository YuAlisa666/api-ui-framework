# framework/tools.py
import time, functools

def retry(times=3, wait=0.2):
    def deco(func):                       # 第 1 层：接住 @retry(...) 的参数
        @functools.wraps(func)            # 保留原函数名字，pytest 才认得
        def wrapper(*args, **kwargs):     # 第 2 层：真正干活
            for i in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except AssertionError as e:
                    if i == times:
                        raise             # 达到重试上限仍失败，原样抛出异常
                    print(f"[重试] 第 {i} 次失败，{wait}s 后再试")
                    time.sleep(wait)
        return wrapper
    return deco

class timer:
    def __init__(self, name):
        self.name = name
    def __enter__(self):                  # 进 with 时
        self.start = time.perf_counter()
        return self
    def __exit__(self, a, b, c):          # 出 with 时（内部抛出异常也会执行）
        print(f"[耗时] {self.name}: {time.perf_counter() - self.start:.3f}s")
        return False                      # False = 异常照常抛，不隐式吞没异常