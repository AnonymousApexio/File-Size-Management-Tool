### Script numéro 2

# partie numéro 1:
import json
import sys
from pathlib import Path

# Partie numéro 2:
def build_list(repertoire_de_base: Path):
    """
    Explore récursivement le répertoire pour récupérer la liste des fichiers avec leur taille.
    Chaque élément est une liste : [chemin absolu (str), taille en octets (int)].
    """
    liste_fichiers = []
    for fichier in repertoire_de_base.rglob('*'):
        if fichier.is_file():
            try:
                taille = fichier.stat().st_size
            except Exception:
                taille = 0
            liste_fichiers.append([str(fichier.resolve()), taille])
    if liste_fichiers:
        print("Some files detected:", liste_fichiers[:25])
    return liste_fichiers

# Partie numéro 3:
def sort_function(liste_fichiers: list):
    """Trie les fichiers du plus gros au plus petit."""
    return sorted(liste_fichiers, key=lambda x: x[1], reverse=True)

# Partie numéro 4:
def filter_function(liste_fichiers: list, TAILLE_MINI_FICHIER_EN_MEGA_OCTET: float, NB_MAXI_FICHIERS: int) -> list:
    """
    Filtre les fichiers selon une taille minimale et un nombre maximal.
    """
    taille_min_octets = TAILLE_MINI_FICHIER_EN_MEGA_OCTET * 1048576  # Conversion Mo → octets
    fichiers_filtres = [f for f in liste_fichiers if f[1] >= taille_min_octets]  # Garde seulement les fichiers assez grands
    return fichiers_filtres[:NB_MAXI_FICHIERS]  # Limite à NB_MAXI_FICHIERS fichiers

# Partie numéro 5:
def build_json(liste_fichiers: list, nom_fichier: str):
    """
    Sauvegarde la liste des fichiers sous forme de JSON.
    """
    fichiers_json = [[chemin.replace('\\', '\\\\'), taille] for chemin, taille in liste_fichiers]
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(fichiers_json, f, indent=4)
    print(f"Fichier JSON '{nom_fichier}' généré avec succès.")

# Partie numéro 6:
def main():
    # Initialisation : Si un argument est passé, on l'utilise sinon le répertoire courant
    repertoire_de_base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    print(f"Analyse du répertoire : {repertoire_de_base}")
    
    # Exploration
    liste_fichiers = build_list(repertoire_de_base)
    print(f"{len(liste_fichiers)} fichiers détectés.")
    
    # Tri
    fichiers_tries = sort_function(liste_fichiers)
    
    # Filtrage
    TAILLE_MIN = 5  # Mo
    NB_MAX = 100
    fichiers_final = filter_function(fichiers_tries, TAILLE_MIN, NB_MAX)
    print(f"{len(fichiers_final)} fichiers retenus après filtrage.")
    
    # Export
    build_json(fichiers_final, "gros_fichiers.json")

if __name__ == '__main__':
    main()
