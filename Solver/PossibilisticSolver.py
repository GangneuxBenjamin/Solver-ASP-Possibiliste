import subprocess
import json
import re


class PossibilisticSolver:
    """
    Gère l'interface avec les outils Potassco pour extraire
    uniquement les modèles stables classiques (S).
    """

    def __init__(self, preprocesseur):
        self.prepro = preprocesseur
        self.regles_ground = []

    def extraire_modeles_stables(self):
        """
        Lance la mise au sol avec Gringo, puis la résolution avec Clasp.
        Retourne la liste des modèles stables (ensembles d'atomes).
        """
        # 1. Récupération du code transformé par le préprocesseur
        code_enrichi = self.prepro.generer_code_asp()

        self.regles_ground = self._parser_code_preprocesseur(self.prepro.regles_transformees)

        # 2. Projection Classique : Nettoyage du code pour obtenir P*
        lignes = []
        for ligne in code_enrichi.splitlines():
            ligne = ligne.strip()
            if ligne.startswith("nu__(") and ligne.endswith(")."):
                continue
            if "#external" in ligne:
                continue
            lignes.append(ligne)

        p_star = "\n".join(lignes)
        p_star = re.sub(r",\s*nu__\(\d+\)", "", p_star)
        p_star = re.sub(r":-\s*nu__\(\d+\)", "", p_star)
        p_star = re.sub(r"\s+\.", ".", p_star)

        # --- MASQUAGE DES ACCENTS POUR GRINGO ---
        p_star_sans_accent = p_star.replace("é", "__accent_e__").replace("è", "__accent_e_grave__").replace("à",
                                                                                                            "__accent_a__")

        # 3. Phase de Grounding (Gringo) - EN MODE BINAIRE
        process_gringo = subprocess.run(
            ["gringo", "-", "--text"],
            input=p_star_sans_accent.encode('utf-8'),
            capture_output=True,
            text=False
        )

        if process_gringo.returncode != 0 or (not process_gringo.stdout and p_star_sans_accent):
            print("❌ Erreur lors de la mise au sol (Gringo) :")
            print(process_gringo.stderr.decode('utf-8', errors='ignore'))
            return []

        # 4. Phase de Résolution (Clasp) - EN MODE BINAIRE POUR L'ENTRÉE
        process_clasp = subprocess.run(
            ["clasp", "-", "0", "--outf=2"],
            input=process_gringo.stdout,
            capture_output=True,
            text=False
        )

        if not process_clasp.stdout:
            print("Erreur : Aucune réponse de Clasp.")
            return []

        # On décode le JSON de Clasp ici (bytes -> str) pour l'analyseur Python
        sortie_json_texte = process_clasp.stdout.decode('utf-8')
        donnees_clasp = json.loads(sortie_json_texte)
        modeles_stables = []

        if "Call" in donnees_clasp:
            for call in donnees_clasp["Call"]:
                for witness in call.get("Witnesses", []):
                    # --- DÉMASQUAGE DES ACCENTS POUR PYTHON ---
                    modele_restaure = set()
                    for atome in witness["Value"]:
                        atome_propre = atome.replace("__accent_e__", "é").replace("__accent_e_grave__", "è").replace(
                            "__accent_a__", "à")
                        modele_restaure.add(atome_propre)

                    modeles_stables.append(modele_restaure)

        return modeles_stables

    def _parser_code_preprocesseur(self, liste_regles_transformees):
        """
        Analyse les règles générées par le préprocesseur (ex: 'maladie1 :- nu__(90).')
        pour reconstruire le catalogue sans subir les optimisations de Gringo.
        """

        class RegleFormattee:
            def __init__(self, tete, corps_positif, corps_negatif, poids_necessite):
                self.tete = tete
                self.corps_positif = corps_positif
                self.corps_negatif = corps_negatif
                self.poids_necessite = poids_necessite

        regles = []
        for ligne in liste_regles_transformees:
            ligne = ligne.strip().rstrip(".")

            # Extraction du poids numérique
            m_poids = re.search(r"nu__\((\d+)\)", ligne)
            if not m_poids:
                continue
            poids = int(m_poids.group(1))

            # Extraction de la tête et du corps
            tete, corps = ligne.split(":-")
            tete = tete.strip()

            # Nettoyage du corps pour enlever le marqueur nu__
            corps_nettoye = re.sub(r"nu__\(\d+\)", "", corps).strip()
            # On enlève les virgules traînantes éventuelles
            corps_nettoye = corps_nettoye.strip(",").strip()

            if not corps_nettoye:
                # C'était un fait (ex: maladie1 :- nu__(90))
                regles.append(RegleFormattee(tete, [], [], poids))
            else:
                atomes_corps = [atome.strip() for atome in corps_nettoye.split(",") if atome.strip()]
                corps_positif = [a for a in atomes_corps if not a.startswith("not")]
                corps_negatif = [a.replace("not ", "").strip() for a in atomes_corps if a.startswith("not")]
                regles.append(RegleFormattee(tete, corps_positif, corps_negatif, poids))

        return regles