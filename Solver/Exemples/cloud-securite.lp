% --- Contraintes et Contexte Client ---
90 besoin_haute_dispo.
80 budget_tres_serre.
95 donnees_sensibles.

% --- Choix d'Architecture (Exclusion mutuelle / Conflit) ---
% Modèle Multi-Régions : idéal pour la disponibilité, mais impossible si le budget est la priorité absolue
100 deploiement_multi_region :- besoin_haute_dispo, not option_low_cost.

% Option Low-Cost : une seule instance, choisie si le budget presse et qu'on sacrifie le multi-régions
100 option_low_cost :- budget_tres_serre, not deploiement_multi_region.

% --- Conséquences du Choix Multi-Régions ---
% Le multi-régions implique une réplication active des bases de données
90 replication_active :- deploiement_multi_region.

% Si les données sont sensibles et qu'on réplique, le chiffrement inter-régions est obligatoire
100 chiffrement_flux :- replication_active, donnees_sensibles.

% --- Conséquences de l'Option Low-Cost ---
% En mode low-cost, on met en place des sauvegardes simples la nuit
70 sauvegarde_nocturne :- option_low_cost.

% Risque de perte de données en cas de crash (puisqu'on n'est pas en multi-régions)
60 risque_perte_donnees :- option_low_cost.