# SNCF TGV Performance & Regularity Pipeline

Projet d'ingénierie de données (*Modern Data Stack*) permettant d'ingérer, de transformer et d'orchestrer les données mensuelles de régularité et de retard des TGV de la SNCF.

---

## Architecture du Projet

Le pipeline suit l'architecture moderne **ELT (Extract, Load, Transform)** :

[ API SNCF ] ──(Python / Pandas)──> [ DuckDB (raw) ] ──(dbt)──> [ Staging ➔ Intermediate ➔ Marts ]

[ Orchestration Dagster ]

1. **Ingestion (Extract & Load)** : Récupération des données brutes depuis l'API Open Data SNCF via Python (`requests` / `pandas`) et stockage dans une base **DuckDB** (`raw.raw_tgv_regularity`).

2. **Transformation (dbt)** :
   * **Staging** (`stg_tgv_regularity`) : Nettoyage, renommage explicite et typage fort des 26 colonnes.
   * **Intermediate** (`int_tgv_regularity_indexed`) : Création d'une clé primaire unique (*surrogate key*) combinant la date et l'axe de trajet.
   * **Marts** (`fct_tgv_monthly_performance`) : Modèle analytique prêt pour le reporting (calcul automatique des taux d'annulation, de retard et répartition des causes).

3. **Orchestration & Lineage (Dagster)** : Orchestration globale, gestion des dépendances entre assets Python et modèles dbt, et planification mensuelle automatique.

---

## Stack technique

* **Base de données OLAP** : [DuckDB](https://duckdb.org/)
* **Transformations & Data Quality** : [dbt-core](https://www.getdbt.com/) / `dbt-duckdb`
* **Orchestration & Data Lineage** : [Dagster](https://dagster.io/) / `dagster-dbt`
* **Langage & Scripting** : Python 3.12 (Pandas, Requests)

---

## Structure du Répertoire

```text
projet_duck-db_dagster_dbt/
├── sncf_dagster/           # Code d'orchestration Dagster
│   ├── assets.py           # Définition de l'asset d'ingestion & assets dbt
│   └── __init__.py         # Définitions globales, Jobs & Schedules
├── sncf_dbt/               # Projet de transformations dbt
│   ├── models/
│   │   ├── staging/        # Modèles de staging & schema.yml (tests)
│   │   ├── intermediate/   # Modèles intermédiaires (surrogate keys)
│   │   └── marts/          # Tables de faits / Datamarts analytiques
│   ├── dbt_project.yml
│   └── profiles.yml        # Configuration de connexion DuckDB
├── sncf_data.duckdb        # Base de données DuckDB locale (non versionnée)
├── pyproject.toml
└── README.md
```
---
