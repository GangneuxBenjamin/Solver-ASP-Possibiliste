% =================================================================
% PROGRAMME : Coloration de graphe avec échec (Triangle K3)
% =================================================================

% 1. Définition du domaine (Fermeture du triangle)
node(1..3).
e(1,2).
e(2,3).
e(3,1). % Cette arête ferme le cycle impair et provoque l'insatisfiabilité

% 2. Génération : Chaque sommet doit avoir exactement une couleur (r ou g)
{ color(X, r); color(X, g) } = 1 :- node(X).

% 3. Contrainte d'intégrité : Deux sommets connectés ne peuvent pas partager la même couleur
:- e(X, Y), color(X, C), color(Y, C).

% 4. Directive d'affichage
#show color/2.