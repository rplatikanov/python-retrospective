from collections import deque


def groupby(func, seq):
    keys = {func(i) for i in seq}
    return {k: [x for x in seq if func(x) == k] for k in keys}


def compose(func1, func2):
    return lambda *args, **kwargs: func1(func2(*args, **kwargs))


def iterate(func):
    f = lambda x: x
    yield f
    while True:
        f = compose(f, func)
        yield f


def zip_with(func, *iterables):
    if len(iterables) == 0:
        return
    iterators = [iter(i) for i in iterables]
    while True:
        params = [next(it) for it in iterators]
        if len(params) != len(iterables):
            break
        else:
            yield func(*params)


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
