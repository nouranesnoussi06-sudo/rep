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