import re

class Preprocesseur:
    """
    Classe chargée de transformer le programme possibiliste en programme ASP
    compatible avec Gringo, en préservant les poids via l'atome nu__(poids).
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
        Et retourne "tete :- corps, nu__(poids)."
        """
        # Nettoyage des espaces superflus
        regle_brute = regle_brute.strip()

        # Expression régulière pour capturer :
        # 1. Le poids au début (chiffres)
        # 2. Le reste de la règle (tête et corps)
        # On gère les deux formats : "poids tete :- corps." et "poids tete."
        match = re.match(r"^(\d+)\s+(.+)$", regle_brute)

        if not match:
            # Si la ligne n'a pas de poids (ex: une directive), on la laisse telle quelle
            return regle_brute

        poids = match.group(1)
        structure_logique = match.group(2).rstrip('.')  # On enlève le point final pour l'instant

        # Ajout du poids dans l'ensemble des poids utilisés (pour les déclarations #external)
        self.poids_utilises.add(poids)

        # Reconstruction de la règle en injectant nu__(poids)
        # Si la règle a un corps (contient ":-")
        if ":-" in structure_logique:
            tete, corps = structure_logique.split(":-", 1)
            # On injecte nu__(poids) dans le corps positif
            regle_transformee = f"{tete.strip()} :- {corps.strip()}, nu__({poids})."
        else:
            # C'est un fait (ex: "100 a(1)."), on lui crée un corps avec le poids
            regle_transformee = f"{structure_logique.strip()} :- nu__({poids})."

        # On stocke pour usage ultérieur
        self.regles_transformees.append(regle_transformee)

        return regle_transformee

    def generer_code_asp(self):
        """
        Génère le bloc de code final à envoyer au grounder.
        Inclut la directive #external et les faits nu__(poids).
        """
        code = []

        # Ajout de la directive cruciale
        code.append("#external nu__(poids).")

        # Ajout des faits de poids pour que Gringo reconnaisse les symboles
        for p in self.poids_utilises:
            code.append(f"nu__({p}).")

        # Ajout des règles transformées
        code.extend(self.regles_transformees)

        return "\n".join(code)