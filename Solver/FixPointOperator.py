class FixPointOperator:
    def __init__(self, programme_reduit):
        self.programme_reduit = programme_reduit
        self.modele_S = programme_reduit.modele_S

        # 1. Initialisation générale à 0
        self.poids_atomes = {atome: 0 for atome in self.modele_S}

        # 2. On s'assure que toutes les enveloppes techniques possèdent leur entrée à 0
        for regle in self.programme_reduit.regles_reduites:
            if regle.tete not in self.poids_atomes:
                self.poids_atomes[regle.tete] = 0
            for atome in regle.corps_positif:
                if atome not in self.poids_atomes:
                    self.poids_atomes[atome] = 0

        # Ancrage initial incontestable
        self.poids_atomes["true"] = 100

    def calculer(self):
        """
        Applique l'opérateur jusqu'à convergence complète (Point Fixe).
        """
        modifie = True
        while modifie:
            modifie = False

            for regle in self.programme_reduit.regles_reduites:
                # Évaluation robuste du corps positif
                if not regle.corps_positif:
                    certitude_corps = 100
                else:
                    # Court-circuit : si l'atome est 'true', sa certitude vaut 100 d'office
                    certitude_corps = min(
                        100 if atome == "true" else self.poids_atomes.get(atome, 0)
                        for atome in regle.corps_positif
                    )

                # Application de la borne possibiliste (Modus Ponens Généralisé)
                certitude_conclusion = min(regle.poids_necessite, certitude_corps)

                # Accumulation par Maximum
                if certitude_conclusion > self.poids_atomes.get(regle.tete, 0):
                    self.poids_atomes[regle.tete] = certitude_conclusion
                    modifie = True

        # Renvoi des résultats épurés et strictement synchronisés avec l'Answer Set de Clasp
        return {
            atome: poids
            for atome, poids in self.poids_atomes.items()
            if atome in self.modele_S and not atome.startswith("poss_rule__") and atome != "true"
        }