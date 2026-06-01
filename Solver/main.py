import os
from Preprocesseur import Preprocesseur
from PossibilisticSolver import PossibilisticSolver
from PossibilisticProgram import PossibilisticProgram
from FixPointOperator import FixPointOperator


def main():
    # 1. Configuration du chemin d'accès absolu au fichier .lp
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_lp = os.path.join(dossier_actuel, "Exemples", "combinatoire.lp")

    # 2. Instanciation et exécution du préprocesseur
    prepro = Preprocesseur()
    prepro.charger_fichier(chemin_lp)

    # 3. Instanciation du solveur et extraction des modèles classiques (S)
    solver = PossibilisticSolver(prepro)
    modeles_stables = solver.extraire_modeles_stables()

    print(f"--- {len(modeles_stables)} Modèle(s) Stable(s) Classique(s) trouvé(s) ---")

    # 4. Récupération du catalogue de règles mis au sol par le solveur
    catalogue_regles = solver.regles_ground

    # 5. Évaluation possibiliste (Réduction + Point Fixe) pour chaque modèle
    for i, S in enumerate(modeles_stables):
        print(f"\n================ Modèle Possibiliste {i + 1} ================")

        # Construction du programme réduit P^S pour le modèle courant
        prog_reduit = PossibilisticProgram(S, catalogue_regles)

        # Calcul des degrés de nécessité via l'opérateur de point fixe
        operateur = FixPointOperator(prog_reduit)
        poids_finaux = operateur.calculer()

        print("Atomes et leurs poids de nécessité finaux :")
        for atome, poids in poids_finaux.items():
            # On masque les atomes techniques nu__ pour n'afficher que la logique métier
            if not atome.startswith("nu__"):
                print(f"  -> {atome} : {poids}")


if __name__ == "__main__":
    main()