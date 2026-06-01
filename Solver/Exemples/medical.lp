% --- Faits initiaux (Certitude des maladies) ---
90 maladie1.
70 maladie2.

% --- Protocole 1 ---
% On prescrit medoc1 si maladie1 est présente et que medoc2 n'est pas pris
100 medoc1 :- maladie1, not medoc2.
% La guérison 1 dépend du médicament et de la maladie
70 guerison1 :- medoc1, maladie1.

% --- Protocole 2 ---
% On prescrit medoc2 si maladie2 est présente et que medoc1 n'est pas pris
100 medoc2 :- maladie2, not medoc1.
% La guérison 2 est moins certaine
30 guerison2 :- medoc2, maladie2.