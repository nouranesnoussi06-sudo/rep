import itertools, subprocess, sys
from pathlib import Path
from jinja2 import Template

template = Template(Path("exp/assoc.py.jinja").read_text())
properties = {
    "assoc_add": ("(x + y) + z", "x + (y + z)"),
    "assoc_mul": ("(x * y) * z", "x * (y * z)"),
    "distrib": ("x * (y + z)", "x * y + x * z"),
}
dtypes = {"float64": "np.float64", "float32": "np.float32"}

Path("generated").mkdir(exist_ok=True)
for (pname, (lhs, rhs)), (tname, dtype) in itertools.product(properties.items(), dtypes.items()):
    path = Path(f"generated/{pname}_{tname}.py")
    path.write_text(template.render(lhs=lhs, rhs=rhs, dtype=dtype,
                                    repetitions=100000, seed=42))
    result = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, check=True)
    print(f"{pname:10} {tname:8} {float(result.stdout):.3f}%")
