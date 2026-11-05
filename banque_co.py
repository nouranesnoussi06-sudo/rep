import os
from decimal import Decimal, getcontext

getcontext().prec = 120
e = Decimal(1).exp()
u = e
for k in range(1, 51):
    u = k * (u - 1)
result = u - 1

out = os.path.join(os.environ.get("OUT_DIR", "."), "answer_banking.txt")
with open(out, "w") as f:
    f.write(f"{result:.30f}\n")