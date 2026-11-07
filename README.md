# TP2 reproductibilité : associativité et banque

## Réponses attendues

- `answer_associativity.txt` : `83.0100%`
- `answer_banking.txt` : `0.019992165836667903219891152066`
- `answer_associativity_llm.txt` : `Percentage: 93.06%` (930600 égalités sur 1 000 000 tests)
- `answer_banking_llm.txt` : montant final d'environ -4.397e48 euros (résultat faux, voir plus bas)

Le "même résultat" veut dire que le contenu du fichier est strictement identique. Les deux programmes Python sont déterministes (graine fixée pour l'associativité, calcul en précision décimale pour la banque), donc on n'accepte aucune tolérance.

## Choix faits

Associativité (Python) : x, y, z tirés uniformément dans [0, 1), type float (double IEEE 754), 10 000 tirages, `random.Random(42)`, comparaison exacte avec `==`. Avec seulement 10 000 tirages, l'incertitude statistique est d'environ 0,4 point : un autre tirage donnerait un résultat proche mais pas identique.

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
- Associativité : 83,01 % pour mon Python contre 93,06 % pour le C du LLM. La différence vient des choix (le LLM tire ses valeurs dans [-1 000 000, 1 000 000], moi dans [0, 1), et le nombre de tests n'est pas le même), pas d'une erreur de code. Le pourcentage dépend beaucoup de la distribution choisie.
