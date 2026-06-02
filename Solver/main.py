import os
import sys
from Preprocesseur import Preprocesseur
from PossibilisticSolver import PossibilisticSolver
from PossibilisticProgram import PossibilisticProgram
from FixPointOperator import FixPointOperator


def main():
    # 1. Gestion dynamique des arguments de la ligne de commande
    if len(sys.argv) < 2:
        print("Erreur : Aucun fichier d'entrée spécifié.")
        print("Usage : python3 main.py <nom_fichier.lp> [fichier_destination]")
        sys.exit(1)

    nom_fichier_entree = sys.argv[1]
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_lp = os.path.join(dossier_actuel, "Exemples", nom_fichier_entree)

    if not os.path.exists(chemin_lp):
        print(f"Erreur : Le fichier '{chemin_lp}' est introuvable.")
        sys.exit(1)

    # Détermination du canal de sortie (Fichier ou Console)
    fichier_sortie = None
    if len(sys.argv) >= 3:
        nom_fichier_sortie = sys.argv[2]
        chemin_sortie = os.path.join(dossier_actuel, nom_fichier_sortie)
        try:
            fichier_sortie = open(chemin_sortie, "w", encoding="utf-8")
        except IOError as e:
            print(f"Erreur lors de la création du fichier de destination : {e}")
            sys.exit(1)

    # 2. Instanciation et exécution du préprocesseur
    prepro = Preprocesseur()
    prepro.charger_fichier(chemin_lp)

    # 3. Instanciation du solveur et extraction des modèles classiques (S)
    solver = PossibilisticSolver(prepro)
    modeles_stables = solver.extraire_modeles_stables()

    # Fonction utilitaire pour écrire dans le bon canal
    def ecrire(texte):
        if fichier_sortie:
            fichier_sortie.write(texte + "\n")
        else:
            print(texte)

    ecrire(f"--- {len(modeles_stables)} Modèle(s) Stable(s) Classique(s) trouvé(s) ---")

    # 4. Récupération du catalogue de règles mis au sol par le solveur
    catalogue_regles = solver.regles_ground

    # 5. Évaluation possibiliste (Réduction + Point Fixe) pour chaque modèle
    for i, S in enumerate(modeles_stables):
        ecrire(f"\n================ Modèle Possibiliste {i + 1} ================")

        # Construction du programme réduit P^S pour le modèle courant
        prog_reduit = PossibilisticProgram(S, catalogue_regles)

        # Calcul des degrés de nécessité via l'opérateur de point fixe
        operateur = FixPointOperator(prog_reduit)
        poids_finaux = operateur.calculer()

        ecrire("Atomes et leurs poids de nécessité finaux :")
        for atome, poids in poids_finaux.items():
            # On masque les atomes techniques nu__ pour n'afficher que la logique métier
            if not atome.startswith("nu__"):
                ecrire(f"  -> {atome} : {poids}")

    # Fermeture propre du fichier si nécessaire
    if fichier_sortie:
        fichier_sortie.close()
        print(f"Traitements terminés. Les résultats ont été consignés dans : {sys.argv[2]}")


if __name__ == "__main__":
    main()