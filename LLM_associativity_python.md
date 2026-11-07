# LLM : problème d'associativité, version Python (TP3)

- Modèle : GPT-6 (le même que dans LLM_associativity.md)
- Interface : ChatGPT
- Date : 7 novembre 2026

## Prompt

Énoncé du problème d'associativité (le même qu'au TP2), puis : "How often (x+y)+z == x+(y+z)? Write a program that prints a percentage. The question is deliberately under-specified ("x, y, z: number"), so you will have to make choices. Make them, and write each one down: they are part of your result." Demande de générer le programme en Python.

## Réponse complète du LLM

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

## Mes commentaires

- Le code est correct, il s'exécute sans modification et donne toujours le même résultat grâce à la graine fixe : 930606 égalités sur 1 000 000, soit 93,06 %.
- La réponse est uniquement du code. Les choix (type, distribution, nombre de tirages, graine, comparaison) ne sont pas écrits explicitement alors que l'énoncé demande de les noter.
- Les choix sont les mêmes que dans la version C du TP2 : N = 10^6, graine 123456789, valeurs dans [-10^6, 10^6]. La différence avec ma version (83,01 %) vient surtout de la plage des valeurs et du nombre de tirages.
- `random.uniform(a, b)` calcule `a + (b - a) * random()`, ce qui est une autre façon de fabriquer le nombre que le `random()` utilisé dans ma version. C'est un facteur de plus à noter.
- Le résultat est quasi identique à celui du LLM en C (93,06 % dans les deux cas), alors que le langage et le générateur sont différents.
