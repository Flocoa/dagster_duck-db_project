from dagster import Definitions, load_assets_from_modules
from sncf_dagster import assets  # <--- Remplacer 'from . import assets' par ceci

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
)
