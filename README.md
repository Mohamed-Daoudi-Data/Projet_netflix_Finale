
# 🎬 Projet Netflix Content Insights

> Un pipeline **ETL complet** et un **dashboard interactif** pour explorer le catalogue Netflix.

---

## 📁 Structure du projet

```
PROJET_NETFLIX/
│
├─ data/
│   ├─ raw/        → Données brutes (CSV)
│   ├─ silver/     → Données nettoyées (Parquet)
│   └─ gold/       → Données agrégées KPI (CSV)
│
├─ src/            → Scripts du pipeline
│   ├─ ingestion.py       → Copie netflix_titles.csv → raw/
│   ├─ cleaning.py        → Nettoyage → silver/.parquet
│   ├─ enrichment.py      → Génère les KPI → gold/.csv
│   └─ dashboard_app.py   → Application Streamlit
│
├─ tests/
│   └─ test_pipeline.py   → Tests unitaires (pytest)
│
├─ requirements.txt       → Dépendances Python
├─ .streamlit/config.toml → Config optionnelle Streamlit
└─ README.md              → Ce fichier
```

---

## ⚙️ Prérequis

- Python 3.11+
- `pip` et `venv` (ou `virtualenv`)
- Git

---

## 🚧 Installation

```bash
git clone https://github.com/Mohamed-Daoudi-Data/Projet_netflix_Finale.git
cd Projet_netflix_Finale

# Créer et activer l’environnement virtuel
python3 -m venv venv
source venv/bin/activate         # Linux/macOS
# .\venv\Scripts\Activate.ps1    # Windows PowerShell

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔄 Exécution du pipeline

### ▶️ Mode script simple

```bash
python run_pipeline.py
```

### 🪂 Mode Airflow

```bash
# Initialisation
export AIRFLOW_HOME="$PWD/airflow"
export AIRFLOW__WEBSERVER__AUTHENTICATE=False
export AIRFLOW__WEBSERVER__RBAC=False

airflow db reset --yes
airflow connections create-default-connections
```

```bash
# Terminal 1
airflow scheduler
```

```bash
# Terminal 2
airflow standalone
```

- Ouvre l’UI : http://localhost:8080  
- Déclenche le DAG : `netflix_pipeline`  
- Suis l’exécution en direct

---

## 📊 Dashboard interactif

```bash
streamlit run src/dashboard_app.py
```

Fonctionnalités :
- Filtres : année, pays, genre
- Carte du monde interactive 🌍
- Vue des données agrégées (KPI)

---

## ✅ Tests unitaires

```bash
pytest -q
```

Couvre :
- L’ingestion
- Le nettoyage
- L’enrichissement KPI

---

## 🔧 Extensions possibles

- 🔁 Passage en production : PostgreSQL + CeleryExecutor  
- 🔐 Sécurisation (RBAC, gestion utilisateurs)  
- 🐳 Déploiement Docker Compose ou cloud (Azure, GCP)  
- 🎯 Module de recommandation (similarité de genres)

---

## 🧾 Glossaire technique

| 🛠️ Technologie | Description / Pourquoi ? |
|----------------|--------------------------|
| **Pandas** | Manipulation rapide des données |
| **Parquet** | Format colonne performant pour traitement et stockage |
| **Streamlit** | Création simple de dashboards interactifs |
| **Airflow** | Orchestration et planification de pipeline ETL |
| **pytest** | Test unitaire des fonctions critiques |

---

## 👨‍💻 Auteur

Mohamed Daoudi — Licence Informatique  
Université XYZ — © 2025
