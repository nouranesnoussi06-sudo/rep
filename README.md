# Reproducibility lab 2: associativity and banking

## Expected results

| File | Expected content |
|---|---|
| `answer_associativity.txt` | `83.0100%` |
| `answer_banking.txt` | `0.019992165836667903219891152066` |
| `answer_associativity_llm.txt` | `Percentage: 93.06%` (equal results: 930600 / 1000000) |
| `answer_banking_llm.txt` | final amount about -4.397e48 euros (wrong, see below) |

"Same result" means identical file content, byte for byte. Both Python programs are deterministic (fixed seed 42 for the associativity one, 120-digit Decimal arithmetic for the banking one), so no tolerance is needed.

## Choices

- **Associativity (Python):** x, y, z independent and uniform in [0, 1), type float (IEEE double), N = 10 000 draws, `random.Random(42)`, exact comparison with `==`. With N = 10 000 the statistical uncertainty is about +-0.4 points.
- **Banking (Python):** exact value of e with `decimal` at 120 digits, M_0 = e, M_k = k * (M_{k-1} - 1) for k = 1..50, then a final fee of 1 euro. The true value is about 0.02 euro (series sum_{k>=51} 50!/k!).
- **Associativity (C, LLM):** double, x, y, z uniform in [-1 000 000, 1 000 000], N = 1 000 000, xorshift64 with a fixed seed.
- **Banking (C, LLM):** double, starting from 2.718281828459045.

## Reproduce with Docker

    docker build -t rep .
    docker run --rm -v "$(pwd)":/out --user "$(id -u):$(id -g)" rep

LLM version (C):

    docker build -f Dockerfile.llm -t rep-llm .
    docker run --rm -v "$(pwd)":/out --user "$(id -u):$(id -g)" rep-llm

## Reproduce with Nix

    nix-shell --run ./run.sh

`shell.nix` uses a pinned nixpkgs snapshot (`nixpkgs-pin.nix`).

## GitHub Actions

On every push, `.github/workflows/reproduce.yml` builds both images, runs both containers and commits `answer_*.txt` (including the `_llm` files) if they changed. The answer files in this repository are produced by Actions.

## LLM part and comparison

The prompts, model details and full answers are in `LLM_associativity.md` and `LLM_banking.md`.

| | Banking | Associativity |
|---|---|---|
| Hand-written Python | 0.019992165836667903... (correct) | 83.01 % |
| C by the LLM | about -4.4e48 (wrong) | 93.06 % |

- **Banking:** the error on e (about 1e-16 in double) is multiplied by n at each year, so by 50! (about 3e64) at the end. The double computation is meaningless: the balance looks correct until year 16 and then diverges. The LLM did not notice that its result is absurd.
- **Associativity:** the two percentages differ because the choices differ (range of the values, number of tests), not because of a bug. The percentage depends strongly on the distribution.
