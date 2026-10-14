$OutputEncoding = [System.Text.Encoding]::UTF16

$rep_base = (python .\Script_1.py)
if (-not $rep_base) {
    Write-Host "Aucun repertoire selectionne."
    exit
}

Write-Host "Directory passed to Script_2: $rep_base"
python .\Script_2.py $rep_base

if (-not (Test-Path "gros_fichiers.json")) {
    Write-Host "Erreur lors de l'analyse du répertoire."
    exit
}


python .\Script_3.py
