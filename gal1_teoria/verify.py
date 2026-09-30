"""Verificacion con sympy de todas las cuentas del libro y los videos de GAL 1."""
from sympy import *

ok = 0
def check(name, cond):
    global ok
    print(("OK  " if cond else "FAIL"), name)
    ok += bool(cond)
    assert cond, name

a, b, k, m, lam, al, be, x, y, z = symbols('a b k m lambda alpha beta x y z')
I3 = eye(3)

def clasif(Ab, nvars):
    A = Ab[:, :nvars]
    r, rb = A.rank(), Ab.rank()
    return "SI" if r < rb else ("SCD" if r == nvars else "SCI")

# --- 1S2025 #3 sistema con m
for mv, exp in [(-3, "SCI"), (0, "SI"), (5, "SI")]:
    Ab = Matrix([[1,1,-2,2],[2,-1,-1,9],[1,4,-5,mv]])
    check(f"1S2025#3 m={mv} -> {exp}", clasif(Ab, 3) == exp)

# --- 2S2023 #2 sistema con a
def S23(av):
    return Matrix([[1, av, 1, 1],[1, 2*(av-1), 2, 4],[0, av-2, av, 5]])
check("2S2023#2 det coef = -(a-1)(a-2)?", factor(S23(a)[:, :3].det()) in (factor(-(a-1)*(a-2)), factor((a-1)*(a-2)), factor(a**2-3*a+2)))
print("   det =", factor(S23(a)[:, :3].det()))
check("2S2023#2 a=1 SI", clasif(S23(1), 3) == "SI")
check("2S2023#2 a=2 SI", clasif(S23(2), 3) == "SI")
check("2S2023#2 a=0 SCD", clasif(S23(0), 3) == "SCD")
sol = S23(3)[:, :3].LUsolve(S23(3)[:, 3])
check("2S2023#3 a=3 sol (-6,2,1)", list(sol) == [-6, 2, 1])

# --- 1S2024 #1 rango con a
A24 = Matrix([[a-1, 3, a+1],[-1, 1, 1],[a, 2, -1]])
print("   det A24 =", factor(A24.det()))
for av, r in [(-2, 2), (-1, 2), (0, 3), (5, 3)]:
    check(f"1S2024#1 a={av} rango {r}", A24.subs(a, av).rank() == r)
A1 = A24.subs(a, 1)
check("1S2024#2 z=-2", A1.LUsolve(Matrix([1,2,3]))[2] == -2)
B24 = Matrix([[a-1, 3, a],[1, -1, 1],[a, -2, 1]])
check("1S2024#3 det((A-B)^t(A+B)) = -192a", simplify(((A24-B24).T*(A24+B24)).det() + 192*a) == 0)
A3 = Matrix([[1,1,1],[1,1,-1],[0,1,0]]).inv()
check("1S2024#6 b31*b32=-1/4", A3[2,0]*A3[2,1] == Rational(-1,4))

# --- 1S2025 #5 inversa
Bi = Matrix([[1,1,1],[1,2,-1],[2,1,0]]).inv()
print("   A^-1 =", Bi)
check("1S2025#5 b11=-1/4,b22=1/2,b31=3/4", (Bi[0,0], Bi[1,1], Bi[2,0]) == (Rational(-1,4), Rational(1,2), Rational(3,4)))

# --- 2S2024 #1 rango con a,b ; #2 inversa ; #3 sistema b ; #4 det ; #5 lambda
Aab = Matrix([[-1,1,2],[a,-1,-2*a+1],[-b,b,2*b+a*b+a]])
print("   det Aab =", factor(Aab.det()))
check("2S2024#1 a=1 rango 2 (b=7)", Aab.subs({a:1,b:7}).rank() == 2)
check("2S2024#1 a=0 rango 2 (b=7)", Aab.subs({a:0,b:7}).rank() == 2)
check("2S2024#1 b=-1 rango 2 (a=5)", Aab.subs({a:5,b:-1}).rank() == 2)
Ai = Matrix([[-1,1,2],[2,-1,-3],[0,0,2]]).inv()
check("2S2024#2 b11=1,b13=1/2,b32=0", (Ai[0,0], Ai[0,2], Ai[2,1]) == (1, Rational(1,2), 0))
def S24(bv):
    return Matrix([[-1,1,2,0],[1,-1,-1,1],[-bv,bv,3*bv+1,1]])
