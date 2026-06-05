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
        reduit = []
        for regle in self.catalogue:
            if any(atome in self.modele_S for atome in regle.corps_negatif):
                continue

            tete_test = regle.tete
            if regle.tete.startswith("poss_rule__"):
                # Exemple : poss_rule__(70,b(1)) -> on coupe au premier ',' et on enlève le dernier ')'
                partie_interne = regle.tete.split("poss_rule__(")[1]
                # On isole tout ce qui est après la première virgule (le reste de l'atome)
                tete_test = partie_interne.split(",", 1)[1]
                # On enlève uniquement la toute dernière parenthèse de l'enveloppe
                if tete_test.endswith(")"):
                    tete_test = tete_test[:-1]

            if tete_test not in self.modele_S and tete_test != "true":
                continue

            reduit.append(copy.deepcopy(regle))
        return reduit

    def obtenir_poids_regle(self, regle):
        """ Extrait la valeur numérique alpha du marqueur nu__(alpha). """
        # Correction de la faute de frappe (retrait du '4' parasite)
        return regle.poids_necessite