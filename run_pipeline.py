# run_pipeline.py

from src.ingestion import ingest
from src.cleaning   import clean
from src.enrichment import enrich

if __name__ == "__main__":
    print("▶️ Début du pipeline Netflix")
    ingest()
    clean()
    enrich()
    print("✅ Pipeline terminé avec succès")
