% ==================================================
% CONFIGURATIONS DE POIDS (Préférences du Client)
% ==================================================
80 pref_viande.
30 pref_poisson.
90 pref_chocolat.
40 pref_fruits.
70 pref_vin.
50 pref_soda.
85 entrée_soupe.
60 entrée_salade.

% ==================================================
% STRUCTURE COMBINATOIRE (Génère 32 Answer Sets)
% ==================================================

% 1. Le choix de l'entrée (2 possibilités)
100 option_soupe :- entrée_soupe, not option_salade.
100 option_salade :- entrée_salade, not option_soupe.

% 2. Le choix du plat principal (2 possibilités)
100 option_viande :- pref_viande, not option_poisson.
100 option_poisson :- pref_poisson, not option_viande.

% 3. Le choix du dessert (2 possibilités)
100 option_chocolat :- pref_chocolat, not option_fruits.
100 option_fruits :- pref_fruits, not option_chocolat.

% 4. Le choix de la boisson (2 possibilités)
100 option_vin :- pref_vin, not option_soda.
100 option_soda :- pref_soda, not option_vin.

% 5. Le choix du café ou de l'infusion (2 possibilités libres sans prérequis)
100 option_cafe :- not option_infusion.
100 option_infusion :- not option_cafe.

% ==================================================
% PROPAGATION DES CONSÉQUENCES POSSIBILISTES
% ==================================================
% Un menu est considéré comme "Menu Prestige" si on combine Viande, Chocolat et Vin
80 menu_prestige :- option_viande, option_chocolat, option_vin.

% Un menu est considéré comme "Menu Light" si on combine Salade, Poisson et Fruits
90 menu_light :- option_salade, option_poisson, option_fruits.