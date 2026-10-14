import json
import sys
import random
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons
import subprocess


NB_MAXI_FICHIERS = 100
NB_LEGENDES_PAR_PAGE = 25
JSON_FILE = "gros_fichiers.json"


def charger_donnees_json(fichier_json):
    """Charge les données du fichier JSON et vérifie sa conformité."""
    with open(fichier_json, "r") as f:
        data = json.load(f)
        if not all(
                isinstance(item, list) and len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], int) for
                item in data):
            raise ValueError("Le fichier JSON ne respecte pas la structure attendue.")
        return data


def generer_couleurs(n):
    """Génère une liste de n couleurs aléatoires au format QColor."""
    return [QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(n)]


def creer_script_suppression(liste_fichiers, etats_cases):
    """Génère un script PowerShell compatible multi-plateforme pour supprimer les fichiers sélectionnés."""
    script_path = Path("suppression_fichiers.ps1")
    with script_path.open("w", encoding="utf-8") as f:
        f.write("Write-Output \"Script de suppression de fichiers\"\n")
        f.write("$reponse = Read-Host \"Confirmer suppression (OUI)\"\n")
        f.write("if ($reponse -eq 'OUI') {\n")
        f.write("    $confirmation = Read-Host \"Etes-vous sur ? (OUI)\"\n")
        f.write("    if ($confirmation -eq 'OUI') {\n")
        for fichier, etat in zip(liste_fichiers, etats_cases):
            if etat:
                path_correct = Path(fichier[0]).as_posix()
                f.write(f'        Remove-Item -Path "{path_correct}" -Force\n')
        f.write("    } else { Write-Output \"Opération annulée\" }\n")
        f.write("} else { Write-Output \"Opération annulée\" }\n")
    print("Script de suppression généré.")

    # Exécuter le script PowerShell
    try:
        subprocess.run(["powershell", "-File", str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script PowerShell: {e}")

def main():
    """Programme principal d'affichage graphique."""
    app = QApplication(sys.argv)
    fenetre = Onglets()

    liste_fichiers = charger_donnees_json(JSON_FILE)
    liste_couleurs = generer_couleurs(len(liste_fichiers))

    fromage = Camembert(liste_fichiers, liste_couleurs)
    layout_fromage = fromage.dessine_camembert()
    fenetre.add_onglet("Camembert", layout_fromage)

    listes_legendes = []
    for num_page in range((len(liste_fichiers) + NB_LEGENDES_PAR_PAGE - 1) // NB_LEGENDES_PAR_PAGE):
        # Pass the starting index and the number of legends per page to Legendes
        legende = Legendes(liste_fichiers, liste_couleurs, num_page * NB_LEGENDES_PAR_PAGE, NB_LEGENDES_PAR_PAGE)
        listes_legendes.append(legende)
        layout_legende = legende.dessine_legendes()
        fenetre.add_onglet(f"Légende {num_page + 1}", layout_legende)


    def callback_suppression():
        etats = [etat for legende in listes_legendes for etat in legende.recupere_etats_cases_a_cocher()]
        creer_script_suppression(liste_fichiers, etats)

    repertoire_base = Path.cwd()  # Assurez-vous que le répertoire de base est correctement transmis
    ihm = Boutons(str(repertoire_base), callback_suppression)
    layout_ihm = ihm.dessine_boutons()
    fenetre.add_onglet("IHM", layout_ihm)

    fenetre.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
