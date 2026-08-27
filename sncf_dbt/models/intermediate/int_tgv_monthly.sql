with staging as (

    select * from {{ ref('stg_tgv_regularity') }}

),

intermediate as (

    SELECT
      CONCAT(journey_month, train_service, departure_station, arrival_station) as unique_key,
      *
    FROM staging )

SELECT
*

FROM intermediate
