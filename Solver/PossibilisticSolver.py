import subprocess
import json
import re


class PossibilisticSolver:
    """
    Gère l'interface avec les outils Potassco pour extraire
    les modèles stables classiques (S) et les règles entièrement groundées.
    """

    def __init__(self, preprocesseur):
        self.prepro = preprocesseur
        self.regles_ground = []

    def extraire_modeles_stables(self):
        """
        Gère le pipeline de grounding et de résolution de manière isolée.
        """
        # 1. Récupération du code transformé par le préprocesseur (contient les poss_rule__)
        code_enrichi = self.prepro.generer_code_asp()

        # --- MASQUAGE DES ACCENTS POUR GRINGO ---
        code_enrichi_sans_accent = code_enrichi.replace("é", "__accent_e__").replace("è", "__accent_e_grave__").replace(
            "à", "__accent_a__")

        # 2. Phase de Grounding GLOBALE (Gringo)
        process_gringo = subprocess.run(
            ["gringo", "-", "--text"],
            input=code_enrichi_sans_accent.encode('utf-8'),
            capture_output=True,
            text=False
        )

        if process_gringo.returncode != 0 or not process_gringo.stdout:
            print("❌ Erreur lors de la mise au sol (Gringo) :")
            print(process_gringo.stderr.decode('utf-8', errors='ignore'))
            return []

        texte_grounde_brut = process_gringo.stdout.decode('utf-8')

        # 3. Construction du catalogue des règles à partir du texte BRUT (Découpage sécurisé)
        self.regles_ground = self._parser_code_grounde(texte_grounde_brut.splitlines())

        # 4. Projection Classique P* : On travaille sur une COPIE pour Clasp
        lignes_p_star = []
        for ligne in texte_grounde_brut.splitlines():
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#external"):
                continue

            # Simplification des structures poss_rule__ pour Clasp
            # Exemple : poss_rule__(50,a(1)) :- ... devient a(1) :- ...
            if "poss_rule__" in ligne:
                ligne = re.sub(r"poss_rule__\(\d+,([^)]+\)?)\)", r"\1", ligne)

            lignes_p_star.append(ligne)

        p_star = "\n".join(lignes_p_star)

        # 5. Phase de Résolution (Clasp) sur la projection classique
        process_clasp = subprocess.run(
            ["clasp", "-", "0", "--outf=2"],
            input=p_star.encode('utf-8'),
            capture_output=True,
            text=False
        )

        if not process_clasp.stdout:
            print("Erreur : Aucune réponse de Clasp.")
            return []

        sortie_json_texte = process_clasp.stdout.decode('utf-8')
        donnees_clasp = json.loads(sortie_json_texte)
        modeles_stables = []

        if "Call" in donnees_clasp:
            for call in donnees_clasp["Call"]:
                for witness in call.get("Witnesses", []):
                    modele_restaure = set()
                    for atome in witness["Value"]:
                        # --- DÉMASQUAGE DES ACCENTS ---
                        atome_propre = atome.replace("__accent_e__", "é").replace("__accent_e_grave__", "è").replace(
                            "__accent_a__", "à")
                        modele_restaure.add(atome_propre)
                    modeles_stables.append(modele_restaure)

        return modeles_stables

    def _parser_code_grounde(self, lignes_groundees):
        class RegleFormattee:
            def __init__(self, tete, corps_positif, corps_negatif, poids_necessite):
                self.tete = tete
                self.corps_positif = corps_positif
                self.corps_negatif = corps_negatif
                self.poids_necessite = poids_necessite

        regles = []
        for ligne in lignes_groundees:
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#external"):
                continue

            ligne = ligne.replace(", ", ",")

            ligne_propre = ligne.rstrip(".")
            ligne_propre = ligne_propre.replace("__accent_e__", "é").replace("__accent_e_grave__", "è").replace("__accent_a__", "à")

            if ":-" not in ligne_propre:
                regles.append(RegleFormattee(ligne_propre, [], [], 100))
                continue

            tete, corps = ligne_propre.split(":-", 1)
            tete = tete.strip()

            # Découpage algorithmique par niveau de parenthèses
            atomes_corps = []
            atome_courant = []
            niveau_parentheses = 0
            for caractere in corps:
                if caractere == '(': niveau_parentheses += 1
                elif caractere == ')': niveau_parentheses -= 1
                if caractere == ',' and niveau_parentheses == 0:
                    atomes_corps.append("".join(atome_courant).strip())
                    atome_courant = []
                else:
                    atome_courant.append(caractere)
            if atome_courant:
                atomes_corps.append("".join(atome_courant).strip())

            corps_positif = [a for a in atomes_corps if a and not a.startswith("not")]
            corps_negatif = [a.replace("not ", "").strip() for a in atomes_corps if a and a.startswith("not")]

            poids = 100
            if tete.startswith("poss_rule__"):
                try:
                    # Extraction propre du poids : ce qui est entre 'poss_rule__(' et la première virgule
                    poids = int(tete.split("poss_rule__(")[1].split(",")[0])
                except (IndexError, ValueError):
                    poids = 100

            regles.append(RegleFormattee(tete, corps_positif, corps_negatif, poids))

        print("------------------------------------------------")
        return regles