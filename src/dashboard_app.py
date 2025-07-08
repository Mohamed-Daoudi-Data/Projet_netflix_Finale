import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# ─── Config page ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Netflix Content Insights",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Chargement des données (cache pour performance) ───────────────────────────
@st.cache_data
def load_data():
    root        = Path(__file__).parents[1]
    silver_pq   = root / "data" / "silver" / "netflix_silver.parquet"
    df_silver   = pd.read_parquet(silver_pq)
    df_yearly   = df_silver.groupby("year_added").size().rename("count").reset_index()
    df_ratio    = df_silver.groupby(["year_added", "type"]).size().unstack(fill_value=0).reset_index()
    df_duration = df_silver.assign(
        duration_num=df_silver["duration"].str.extract(r"(\d+)").astype(float)
    )
    df_duration_stats = pd.DataFrame({
        "metric": ["avg_movie_duration", "avg_tv_seasons"],
        "value": [
            df_duration[df_duration["type"]=="Movie"]["duration_num"].mean(),
            df_duration[df_duration["type"]=="TV Show"]["duration_num"].mean()
        ]
    })
    return df_silver, df_yearly, df_ratio, df_duration_stats

df_silver, df_yearly, df_ratio, df_duration_stats = load_data()

# ─── Sidebar : filtres ──────────────────────────────────────────────────────────
st.sidebar.header("Filtres")

ymin, ymax = int(df_yearly.year_added.min()), int(df_yearly.year_added.max())
year_sel   = st.sidebar.slider("Année d’ajout", ymin, ymax, (ymin, ymax))

top_n_countries = st.sidebar.number_input("Top N pays", 1, 50, 5)
top_n_genres    = st.sidebar.number_input("Top N genres", 1, 50, 10)

show_raw = st.sidebar.checkbox("Afficher les données brutes")

# ─── Metrics header ─────────────────────────────────────────────────────────────
st.title("🎬 Netflix Content Insights")

total_titles = int(df_yearly["count"].sum())
total_movies = int(df_ratio["Movie"].sum())
total_shows  = int(df_ratio["TV Show"].sum())
avg_movie    = df_duration_stats.query("metric=='avg_movie_duration'")["value"].iloc[0]
avg_seasons  = df_duration_stats.query("metric=='avg_tv_seasons'")["value"].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5, gap="large")
c1.metric("📦 Total titres", f"{total_titles}")
c2.metric("🎥 Films", f"{total_movies}")
c3.metric("📺 Séries", f"{total_shows}")
c4.metric("⏱️ Durée moy. film", f"{avg_movie:.1f} min")
c5.metric("🔢 Saisons moy.", f"{avg_seasons:.1f}")

# ─── Visualisations ────────────────────────────────────────────────────────────

# 1) Titres par année
st.header("Titres ajoutés par année")
df_y = df_yearly.query("@year_sel[0] <= year_added <= @year_sel[1]")
st.line_chart(df_y.set_index("year_added")["count"])

# 2) Films vs Séries
st.header("Répartition Films vs Séries")
df_r = df_ratio.query("@year_sel[0] <= year_added <= @year_sel[1]")
st.bar_chart(df_r.set_index("year_added"))

# 3) Top pays producteurs (live)
st.header(f"Top {top_n_countries} Pays producteurs")
df_c = (
    df_silver
    .assign(country=df_silver["country"].str.split(", "))
    .explode("country")
    .groupby("country")
    .size()
    .nlargest(top_n_countries)
    .rename("count")
    .reset_index()
)

st.bar_chart(df_c.set_index("country")["count"])

# 4) Carte du monde – bulle par pays
st.header("🌍 Production par pays (carte)")
fig = px.scatter_geo(
    df_c,
    locations="country",
    locationmode="country names",
    size="count",
    projection="natural earth",
    title="Plus la bulle est grosse, plus le pays a de titres sur Netflix",
)
st.plotly_chart(fig, use_container_width=True)

# 5) Top genres (live)
st.header(f"Top {top_n_genres} Genres")
df_g = (
    df_silver
    .explode("listed_in")
    .groupby("listed_in")
    .size()
    .nlargest(top_n_genres)
    .rename("count")
    .reset_index()
)
st.bar_chart(df_g.set_index("listed_in")["count"])

# 6) Durée moyenne détaillée
st.header("Durée moyenne par type")
st.table(df_duration_stats.set_index("metric"))

# ─── Données brutes (optionnel) ───────────────────────────────────────────────
if show_raw:
    st.header("Données brutes Silver")
    st.dataframe(df_silver)
    st.header("Yearly")
    st.dataframe(df_yearly)
    st.header("Ratio")
    st.dataframe(df_ratio)
    st.header("Durée stats")
    st.dataframe(df_duration_stats)
