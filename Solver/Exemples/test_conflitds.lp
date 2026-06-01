% --- Faits de base avec certitudes variées ---
100 oiseau(tweety).
80 oiseau(pingouin).
100 pingouin(pingouin).

% --- Règles de comportement ---
% Un oiseau vole sauf s'il est un pingouin
90 vole(X) :- oiseau(X), not pingouin(X).
100 immobile(X) :- pingouin(X).

% --- Un choix incertain (pour générer deux modèles) ---
% On ne sait pas si tweety est un oiseau migrateur ou sédentaire
50 migrateur(X) :- oiseau(X), not sedentaire(X).
50 sedentaire(X) :- oiseau(X), not migrateur(X).

% --- Une conséquence de la migration ---
70 fatigue(X) :- migrateur(X).