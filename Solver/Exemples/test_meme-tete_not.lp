% --- Observations / Symptômes ---
80 fievre.
80 toux.

% --- Règles de Diagnostic avec "not" (mêmes têtes sur deux lignes) ---
% Règle 1 : On ne peut pas exclure la grippe (not pas_grippe_fievre) si on a la fièvre
40 grippe :- fievre, not pas_grippe_fievre.

% Règle 2 : On ne peut pas exclure la grippe (not pas_grippe_toux) si on a la toux
70 grippe :- toux, not pas_grippe_toux.

% --- Conséquence du diagnostic ---
90 traitement :- grippe.