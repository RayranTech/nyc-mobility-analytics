select
    cast(tpep_pickup_datetime as date) as trip_date,

    count(*) as total_trips,

    sum(
        case
            when amount_quality = 'valid'
            then total_amount
            else 0
        end
    ) as valid_revenue,

    avg(trip_distance) as avg_trip_distance,

    avg(trip_duration_minutes) as avg_trip_duration

from {{ ref('mart_yellow_trips') }}

where tpep_pickup_datetime >= '2024-01-01'
  and tpep_pickup_datetime < '2024-02-01'

group by 1

order by 1