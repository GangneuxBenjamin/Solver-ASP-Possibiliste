
# Serveur de Résolution d'ASP Possibiliste

Ce projet présente l'implémentation d'un solveur dédié à la programmation logique par ensembles de réponses possibilistes (Possibilistic Answer Set Programming - PASP). Cet outil a pour objectif la résolution de problèmes combinatoires complexes enrichis par une modélisation de l'incertitude épistémique, combinant la puissance du raisonnement non-monotone et les fondements de la théorie des possibilités.

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
2. **Phase de projection classique et résolution (`PossibilisticSolver`)** : Génération de la projection classique $P^*$ du programme. Le script pilote ensuite par flux de données (sous-processus) les outils de mise au sol et de résolution de la suite Potassco pour extraire l'ensemble des modèles stables classiques ($S$).
3. **Phase de réduction possibiliste (`PossibilisticProgram`)** : Pour chaque modèle stable classique identifié, un programme réduit $P^S$ est instancié en évaluant la cohérence des corps négatifs (les expressions précédées d'un opérateur de négation par l'échec `not`).
4. **Phase d'évaluation possibiliste (`FixPointOperator`)** : Application itérative d'un opérateur de point fixe. Le degré de validité d'une conjonction de faits (le corps de la règle) est déterminé par la valeur minimale de ses composants ($\min$). La mise à jour du degré de nécessité de la conclusion (la tête de la règle) applique l'opérateur $\max$ par rapport aux itérations précédentes. Le processus converge lorsque la table des poids atteint une stabilité stricte.

---

## 3. Implémentation et Exigences Techniques

L'environnement opérationnel repose sur le couplage d'un code applicatif de haut niveau et de moteurs d'inférence natifs compilés.

### 1. Environnement Python

L'architecture globale, incluant le préprocesseur, les structures de données de filtrage ainsi que l'opérateur mathématique de point fixe, est intégralement développée en langage Python. L'exécution requiert l'installation d'un interpréteur Python 3 standard.

### 2. Moteurs d'inférence : Gringo et Clasp

Le traitement combinatoire intermédiaire nécessite l'utilisation des binaires de l'organisation Potassco :

* **Gringo** : Assure la mise au sol (grounding) des variables logiques.
* **Clasp** : Constitue le solveur d'ensembles de réponses chargé de l'analyse structurelle des modèles.

Ces composants externes doivent être impérativement accessibles via les variables d'environnement du système (`PATH`). Les fichiers exécutables correspondants peuvent être obtenus via la plateforme officielle de distribution :

> [Dépôt Officiel des Outils Potassco (Clingo)](https://potassco.org/clingo/)

---

## 4. Guide de Déploiement et d'Exécution

Une fois les dépendances logicielles installées et configurées :

1. Ouvrir une invite de commande ou un environnement de développement intégré (tel que PyCharm).
2. Se positionner à la racine du répertoire du projet.
3. Exécuter la commande d'initialisation :
```bash
python main.py

```



L'application chargera le jeu de données configuré par défaut (`Exemples/combinatoire.lp`), exécutera le traitement possibiliste, puis restituera au sein du terminal les différents modèles stables accompagnés des indices de nécessité calculés pour chaque atome.

---

## 5. Procédure de Création et d'Évaluation de Nouvelles Instances

L'évaluation de nouveaux scénarios ou de cas d'étude distincts s'effectue sans altération du code source algorithmique Python. Le solveur est conçu pour charger dynamiquement de nouvelles spécifications déclaratives formalisées dans des fichiers indépendants.

Pour soumettre une nouvelle instance de problème au système, la procédure opérationnelle requiert les étapes suivantes :

### A. Formalisation de la nouvelle base de connaissances

1. **Création du fichier source** : Au sein du répertoire `Exemples`, instancier un nouveau fichier texte et lui affecter explicitement l'extension `.lp` (par exemple : `analyse_decisionnelle.lp`).
2. **Syntaxe des clauses possibilistes** : Consigner les axiomes et les règles du problème au sein du fichier. Chaque énoncé doit impérativement débuter par une valeur entière (représentant le poids de nécessité), suivie d'un espace syntaxique faisant office de séparateur avant la structure logique ASP classique.
*Exemple de formalisation cible :*
```asp
100 composant(c1).
95  defaillant(X) :- composant(X), surchauffe(X).
85  surchauffe(c1).

```



### B. Routage et reconfiguration du pipeline d'exécution

Afin d'orienter le préprocesseur et le solveur vers cette nouvelle instance au lieu du jeu d'essai par défaut, il est nécessaire de modifier l'assignation de la variable définissant le chemin d'accès au sein du module principal `main.py` (aux alentours de la ligne 12) :

```python
# Configuration initiale (Jeu d'essai par défaut) :
chemin_lp = os.path.join(dossier_actuel, "Exemples", "combinatoire.lp")

# Reconfiguration cible (Chargement de la nouvelle instance) :
chemin_lp = os.path.join(dossier_actuel, "Exemples", "analyse_decisionnelle.lp")

```

### C. Phase de test et d'analyse des résultats

Une fois le ciblage mis à jour dans le script principal, l'exécution de la commande standard permet de valider le comportement du système face au nouveau modèle :

```bash
python main.py

```

Le pipeline effectuera automatiquement la traduction syntaxique via l'atome externe `nu__`, extraira les nouveaux modèles stables via la suite Potassco, et appliquera l'opérateur de point fixe pour restituer les degrés de certitude propres à cette nouvelle instance directement au sein du terminal.
