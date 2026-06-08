import copy


class PossibilisticProgram:
    """
    Construit le programme réduit P^S pour un modèle stable S donné.
    """

    def __init__(self, modele_S, catalogue_regles_ground):
        self.modele_S = modele_S
        self.catalogue = catalogue_regles_ground
        self.regles_reduites = self._generer_reduit()

    def _generer_reduit(self):
        import copy
        import re
        reduit = []

        for regle in self.catalogue:
            # 1. Réduction de Gelfond-Lifschitz : si le corps négatif intersecte le modèle, on jette
            if any(atome in self.modele_S for atome in regle.corps_negatif):
                continue

            # 2. Identification propre de la tête utilisateur
            tete_test = regle.tete
            if regle.tete.startswith("poss_rule__"):
                # On capture uniquement ce qui est après la première virgule et avant la dernière parenthèse
                # Exemple 1 : poss_rule__(100,mary) -> mary
                # Exemple 2 : poss_rule__(50,a(1)) -> a(1)
                match = re.match(r"poss_rule__\(\d+,(.+)\)$", regle.tete)
                if match:
                    tete_test = match.group(1).strip()

            # 3. Validation de l'existence logique dans l'Answer Set classique
            if tete_test not in self.modele_S and tete_test != "true":
                continue

            reduit.append(copy.deepcopy(regle))

        return reduit

    def obtenir_poids_regle(self, regle):
        """ Extrait la valeur numérique alpha du marqueur nu__(alpha). """
        # Correction de la faute de frappe (retrait du '4' parasite)
        return regle.poids_necessite