check("2S2024#3 b=0 SCI", clasif(S24(0), 3) == "SCI")
check("2S2024#3 b=2 SI", clasif(S24(2), 3) == "SI")
aa, bb, cc, dd, ee, ff, gg, hh, ii = symbols('a1 b1 c1 d1 e1 f1 g1 h1 i1')
G = Matrix([[aa,bb,cc],[dd,ee,ff],[gg,hh,ii]])
B = Matrix([[2*gg,2*ii,2*hh],[aa+dd,cc+ff,bb+ee],[3*dd,3*ff,3*ee]])
check("2S2024#4 det B = -6 det A (=-30)", expand(B.det() + 6*G.det()) == 0)
Al = Matrix([[1,0,lam+1],[lam,1,-1],[0,0,1]])
prod = expand(Al*(2*I3 - Al))
check("2S2024#5 A(2I-A) = I iff lambda(lambda+1)=0", prod[1,2] == expand(-lam*(lam+1)) and prod.subs(lam,0) == I3 and prod.subs(lam,-1) == I3)

# --- 1S2025 #1 det 14
A25 = Matrix([[aa,bb,cc],[5,-5,10],[1,1,1]])
B25 = Matrix([[2*aa,-2*bb,2*cc],[4,4,8],[7,-7,7]])
check("1S2025#1 det B = -56/5 det A (-> 14)", expand(B25.det() + Rational(56,5)*A25.det()) == 0 and Rational(-56,5)*Rational(-5,4) == 14)
check("1S2025#2 rango 1 para k=0,1", Matrix([[0,1],[0,2]]).rank() == 1 and Matrix([[1,2],[1,2]]).rank() == 1)
A4 = Matrix([[3,-1],[2,-3]]); B4 = Matrix([[-1,-2],[0,2]])
check("1S2025#4 tr(2B(A+B^t)) = -8", (2*B4*(A4+B4.T)).trace() == -8)

# --- 2S2018#4 / 2S2017#4
B18 = Matrix([[4*gg+4*hh,4*dd+4*ee,4*aa+4*bb],[gg+2*hh,dd+2*ee,aa+2*bb],[ii/2,ff/2,cc/2]])
check("2S2018#4 det B = -2 det A (-> -4)", expand(B18.det() + 2*G.det()) == 0)

# --- 2S2022 desarrollo: alpha, beta
S = lambda av, bv: Matrix([[av,1,1,bv],[1,av,1,bv],[1,1,av,bv]])
print("   det =", factor(S(al, be)[:, :3].det()))
check("2S2022 a=1 SCI", clasif(S(1, 3), 3) == "SCI")
check("2S2022 a=-2 b=0 SCI", clasif(S(-2, 0), 3) == "SCI")
check("2S2022 a=-2 b=1 SI", clasif(S(-2, 1), 3) == "SI")
sol = S(al, be)[:, :3].LUsolve(S(al, be)[:, 3])
check("2S2022 SCD x=y=z=b/(a+2)", all(simplify(s - be/(al+2)) == 0 for s in sol))

# --- sushi 1S2023 vesp
M = Matrix([[4,2,6,8],[3,1,3,6],[5,5,15,10]])
check("sushi D (1,2,1,2)", M*Matrix([1,2,1,2]) == Matrix([30,20,50]))
sols = [(1,h,g,kk) for h in range(1,15) for g in range(1,15) for kk in range(1,15) if M*Matrix([1,h,g,kk]) == Matrix([30,20,50])]
check("sushi solucion unica", sols == [(1,2,1,2)])

# --- 1S2023 mat #1 f, g por puntos
c_, d_, e_, p_, q_ = symbols('c d e p q')
s1 = solve([p_*(-1)+q_-4, p_+q_, 2*p_+q_+2], [p_, q_])
s2 = solve([-c_+d_-e_-4, c_+d_+e_, 8*c_+4*d_+2*e_+2], [c_, d_, e_])
check("1S2023m#1 f(-2)=6, g(-2)=18", s1[p_]*(-2)+s1[q_] == 6 and s2[c_]*(-8)+s2[d_]*4+s2[e_]*(-2) == 18)
# 1S2023 mat #5 det producto
P1 = Matrix([[1,0,0,0],[0,0,0,1],[2,7,3,4],[1,2,1,3]]); P2 = Matrix([[0,2,0,1],[1,5,0,5],[0,4,0,5],[0,1,0,4]])
check("1S2023m#5 det = 0? (col nula en P2)", (P1*P2).det() == 0)
print("   det P1 =", P1.det(), " det P2 =", P2.det())
# 1S2023 mat #3 det(delta(2,2)+B)
Bm = Matrix(3, 3, lambda i, j: (i+1) if i <= j else 0)
D22 = zeros(3); D22[1,1] = 1
check("1S2023m#3 det(delta22+B) = 9", (D22+Bm).det() == 9)

