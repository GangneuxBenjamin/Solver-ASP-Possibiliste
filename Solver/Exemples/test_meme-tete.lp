% --- Observations / Symptômes ---
80 fievre.
80 toux.

% --- Règles de Diagnostic menant au même atome (grippe) ---
% Règle 1 : Une forte fièvre est un indicateur assez fiable de la grippe
40 grippe :- fievre.

% Règle 2 : Une simple toux est un indicateur beaucoup plus faible
70 grippe :- toux.

% --- Conséquence du diagnostic ---
% Le besoin d'un traitement dépend de la certitude du diagnostic de grippe
90 traitement :- grippe.