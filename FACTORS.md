# Facteurs de variabilité : matrice de comparaison

## Matrice des trois programmes

| Programme | Langage / environnement | Type | Distribution | Tirages | Générateur (graine) | Comparaison | Résultat |
|---|---|---|---|---|---|---|---|
| Le mien (TP1) | Python (3.14 sous Docker, 3.11 sous Nix) | float (double) | uniforme [0,1) via `random()` | 10 000 | Mersenne Twister, `Random(42)` | `==` | 83,01 % |
| LLM en C (TP2) | C, gcc:15 sous Docker | double | uniforme [-1e6, 1e6], à partir de 53 bits aléatoires | 1 000 000 | xorshift64 (123456789) | `==` | 93,06 % (930600 sur 10^6) |
| LLM en Python (TP3, nouveau) | Python 3, machine locale | float (double) | uniforme [-1e6, 1e6] via `random.uniform` | 1 000 000 | Mersenne Twister (123456789) | `==` | 93,06 % (930606 sur 10^6) |

## Liste des facteurs et valeurs possibles

| Facteur | Valeurs possibles |
|---|---|
| Propriété testée | associativité de +, associativité de *, distributivité, x * (1/x) == 1 |
| Type des nombres | float32, float64 (double), long double |
| Distribution et plage des valeurs | [0,1), [-1,1], [-1e6, 1e6], loi normale, échelles très différentes |
| Façon de fabriquer le nombre aléatoire | `random()`, `uniform(a, b)`, bits aléatoires * (b - a) + a |
| Nombre de tirages | de 100 à 10 000 000 |
| Générateur pseudo-aléatoire | Mersenne Twister, xorshift64, autre |
| Graine | 42, 123456789, aucune (graine aléatoire) |
| Comparaison | `==`, égalité à une tolérance près, comparaison bit à bit |
| Langage et version de l'interpréteur ou du compilateur | Python 3.11 / 3.14, gcc 13 / 15, autre langage |
| Options de compilation | `-O0`, `-O2`, `-O3`, `-ffast-math`, `-march=native` (FMA) |
| Précision des calculs intermédiaires | SSE (64 bits), x87 (80 bits) |
| Architecture et système | x86-64, ARM, Linux, Docker, Nix |
| Format de la sortie | 2 ou 4 décimales, pourcentage ou nombre d'égalités |
| Nombre d'exécutions par configuration | 1 à plusieurs, pour mesurer la variabilité statistique |

## Ce que le troisième programme apprend

Le LLM en Python reprend les mêmes choix que le LLM en C (même plage, même nombre de tirages, même valeur de graine) mais avec un autre langage et un autre générateur. Le résultat est quasi identique (930606 contre 930600 égalités sur 10^6). Le langage et le générateur ont donc très peu d'effet ici, l'écart est du bruit statistique (de l'ordre de 0,03 point à 10^6 tirages).

À l'inverse, mon Python et le LLM en Python utilisent le même langage et le même type, mais donnent 83,01 % contre 93,06 %. Ce qui change entre les deux, c'est la distribution (plage des valeurs) et le nombre de tirages. La distribution est donc le facteur qui semble dominer, ce qu'aucune comparaison à deux programmes seulement ne permettait de dire.

## Pistes à tester

- Effet des options de compilation, notamment `-ffast-math`, sur le programme C.
- Effet du type float32 contre float64.
- Effet de la plage des valeurs, à N et générateur fixés.
- Effet de la propriété testée (branche `distributivity`).

La liste n'est jamais terminée : elle sera mise à jour à chaque nouveau facteur découvert.

## Résultats expérimentaux

### 3.1 Paramètres d'exécution : nombre de tirages (`exp/runtime_params.py`)

Programme du TP1 (valeurs dans [0,1), graine 42), nombre de tirages variable dans une seule exécution :

| Tirages | Pourcentage |
|---|---|
| 100 | 80.0000 % |
| 1 000 | 82.0000 % |
| 10 000 | 83.0100 % |
| 100 000 | 82.7590 % |
| 1 000 000 | 82.8487 % |

Le nombre de tirages ne change pas la valeur moyenne mais la précision : l'incertitude statistique vaut environ sqrt(p(1-p)/N), soit ±3,8 points à 100 tirages et ±0,04 point à 10^6. Le résultat se stabilise autour de 82,8 %. Le 83,01 % du TP1 (10 000 tirages) est donc dans le bruit.
