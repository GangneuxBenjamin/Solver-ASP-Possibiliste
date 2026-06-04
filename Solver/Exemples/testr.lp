100 c(1).
100 c(2).

50 a(X) :- c(X), not b(X).
70 b(X) :- c(X), not a(X).