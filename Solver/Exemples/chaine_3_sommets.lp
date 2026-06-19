% =================================================================
% PROGRAMME : 2-coloration d'une chaîne à 3 sommets PONDÉRÉ
% =================================================================

% 1. Définition du domaine (Faits stricts, certitude 100 implicite)
node(1..3).
e(1,2).
e(2,3).

% 2. Génération avec des poids d'incertitude
% On imagine par exemple qu'on préfère largement le rouge (90) au vert (70)
90 color(X, r) :- node(X), not color(X, g).
70 color(X, g) :- node(X), not color(X, r).

% 3. Contrainte d'intégrité stricte (Pas de poids = certitude 100)
:- e(X, Y), color(X, C), color(Y, C).

% 4. Directive d'affichage
#show color/2.