import argparse, csv, json, platform, subprocess, sys
from pathlib import Path
from jinja2 import Template

PROPERTIES = {
    "AssocAdd": ("(x + y) + z", "x + (y + z)"),
    "AssocMul": ("(x * y) * z", "x * (y * z)"),
    "Distributivity": ("x * (y + z)", "x * y + x * z"),
}
DTYPES = {"Float32": "np.float32", "Float64": "np.float64"}
RANGES = {"Unit": (0.0, 1.0), "Wide": (-1_000_000.0, 1_000_000.0)}
REPETITIONS = {"R10000": 10_000, "R1000000": 1_000_000}
SEEDS = {"Seed42": 42, "Seed123456789": 123456789}
FLAGS = {"O0": "-O0", "O2": "-O2", "O2MarchNative": "-O2 -march=native",
         "O2FastMath": "-O2 -ffast-math"}


def gcc_major():
    try:
        out = subprocess.run(["gcc", "-dumpversion"], capture_output=True, text=True).stdout
        return out.strip().split(".")[0]
    except FileNotFoundError:
        return "none"


def cpu_name():
    try:
        for line in open("/proc/cpuinfo"):
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or platform.machine()


def derive(row, workdir):
    """Write (and compile if C) the variant of a configuration; return the command prefix."""
    lhs, rhs = PROPERTIES[row["Property"]]
    if row["Language"] == "Python":
        template = Template(Path("exp/variant.py.jinja").read_text())
        path = workdir / f"{row['config_id']}.py"
        path.write_text(template.render(lhs=lhs, rhs=rhs, dtype=DTYPES[row["NumberType"]]))
        return [sys.executable, str(path)]
    template = Template(Path("exp/variant.c.jinja").read_text())
    source = workdir / f"{row['config_id']}.c"
    source.write_text(template.render(lhs=lhs, rhs=rhs))
    binary = workdir / row["config_id"]
    subprocess.run(["gcc", *FLAGS[row["Flags"]].split(), "-o", str(binary), str(source)],
                   check=True)
    return [str(binary)]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sample", default="configs/sample.csv")
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("-o", "--output", default="results/results.csv")
    p.add_argument("--match-env", action="store_true",
                   help="only run the configurations whose Python/gcc version is the current one")
    args = p.parse_args()

    python_now = f"{sys.version_info.major}.{sys.version_info.minor}"
    gcc_now = gcc_major()
    workdir = Path("generated")
    workdir.mkdir(exist_ok=True)

    rows = []
    for config in csv.DictReader(open(args.sample)):
        if config["Language"] == "Python":
            env_matches = config["PythonVersion"] == "Py" + python_now.replace(".", "")
        else:
            env_matches = config["GccVersion"] == "Gcc" + gcc_now
        if args.match_env and not env_matches:
            continue
        command = derive(config, workdir)
        low, high = RANGES[config["Distribution"]]
        for run in range(args.repeats):
            seed_used = SEEDS[config["Seed"]] + run
            arguments = [f"--repetitions={REPETITIONS[config['Repetitions']]}",
                         f"--seed={seed_used}", f"--low={low}", f"--high={high}"]
            out = subprocess.run(command + arguments, capture_output=True, text=True,
                                 check=True).stdout
            rows.append({
                **config, "run": run, "seed_used": seed_used,
                "repetitions_n": REPETITIONS[config["Repetitions"]],
                "low": low, "high": high,
                "percentage": json.loads(out)["percentage"],
                "python_actual": python_now, "gcc_actual": gcc_now,
                "env_matches": env_matches, "machine": platform.machine(),
                "platform": platform.platform(), "cpu": cpu_name(),
                "command": " ".join(command + arguments),
            })

    if not rows:
        print("no configuration matches this environment, nothing written")
        return

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} runs written to {out}")


if __name__ == "__main__":
    main()
