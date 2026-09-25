"""Verifica con sympy los resultados numéricos del cuaderno de prácticos resueltos."""
import math
from fractions import Fraction as Fr

import numpy as np
from sympy import (Abs, Interval, Rational, Union, exp, floor, integrate, limit, log, oo, pi,
                   simplify, sin, solve_univariate_inequality, sqrt, symbols, cos)

x = symbols("x", real=True)
R = []


def chk(name, cond):
    R.append((name, bool(cond)))


def area(f, a, b, n=400001):
    xs = np.linspace(a, b, n)
    ys = np.array([f(v) for v in xs])
    return float(np.sum((ys[1:] + ys[:-1]) / 2 * np.diff(xs)))


def ineq(e, expected):
    return solve_univariate_inequality(e, x, relational=False) == expected


# --- Capítulo 1
A, B, C = set(range(1, 7)), set(range(3, 9)), {7, 8, 9, 10}
chk("1.1.2 l", (A - B) | (B - A) == {1, 2, 7, 8})
chk("1.1.2 k", (A | B) & (B | C) == set(range(3, 9)))
chk("1.1.6", (15 * 7, 20 + 30 - 37, 20 + 30 - 15) == (105, 13, 35))
chk("1.2.3c", simplify(2 * sqrt(Rational(1, 64)) - Rational(1, 64) ** Rational(1, 3)) == 0)
chk("1.2.5c", simplify((2 * x + 1) ** 3 - (2 * x + 1) ** 2 - 4 - (8 * x**3 + 8 * x**2 + 2 * x - 4)) == 0)
chk("1.2.5d", simplify(2 * (3 * x**2 + 4) ** 2 + 1 - (18 * x**4 + 48 * x**2 + 33)) == 0)
onda = lambda t: -5 * math.floor(0.5 * math.cos(math.pi * math.floor(2 * t)))
chk("1.3.9 onda", [onda(k / 10) for k in range(10)] == [0] * 5 + [5] * 5)

# --- Capítulo 2
chk("2.1.2d", ineq((2 - x) / (1 + x) <= (1 + x) / (2 - x), Union(Interval.open(-oo, -1), Interval.Ropen(Rational(1, 2), 2))))
chk("2.1.2h", ineq(sqrt(x**2 + 1) > 2 * x - 3, Interval.open(-oo, 2 + 2 * sqrt(3) / 3)))
chk("2.1.2i", ineq(Abs(2 * x - 5) < Abs(3 * x + 4), Union(Interval.open(-oo, -9), Interval.open(Rational(1, 5), oo))))
chk("2.1.2k", ineq(3 * Abs(x) - Abs(x - 2) > 2, Union(Interval.open(-oo, -2), Interval.open(1, oo))))
chk("2.1.4 medias", 1 < Fr(8, 5) < 2 < Fr(5, 2) < math.sqrt(8.5) < 4)
chk("2.3.2c max 10", math.cos(10) < math.sin(10) and math.cos(8) < math.sin(8))

# --- Capítulo 3
dn = lambda v: abs(v - round(v))
chk("3.1.1 i", abs(area(lambda v: 3 * dn(v), 1, 3) - 1.5) < 1e-4)
chk("3.1.7 e", abs(area(lambda v: abs(3 * v - 1), -1, 2) - 41 / 6) < 1e-4)
chk("3.1.7 f", abs(area(lambda v: abs(dn(v) - 2 * v - math.floor(2 * v)), 0, 2) - 6.5) < 1e-3)
chk("3.1.8 d", abs(area(lambda v: math.floor(v * v), 2, 3) - float(16 - sqrt(5) - sqrt(6) - sqrt(7) - 2 * sqrt(2))) < 1e-3)
chk("3.1.8 j", sum(Fr(1, k * k) for k in range(2, 6)) == Fr(1669, 3600))
chk("3.3.5 b", integrate(x**2, (x, 0, 3)) == 9)
chk("3.3.3 cota", float(2 * pi - 9) < 0)
chk("3.4.7 b", simplify(integrate(sqrt(x), (x, 1, 2)) - Rational(2, 3) * (2 * sqrt(2) - 1)) == 0)
chk("3.6.7 a", simplify(integrate(1 / (1 - x**2), (x, 2, 5)) + log(2) / 2) == 0)
chk("3.6.11 a", simplify(integrate(-2 * x + 1 - x**2, (x, -1 - sqrt(2), -1 + sqrt(2))) - 8 * sqrt(2) / 3) == 0)
chk("3.6.11 b", integrate(-2 * x**2 - x, (x, Rational(-1, 2), 0)) == Rational(1, 24))
chk("3.6.11 d", abs(float(integrate(5 - x - 1 / x, (x, (5 - sqrt(21)) / 2, (5 + sqrt(21)) / 2))) - 8.3228) < 1e-3)

# --- Capítulo 4
for e, p, v in [((x**2 - 1) / (x**2 - 3 * x + 2), 1, -2), ((sqrt(x) - x) / (x - 1), 1, Rational(-1, 2)),
                (log(x) / (x - 1), 1, 1), (x * log(x), 0, 0), (floor(x) / x, oo, 1), (sqrt(x + 1) - sqrt(x), oo, 0)]:
    chk(f"lim {e}", limit(e, x, p) == v)
chk("4.1.4 δ(ε=1)≈0.60", all(abs(math.exp(t) - math.cos(t)) < 1 for t in np.linspace(-0.6, 0.6, 2001)))

# --- Capítulo 5
chk("5.2.1a", 0 + 2 * math.cos(0) > 0 and -math.pi / 2 + 2 * math.cos(-math.pi / 2) < 0)
chk("5.3.2", integrate(3 * x**2 + 1, (x, 0, 2)) == 10)

bad = [n for n, ok in R if not ok]
print(f"{len(R) - len(bad)}/{len(R)} verificaciones OK")
for n in bad:
    print("FALLA:", n)
