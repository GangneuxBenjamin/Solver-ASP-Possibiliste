class FixPointOperator:
    """
    Exécute le calcul de point fixe possibiliste sur un programme réduit P^S
    en appliquant l'opérateur de déduction itératif jusqu'à convergence.
    """

    def __init__(self, programme_reduit):
        # On récupère le programme réduit P^S et le modèle stable associé
        self.programme_reduit = programme_reduit
        self.modele_S = programme_reduit.modele_S

        # 1. Initialisation de base : tous les atomes du modèle classique commencent à 0
        self.poids_atomes = {atome: 0 for atome in self.modele_S}

        # 2. INJECTION DES CONSTANTES POSSIBILISTES AUTOMATIQUE
        # On scanne le modèle stable et toutes les règles pour trouver les poss_rule__
        # et on leur donne immédiatement leur vrai poids inscrit dans leur nom.
        tous_les_atomes = set(self.modele_S)
        for regle in self.programme_reduit.regles_reduites:
            tous_les_atomes.add(regle.tete)
            tous_les_atomes.update(regle.corps_positif)

        for atome in tous_les_atomes:
            if atome.startswith("poss_rule__"):
                try:
                    # On extrait le nombre situé entre "poss_rule__(" et la première virgule
                    poids_extrait = int(atome.split("poss_rule__(")[1].split(",")[0])
                    self.poids_atomes[atome] = poids_extrait
                except (IndexError, ValueError):
                    self.poids_atomes[atome] = 100
    def calculer(self):
        """
        Applique l'opérateur jusqu'à stabilité du système (Point Fixe).
        Retourne le modèle stable possibiliste (atomes associés à leur poids).
        """
        for r in self.programme_reduit.regles_reduites:
            modifie = True

        while modifie:
            modifie = False

            # Parcours de toutes les règles du programme réduit P^S
            for regle in self.programme_reduit.regles_reduites:

                # Liste pour stocker les certitudes des éléments du corps
                poids_elements_corps = []

                for atome in regle.corps_positif:
                    # Si c'est un atome technique de poids (ex: nu__(50))
                    if atome.startswith("nu__"):
                        try:
                            # On extrait la valeur entière située entre les parenthèses
                            poids_extrait = int(atome.split("__(")[1].split(")")[0])
                            poids_elements_corps.append(poids_extrait)
                        except (IndexError, ValueError):
                            # Sécurité si le format du nu__ est altéré
                            poids_elements_corps.append(0)
                    else:
                        # Sinon c'est un atome logique standard, on prend sa valeur courante dans la table
                        poids_elements_corps.append(self.poids_atomes.get(atome, 0))

                # 1. Calcul de la certitude du corps : C(body) = min(poids_elements)
                if poids_elements_corps:
                    certitude_corps = min(poids_elements_corps)
                else:
                    # Si le corps positif est vide (cas d'un fait pur), la certitude du corps est maximale
                    certitude_corps = float('inf')

                # 2. Calcul de la certitude de la conclusion : C(head) = min(poids_règle, C(body))
                poids_regle = self.programme_reduit.obtenir_poids_regle(regle)
                nouvelle_certitude = min(poids_regle, certitude_corps)

                # 3. Mise à jour de l'atome de tête : application de l'opérateur MAX
                # Sécurité : on s'assure de ne pas mettre à jour un nu__ s'il se retrouvait par erreur en tête
                if regle.tete in self.poids_atomes and not regle.tete.startswith("nu__"):
                    if nouvelle_certitude > self.poids_atomes[regle.tete]:
                        self.poids_atomes[regle.tete] = nouvelle_certitude
                        modifie = True  # Une valeur a changé, on devra refaire une itération

        # Filtrage final pour ne retourner que les vrais atomes du modèle (on masque les nu__)
        # Au lieu de : return self.poids_atomes
        # Mets ceci :
        return {atome: poids for atome, poids in self.poids_atomes.items() if not atome.startswith("poss_rule__")}