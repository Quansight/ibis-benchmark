import os

expr_list = [
    (
        'trip_count_cab_type',
        lambda t, is_pandas: t[t.cab_type, t.count()].group_by(t.cab_type),
    ),
    (
        'trip_passenger_total_amount_mean',
        lambda t, is_pandas: t[
            t.passenger_count, t.total_amount.mean().name('total_amount_mean')
        ].group_by(t.passenger_count),
    ),
    (
        'trip_group_by_passenger_count_and_pickup_year',
        lambda t, is_pandas: t[
            t.passenger_count,
            t.pickup_datetime.year().name('pickup_year'),
            t.count().name('pickup_year_count'),
        ].group_by([t.passenger_count, t.pickup_year]),
    ),
    (
        'trip_grouped_by_passenger_count_and_pickup_year_and_distance',
        lambda t, is_pandas: t[
            t.passenger_count,
            t.pickup_datetime.year().name('pickup_year'),
            t.trip_distance.cast(int).name('distance'),
            t.count().name('the_count'),
        ]
        .group_by([t.passenger_count, t.pickup_year, t.distance])
        .order_by([t.pickup_year, t.the_count], asc=False),
    ),
]


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
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'docs',
    'static',
)
os.makedirs(results_path, exist_ok=True)

log_path = os.path.join(results_path, 'benchmark-nyc-taxi.json')

bechmark_config = {'repeat': 3, 'log_path': log_path}
