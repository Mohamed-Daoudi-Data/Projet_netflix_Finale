import streamlit as st
import pandas as pd
import os

# Détecte la racine du projet selon le répertoire courant
cwd = os.getcwd()
if os.path.basename(cwd) == 'src':
    PROJECT_ROOT = os.path.abspath(os.path.join(cwd, os.pardir))
else:
    PROJECT_ROOT = cwd

GOLD_DIR = os.path.join(PROJECT_ROOT, "data", "gold")

st.title("Netflix Content Insights")

# Chargement des données agrégées
yearly        = pd.read_csv(os.path.join(GOLD_DIR, "yearly.csv"))
ratio         = pd.read_csv(os.path.join(GOLD_DIR, "ratio_type.csv"))
top_countries = pd.read_csv(os.path.join(GOLD_DIR, "top_countries.csv"))
top_genres    = pd.read_csv(os.path.join(GOLD_DIR, "top_genres.csv"))
duration      = pd.read_csv(os.path.join(GOLD_DIR, "duration_stats.csv"))

# Filtre d'années
year_min, year_max = int(yearly.year_added.min()), int(yearly.year_added.max())
year_sel = st.sidebar.slider("Année d'ajout", year_min, year_max, (year_min, year_max))

# Graphiques
st.header("Titres ajoutés par année")
st.line_chart(yearly.set_index('year_added').loc[year_sel[0]:year_sel[1]])

st.header("Films vs Séries")
st.bar_chart(ratio.set_index('year_added').loc[year_sel[0]:year_sel[1]])

st.header("Top 5 Pays producteurs")
st.bar_chart(top_countries.set_index('country'))

st.header("Top 10 Genres")
st.bar_chart(top_genres.set_index('listed_in'))

st.header("Durée moyenne")
st.write(duration.set_index('metric'))
