# 🏠 Darkom Data Warehouse & BI

Projet de conception d’un pipeline de données end-to-end pour l’analyse du marché immobilier marocain à partir des données de Darkom.ma.

---

# 📌 Objectif du Projet

Construire une architecture complète de traitement de données :

CSV → Staging → Clean → Data Warehouse → Power BI

Le projet permet de :

- Importer des données immobilières
- Nettoyer et transformer les données
- Construire un Data Warehouse
- Créer des dashboards interactifs avec Power BI
- Produire des KPIs décisionnels

---

# 🛠️ Technologies Utilisées

- Python
- PostgreSQL
- Pandas
- SQLAlchemy
- Power BI
- DAX
- Power Query

---

# 📂 Structure du Projet

```bash
DARKOM-DATA-WAREHOUSE/
│
├── data/
│   └── darkom-annonces.csv
│
├── staging/
│   ├── staging.sql
│   └── load_raw.py
│
├── clean/
│   ├── clean.sql
│   ├── clean_raw.py
│   └── clean.ipynb
│
├── warehouse/
│   ├── warehouse.sql
│   └── load_warehouse.py
│
├── .env
├── .gitignore
├── requirements.txt
├── clean.csv
└── README.md