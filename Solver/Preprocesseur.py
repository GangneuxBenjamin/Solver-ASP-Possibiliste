import re


class Preprocesseur:
    """
    Classe chargée de transformer le programme possibiliste en programme ASP
    compatible avec Gringo, en préservant l'intégrité des structures via l'atome poss_rule__.
    """

    def __init__(self):
        # Ensemble pour stocker tous les poids uniques rencontrés
        self.poids_utilises = set()
        # Liste des règles transformées
        self.regles_transformees = []

    def charger_fichier(self, chemin_fichier):
        """
        Lit un fichier ligne par ligne et transforme chaque règle.
        """
        with open(chemin_fichier, 'r') as f:
            for ligne in f:
                # On ignore les lignes vides ou les commentaires
                ligne = ligne.strip()
                if ligne and not ligne.startswith('%'):
                    self.transformer_regle(ligne)

    def transformer_regle(self, regle_brute):
        """
        Prend une chaîne "poids tete :- corps."
        Et applique l'encapsulation de tête anti-optimisation :
        "poss_rule__(poids, tete) :- corps."
        Suivie de la projection classique : "tete :- poss_rule__(poids, tete)."
        """
        # Nettoyage des espaces superflus
        regle_brute = regle_brute.strip()

        # Expression régulière pour capturer le poids et le reste de la règle
        match = re.match(r"^(\d+)\s+(.+)$", regle_brute)

        if not match:
            # Si la ligne n'a pas de poids (ex: contrainte d'intégrité), on la conserve telle quelle
            self.regles_transformees.append(regle_brute)
            return regle_brute

        poids = match.group(1)
        structure_logique = match.group(2).rstrip('.').strip()  # Enlèvement du point final

        # Ajout du poids dans l'ensemble des poids utilisés
        self.poids_utilises.add(poids)

        # Extraction de la tête et du corps d'origine
        if ":-" in structure_logique:
            tete, corps = structure_logique.split(":-", 1)
            tete = tete.strip()
            corps = corps.strip()

            # 1. Règle encapsulée : poss_rule__(poids, tete) :- corps.
            regle_encapsulee = f"poss_rule__({poids}, {tete}) :- {corps}."
        else:
            tete = structure_logique
            # 1. Cas d'un fait : poss_rule__(poids, tete).
            regle_encapsulee = f"poss_rule__({poids}, {tete})."

        # 2. Projection classique indispensable pour Clasp : tete :- poss_rule__(poids, tete).
        projection_classique = f"{tete} :- poss_rule__({poids}, {tete})."

        # On stocke les deux règles générées dans le catalogue
        self.regles_transformees.append(regle_encapsulee)
        self.regles_transformees.append(projection_classique)

        return regle_encapsulee

    def generer_code_asp(self):
        """
        Génère le bloc de code final à envoyer au grounder.
        """
        # Plus besoin de forcer des externals ou des nu__() artificiels ici,
        # la structure poss_rule__ se suffit à elle-même pour bloquer Gringo.
        return "\n".join(self.regles_transformees)