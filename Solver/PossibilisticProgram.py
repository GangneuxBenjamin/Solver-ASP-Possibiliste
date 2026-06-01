class PossibilisticProgram:
    """
    Construit le programme réduit P^S pour un modèle stable S donné.
    """

    def __init__(self, modele_S, catalogue_regles_ground):
        self.modele_S = modele_S
        self.catalogue = catalogue_regles_ground
        self.regles_reduites = self._generer_reduit()

    def _generer_reduit(self):
        """ Filtre les règles pour construire le réduit possibiliste. """
        reduit = []
        for regle in self.catalogue:
            # 1. On vérifie si le corps négatif n'est pas contredit par le modèle S
            # (Si un atome après un 'not' est vrai dans S, la règle est bloquée)
            if any(atome in self.modele_S for atome in regle.corps_negatif):
                continue

            # 2. On s'assure que la tête de la règle appartient bien au modèle S
            if regle.tete not in self.modele_S:
                continue

            # Si la règle passe ces critères, elle fait partie du réduit P^S
            reduit.append(regle)
        return reduit

    def obtenir_poids_regle(self, regle):
        """ Extrait la valeur numérique alpha du marqueur nu__(alpha). """
        return regle.poids_necessite