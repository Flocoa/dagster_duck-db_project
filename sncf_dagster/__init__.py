from dagster import Definitions, load_assets_from_modules, define_asset_job, ScheduleDefinition
from dagster_dbt import DbtCliResource
from sncf_dagster import assets
from sncf_dagster.assets import dbt_project

# Chargement de tous les assets
all_assets = load_assets_from_modules([assets])

# Job exécutant l'intégralité du pipeline (Ingestion + dbt)
full_pipeline_job = define_asset_job(
    name="full_sncf_pipeline",
    selection="*"
)

# Schedule mensuel (le 1er du mois à 02h00)
monthly_schedule = ScheduleDefinition(
    job=full_pipeline_job,
    cron_schedule="0 2 1 * *",
)

# Déclarations globales Dagster
defs = Definitions(
    assets=all_assets,
    schedules=[monthly_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=dbt_project),
    },
)
