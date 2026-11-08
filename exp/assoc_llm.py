import argparse, json, random

parser = argparse.ArgumentParser()
parser.add_argument("--repetitions", type=int, default=1_000_000)
parser.add_argument("--seed", type=int, default=123456789)
parser.add_argument("--low", type=float, default=-1_000_000.0)
parser.add_argument("--high", type=float, default=1_000_000.0)
args = parser.parse_args()

random.seed(args.seed)
count = 0
for i in range(args.repetitions):
    x = random.uniform(args.low, args.high)
    y = random.uniform(args.low, args.high)
    z = random.uniform(args.low, args.high)
    a = (x + y) + z
    b = x + (y + z)
    if a == b:
        count += 1

print(json.dumps({"repetitions": args.repetitions, "seed": args.seed,
                  "low": args.low, "high": args.high,
                  "percentage": 100 * count / args.repetitions}))
