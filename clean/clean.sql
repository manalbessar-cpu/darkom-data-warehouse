
drop schema if exists clean;
CREATE SCHEMA IF NOT EXISTS clean;

CREATE TABLE clean.clean_annonces (
    annonce_id TEXT,
    date_publication TEXT,
    titre TEXT,
    ville TEXT,
    quartier TEXT,
    type_bien TEXT,
    transaction TEXT,
    prix TEXT,
    surface TEXT,
    nb_chambres TEXT,
    nb_salles_bain TEXT,
    etage TEXT,
    annee_construction TEXT,
    prix_m2 TEXT,
    age_bien_immobilier TEXT,
    prix_categorie TEXT,
    categorie_surface TEXT,
    annee TEXT,
    mois TEXT,
    trimestre TEXT
);