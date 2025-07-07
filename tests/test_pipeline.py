# tests/test_pipeline.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest

from src.ingestion import ingest
from src.cleaning import clean
from src.enrichment import enrich

def test_ingestion_ok(tmp_path, monkeypatch, capsys):
    # Prépare un CSV factice à la racine temporaire
    src_csv = tmp_path / "netflix_titles.csv"
    src_csv.write_text(
        "show_id,type,title,director,cast,country,date_added,release_year,"
        "rating,duration,listed_in,description\n"
        "s0,Movie,Test,John Doe,Jane Doe,USA,2025-01-01,2025,PG,100 min,Test,Desc\n"
    )
    # On reste dans tmp_path pour l'ingestion
    monkeypatch.chdir(tmp_path)
    ingest()
    captured = capsys.readouterr()
    assert "Ingestion OK" in captured.out

def test_cleaning_creates_parquet(tmp_path, monkeypatch):
    # Prépare raw/ et silver/
    raw = tmp_path / "data" / "raw"
    silver = tmp_path / "data" / "silver"
    raw.mkdir(parents=True)
    silver.mkdir(parents=True)

    # CSV factice dans raw/
    df = pd.DataFrame({
        "show_id": ["s0"], "type": ["Movie"], "director": [None],
        "cast": [None], "country": [None], "date_added": ["2025-01-01"],
        "release_year": [2025], "rating": ["PG"], "duration": ["100 min"],
        "listed_in": ["Test"], "description": ["Desc"]
    })
    df.to_csv(raw / "netflix_titles.csv", index=False)

    # Crée le dossier src pour pouvoir y chdir
    (tmp_path / "src").mkdir()

    # Change de cwd vers tmp_path/src
    monkeypatch.chdir(tmp_path / "src")
    clean()

    out = tmp_path / "data" / "silver" / "netflix_silver.parquet"
    assert out.exists(), "Le fichier Parquet nettoyé n'a pas été créé."

def test_enrichment_generates_all_csvs(tmp_path, monkeypatch):
    # Prépare silver/ et gold/
    silver = tmp_path / "data" / "silver"
    gold = tmp_path / "data" / "gold"
    silver.mkdir(parents=True)
    gold.mkdir(parents=True)

    # Parquet factice dans silver/
    df = pd.DataFrame({
        "show_id": ["s0"], "type": ["Movie"], "director": ["Unknown"],
        "cast": ["Unknown"], "country": ["Unknown"],
        "date_added": pd.to_datetime(["2025-01-01"]),
        "year_added": [2025], "rating": ["PG"], "duration": ["100 min"],
        "listed_in": [["Test"]], "duration_num": [100.0]
    })
    df.to_parquet(silver / "netflix_silver.parquet", index=False)

    # Crée le dossier src pour pouvoir y chdir
    (tmp_path / "src").mkdir()

    # Change de cwd vers tmp_path/src
    monkeypatch.chdir(tmp_path / "src")
    enrich()

    expected = {
        "yearly.csv",
        "ratio_type.csv",
        "top_countries.csv",
        "top_genres.csv",
        "duration_stats.csv",
    }
    generated = set(os.listdir(tmp_path / "data" / "gold"))
    assert expected.issubset(generated), f"Il manque : {expected - generated}"
