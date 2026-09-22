select
    *,
    
    extract(
        epoch from (tpep_dropoff_datetime - tpep_pickup_datetime)
    ) / 60.0 as trip_duration_minutes,

    trip_distance * 60.0 /
        (
            extract(
                epoch from (tpep_dropoff_datetime - tpep_pickup_datetime)
            ) / 60.0
        ) as average_speed_mph,

    case
        when trip_distance > 100 then 'suspicious'
        else 'valid'
    end as distance_quality

from {{ ref('stg_yellow_trips') }}