
80 besoin_rapidite.
30 budget_confortable.
70 expertise_interne.
90 securite_critique.

% ==================================================
% STRATÉGIE DE DÉVELOPPEMENT (Exclusion mutuelle)
% ==================================================
% On choisit l'externalisation si on a besoin de rapidité ou d'un budget confortable,
% et qu'on ne fait pas le choix interne.
90 option_externaliser :- besoin_rapidite, not option_interne.
60 option_externaliser :- budget_confortable, not option_interne.

% On choisit le développement en interne si l'expertise existe ou si la sécurité est critique,
% et qu'on n'externalise pas.
80 option_interne :- expertise_interne, not option_externaliser.
100 option_interne :- securite_critique, not option_externaliser.

% ==================================================
% CONSÉQUENCES ET RISQUES ASSOCIÉS
% ==================================================
% Si on externalise :
85 livraison_rapide :- option_externaliser, besoin_rapidite.
70 risque_dependance_prestataire :- option_externaliser.

% Si on développe en interne :
95 maitrise_code :- option_interne, securite_critique.
50 surcharge_equipe :- option_interne.