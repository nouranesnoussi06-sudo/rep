# Facteurs de variabilité : matrice de comparaison

| Programme | Langage | Type | Distribution | Nb de tirages | Générateur / graine | Comparaison | Résultat |
|---|---|---|---|---|---|---|---|
| Le mien (TP1) | Python 3.14 (Docker) | float (double) | uniforme [0,1) | 10 000 | Mersenne Twister, graine 42 | == | 83.01 % |
| LLM en C (TP2) | C, gcc:15 | double | uniforme [-1e6, 1e6] | 1 000 000 | xorshift64, graine 123456789 | == | 93.06 % |
| LLM en Python (nouveau) | | | | | | | |

## Autres facteurs à considérer

- type de nombre : float32, float64, long double
- distribution et plage : [0,1), [-1e6,1e6], loi normale, échelles différentes
- nombre de tirages et graine
- générateur pseudo-aléatoire et façon de fabriquer un flottant à partir de bits aléatoires
- opérateur de comparaison (== ou tolérance)
- propriété testée (associativité de + ou de *, distributivité...)
- compilateur et options (-O0, -O2, -ffast-math), FMA
- version de l'interpréteur ou du compilateur
- architecture du processeur (x86, ARM) et OS
- mode d'arrondi, précision des calculs intermédiaires
- formatage de la sortie (nombre de décimales)
