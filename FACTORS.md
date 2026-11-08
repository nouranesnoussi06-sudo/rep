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

Le nombre de tirages ne change pas la valeur moyenne mais la précision. Le résultat se stabilise autour de 82,8 %. Le 83,01 % du TP1 (10 000 tirages) est donc dans le bruit.

### 3.2 CLI : mêmes arguments pour les trois programmes (`exp/run_cli.py`)

Arguments communs : `--repetitions`, `--seed`, `--low`, `--high`. Le script lance les 3 programmes sur 4 nombres de tirages x 2 plages de valeurs x 3 graines (72 exécutions) et écrit un CSV. Moyenne sur les 3 graines à 100 000 tirages :

| Plage | Mon Python | LLM Python | LLM C |
|---|---|---|---|
| [0, 1) | 82.76 % | 82.76 % | 82.91 % |
| [-1e6, 1e6] | 93.05 % | 93.05 % | 92.97 % |

- Mon Python et le LLM Python donnent exactement le même résultat avec les mêmes arguments (24 configurations sur 24) : leurs écarts initiaux (83 % contre 93 %) venaient de leurs valeurs par défaut, pas de la logique du code.
- Le C n'est identique que dans 1 configuration sur 24 : il utilise un autre générateur (xorshift64 contre Mersenne Twister), donc une autre suite de nombres. Les moyennes restent très proches : l'écart est du bruit statistique.
- La plage des valeurs est le facteur dominant (environ 83 % contre environ 93 %).

### 3.3 Template : propriété testée et type des nombres (`exp/assoc.py.jinja`, `exp/generate.py`)

100 000 tirages, graine 42, valeurs dans [0, 1) :

| Propriété | float64 | float32 |
|---|---|---|
| (x+y)+z == x+(y+z) | 82.759 % | 74.616 % |
| (x*y)*z == x*(y*z) | 65.131 % | 64.990 % |
| x*(y+z) == x*y+x*z | 68.728 % | 64.782 % |

- Le type des nombres a un fort effet sur l'associativité de l'addition (environ 8 points de moins en 32 bits), et un effet plus faible sur les deux autres propriétés.
- La propriété testée change fortement la réponse (de 65 % à 83 % en 64 bits).

### 3.4 Environnement de calcul (`exp/Dockerfile.python`, `exp/Dockerfile.c`)

Python : `exp/assoc_mine.py`, 100 000 tirages, graine 42, dans des images python:3.10, 3.12 et 3.14. Le résultat est identique dans les trois versions.

C : `exp/assoc_llm.c`, 1 000 000 tirages, graine 42, valeurs dans [-1e6, 1e6], images gcc:12 et gcc:15.

| Options | gcc 12 | gcc 15 |
|---|---|---|
| -O2 | 93.0794 % | 93.0794 % |
| -O2 -march=native | 67.3535 % | 67.3535 % |
| -O2 -ffast-math | 100.0000 % | 100.0000 % |

- La version du compilateur n'a aucun effet ici, les options de compilation oui.
- `-ffast-math` autorise le compilateur à réassocier les additions : les deux membres de l'égalité deviennent le même calcul, d'où 100 %. La propriété n'est plus testée.
- `-march=native` active l'FMA. La génération `r * (high - low) + low` est alors faite avec un seul arrondi, ce qui donne des valeurs plus précises et moins souvent exactes à l'addition. Vérification en Python avec 100 000 tirages : 92,98 % avec deux arrondis, 67,22 % avec un seul (FMA émulé). Une partie des 93 % observés sur [-1e6, 1e6] dépend donc de la façon de fabriquer les nombres, pas seulement de la plage.
- Test causal à faire : `-O2 -march=native -ffp-contract=off` doit redonner 93,08 %.

Nouveaux facteurs : contraction FMA (`-ffp-contract`), `-ffast-math`.
