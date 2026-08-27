from pathlib import Path
import duckdb
import pandas as pd
import requests

from dagster import asset, AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = str(PROJECT_ROOT / "sncf_data.duckdb")
DBT_PROJECT_DIR = PROJECT_ROOT / "sncf_dbt"

# Initialisation simple (profiles.yml est maintenant présent dans DBT_PROJECT_DIR)
dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    packaged_project_dir=DBT_PROJECT_DIR,
)
dbt_project.prepare_if_dev()

# --- ASSET INGESTION ---
SNCF_API_URL = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/regularite-mensuelle-tgv-aqst/exports/json"

@asset
def raw_tgv_regularity():
    """Télécharge les données brutes SNCF et les stocke dans DuckDB."""
    response = requests.get(SNCF_API_URL)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data)

    conn = duckdb.connect(DB_PATH)
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    conn.execute("CREATE OR REPLACE TABLE raw.raw_tgv_regularity AS SELECT * FROM df;")
    conn.close()

# --- ASSETS DBT ---
@dbt_assets(manifest=dbt_project.manifest_path)
def sncf_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
