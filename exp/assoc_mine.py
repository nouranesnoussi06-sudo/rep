import argparse, json, random

parser = argparse.ArgumentParser()
parser.add_argument("--repetitions", type=int, default=10_000)
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--low", type=float, default=0.0)
parser.add_argument("--high", type=float, default=1.0)
args = parser.parse_args()

rng = random.Random(args.seed)
eq = 0
for _ in range(args.repetitions):
    x, y, z = (args.low + (args.high - args.low) * rng.random() for _ in range(3))
    if (x + y) + z == x + (y + z):
        eq += 1

print(json.dumps({"repetitions": args.repetitions, "seed": args.seed,
                  "low": args.low, "high": args.high,
                  "percentage": 100 * eq / args.repetitions}))
