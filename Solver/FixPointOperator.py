class FixPointOperator:
    """
    Exécute le calcul de point fixe possibiliste sur un programme réduit P^S
    en appliquant l'opérateur de déduction itératif jusqu'à convergence.
    """

    def __init__(self, programme_reduit):
        # On récupère le programme réduit P^S et le modèle stable associé
        self.programme_reduit = programme_reduit
        self.modele_S = programme_reduit.modele_S

        # Initialisation de la table des poids : tous les atomes du modèle commencent à 0
        self.poids_atomes = {atome: 0 for atome in self.modele_S}

    def calculer(self):
        """
        Applique l'opérateur jusqu'à stabilité du système (Point Fixe).
        Retourne le modèle stable possibiliste (atomes associés à leur poids).
        """
        modifie = True

        while modifie:
            modifie = False

            # Parcours de toutes les règles du programme réduit P^S
            for regle in self.programme_reduit.regles_reduites:

                # 1. Calcul de la certitude du corps : C(body) = min(poids_atomes)
                if regle.corps_positif:
                    certitude_corps = min(self.poids_atomes[atome] for atome in regle.corps_positif)
                else:
                    # Si le corps positif est vide (cas d'un fait), la certitude du corps est maximale
                    certitude_corps = float('inf')

                # 2. Calcul de la certitude de la conclusion : C(head) = min(poids_règle, C(body))
                poids_regle = self.programme_reduit.obtenir_poids_regle(regle)
                nouvelle_certitude = min(poids_regle, certitude_corps)

                # 3. Mise à jour de l'atome de tête : application de l'opérateur MAX
                if nouvelle_certitude > self.poids_atomes[regle.tete]:
                    self.poids_atomes[regle.tete] = nouvelle_certitude
                    modifie = True  # Une valeur a changé, on devra refaire une itération

        return self.poids_atomes