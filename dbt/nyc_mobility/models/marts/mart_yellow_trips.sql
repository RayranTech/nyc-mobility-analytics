select
    {{ dbt_utils.generate_surrogate_key([
        'vendor_id',
        'tpep_pickup_datetime',
        'tpep_dropoff_datetime',
        'pu_location_id',
        'do_location_id',
        'trip_distance',
        'total_amount'
    ]) }} as trip_id,

    vendor_id,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    extract(hour from tpep_pickup_datetime) as pickup_hour,
    passenger_count,
    trip_distance,
    pu_location_id,
    do_location_id,
    payment_type,

    case
        when payment_type = 1 then 'Credit Card'
        when payment_type = 2 then 'Cash'
        when payment_type = 3 then 'No Charge'
        when payment_type = 4 then 'Dispute'
        when payment_type = 5 then 'Unknown'
        when payment_type = 6 then 'Voided Trip'
        else 'Other'
    end as payment_type_name,

    fare_amount,
    tip_amount,
    total_amount,
    trip_duration_minutes,
    average_speed_mph,
    distance_quality,

    case
        when total_amount < 0 then 'suspicious'
        else 'valid'
    end as amount_quality

from {{ ref('int_yellow_trips') }}