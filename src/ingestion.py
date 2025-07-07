import os
import shutil

def ingest():
    """Vérifie et copie le CSV brut dans data/raw/ en fonction du cwd."""
    # Détermination dynamique de la racine
    cwd = os.getcwd()
    if os.path.basename(cwd) == "src":
        project_root = os.path.dirname(cwd)
    else:
        project_root = cwd

    source = os.path.join(project_root, "netflix_titles.csv")
    dest_dir = os.path.join(project_root, "data", "raw")
    dest = os.path.join(dest_dir, "netflix_titles.csv")

    os.makedirs(dest_dir, exist_ok=True)
    if not os.path.exists(source):
        raise FileNotFoundError(f"Fichier introuvable : {source}")
    shutil.copy(source, dest)
    print(f"Ingestion OK → {dest}")
    
if __name__ == "__main__":
    ingest()
