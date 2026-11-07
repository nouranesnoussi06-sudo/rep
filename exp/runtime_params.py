import random

def percentage(repetitions, seed=42):
    rng = random.Random(seed)
    eq = 0
    for _ in range(repetitions):
        x, y, z = rng.random(), rng.random(), rng.random()
        if (x + y) + z == x + (y + z):
            eq += 1
    return 100 * eq / repetitions

for n in [100, 1_000, 10_000, 100_000, 1_000_000]:
    print(n, f"{percentage(n):.4f}%")
