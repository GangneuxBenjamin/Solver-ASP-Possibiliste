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
        regle_brute = regle_brute.strip()
        match = re.match(r"^(\d+)\s+(.+)$", regle_brute)

        if not match:
            self.regles_transformees.append(regle_brute)
            return regle_brute

        poids = match.group(1)
        structure_logique = match.group(2).rstrip('.').strip()
        self.poids_utilises.add(poids)

        # --- CAS PARTICULIER : C'est une contrainte d'intégrité (pas de tête) ---
        if structure_logique.startswith(":-"):
            corps = structure_logique.split(":-", 1)[1].strip()
            # On crée un identifiant technique unique pour cette contrainte
            id_contrainte = f"constraint_{len(self.regles_transformees)}"

            regle_encapsulee = f"poss_rule__({poids},{id_contrainte}) :- {corps}."
            # Si la contrainte est violée, on déclenche une contradiction classique
            projection_classique = f":- {corps}, poss_rule__({poids},{id_contrainte})."

            self.regles_transformees.append(regle_encapsulee)
            self.regles_transformees.append(projection_classique)
            return regle_encapsulee

        # --- CAS GÉNÉRAL (Règles et Faits) ---
        if ":-" in structure_logique:
            tete, corps = structure_logique.split(":-", 1)
            regle_encapsulee = f"poss_rule__({poids},{tete.strip()}) :- {corps.strip()}."
            projection_classique = f"{tete.strip()} :- poss_rule__({poids},{tete.strip()})."
        else:
            regle_encapsulee = f"poss_rule__({poids},{structure_logique}) :- true."
            projection_classique = f"{structure_logique} :- poss_rule__({poids},{structure_logique})."

        self.regles_transformees.append(regle_encapsulee)
        self.regles_transformees.append(projection_classique)
        return regle_encapsulee

    def generer_code_asp(self):
        """
        Génère le bloc de code final à envoyer au grounder.
        Force la présence d'un external pour briser l'évaluation partielle de Gringo.
        """
        code = [
            "#external _bloquer_optimisation.",
            "true :- not _bloquer_optimisation." # true devient indécidable statiquement pour Gringo !
        ]
        code.extend(self.regles_transformees)
        return "\n".join(code)