"""This module group all the expressions used by benchmark.

Each item of `expr` has a name and a function. Each function receive
a parameter, one with a table or dataframe object.
"""

expr_list = [
    (
        'trip_count_cab_type',
        lambda t: t[t.cab_type, t.count()].group_by(t.cab_type),
    ),
    (
        'trip_passenger_total_amount_mean',
        lambda t: t[
            t.passenger_count, t.total_amount.mean().name('total_amount_mean')
        ].group_by(t.passenger_count),
    ),
    (
        'trip_group_by_passenger_count_and_pickup_year',
        lambda t: t[
            t.passenger_count,
            t.pickup_datetime.year().name('pickup_year'),
            t.count().name('pickup_year_count'),
        ].group_by([t.passenger_count, t.pickup_year]),
    ),
    (
        'trip_grouped_by_passenger_count_and_pickup_year_and_distance',
        lambda t: t[
            t.passenger_count,
            t.pickup_datetime.year().name('pickup_year'),
            t.trip_distance.cast(int).name('distance'),
            t.count().name('the_count'),
        ]
        .group_by([t.passenger_count, t.pickup_year, t.distance])
        .order_by([t.pickup_year, t.the_count], asc=False),
    ),
]
