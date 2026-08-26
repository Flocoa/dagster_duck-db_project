#Import des libraries nécessaires

import os
import duckdb
import requests
from dagster import asset

# API SNCF pour récupérer les données de régularité TGV
SNCF_API_URL = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/regularite-mensuelle-tgv-aqst/exports/json"

@asset
def raw_sncf_tgv_data():
    """téléchargement des données brutes de régularité TGV depuis l'API SNCF et stockage dans DuckDB"""

    # Call API
    response = requests.get(SNCF_API_URL)
    response.raise_for_status() # bloque directement l'exécution si la requête échoue (erreur 4xx ou 5xx)
    data = response.json()

    # Connexion à DuckDB
    db_path = "sncf_data.duckdb"
    conn = duckdb.connect(db_path)

    # Ingestion dans la table raw_tgv_regularity sur duckdb
    import pandas as pd
    df = pd.DataFrame(data)

    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    conn.execute("CREATE OR REPLACE TABLE raw.raw_tgv_regularity AS SELECT * FROM df;")

    row_count = conn.execute("SELECT COUNT(*) FROM raw.raw_tgv_regularity").fetchone()[0] # va chercher le nombre de lignes insérées dans la table raw.raw_tgv_regularity
    conn.close() #ferme duckdb

    print(f"{row_count} lignes insérées dans raw.raw_tgv_regularity")
