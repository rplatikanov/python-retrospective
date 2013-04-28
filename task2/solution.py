from collections import OrderedDict


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


def cache(func, cache_size):
    if cache_size <= 0:
        return func

    cache = OrderedDict()

    def cached(*args):
        arg_key = tuple(args)
        if arg_key in cache:
            return cache[arg_key]

        if len(cache) == cache_size:
            cache.popitem(False)

        result = func(*args)
        cache[arg_key] = result
        return result

    return cached
