import json
import os
from time import time


def cacheit(f):
    cache = {}

    def _cacheit(*args, **kwargs):
        k = str(args) + str(kwargs)
        if k in cache:
            return cache[k]
        cache[k] = f(*args, **kwargs)
        return cache[k]

    return _cacheit


def timeit(f):
    t = time()
    f()
    return time() - t


def register_log(file_path, data={}, new_log=False):
    if os.path.exists(file_path) and not new_log:
        with open(file_path, 'r') as f:
            _data = json.load(f)
    else:
        _data = {}

    with open(file_path, 'w') as f:
        for k, v in data.items():
            if k not in _data:
                _data[k] = {}
            _data[k].update(v)
        json.dump(_data, f, indent=1)


def benchmark(backend, id, log_path='/tmp/log_benchmark.json', repeat=1):
    def benchmark_backend(f):
        ts = 0
        for _ in range(repeat):
            ts += timeit(f)

        t_mean = ts / repeat
        register_log(log_path, {backend: {id: t_mean}})
        return t_mean

    return benchmark_backend
