# Serveur de Résolution d'ASP Possibiliste

Ce projet présente l'implémentation d'un solveur dédié à la programmation logique par ensembles de réponses possibilistes . Cet outil a pour objectif la résolution de problèmes combinatoires complexes enrichis par une modélisation de l'incertitude épistémique, combinant la puissance du raisonnement non-monotone et les fondements de la théorie des possibilités.

---

## 1. Présentation et Objectifs Phares

Dans le cadre de la représentation des connaissances, la programmation logique classique (ASP) souffre d'une rigidité binaire face aux informations incomplètes ou incertaines. L'ASP Possibiliste résout cette limitation en associant à chaque règle ou fait logique un degré de nécessité ou de certitude ($\alpha \in [0, 1]$).

L'objectif de cette application est de :
* Traiter des bases de connaissances logiques pondérées.
* Éliminer les scénarios mutuellement exclusifs ou contradictoires afin d'extraire les structures de solutions cohérentes (les modèles stables).
* Évaluer la propagation des incertitudes à l'aide d'un opérateur mathématique rigoureux, déterminant ainsi le degré de certitude final de chaque conclusion induite par le système.

---

## 2. Architecture et Principes Fonctionnels

Le système s'articule autour d'un pipeline d'exécution séquentiel, piloté par le module principal `main.py`, et requiert l'interaction entre des composants de traduction et des moteurs d'inférence externes.

### A. Spécification formelle du fichier d'entrée (`.lp`)
Le problème est consigné au sein d'un fichier portant l'extension `.lp` (Logic Programming). Chaque clause logique y est précédée d'un entier représentant de manière proportionnelle son poids de nécessité.

Exemple de syntaxe :
```asp
100 oiseau(tweety).
90  vole(X) :- oiseau(X), not manchot(X).
80  manchot(tweety).

```

### B. Cinématique d'exécution du script principal (`main.py`)

Lors de l'appel du point d'entrée du programme, les traitements suivants sont séquentiellement appliqués :

1. **Phase de préprocessing (`Preprocesseur`)** : Analyse syntaxique du fichier source afin d'isoler les valuations numériques. Afin de prémunir le système contre les optimisations agressives des solveurs classiques (qui tendraient à supprimer les annotations numériques), les poids sont encapsulés sous la forme d'atomes techniques externes via la structure `nu__(poids)`.
2. **Phase de projection classique et résolution (`PossibilisticSolver`)** : Génération de la projection classique $P^*$ du programme. Le script pilote ensuite par flux de données (sous-processus) les outils de mise au sol et de résolution pour extraire l'ensemble des modèles stables classiques ($S$).
3. **Phase de réduction possibiliste (`PossibilisticProgram`)** : Pour chaque modèle stable classique identifié, un programme réduit $P^S$ est instancié en évaluant la cohérence des corps négatifs (les expressions précédées d'un opérateur de négation par l'échec `not`).
4. **Phase d'évaluation possibiliste (`FixPointOperator`)** : Application itérative d'un opérateur de point fixe. Le degré de validité d'une conjonction de faits (le corps de la règle) est déterminé par la valeur minimale de ses composants ($\min$). La mise à jour du degré de nécessité de la conclusion (la tête de la règle) applique l'opérateur $\max$ par rapport aux itérations précédentes. Le processus converge lorsque la table des poids atteint une stabilité stricte.

---

## 3. Implémentation et Exigences Techniques

L'environnement opérationnel repose sur le couplage d'un code applicatif de haut niveau écrit en Python et de moteurs d'inférence natifs.

### 1. Environnement Python

L'architecture globale (préprocesseur, structures de filtrage, opérateur de point fixe) est développée en Python 3. L'exécution requiert un interpréteur Python 3 standard.

### 2. Configuration des moteurs d'inférence (Gringo et Clasp)

