create schema if not exists warehouse;
create table if not exists warehouse.dim_temps(
    date_publication_id varchar(15) primary key,
    date_publication date,
    annee int,
    mois int,
    trimestre int,
    semaine int
);

create table if not exists warehouse.dim_type_bien(
    type_bien_id varchar(15) primary key,
    type_bien varchar(40),
    categorie varchar(100)
);

create table if not exists warehouse.dim_categorie_prix(
    categorie_prix_id varchar(15) primary key,
    categorie_prix varchar(30) 
);

create table if not exists warehouse.dim_transaction(
    transaction_id varchar(40) primary key,
    transaction varchar(40)
);

create table if not exists warehouse.dim_ville(
    ville_id varchar(40) primary key,
    ville varchar(40)
);

create table if not exists warehouse.dim_quartier(
    quartier_id varchar(40) primary key,
    quartier varchar(40),
    ville_id varchar(40) references warehouse.dim_ville(ville_id)
);

create table if not exists warehouse.fact_annonces(
    annonce_id varchar(40) primary key,
    date_publication_id varchar(15),
    ville_id varchar(40),
    quartier_id varchar(40),
    type_bien_id varchar(15),
    transaction_id varchar(40),
    prix_categorie_id varchar(15),
    prix numeric(12,2),
    surface numeric(12,2),
    nb_chambres int,
    nb_salles_bain int,
    etage int,
    prix_m2 numeric(12,2),
    age_bien_immobilier int,
    FOREIGN KEY (date_id) REFERENCES warehouse.dim_temps(date_id),
    FOREIGN KEY (ville_id) REFERENCES warehouse.dim_ville(ville_id),
    FOREIGN KEY (quartier_id) REFERENCES warehouse.dim_quartier(quartier_id),
    FOREIGN KEY (type_bien_id) REFERENCES warehouse.dim_type_bien(type_bien_id),
    FOREIGN KEY (transaction_id) REFERENCES warehouse.dim_transaction(transaction_id),
    FOREIGN KEY (categorie_prix_id) REFERENCES warehouse.dim_categorie_prix(categorie_prix_id)
);