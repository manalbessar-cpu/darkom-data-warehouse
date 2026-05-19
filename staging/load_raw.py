# staging_load_raw.py

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
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

CSV_PATH = "data/darkom-annonces-6a0a532a16460470060059 - Copie.csv"

TABLE_NAME = "stg_annonces"
SCHEMA_NAME = "staging"

# =========================
# CONNEXION POSTGRESQL
# =========================

engine = create_engine(

   f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# =========================
# LECTURE CSV
# =========================

print("Lecture du fichier CSV...")

df = pd.read_csv(CSV_PATH)

print(f"{len(df)} lignes trouvées.")

# =========================
# CHARGEMENT STAGING
# =========================
from sqlalchemy import text



with engine.begin() as conn:
    with open(r"C:\Users\manal\OneDrive\Desktop\Darkom Data Warehouse & BI Dashboard\staging\staging.sql", "r", encoding="utf-8") as file:
        sql_script = file.read()

    try:
        conn.execute(text(sql_script))
        print("Schema exécuté avec succès")
    except Exception as e:
        print("Schema déjà existant ou erreur :", e)

print("Chargement vers PostgreSQL...")

df.to_sql(
    TABLE_NAME ,
    engine,
    schema=SCHEMA_NAME,
    if_exists="replace",
    index=False
)

print("Chargement terminé.")

# =========================
# LOG SIMPLE
# =========================

log_data = pd.DataFrame({
    "date_chargement": [datetime.now()],
    "nombre_lignes": [len(df)],
    "statut": ["SUCCESS"]
})

log_data.to_sql(
    "logs_chargement",
    engine,
    schema=SCHEMA_NAME,
    if_exists="append",
    index=False
)

print("Log enregistré.")

# =========================
# VERIFICATION
# =========================

query = f"""
SELECT COUNT(*) AS total_lignes
FROM {SCHEMA_NAME}.{TABLE_NAME}
"""

result = pd.read_sql(query, engine)

print(result)

print("STAGING LOAD COMPLETED.")