Sur les distributions Linux modernes (telles que Debian 12), les outils de la suite Potassco sont regroupés au sein d'un exécutable unique nommé `clingo`. Afin de garantir le bon fonctionnement du pipeline de résolution, le système doit disposer de redirections nommées `gringo` et `clasp`.

#### Procédure d'installation et de configuration système :

1. **Installation du paquet moteur** :
```bash
sudo apt update && sudo apt install gringo

```


2. **Création des liens symboliques** (indispensable pour l'interconnexion du script Python) :
```bash
sudo ln -s /usr/bin/clingo /usr/bin/gringo
sudo ln -s /usr/bin/clingo /usr/bin/clasp

```


3. **Actualisation du cache du terminal** :
```bash
hash -r

```



Vous pouvez valider la bonne configuration du système à l'aide de la commande `which gringo clasp` qui doit retourner les chemins `/usr/bin/gringo` et `/usr/bin/clasp`.

---

## 4. Guide de Déploiement et d'Exécution

Une fois l'environnement configuré, le script principal `main.py` reçoit dynamiquement ses instructions depuis l'invite de commande (ou depuis le terminal intégré de PyCharm).

> ⚠️ **IMPORTANT** : Pour que le chargement des modules Python et des fichiers du projet s'effectue correctement, vous devez impérativement vous positionner dans le répertoire contenant les classes (le dossier `Solver/`) avant de lancer l'exécution.

```bash
cd SolverASPPossibiliste/Solver/

```

L'application peut ensuite être appelée de deux manières distinctes selon le canal de restitution souhaité.

### Option A : Restitution standard dans la console

Pour afficher directement les modèles calculés et l'évaluation possibiliste au sein du terminal d'exécution, passez uniquement le nom du fichier source en paramètre (le script cherchera automatiquement le fichier dans le répertoire `Exemples/`) :

```bash
python3 main.py meteo.lp

```

### Option B : Exportation vers un fichier de destination

Pour consigner l'intégralité des résultats et des modèles calculés au sein d'un fichier textuel spécifique sans encombrer la console, spécifiez un second argument représentant le nom du fichier cible :

```bash
python3 main.py meteo.lp resultats.txt

```

*Note : Le fichier de destination sera automatiquement généré ou écrasé à la racine du dossier d'exécution.*

---

## 5. Procédure de Création et d'Évaluation de Nouvelles Instances

L'évaluation de nouveaux scénarios ou de cas d'étude distincts s'effectue sans aucune altération du code source algorithmique Python. Le solveur charge dynamiquement les spécifications déclaratives formalisées dans des fichiers indépendants transmis en argument.

### A. Formalisation de la nouvelle base de connaissances

1. **Création du fichier source** : Au sein du répertoire `Exemples/`, instanciez un nouveau fichier texte et affectez-lui explicitement l'extension `.lp` (par exemple : `analyse_decisionnelle.lp`).
2. **Syntaxe des clauses possibilistes** : Consignez les axiomes et les règles du problème. Chaque énoncé doit impérativement débuter par une valeur entière (représentant le poids de nécessité), suivie d'un espace syntaxique faisant office de séparateur avant la structure logique ASP classique.

*Exemple de formalisation (`Exemples/analyse_decisionnelle.lp`) :*

```asp
100 composant(c1).
95  defaillant(X) :- composant(X), surchauffe(X).
85  surchauffe(c1).

```

### B. Phase d'exécution et d'analyse

Pour évaluer cette nouvelle instance et stocker directement ses conclusions dans un fichier de sortie dédié, assurez-vous d'être dans le bon répertoire et lancez la commande en adaptant les arguments :

```bash
python3 main.py analyse_decisionnelle.lp rapport_sortie.txt

```

Le pipeline effectuera automatiquement la traduction syntaxique via l'atome externe `nu__`, extraira les configurations stables à l'aide de la suite Potassco interconnectée, et appliquera l'opérateur mathématique de point fixe avant d'écrire le bilan des degrés de certitude dans le fichier spécifié.

