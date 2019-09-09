import json
import os
from time import time


def cached(f):
    cache = {}

    def f_cached(*args, **kwargs):
        k = str(args) + str(kwargs)
        if k in cache:
            return cache[k]
        cache[k] = f(*args, **kwargs)
        return cache[k]

    return f_cached


def timeit(f, *args, verbose: bool = False, **kwargs):
    t = time()
    f(*args)
    time_diff = time() - t

    if verbose:
        k = kwargs["id"] or f.__name__
        print({k: time_diff})

    return time_diff


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


def param(*args, group='default', id=None):
    return {'args': args, 'group': group, 'id': id}


def benchmark(arg_names, params, log_path='/tmp/log_benchmark.json', repeat=1):
    def _run_f(f):
        for param in params:
            ts = 0
            for _ in range(repeat):
                ts += timeit(f, *param["args"], id=param["id"])
            register_log(
                log_path, {param['group']: {param['id']: ts / repeat}}
            )
        return

    return _run_f
