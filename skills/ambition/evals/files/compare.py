"""Paired A/B wall-clock comparison of two commands (eval fixture).

Runs the two commands alternately so drift in machine load hits both sides
equally, then reports the median ratio. Variable names are deliberately
unclear: eval 4 asks for them to be renamed.
"""

import statistics
import subprocess
import sys
import time


def run(c):
    t0 = time.perf_counter()
    subprocess.run(c, shell=True, check=True, capture_output=True)
    return time.perf_counter() - t0


def cmp(a, b, n=10):
    xs, ys = [], []
    for i in range(n):
        # Alternate the order each round so neither side always runs first.
        if i % 2 == 0:
            xs.append(run(a))
            ys.append(run(b))
        else:
            ys.append(run(b))
            xs.append(run(a))
    r = [y / x for x, y in zip(xs, ys)]
    return statistics.median(xs), statistics.median(ys), statistics.median(r)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: compare.py '<command A>' '<command B>' [rounds]")
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    m1, m2, q = cmp(sys.argv[1], sys.argv[2], k)
    print(f"A median {m1:.4f}s  B median {m2:.4f}s  median B/A {q:.3f}")
