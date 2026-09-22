select
    "VendorID" as vendor_id,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    "RatecodeID" as ratecode_id,
    store_and_fwd_flag,
    "PULocationID" as pu_location_id,
    "DOLocationID" as do_location_id,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    "Airport_fee" as airport_fee

from {{ source('raw', 'yellow_trips') }}

where tpep_dropoff_datetime > tpep_pickup_datetime