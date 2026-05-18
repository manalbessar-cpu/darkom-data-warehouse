import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

engine = create_engine(

   f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
query = "SELECT * FROM  staging.stg_annonces;"
df = pd.read_sql(query, engine)

print(df.head())




df = df.drop_duplicates(subset=["annonce_id"])

df.isnull().sum()
df = df.dropna(subset=["date_publication"])





num_cols = ["nb_salles_bain", "annee_construction", "nb_chambres", "etage"]

colors = ["#5EC10D", "#7A9909", "#0DC17C", "#384B04"]

plt.figure(figsize=(12,8))

for i, col in enumerate(num_cols):
    plt.subplot(2, 2, i+1)
    sns.histplot(df[col], bins=30, kde=True, color=colors[i])
    plt.title(f"Distribution de {col}")

plt.tight_layout()
plt.show()
df["nb_chambres"] = df["nb_chambres"].fillna(df["nb_chambres"].median())
df["nb_salles_bain"] = df["nb_salles_bain"].fillna(df["nb_salles_bain"].median())
df["annee_construction"] = df ["annee_construction"].fillna(df["annee_construction"].median())
df["etage"] = df["etage"].fillna(df["etage"].median())