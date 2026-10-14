# Reporting Tool - SAÉ 1.05

Outil de reporting et d'analyse d'espace disque : il parcourt un répertoire, identifie les fichiers les plus volumineux, les affiche dans une interface graphique (camembert + légendes interactives) et permet de générer un script PowerShell de suppression des fichiers sélectionnés.

---

## Sommaire

- [Contexte](#contexte)
- [Fonctionnalités](#fonctionnalités)
- [Architecture du projet](#architecture-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Détail des scripts](#détail-des-scripts)
- [Sécurité](#sécurité)
- [Auteur](#auteur)

---

## Contexte

Projet réalisé dans le cadre de la **SAÉ 1.05 « Traitement des données »** du BUT Réseaux & Télécommunications. L'objectif est de mettre en œuvre une chaîne complète de traitement de données : collecte sur le système de fichiers, filtrage, export au format JSON, puis restitution graphique via une interface PyQt5.

---

## Fonctionnalités

- **Sélection interactive** d'un répertoire à analyser via une boîte de dialogue native.
- **Parcours récursif** du répertoire pour récupérer tous les fichiers et leurs tailles.
- **Tri et filtrage** : ne conserve que les fichiers ≥ 5 Mo, limités à 100 fichiers maximum.
- **Export JSON** des résultats (`gros_fichiers.json`).
- **Visualisation graphique** :
  - Camembert représentant la répartition des tailles de fichiers.
  - Légendes paginées (25 fichiers par page) avec cases à cocher.
- **Génération d'un script PowerShell** de suppression des fichiers cochés, avec double confirmation.
- **Exécution immédiate** du script de suppression depuis l'interface.

---

## Architecture du projet

```
/
└── docs/
    ├── Clément_Ryan_SAE_1.05.pdf
    ├── Clément_Ryan_SAE_1.05.ppt
└── src/
    ├── Creation_Boutons.py     # Composant graphique : bouton + textbox
    ├── Creation_Camembert.py   # Composant graphique : diagramme circulaire
    ├── Creation_Legendes.py    # Composant graphique : légendes avec cases à cocher
    ├── Creation_Onglets.py     # Fenêtre principale à onglets
    ├── gros_fichiers.json      # Données générées par Script_2.py
    ├── Run_Reporting_Tool.ps1  # Orchestrateur PowerShell (point d'entrée)
    ├── Script_1.py             # Sélection du répertoire (IHM)
    ├── Script_2.py             # Exploration, tri, filtrage, export JSON
    ├── Script_3.py             # Interface graphique PyQt5 (camembert + légendes)
├── LICENSE
├── README.md
└── requirements.txt            # Fichier de dépendances.
```

---

## Prérequis

- **Python 3.8+**
- **PyQt5** (avec les modules `QtWidgets`, `QtGui`, `QtChart`, `QtCore`)
- **PowerShell** (Windows) ou **PowerShell Core** (Linux/macOS) pour exécuter l'orchestrateur.

Installation des dépendances Python :

```bash
pip install PyQt5 PyQtChart
```

---

## Installation

1. Cloner le dépôt :

   ```bash
   git clone https://github.com/AnonymousApexio/Reporting-tool
   cd Reporting-tool
   ```

2. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```
---

## Utilisation

### Lancement complet (recommandé)

Depuis PowerShell, à la racine du projet :

```powershell
.\Run_Reporting_Tool.ps1
```

L'orchestrateur enchaîne automatiquement :

1. **Script_1** - sélection du répertoire par l'utilisateur.
2. **Script_2** - analyse et génération de `gros_fichiers.json`.
3. **Script_3** - affichage de l'interface graphique.

### Lancement manuel, étape par étape (Non-recommendé)

```bash
# 1. Sélectionner le répertoire à analyser
python Script_1.py

# 2. Analyser le répertoire (le chemin est passé en argument)
python Script_2.py "C:\Users\mon_user\Downloads"

# 3. Lancer l'interface graphique
python Script_3.py
```

---

## Détail des scripts

### `Run_Reporting_Tool.ps1`

Orchestrateur qui exécute les trois scripts Python à la suite, en vérifiant à chaque étape que la précédente a bien produit un résultat (répertoire sélectionné, fichier JSON généré).

### `Script_1.py`

- Ouvre une boîte de dialogue `QFileDialog.getExistingDirectory`.
- Renvoie le chemin sélectionné via `stdout` pour être capturé par PowerShell.

### `Script_2.py`

| Étape | Fonction | Rôle |
|-------|----------|------|
| 1 | `build_list()` | Parcours récursif (`rglob`) et collecte `[chemin, taille]`. |
| 2 | `sort_function()` | Tri décroissant par taille. |
| 3 | `filter_function()` | Filtre ≥ X (`TAILLE_MIN`) Mo et limite à 100 fichiers. |
| 4 | `build_json()` | Export JSON indenté avec chemins échappés. |

### `Script_3.py`

- Charge `gros_fichiers.json` et valide sa structure.
- Génère des couleurs aléatoires (`QColor`) pour chaque fichier.
- Construit une fenêtre à onglets contenant :
  - **Onglet Camembert** : répartition visuelle des tailles.
  - **Onglets Légende N** : 25 fichiers par page avec cases à cocher.
  - **Onglet IHM** : bouton de génération du script de suppression.
- Génère `suppression_fichiers.ps1` et l'exécute via `subprocess`.

### Composants graphiques

| Fichier | Rôle |
|---------|------|
| `Creation_Onglets.py` | Fenêtre principale `QMainWindow` + `QTabWidget`. |
| `Creation_Camembert.py` | Diagramme circulaire `QPieSeries` avec pourcentages. |
| `Creation_Legendes.py` | Lignes de légende avec case à cocher + pastille colorée. |
| `Creation_Boutons.py` | Bouton de génération + champ texte du répertoire. |

---

## Sécurité

⚠️ **Ce projet génère et exécute un script PowerShell de suppression de fichiers.**

- La suppression est **conditionnée par deux saisies manuelles** (`OUI` puis `OUI`).
- Les fichiers supprimés sont **définitivement perdus** (`Remove-Item -Force`), sans passer par la corbeille.
- Il est fortement recommandé de **tester l'outil dans un répertoire de test** avant toute utilisation sur des données sensibles.
- Le projet n'intègre **pas** de mécanisme de sauvegarde automatique.

---

## Auteur
Développé dans le cadre du **BUT Réseaux & Télécommunications - IUT de Colmar**.

Répartition des rôles :
- **Scripts 1 et 2** : sélection du répertoire et traitement des données.
- **Script 3 et composants graphiques** : interface PyQt5, visualisation et génération du script de suppression.

---

## Licence

Projet pédagogique — usage strictement éducatif.