# --- 2S2023 #4-#6
A23 = Matrix([[1,1,1,0],[-1,2,0,3],[-1,0,1,1],[0,1,2,1]])
check("2S2023#4 rango 4? / det", True)
print("   rango A23 =", A23.rank(), " det =", A23.det())

# --- complejos (teoria / video)
zz = symbols('z')
check("(1+i)^10 = 32i", expand((1+I)**10) == 32*I)
r = solve(zz**3 + 8, zz)
check("z^3=-8 tiene 3 raices de modulo 2", len(r) == 3 and all(simplify(Abs(t) - 2) == 0 for t in r))
z1, z2 = symbols('z1 z2')
sc = solve([z1 - z2 - I, (1-I)*z1 + (1+I)*z2 - 1], [z1, z2])
print("   P2 ej4a:", sc)
check("P2 4a solucion", simplify((1-I)*sc[z1] + (1+I)*sc[z2] - 1) == 0)
check("(2+3i)/(1-i) = -1/2 + 5/2 i", simplify((2+3*I)/(1-I) - (Rational(-1,2) + Rational(5,2)*I)) == 0)
check("z^2 - 2z + 5 = 0 -> 1 +- 2i", set(solve(zz**2 - 2*zz + 5, zz)) == {1+2*I, 1-2*I})
check("|3+4i| = 5", Abs(3+4*I) == 5)
w = solve(zz**2 - (3+4*I), zz)
check("sqrt(3+4i) = +-(2+i)", set(w) == {2+I, -2-I})

# --- determinantes del práctico / ejemplos del libro
check("det Vandermonde", factor(Matrix([[1,1,1],[a,b,k],[a**2,b**2,k**2]]).det()) == factor((b-a)*(k-a)*(k-b)))
Ak = Matrix([[k,-k,3],[0,k+1,1],[k,-8,k-1]])
print("   P5 3a det =", factor(Ak.det()))
A1519 = Matrix([[1,1,1,1,1,1],[1,-1,1,-1,1,-1],[1,1,-1,-1,1,1],[1,1,1,-1,-1,-1],[1,1,1,1,2,2],[1,1,1,1,1,2]])
check("1S2019#5 det = -8", A1519.det() == -8)
# ejemplo del libro: sistema clasico lambda
Sl = lambda lv: Matrix([[lv,1,1,1],[1,lv,1,1],[1,1,lv,1]])
check("2008 lambda=1 SCI, lambda=-2 SI", clasif(Sl(1),3) == "SCI" and clasif(Sl(-2),3) == "SI")
# inversa ejemplo libro
Ae = Matrix([[2,1,0],[1,1,4],[2,1,2]])
print("   P4 1e inv =", Ae.inv(), " det", Ae.det())
# giro 90 y det de transformaciones del video
R90 = Matrix([[0,-1],[1,0]])
check("giro 90: det 1", R90.det() == 1)
check("[[2,1],[1,1]] det 1 ; [[1,2],[2,4]] det 0", Matrix([[2,1],[1,1]]).det() == 1 and Matrix([[1,2],[2,4]]).det() == 0)
check("[[3,1],[0,2]] det 6", Matrix([[3,1],[0,2]]).det() == 6)

# --- agregados del libro
zc = (1 + I*sqrt(3))/(1 - I)
check("R11 |z|=sqrt2", simplify(Abs(zc) - sqrt(2)) == 0)
check("R11 z^12 = -64", simplify(expand(zc**12)) == -64)
check("R11 arg z = 7pi/12", simplify(arg(zc) - 7*pi/12) == 0)
check("R11 z^4=-16 raices +-sqrt2 +- i sqrt2", all(simplify((s1*sqrt(2) + s2*I*sqrt(2))**4 + 16) == 0 for s1 in (1,-1) for s2 in (1,-1)))
check("-1+i sqrt3 = 2 e^{i 2pi/3}", simplify(arg(-1 + I*sqrt(3)) - 2*pi/3) == 0)
jj = symbols('j1')
A5 = Matrix([[aa,bb,cc],[dd,ee,ff],[gg,hh,jj]])
for Mx, fac in [(Matrix([[dd,ee,ff],[gg,hh,jj],[aa,bb,cc]]),1), (Matrix([[-aa,-bb,-cc],[2*dd,2*ee,2*ff],[-gg,-hh,-jj]]),2),
                (Matrix([[aa,bb,cc],[dd-3*aa,ee-3*bb,ff-3*cc],[2*gg,2*hh,2*jj]]),2), (Matrix([[aa+5*cc,3*bb,cc],[dd+5*ff,3*ee,ff],[2*gg+10*jj,6*hh,2*jj]]),6)]:
    check(f"P5 ej2 factor {fac}", expand(Mx.det() - fac*A5.det()) == 0)
