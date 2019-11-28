import os

conn_info = {
    'cpu_cursor': {
        'host': 'localhost',
        'port': 6274,
        'user': 'admin',
        'password': 'HyperInteractive',
        'database': 'omnisci',
        'ipc': False,
        'gpu_device': None,
    }
}

conn_info['cpu_ipc'] = dict(conn_info['cpu_cursor'])
conn_info['cpu_ipc'].update({'ipc': True})

conn_info['gpu_ipc'] = dict(conn_info['cpu_cursor'])
conn_info['gpu_ipc'].update({'port': 26274, 'ipc': True, 'gpu_device': 1})


# start a new benchmark log
results_path = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ),
    'docs',
    'static',
)
os.makedirs(results_path, exist_ok=True)

log_path = os.path.join(results_path, 'benchmark-nyc-taxi.json')

bechmark_config = {'repeat': 3, 'log_path': log_path}
