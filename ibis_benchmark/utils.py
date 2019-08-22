from time import time


def timeit(f, *args, **kwargs):
    k = kwargs["id"] or f.__name__

    t = time()
    f(*args)
    result = {k: time() - t}
    print(result)


def benchmark(arg_names, params):
    def _run_f(f):
        for param in params:
            timeit(f, *param["args"], id=param["id"])
        return

    return _run_f


def param(*args, id=None):
    return {"args": args, "id": id}
