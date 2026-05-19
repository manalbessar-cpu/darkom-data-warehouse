
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
# =========================
# CONFIGURATION
# =========================
DB_USER=os.getenv("POSTGRES_USER")
DB_PASSWORD=os.getenv("POSTGRES_PASSWORD")
DB_HOST=os.getenv("POSTGRES_HOST")
DB_PORT=os.getenv("POSTGRES_PORT")
DB_NAME=os.getenv("POSTGRES_DB")

engine = create_engine(

   f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

query="select * from clean.clean_annonces;"
df = pd.read_sql(query,engine)


with engine.begin() as conn:
    conn.execute(text("DROP SCHEMA IF EXISTS warehouse CASCADE"))
    conn.execute(text("create schema warehouse"))



print("Warehouse schema created")

# =========================
# LOAD DIMENSIONS
# =========================

# DIM VILLE
df_ville = df[["ville"]].drop_duplicates().reset_index(drop=True)
df_ville["ville_id"] = df_ville.index.astype(str)

df_ville.to_sql("dim_ville", engine, schema="warehouse", if_exists="append", index=False)

# DIM QUARTIER
df_quartier = df[["quartier", "ville"]].drop_duplicates().reset_index(drop=True)
df_quartier["quartier_id"] = df_quartier.index.astype(str)

df_quartier = df_quartier.merge(df_ville, on="ville", how="left")

df_quartier.to_sql("dim_quartier", engine, schema="warehouse", if_exists="append", index=False)

# DIM TYPE BIEN
df_type = df[["type_bien","categorie_surface"]].drop_duplicates().reset_index(drop=True)
df_type["type_bien_id"] = df_type.index.astype(str)


df_type.to_sql("dim_type_bien", engine, schema="warehouse", if_exists="append", index=False)

# DIM TRANSACTION
df_trans = df[["transaction"]].drop_duplicates().reset_index(drop=True)
df_trans["transaction_id"] = df_trans.index.astype(str)

df_trans.to_sql("dim_transaction", engine, schema="warehouse", if_exists="append", index=False)

# DIM PRIX CATEGORIE
df_prix = df[["prix_categorie"]].drop_duplicates().reset_index(drop=True)
df_prix["categorie_prix_id"] = df_prix.index.astype(str)

df_prix.to_sql("dim_categorie_prix", engine, schema="warehouse", if_exists="append", index=False)

# DIM TEMPS
df_time = df[["date_publication", "anne", "mois", "Trimestre"]].drop_duplicates().reset_index(drop=True)
df_time["date_publication_id"] = df_time.index.astype(str)

df_time.to_sql("dim_temps", engine, schema="warehouse", if_exists="append", index=False)

# =========================
# FACT TABLE
# =========================

df_fact = df.copy()

# join IDs
df_fact = df_fact.merge(df_ville, on="ville", how="left")
df_fact = df_fact.merge(df_quartier[["quartier", "quartier_id"]], on="quartier", how="left")
df_fact = df_fact.merge(df_type[["type_bien", "type_bien_id"]], on="type_bien", how="left")
df_fact = df_fact.merge(df_trans[["transaction", "transaction_id"]], on="transaction", how="left")
df_fact = df_fact.merge(df_prix[["prix_categorie", "categorie_prix_id"]], on="prix_categorie", how="left")
df_fact = df_fact.merge(df_time[["date_publication", "date_publication_id"]], on="date_publication", how="left")

df_fact = df_fact.rename(
    columns={"Âge_bien_immobilier": "age_bien_immobilier"}
)
df_fact = df_fact[[
    "annonce_id",
    "date_publication_id",
    "ville_id",
    "quartier_id",
    "type_bien_id",
    "transaction_id",
    "categorie_prix_id",
    "prix",
    "surface",
    "nb_chambres",
    "nb_salles_bain",
    "etage",
    "prix_m2",
    "age_bien_immobilier"
]]

df_fact.to_sql("fact_annonces", engine, schema="warehouse", if_exists="append", index=False)

print("ETL Warehouse terminé avec succès")