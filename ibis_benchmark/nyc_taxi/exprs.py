"""This module group all the expressions used by benchmark.

Each item of `expr` has a name and a function. Each function receive
a parameter, one with a table or dataframe object.
"""

expr_list = [
    (
        'trip_count_cab_type',
        lambda t: t.group_by('passenger_count').aggregate(
            t.total_amount.mean().name('_mean')
        ),
    ),
    (
        'trip_passenger_total_amount_mean',
        lambda t: t[
            [
                t.passenger_count,
                t.pickup_datetime.year().name('pickup_year'),
                t.total_amount,
            ]
        ]
        .group_by(['passenger_count', 'pickup_year'])
        .aggregate(t.total_amount.mean().name('_mean')),
    ),
    (
        'trip_group_by_passenger_count_and_pickup_year',
        lambda t: t[
            [
                t.passenger_count,
                t.pickup_datetime.year().name('pickup_year'),
                t.total_amount,
            ]
        ]
        .group_by(['passenger_count', 'pickup_year'])
        .aggregate(t.total_amount.mean().name('_mean')),
    ),
    (
        'trip_grouped_by_passenger_count_and_pickup_year_and_distance',
        lambda t: t[
            [
                t.passenger_count,
                t.pickup_datetime.year().name('pickup_year'),
                t.trip_distance.cast('int32').name('distance'),
            ]
        ]
        .group_by(['passenger_count', 'pickup_year', 'distance'])
        .aggregate([t.count().name('_count')])
        .sort_by(['pickup_year', ('_count', False)]),
    ),
]