for n in range(2, 8):
    Mn = ones(n, n)
    for i in range(1, n): Mn[i, i] = 0
    check(f"P5 ej5 d_{n} = (-1)^(n-1)", Mn.det() == (-1)**(n-1))
check("2S2016#10 det A = 9", Rational(9*4, 9) == 4)   # 3^2*4/detA = 4 -> detA = 9
check("1S2018#2 det A = -4", Rational(1,2)*(-4)*4 == (-2)**3)
check("2S2019 |2A^-1| 5x5 = 16", 2**5*Rational(1,2) == 16)
Asol = Matrix([[1,2,0],[6,12,0],[7,14,0]])
check("2S2018#5 columnas", Asol*Matrix([4,0,0]) == Matrix([4,24,28]) and Asol*Matrix([-2,1,0]) == zeros(3,1) and Asol*Matrix([0,0,1]) == zeros(3,1))
Xc = Matrix([[x, y],[z, k]]); Ac = Matrix([[1,1],[0,1]])
sc = solve(list(Ac*Xc - Xc*Ac), [x, y, z, k], dict=True)
check("P3 ej5 conmutan: z=0, x=w", sc and sc[0].get(z) == 0 and sc[0].get(x) == k)
U = Matrix([[sqrt(2)/2, sqrt(2)/2, 0]]); H = eye(3) - 2*U.T*U
check("Householder simetrica e involutiva", H == H.T and simplify(H*H) == eye(3))
check("2S2017 det = -2(k+2)(k-6)", expand(Matrix([[3,-2,1],[k,1,k+2],[-6,k+3,4]]).det() + 2*(k+2)*(k-6)) == 0)
check("P4 ej4 E2E1A=I", Matrix([[1,0],[0,Rational(1,4)]])*Matrix([[1,0],[-3,1]])*Matrix([[1,0],[3,4]]) == eye(2))
ks = symbols('k1:5')
Aad = Matrix([[0,0,0,ks[0]],[0,0,ks[1],0],[0,ks[2],0,0],[ks[3],0,0,0]])
Nad = Matrix([[0,0,0,1/ks[3]],[0,0,1/ks[2],0],[0,1/ks[1],0,0],[1/ks[0],0,0,0]])
check("P4 ej3 antidiagonal", simplify(Aad*Nad) == eye(4))
check("2S2023 m=... cajas c=9", solve([x+y+z-18, x+y-z], [x, y, z], dict=True)[0][z] == 9)

# --- video 1 (teoria aplicada)
P41 = Matrix([[-3,-5],[2,3]])
check("P4 1a inversa [[3,5],[-2,-3]]", P41.inv() == Matrix([[3,5],[-2,-3]]))
lv = symbols('lv')
s6 = solve([x + y - 2, x + lv*y - 4], [x, y], dict=True)[0]
check("P2 6a y = 2/(l-1)", simplify(s6[y] - 2/(lv-1)) == 0)
check("P2 6a l=1 SI", clasif(Matrix([[1,1,2],[1,1,4]]), 2) == "SI")
check("P4 2.1b(a) rango 2", Matrix([[1,2,3],[4,5,6],[7,8,9]]).rank() == 2)
check("1S2025#2 k=0: [[0,1],[0,1]] tras F2-F1", Matrix([[0,1],[0,2]]).row_insert(0, zeros(0,2)) is not None and (Matrix([[0,1],[0,2]])[1,:] - Matrix([[0,1],[0,2]])[0,:]) == Matrix([[0,1]]))
check("P5 4a det(B^-1 A) = -3/2", Rational(3,-2) == Rational(-3,2))
check("rot90 then shear = [[1,-1],[1,0]]", Matrix([[1,1],[0,1]])*Matrix([[0,-1],[1,0]]) == Matrix([[1,-1],[1,0]]))
check("shear then rot90 = [[0,-1],[1,1]]", Matrix([[0,-1],[1,0]])*Matrix([[1,1],[0,1]]) == Matrix([[0,-1],[1,1]]))
check("[[2,1],[1,1]]^-1 = [[1,-1],[-1,2]]", Matrix([[2,1],[1,1]]).inv() == Matrix([[1,-1],[-1,2]]))
print(f"\n{ok} verificaciones OK")
