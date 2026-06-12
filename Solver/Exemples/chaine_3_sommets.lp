% =================================================================
% PROGRAMME : 2-coloration d'une chaîne à 3 sommets
% =================================================================

% 1. Définition du domaine (Faits)
node(1..3).
e(1,2).
e(2,3).

% 2. Génération : Chaque sommet doit avoir exactement une couleur (r ou g)
{ color(X, r); color(X, g) } = 1 :- node(X).

% 3. Contrainte d'intégrité : Deux sommets connectés ne peuvent pas partager la même couleur
:- e(X, Y), color(X, C), color(Y, C).

% 4. Directive d'affichage : Masque les faits node/1 et e/2 pour n'afficher que la coloration
#show color/2.