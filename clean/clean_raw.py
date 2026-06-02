import pandas as pd
from sqlalchemy import create_engine,text
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




cat_cols = ["quartier", "type_bien", "transaction"]

colors = ["#5EC10D", "#7A9909", "#0DC17C"]

plt.figure(figsize=(18,5))

for i, col in enumerate(cat_cols):
    plt.subplot(1, 3, i+1)

    sns.countplot(
        data=df,
        x=col,
        color=colors[i],
        order=df[col].value_counts().index
    )

    plt.title(f"Distribution de {col}")
    plt.xticks(rotation=45)

plt.tight_layout()
plt.show()



# Colonnes catégorielles
cat_cols = ["quartier", "type_bien", "transaction"]

# Remplissage des valeurs manquantes par mode selon ville
for col in cat_cols:
    df[col] = df[col].fillna(
        df.groupby("ville")[col]
          .transform(lambda x: x.mode()[0] if not x.mode().empty else "Inconnu")
    )

# Vérification finale
print(df[cat_cols].isnull().sum())









cols = ["prix", "surface", "nb_chambres"]

for col in cols:
    plt.figure(figsize=(6,3))
    sns.histplot(df[col], kde=True , color= "#EF476F")
    plt.title(col)
    plt.show()

    cols = ["prix", "surface", "nb_chambres"]

def remove_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    return df[(df[col] >= lower) & (df[col] <= upper)]


for col in cols:
    df = remove_outliers_iqr(df, col)

print(df.shape)

df = df.reset_index(drop=True)

cols = ["prix", "surface", "nb_chambres"]

for col in cols:
    plt.figure(figsize=(6,3))
    sns.histplot(df[col], kde=True , color= "#EF476F")
    plt.title(col)
    plt.show()

    cols = ["prix", "surface", "nb_chambres"]

df["ville"] = df["ville"].str.lower().str.strip().replace("casa","casablanca")
df["quartier"] = df["quartier"].str.lower().str.strip()
df["type_bien"] = df["type_bien"].str.lower().str.strip()
df["transaction"] = df["transaction"].str.lower().str.strip()

df["date_publication"] = pd.to_datetime(
    df["date_publication"],
    errors="coerce"
)

numeric_cols = [
    "prix",
    "surface",
    "nb_chambres",
    "nb_salles_bain",
    "etage",
    "annee_construction"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
max_prix = df["prix"].max()
min_prix = df["prix"].min()
print(max_prix)
print(min_prix)


##Feature Engineering

df["prix_m2"]=df["prix"]/df["surface"]
df["prix_m2"]=df["prix_m2"].astype(int)

df["Âge_bien_immobilier"]= 2026 - df["annee_construction"]




df["prix_categorie"] = pd.qcut(
    df["prix"],
    q=4,
    labels=["Economique", "Moyen", "Haut standing", "Luxe"]
)



def Catégories_de_surface (surface) : 
   if surface  < 80 :
        return "petit"
   
   elif 80< surface < 150 :
         return "moyen"
   
   else :
       return "grand"


df["categorie_surface"]=df["surface"].apply(Catégories_de_surface)

df["date_publication"] = pd.to_datetime(df["date_publication"])
df ["anne"]=df["date_publication"].dt.year
df["mois"]=df["date_publication"].dt.month
df["Trimestre"]=df["date_publication"].dt.quarter




print(df.head())
df.to_csv("clean.csv",index=False)

with engine.begin() as conn:
    with open(r"C:\Users\manal\OneDrive\Desktop\Darkom Data Warehouse & BI Dashboard\clean\clean.sql", "r", encoding="utf-8") as file:
        sql_script = file.read()

    try:
        conn.execute(text(sql_script))
        print("Schema exécuté avec succès")
    except Exception as e:
        print("Schema déjà existant ou erreur :", e)


df.to_sql(
    "clean_annonces" ,
    engine,
    schema= "clean",
    if_exists="replace",
    index=False
)

print("Chargement terminé.")
