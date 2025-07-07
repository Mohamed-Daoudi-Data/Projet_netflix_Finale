# run_pipeline.ps1

# 1. Se positionner dans le dossier du projet
Set-Location -Path (Split-Path $MyInvocation.MyCommand.Path -Parent)

# 2. Activer le virtualenv
#   Adapte le chemin si nécessaire
.\venv\Scripts\Activate.ps1

# 3. Lancer les étapes du pipeline
python .\src\ingestion.py
python .\src\cleaning.py
python .\src\enrichment.py

# 4. (Optionnel) journaliser la date d’exécution
"$((Get-Date).ToString('u')) — Pipeline exécuté." | Out-File -FilePath ".\logs\pipeline.log" -Append
