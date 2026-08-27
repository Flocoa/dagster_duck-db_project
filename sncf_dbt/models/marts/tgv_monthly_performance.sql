with intermediate as (

    select * from {{ ref('int_tgv_monthly') }}

),

aggregated as (

    select
        journey_month,
        train_service,
        departure_station,
        arrival_station,

        -- Volume total de trains
        scheduled_trains_count,
        canceled_trains_count,
        delayed_arrivals_count,

        -- Taux calculés
        round((canceled_trains_count::double / nullif(scheduled_trains_count, 0)) * 100, 2) as cancellation_rate_pct,
        round((delayed_arrivals_count::double / nullif(scheduled_trains_count, 0)) * 100, 2) as delay_rate_pct,

        -- Retard moyen global à l'arrivée
        avg_delay_arrivals_minutes,

        -- Principales causes de retard
        pct_cause_external,
        pct_cause_infrastructure,
        pct_cause_traffic_management,
        pct_cause_rolling_stock,
        pct_cause_station_management,
        pct_cause_passenger_care

    from intermediate

)

select * from aggregated
