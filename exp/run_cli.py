import csv, itertools, json, subprocess, sys

subprocess.run(["gcc", "-O2", "-o", "exp/assoc_llm_c", "exp/assoc_llm.c"], check=True)

programs = {
    "mine_python": [sys.executable, "exp/assoc_mine.py"],
    "llm_python": [sys.executable, "exp/assoc_llm.py"],
    "llm_c": ["./exp/assoc_llm_c"],
}
repetitions = [100, 1_000, 10_000, 100_000]
ranges = [(0.0, 1.0), (-1_000_000.0, 1_000_000.0)]
seeds = [1, 2, 3]

rows = []
for (name, cmd), r, (low, high), seed in itertools.product(
        programs.items(), repetitions, ranges, seeds):
    out = subprocess.run(
        cmd + [f"--repetitions={r}", f"--seed={seed}", f"--low={low}", f"--high={high}"],
        capture_output=True, text=True, check=True).stdout
    answer = json.loads(out)
    answer["low"] = float(answer["low"])
    answer["high"] = float(answer["high"])
    answer["program"] = name
    rows.append(answer)

fields = ["program", "repetitions", "seed", "low", "high", "percentage"]
with open("results_cli.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
print(f"{len(rows)} runs written to results_cli.csv")
