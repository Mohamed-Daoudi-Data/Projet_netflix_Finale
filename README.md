# Projet Netflix Content Insights

## 🚀 Objectif  
Analyser l’évolution du catalogue Netflix (films vs séries, pays, genres, durées) et fournir un **dashboard Streamlit** interactif pour suivre les KPIs clés :
1. Nombre de titres ajoutés par année  
2. Ratio Films / TV Shows par année  
3. Top 5 pays producteurs  
4. Top 10 genres  
5. Durée moyenne des films et nombre moyen de saisons pour les séries  

## 📂 Structure du projet 

PROJET_NETFLIX/
│
├─ data/
│ ├─ raw/ # CSV originaux
│ ├─ silver/ # Parquet nettoyé
│ └─ gold/ # CSV KPI
│
├─ src/ # Scripts de pipeline
│ ├─ ingestion.py # Copie netflix_titles.csv → data/raw
│ ├─ cleaning.py # Nettoyage → data/silver/.parquet
│ ├─ enrichment.py # Agrégations KPI → data/gold/.csv
│ └─ dashboard_app.py# Dashboard Streamlit
│
├─ tests/ # Tests unitaires (pytest)
│ └─ test_pipeline.py
│
├─ requirements.txt # Dépendances Python
├─ README.md # Ce fichier
└─ .streamlit/ # (optionnel) config Streamlit
└─ config.toml

## ⚙️ Installation & Setup  

1. **Cloner** le repo et se placer dans le dossier :  
   ```bash
   git clone <url_repo>
   cd PROJET_NETFLIX
