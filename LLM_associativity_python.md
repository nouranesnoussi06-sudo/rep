# LLM : problème d'associativité, version Python (TP3)

- Modèle : GPT-6 (le même que dans LLM_associativity.md, à vérifier avec l'interface)
- Interface : ChatGPT
- Date : 7 novembre 2026

## Prompt

"donne moi le programme de l'associativité en Python"

(envoyé dans la même conversation que celle du TP2, où l'énoncé complet du problème avait déjà été donné)

## Réponse complète du LLM

Voici le programme en Python pour l'exercice sur l'associativité, avec les choix explicités dans l'énoncé.

### Programme Python

```python
import random

# Choix des paramètres
N = 1_000_000
random.seed(123456789)

count = 0

for i in range(N):
    # Générer trois nombres aléatoires
    x = random.uniform(-1_000_000, 1_000_000)
    y = random.uniform(-1_000_000, 1_000_000)
    z = random.uniform(-1_000_000, 1_000_000)

    # Calculer les deux expressions
    a = (x + y) + z
    b = x + (y + z)

    # Comparer les résultats
    if a == b:
        count += 1

# Calculer le pourcentage
percentage = (count / N) * 100

print("Nombre de tests :", N)
print("Résultats égaux :", count)
print("Pourcentage :", percentage, "%")
```

### Explication des choix

| Élément | Choix |
|---|---|
| Langage | Python |
| Type des nombres | float (double précision) |
| Nombre de tests | 1 000 000 |
| Valeurs de x, y, z | Entre -1 000 000 et 1 000 000 |
| Génération | Aléatoire |
| Comparaison | Égalité exacte (==) |
| Graine aléatoire | 123456789 |

### Pourquoi utilise-t-on random.seed() ?

Cela permet de rendre l'expérience reproductible. Sans random.seed(), les nombres générés changent à chaque exécution. Avec random.seed(123456789), on génère la même séquence de nombres à chaque exécution, donc on retrouve le même pourcentage.

### Comment exécuter le programme ?

Dans un terminal :

    python3 associativite.py

Remarque : on utilise volontairement == et non une comparaison avec une tolérance (math.isclose), car on cherche à savoir si les deux résultats sont exactement égaux, comme demandé dans l'énoncé.

## Mes commentaires

- Le code est correct : il s'exécute sans modification et donne toujours le même résultat grâce à la graine fixe, 930606 égalités sur 1 000 000, soit 93,06 %.
- Contrairement à une simple réponse de code, le LLM explicite ses choix (langage, type, nombre de tests, plage des valeurs, comparaison, graine) et justifie la graine et l'usage de `==`, ce que demande l'énoncé.
- Il ne donne aucun résultat chiffré attendu : il faut exécuter le programme pour connaître le pourcentage.
- Il ne justifie pas la plage [-10^6, 10^6] ni le nombre de tirages, alors que ce sont des facteurs qui changent beaucoup la réponse : mon programme (valeurs dans [0,1), 10 000 tirages) donne 83,01 %, contre 93,06 % ici.
- Il utilise `random.uniform(a, b)`, qui calcule `a + (b - a) * random()`, alors que ma version utilise `random()` directement. La façon de fabriquer le nombre aléatoire est un facteur de plus.
- Le résultat est quasi identique à celui du LLM en C du TP2 (93,06 % dans les deux cas, 930606 contre 930600 égalités) malgré un autre langage et un autre générateur.
