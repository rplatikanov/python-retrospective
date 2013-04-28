from collections import deque


def groupby(func, seq):
    keys = {func(element) for element in seq}
    return {key: [element
                  for element in seq
                  if func(element) == key]
            for key in keys}


def iterate(func):
    def compose(func1, func2):
        return lambda arg: func1(func2(arg))

    composed = lambda x: x
    while True:
        yield composed
        composed = compose(composed, func)


def zip_with(func, *iterables):
    return map(lambda zipped: func(*zipped), zip(*iterables))


class CachedFunc:
    def __init__(self, func, cache_size):
        self.func = func
        self.cache_size = cache_size
        self.queue = deque()
        self.cache = dict()

    def __call__(self, *args):
        arg_key = tuple(args)
        if arg_key in self.cache:
            return self.cache[arg_key]

        if len(self.queue) == self.cache_size:
            key = self.queue.pop()
            del self.cache[key]

        result = self.func(*args)
        self.cache[arg_key] = result
        self.queue.appendleft(arg_key)
        return result


def cache(func, cache_size):
    if cache_size <= 0:
        return func
    return CachedFunc(func, cache_size)
