# TP2 reproductibilité : associativité et banque

## Réponses attendues

- `answer_associativity.txt` : `83.0100%`
- `answer_banking.txt` : `0.019992165836667903219891152066`
- `answer_associativity_llm.txt` : `Percentage: 93.06%` (930600 égalités sur 1 000 000 tests)
- `answer_banking_llm.txt` : montant final d'environ -4.397e48 euros (résultat faux, voir plus bas)

Le "même résultat" veut dire que le contenu du fichier est strictement identique. Les deux programmes Python sont déterministes (graine fixée pour l'associativité, calcul en précision décimale pour la banque), donc on n'accepte aucune tolérance.

## Choix faits

Associativité (Python) : x, y, z tirés uniformément dans [0, 1], type float (double IEEE 754), 10 000 tirages, `random.Random(42)`, comparaison exacte avec `==`. Avec seulement 10 000 tirages, l'incertitude statistique est d'environ 0,4 point : un autre tirage donnerait un résultat proche mais pas identique.

Banque (Python) : on prend la vraie valeur de e avec le module `decimal` (120 chiffres), puis pour chaque année k de 1 à 50 on enlève 1 euro et on multiplie par k, et on enlève 1 euro à la fin. La valeur exacte est d'environ 0,02 euro.

## Reproduire avec Docker

    docker build -t rep .
    docker run --rm -v "$(pwd)":/out --user "$(id -u):$(id -g)" rep

Les deux fichiers `answer_*.txt` apparaissent dans le dossier courant. Pour la version C (partie LLM) :

    docker build -f Dockerfile.llm -t rep-llm .
    docker run --rm -v "$(pwd)":/out --user "$(id -u):$(id -g)" rep-llm

## Reproduire avec Nix

    nix-shell --run ./run.sh

L'environnement est défini dans `shell.nix`, avec une version de nixpkgs fixée dans `nixpkgs-pin.nix`. Python y est en version 3.11, alors que l'image Docker utilise 3.14 : on obtient quand même les mêmes résultats.

## Sans Docker ni Nix

Il faut Python 3 (testé avec 3.14), sans bibliothèque externe :

    OUT_DIR=. ./run.sh

## GitHub Actions

À chaque push, le workflow `.github/workflows/reproduce.yml` construit les deux images Docker, lance les conteneurs et commit les fichiers `answer_*.txt` s'ils ont changé. Les fichiers de réponses du dépôt sont donc produits par GitHub Actions.

## Partie LLM

Les prompts, le modèle utilisé et les réponses complètes sont dans `LLM_associativity.md` et `LLM_banking.md`.

Comparaison avec mes programmes :

- Banque : mon Python donne 0,019992165836667903..., qui est la bonne valeur. Le C du LLM donne environ -4,4e48. Il calcule en double : l'erreur d'arrondi sur e (environ 1e-16) est multipliée par n à chaque année, donc au total par 50! (environ 3e64). Le montant reste correct jusqu'à l'année 16 puis diverge. Le LLM ne remarque pas que son résultat est absurde.
- Associativité : 83,01 % pour mon Python contre 93,06 % pour le C du LLM. La différence vient des choix (le LLM tire ses valeurs dans [-1 000 000, 1 000 000], moi dans [0, 1], et le nombre de tests n'est pas le même), pas d'une erreur de code. Le pourcentage dépend beaucoup de la distribution choisie.


## Architecture du dépôt

| Chemin | Contenu |
|---|---|
| `pourcentage.py`, `banque_co.py`, `run.sh` | programmes du TP1 (Python) et script qui lance les deux |
| `Dockerfile`, `Dockerfile.llm`, `llm/` | images Docker et programmes C/Python générés par le LLM (TP2) |
| `shell.nix`, `nixpkgs-pin.nix` | environnement Nix avec nixpkgs figé |
| `LLM_*.md` | prompts, modèle et réponses complètes des LLM, avec mes commentaires |
| `FACTORS.md` | facteurs de variabilité, matrice de comparaison des trois programmes, expériences 3.1 à 3.5, échantillonnage |
| `exp/` | expériences du TP3 : versions en ligne de commande, templates Jinja, Dockerfiles par version, `run_sample.py` |
| `fm/experiment.uvl` | modèle de variabilité (288 configurations) |
| `sample.py`, `configs/` | échantillonnage reproductible et ses sorties (`configs/sample.csv`) |
| `results/results.csv` | résultats des 630 exécutions, produits par GitHub Actions |
| `results/causal.csv` | test causal sur la contraction FMA, produit par GitHub Actions |
| `analysis.ipynb` | analyse des résultats (arbre de décision, recommandations) |
| `.github/workflows/` | `reproduce.yml` (TP2), `experiment.yml` (résultats du TP3), `causal.yml` (test causal) |

## TP3 : variabilité

Les trois programmes comparés sont le mien (Python, TP1), le LLM en C (TP2) et le LLM en Python (TP3). Les facteurs de variabilité (propriété testée, type des nombres, plage des valeurs, nombre de tirages, graine, langage, générateur, versions, options de compilation, architecture) sont décrits dans `FACTORS.md` et modélisés dans `fm/experiment.uvl`.

### Reproduire

Échantillon de configurations (Python 3.11 ou plus, `pip install flamapy==2.6.0`) :

    python sample.py fm/experiment.uvl --size 60 --seed 1 --include configs/*.csvconf -o configs/sample.csv

Exécution locale de l'échantillon (`pip install jinja2 numpy`, gcc installé) :

    python exp/run_sample.py --repeats 5 -o results/results.csv

En local, la colonne `env_matches` indique si les versions de Python et de gcc demandées par la configuration sont celles de la machine. Les résultats du dépôt sont produits par GitHub Actions : le workflow `experiment` (push ou "Run workflow") échantillonne, dérive et lance les variantes sur 2 architectures (x86, ARM), Python 3.10 et 3.14, gcc 12 et 15, puis écrit `results/results.csv` (630 lignes). Le workflow `causal` (lancement manuel) produit `results/causal.csv`.

Relancé sur le même commit, `experiment` donne les mêmes pourcentages. Les colonnes `cpu` et `platform` peuvent changer, car GitHub n'attribue pas toujours la même machine.

Notebook : `pip install jupyterlab pandas matplotlib scikit-learn`, ouvrir `anal.ipynb`, "Restart Kernel and Run All Cells".

### Résultats principaux

- `-ffast-math` donne toujours 100 % : le compilateur réorganise les additions et la propriété n'est plus testée.
- La contraction FMA change la réponse : le programme C sur plage large donne 93,08 % sans fusion et 67,35 % avec (ARM en `-O2`, x86 avec `-march=native`). Compiler avec `-ffp-contract=off` redonne 93,08 % sur les deux architectures.
- Le nombre de tirages ne change que la précision : écart-type de 0,38 point entre lancements à 10 000 tirages, 0,04 à 1 000 000.
- Les versions de Python (3.10, 3.14) et de gcc (12, 15) n'ont pas d'effet observé.
- L'écart entre 83 % (TP1) et 93 % (TP2) vient surtout de la plage des valeurs et de la façon de fabriquer les nombres aléatoires, pas du langage ni du générateur.

Détails, recommandations et limites : `analysis.ipynb`.

## Usage de l'IA

- ChatGPT (GPT-6, interface ChatGPT, novembre 2026) : génération des programmes en C (associativité et banque, TP2) et du programme Python d'associativité (TP3). Prompts, réponses et commentaires dans `LLM_*.md`. J'ai exécuté chaque programme, comparé ses résultats aux miens et relevé ses erreurs, notamment le résultat absurde du calcul de la banque en `double`.
- Claude (Claude Sonnet 5.5, claude.ai, novembre 2026) : aide pour le TP2 et le TP3.