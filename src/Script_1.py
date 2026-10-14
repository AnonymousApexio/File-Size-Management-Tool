### Script numéro 1

### Partie 1:
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget

### Partie 2:
def choisir_repertoire():
    """
    Ouvre une boîte de dialogue pour sélectionner un répertoire
    Nous donne le chemin sélectionné sous forme d’objet "Path", ou None si annuléer
    """
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.hide()  # Empêche l’affichage d’une fenêtre superflue
    
    dossier = QFileDialog.getExistingDirectory(widget, "Selectionnez un repertoire", str(Path.home()))
    
    return Path(dossier) if dossier else None

### Partie 3:
def main():
    # Sélection du répertoire
    repertoire_de_base = choisir_repertoire()
    
    # Validation et affichage
    if repertoire_de_base:
        print(f"{repertoire_de_base}")
    else:
        print("Aucun répertoire sélectionné.")
    
    sys.exit()

if __name__ == '__main__':
    main()
