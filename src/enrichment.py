import os
import pandas as pd

def enrich():
    """Charge le Parquet nettoyé, calcule les KPIs et écrit les CSV en fonction du cwd."""
    # Détermination dynamique de la racine
    cwd = os.getcwd()
    if os.path.basename(cwd) == "src":
        project_root = os.path.dirname(cwd)
    else:
        project_root = cwd

    silver_parquet = os.path.join(project_root, "data", "silver", "netflix_silver.parquet")
    gold_dir       = os.path.join(project_root, "data", "gold")

    df = pd.read_parquet(silver_parquet)

    # KPI 1: nombre de titres par année
    yearly = df.groupby('year_added').size().rename('count').reset_index()

    # KPI 2: répartition Film vs TV Show
    ratio = df.groupby(['year_added', 'type']).size().unstack(fill_value=0).reset_index()

    # KPI 3: top 5 pays producteurs
    top_countries = (
        df.assign(country=df['country'].str.split(', '))
          .explode('country')
          .groupby('country').size()
          .nlargest(5).rename('count').reset_index()
    )

    # KPI 4: top 10 genres
    top_genres = (
        df.explode('listed_in')
          .groupby('listed_in').size()
          .nlargest(10).rename('count').reset_index()
    )

    # KPI 5: durée moyenne
    df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
    movie_avg = df[df['type'] == 'Movie']['duration_num'].mean()
    show_avg  = df[df['type'] == 'TV Show']['duration_num'].mean()
    duration_stats = pd.DataFrame({
        'metric': ['avg_movie_duration', 'avg_tv_seasons'],
        'value': [movie_avg, show_avg]
    })

    os.makedirs(gold_dir, exist_ok=True)
    yearly.to_csv(os.path.join(gold_dir, 'yearly.csv'), index=False)
    ratio.to_csv(os.path.join(gold_dir, 'ratio_type.csv'), index=False)
    top_countries.to_csv(os.path.join(gold_dir, 'top_countries.csv'), index=False)
    top_genres.to_csv(os.path.join(gold_dir, 'top_genres.csv'), index=False)
    duration_stats.to_csv(os.path.join(gold_dir, 'duration_stats.csv'), index=False)

    print(f"Enrichment OK → {gold_dir}")

if __name__ == "__main__":
    enrich()
