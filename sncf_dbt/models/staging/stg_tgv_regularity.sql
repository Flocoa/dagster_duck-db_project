with source as (

    select * from {{ source('raw_sncf', 'raw_tgv_regularity') }}

),

renamed_and_casted as (

    select
        -- Identifiants & Temporalité
        cast(date as varchar) as journey_month,
        cast(service as varchar) as train_service,
        cast(gare_depart as varchar) as departure_station,
        cast(gare_arrivee as varchar) as arrival_station,

        -- Métriques de trajet
        cast(duree_moyenne as bigint) as avg_journey_duration_minutes,
        cast(nb_train_prevu as bigint) as scheduled_trains_count,
        cast(nb_annulation as bigint) as canceled_trains_count,
        cast(commentaire_annulation as integer) as cancellation_comments,

        -- Départs
        cast(nb_train_depart_retard as bigint) as delayed_departures_count,
        cast(retard_moyen_depart as double) as avg_delay_departures_minutes,
        cast(retard_moyen_tous_trains_depart as double) as avg_delay_all_departures_minutes,
        cast(commentaire_retards_depart as integer) as departure_delay_comments,

        -- Arrivées
        cast(nb_train_retard_arrivee as bigint) as delayed_arrivals_count,
        cast(retard_moyen_arrivee as double) as avg_delay_arrivals_minutes,
        cast(retard_moyen_tous_trains_arrivee as double) as avg_delay_all_arrivals_minutes,
        cast(commentaires_retard_arrivee as varchar) as arrival_delay_comments,

        -- Tranches de retard
        cast(nb_train_retard_sup_15 as bigint) as trains_delayed_over_15m_count,
        cast(retard_moyen_trains_retard_sup15 as double) as avg_delay_trains_over_15m_minutes,
        cast(nb_train_retard_sup_30 as bigint) as trains_delayed_over_30m_count,
        cast(nb_train_retard_sup_60 as bigint) as trains_delayed_over_60m_count,

        -- Causes de retard (pourcentages)
        cast(prct_cause_externe as double) as pct_cause_external,
        cast(prct_cause_infra as double) as pct_cause_infrastructure,
        cast(prct_cause_gestion_trafic as double) as pct_cause_traffic_management,
        cast(prct_cause_materiel_roulant as double) as pct_cause_rolling_stock,
        cast(prct_cause_gestion_gare as double) as pct_cause_station_management,
        cast(prct_cause_prise_en_charge_voyageurs as double) as pct_cause_passenger_care

    from source

)

select * from renamed_and_casted
