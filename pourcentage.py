import os, random

rng = random.Random(42)
N = 10_000
eq = 0
for _ in range(N):
    x, y, z = rng.random(), rng.random(), rng.random()
    if x * (y + z) == x * y + x * z:
        eq += 1

out = os.path.join(os.environ.get("OUT_DIR", "."), "answer_distributivity.txt")
with open(out, "w") as f:
    f.write(f"{100 * eq / N:.4f}%\n")