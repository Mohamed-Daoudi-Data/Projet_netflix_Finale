import os
import pandas as pd

def clean():
    """Nettoie les données brutes et écrit un Parquet propre en fonction du cwd."""
    # Détermination dynamique de la racine
    cwd = os.getcwd()
    if os.path.basename(cwd) == "src":
        project_root = os.path.dirname(cwd)
    else:
        project_root = cwd

    raw_csv        = os.path.join(project_root, "data", "raw", "netflix_titles.csv")
    silver_dir     = os.path.join(project_root, "data", "silver")
    silver_parquet = os.path.join(silver_dir, "netflix_silver.parquet")

    df = pd.read_csv(raw_csv)

    # Conversion date_added → datetime + extraction année
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year

    # Remplissage des valeurs manquantes
    for col in ['director', 'cast', 'country']:
        df[col] = df[col].fillna('Unknown')

    # Split des genres
    df = df.assign(listed_in=df['listed_in'].str.split(', '))

    os.makedirs(silver_dir, exist_ok=True)
    df.to_parquet(silver_parquet, index=False)
    print(f"Cleaning OK → {silver_parquet}")

if __name__ == "__main__":
    clean()
