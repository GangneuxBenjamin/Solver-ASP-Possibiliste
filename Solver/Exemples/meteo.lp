% --- Alertes Météo et Capteurs ---
95 alerte_tempete.
60 baisse_tension.
40 anomalie_frequence.

% --- Diagnostic de la gravité ---
% La tempête fait craindre des chutes d'arbres sur les lignes
85 risque_coupure_ligne :- alerte_tempete.

% Si on cumule risque de coupure et baisse de tension, le réseau est jugé instable
75 reseau_instable :- risque_coupure_ligne, baisse_tension.

% Une anomalie de fréquence seule est suspecte, mais combinée à l'instabilité, c'est critique
90 situation_critique :- reseau_instable, anomalie_frequence.

% --- Décisions automatiques (Actions) ---
% Si la situation est critique, on déclenche le délestage automatique
100 declencher_delestage :- situation_critique.

% Si le délestage est lancé, on isole les sous-stations par sécurité
50 isoler_sous_station :- declencher_delestage.

% --- Notification ---
% L'alerte de maintenance dépend de la criticité globale
80 alerte_maintenance :- situation_critique.