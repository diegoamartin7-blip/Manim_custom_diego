"""
VIDEO 1 - TEORIA COMPACTA APLICADA  (lo que se usa en el 90% de los primeros parciales)
Cada bloque: la idea (visual) + un ejercicio rapido de practico o parcial donde se aplica.
  00 Las cinco preguntas que te hacen sobre una matriz (y que son una sola)
  01 Complejos: cuentas, polar, raices
  02 Sistemas: rectas, escalerizar, clasificar
  03 Parametros, homogeneos y Rouche-Frobenius
  04 Matrices: maquinas que mueven el plano
  05 Producto, traza, traspuesta, delta
  06 Inversa
  07 Rango
  08 Determinante: el factor de area
  09 Propiedades del determinante
  10 El mapa: que te preguntan y con que se contesta
RENDER LIVIANO: nada de LaTeX que cambie cuadro a cuadro (solo Num y geometria en vivo).
Todas las cuentas estan en gal1_teoria/verify.py (sympy).
"""
from gal_base import *

SCENE_ORDER = ["V1_00_Intro", "V1_01_Complejos", "V1_02_Sistemas", "V1_03_Parametros",
               "V1_04_Matrices", "V1_05_Producto", "V1_06_Inversa", "V1_07_Rango",
               "V1_08_Determinante", "V1_09_DetPropiedades", "V1_10_Mapa"]


class V1(GBase, MatScene):
    VIDEO_TAG = "VIDEO 1 · TEORÍA APLICADA"


I_COL = GREEN     # primera columna (a donde va i-sombrero)
J_COL = RED       # segunda columna (a donde va j-sombrero)
REF = None


def ref_plane():
    """Plano fijo, sin deformar, para ubicar flechas (los planos animados se deforman)."""
    global REF
    if REF is None:
        REF = plano((-8, 8), (-5, 5), unit=1.0)
    return REF


def base_vectors(A=((1, 0), (0, 1)), p=None):
    p = p or ref_plane()
    c1 = complex(A[0][0], A[1][0])
    c2 = complex(A[0][1], A[1][1])
    return VGroup(flecha(p, c1, I_COL, 6), flecha(p, c2, J_COL, 6))


def _fmt(v):
    if isinstance(v, str):
        return v
    return f"{v:g}".replace(".", "{,}")


def mat_cols(A, size=36):
    m = Mat([[_fmt(v) for v in r] for r in A], size=size, h_buff=0.75, v_buff=0.6)
    mcol(m, 0).set_color(I_COL)
    mcol(m, 1).set_color(J_COL)
    return m


def mpanel(m, pos):
    bg = SurroundingRectangle(m, buff=0.2, stroke_width=1.2, color=DIM).set_fill(BG, 0.9)
    return VGroup(bg, m).move_to(pos)


def apply_to(p, A):
    return ApplyMatrix(np.array(A, dtype=float), p, about_point=p.n2p(0))


def full_plane():
    return plano((-8, 8), (-5, 5), unit=1.0, faded=False)


def linea(ax, A, B, C, color=BLUE, sw=4):
    """Recta A x + B y = C recortada al rectangulo de los ejes."""
    x0, x1 = ax.x_range[0], ax.x_range[1]
    y0, y1 = ax.y_range[0], ax.y_range[1]
    pts = []
    if abs(B) > 1e-9:
        for x in (x0, x1):
            y = (C - A * x) / B
            if y0 - 1e-9 <= y <= y1 + 1e-9:
                pts.append((x, y))
    if abs(A) > 1e-9:
        for y in (y0, y1):
            x = (C - B * y) / A
            if x0 - 1e-9 <= x <= x1 + 1e-9:
                pts.append((x, y))
    if len(pts) < 2:
        return VMobject()
    best = max(((p, q) for p in pts for q in pts),
               key=lambda pq: (pq[0][0] - pq[1][0]) ** 2 + (pq[0][1] - pq[1][1]) ** 2)
    return Line(ax.c2p(*best[0]), ax.c2p(*best[1]), color=color, stroke_width=sw)


def apl(fuente, lines, size=24, width=None):
    """Caja APLICADO: el ejercicio rapido donde se usa la teoria recien vista."""
    tag = T("APLICADO · " + fuente, 15, BG, MONO, BOLD)
    tr = SurroundingRectangle(tag, buff=0.08, stroke_width=0).set_fill(GREEN, 1)
    tagg = VGroup(tr, tag)
    txt = VGroup(*[L(l, size, INK) if isinstance(l, str) else l for l in lines])
    txt.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    wdt = width or min(txt.width + 0.6, 13.2)
    if txt.width > wdt - 0.5:
        txt.scale_to_fit_width(wdt - 0.5)
    fr = Rectangle(width=wdt, height=txt.height + 0.5, color=GREEN, stroke_width=1.6)
    fr.set_fill(interpolate_color(ManimColor(BG), ManimColor(GREEN), 0.07), 1)
    txt.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3 + DOWN * 0.04)
    tagg.move_to(fr.get_corner(UL), aligned_edge=LEFT).shift(RIGHT * 0.25)
    return VGroup(fr, txt, tagg)


def stack(*mobs, top=2.85, bottom=-2.4, buff=0.22):
    """Apila de arriba hacia abajo y achica todo junto si no entra entre top y bottom."""
    g = VGroup(*mobs).arrange(DOWN, buff=buff)
    if g.height > top - bottom:
        g.scale_to_fit_height(top - bottom)
    g.move_to([0, 0, 0]).align_to([0, top, 0], UP)
    return g


def boxed(mob, op=0.9):
    return VGroup(SurroundingRectangle(mob, buff=0.14, stroke_width=0).set_fill(BG, op), mob)


# =====================================================================
class V1_00_Intro(V1):
    def construct(self):
        self.setup_frame(header=False)
        t1 = T("GAL 1 · IMERL · FING · 2S 2026", 22, SOFT, MONO)
        t2 = T("Teoría compacta, aplicada", 64, INK, SANS, BOLD)
        t3 = T("Lo que se usa en el 90% de los primeros parciales", 32, BLUE, SANS, BOLD)
        VGroup(t1, t2, t3).arrange(DOWN, buff=0.3).shift(UP * 0.6)
        self.play(FadeIn(t1, shift=DOWN * 0.2), Write(t2), FadeIn(t3), run_time=1.3)
        self.say("Este video complementa al de ejercicios. Cada bloque de teoría es corto, y enseguida lo **aplicamos** a un ejercicio rápido de práctico o de parcial.")
        self.wipe()

        A = Mat([["a_{11}", "\\cdots", "a_{1n}"], ["\\vdots", "", "\\vdots"], ["a_{n1}", "\\cdots", "a_{nn}"]], size=40)
        A.move_to([0, 0.35, 0])
        preg = ["¿AX = b tiene solución?", "¿Cuántas?", "¿Cuál es el rango?", "¿Es invertible?", "¿Cuánto vale el determinante?"]
        pos = [[-4.3, 2.1, 0], [4.3, 2.1, 0], [-4.6, -0.2, 0], [4.6, -0.2, 0], [0, -2.0, 0]]
        qs = VGroup(*[T(q, 24, YELLOW, SANS, BOLD).move_to(p) for q, p in zip(preg, pos)])
        self.say("En el primer parcial te dan una matriz y te hacen, casi siempre, **cinco preguntas**.", FadeIn(A))
        self.say("¿El sistema tiene solución? ¿Cuántas? ¿Qué rango tiene? ¿Es invertible? ¿Cuánto vale el determinante?",
                 LaggedStart(*[FadeIn(q, shift=0.2 * UP) for q in qs], lag_ratio=0.3, run_time=2.4))
        self.say("El secreto de la materia: son **la misma pregunta** disfrazada cinco veces. Mirá.")
        self.wipe()

        p = full_plane()
        self.add(p)
        self.bring_to_front(*self.persist)
        vb = base_vectors()
        self.play(GrowArrow(vb[0]), GrowArrow(vb[1]), run_time=0.5)
        B = [[2, 1], [1, 1]]
        pan = mpanel(mat_cols(B, 38), [-5.3, 2.4, 0])
        self.say("Una matriz es una máquina que mueve el plano. Esta lo deforma, pero **no lo aplasta**: sigue llenando todo el plano.",
                 FadeIn(pan), apply_to(p, B), Transform(vb, base_vectors(B)), run_time=1.8)
        okb = boxed(T("sistema SCD · rango 2 · invertible · det ≠ 0", 26, GREEN, SANS, BOLD)).move_to([2.6, -1.9, 0])
        self.say("Entonces el sistema tiene solución única, el rango es completo, hay inversa y el determinante no es cero. **Todo a la vez.**",
                 FadeIn(okb))
        self.play(FadeOut(p), FadeOut(vb), FadeOut(pan), FadeOut(okb), run_time=0.3)
        q = full_plane()
        vb = base_vectors()
        self.add(q, vb)
        self.bring_to_front(*self.persist)
        C = [[1, 2], [2, 4]]
        pan = mpanel(mat_cols(C, 38), [-5.3, 2.4, 0])
        self.say("Esta otra tiene la segunda columna igual al doble de la primera: **aplasta el plano en una recta**.",
                 FadeIn(pan), apply_to(q, C), Transform(vb, base_vectors(C)), run_time=2.0, focus=True)
        badb = boxed(T("puede no haber solución · rango 1 · sin inversa · det = 0", 26, RED, SANS, BOLD)).move_to([2.2, -1.9, 0])
        self.say("Y todo se cae junto: puede no haber solución, el rango baja, no hay inversa, el determinante es cero.",
                 FadeIn(badb))
        self.say("Con esa imagen en la cabeza, arrancamos. Primero los complejos, que van por otro carril.")
        self.end_scene()


# =====================================================================
class V1_01_Complejos(V1):
    CH_NUM = "01"
    CH_TITLE = "Complejos"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Números complejos", "cuentas · polar · raíces", prob=("ALTA", "nuevo en el programa de este año"))
        p = plano((-5, 5), (-3, 3), unit=0.72).shift(LEFT * 2.8 + DOWN * 0.15)
        o = p.n2p(0)
        z = 3 + 2j
        az = flecha(p, z, BLUE)
        lz = MathTex("z=3+2i", font_size=30, color=BLUE).next_to(az.get_end(), UR, buff=0.06)
        zc = flecha(p, z.conjugate(), TEAL)
        lzc = MathTex(r"\bar z=3-2i", font_size=30, color=TEAL).next_to(zc.get_end(), DR, buff=0.06)
        self.say("Un complejo a + bi es un punto del plano. El **conjugado** lo refleja en el eje real, y el **módulo** es el largo de la flecha.",
                 Create(p), GrowArrow(az), FadeIn(lz), run_time=1.2)
        self.play(ReplacementTransform(az.copy(), zc), FadeIn(lzc), run_time=0.6)
        rules = VGroup(L("$i^2=-1$", 28), L("$|z|=\\sqrt{a^2+b^2}$", 28), L("$z\\,\\bar z=|z|^2$ \\ (real)", 28, YELLOW),
                       L("dividir: por el conjugado de abajo", 22, SOFT)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rules.move_to([4.2, 1.4, 0])
        self.say("La identidad clave: z por su conjugado da el módulo al cuadrado, un real. Por eso, para dividir, multiplicás arriba y abajo por el conjugado del denominador.",
                 FadeIn(rules))
        a1 = apl("CUENTA BÁSICA", ["$\\dfrac{2+3i}{1-i}=\\dfrac{(2+3i)(1+i)}{(1-i)(1+i)}=\\dfrac{-1+5i}{2}$"], size=24, width=6.4)
        a1.move_to([3.6, -1.35, 0])
        self.say("Aplicado: 2 + 3i sobre 1 − i. Abajo queda 1 + 1 = 2. Arriba, distributiva e i² = −1: da −1 + 5i.",
                 FadeIn(a1, shift=UP * 0.2))
        self.wipe(p)

        # ---- polar: solo flechas en vivo (nada de LaTeX por cuadro)
        z = 2 + 0.6j
        th = ValueTracker(0.0)
        r = ValueTracker(1.0)
        wv = lambda: r.get_value() * np.exp(1j * th.get_value())
        az = flecha(p, z, BLUE)
        aw = always_redraw(lambda: flecha(p, wv(), TEAL, 5))
        azw = always_redraw(lambda: flecha(p, z * wv(), YELLOW, 6))
        lz = MathTex("z", font_size=32, color=BLUE).next_to(az.get_end(), DOWN, buff=0.08)
        sl1 = Slider("$\\arg w$", th, 0, 2.2, color=TEAL, width=2.3, decimals=2, size=24).move_to([4.2, 2.1, 0])
        sl2 = Slider("$|w|$", r, 0.5, 1.6, color=TEAL, width=2.3, decimals=2, size=24).move_to([4.2, 1.45, 0])
        leg = L("azul $z$ \\quad verde $w$ \\quad amarilla $zw$", 22, SOFT).move_to([4.2, 0.85, 0])
        self.say("Multiplicar por w hace dos cosas: **gira** el ángulo de w y **estira** por el largo de w.",
                 GrowArrow(az), FadeIn(lz), FadeIn(aw), FadeIn(azw), FadeIn(sl1), FadeIn(sl2), FadeIn(leg))
        self.say("Giro w: la amarilla gira igual. Estiro w: la amarilla se estira igual.",
                 th.animate.set_value(1.5), r.animate.set_value(1.45), run_time=3.0)
        aw.clear_updaters(); azw.clear_updaters()
        s = self.stamp(["$z=|z|\\,e^{i\\theta}$ \\quad (largo y ángulo)",
                        "$re^{i\\theta}\\cdot se^{i\\varphi}=rs\\,e^{i(\\theta+\\varphi)}$",
                        "**De Moivre:** $(re^{i\\theta})^n=r^ne^{in\\theta}$"], "FORMA POLAR", size=26)
        s.scale_to_fit_width(min(s.width, 5.0))
        s.move_to([4.2, -0.55, 0])
        self.say("En forma polar eso es una fórmula: los módulos se multiplican, los ángulos se suman. Y elevar a la n es hacerlo n veces: **De Moivre**.",
                 *self.show_stamp(s))
        a2 = apl("POTENCIA", ["$(1+i)^{10}=(\\sqrt2\\,e^{i\\pi/4})^{10}=32\\,e^{i5\\pi/2}=32i$"], size=24, width=6.4)
        a2.move_to([3.6, -2.1, 0])
        self.say("Aplicado: 1 + i tiene largo √2 y ángulo 45°. A la diez: largo 32, ángulo 450°, o sea 90°. Da 32i, sin desarrollar ningún binomio.",
                 FadeIn(a2, shift=UP * 0.2))
        tr = trampa(["El arcotangente no ve el cuadrante: **dibujá el punto**."], width=6.4)
        tr.move_to([-3.3, -2.05, 0])
        self.play(FadeIn(tr), run_time=0.3)
        self.w(0.6)
        self.wipe(p)

        # ---- raices
        R = 2
        roots = [R * np.exp(1j * (PI + 2 * k * PI) / 3) for k in range(3)]
        circ = Circle(radius=p.x_axis.unit_size * R, color=DIM).move_to(o)
        tri = Polygon(*[p.n2p(q) for q in roots], color=RED, stroke_width=3)
        dots = VGroup(*[Dot(p.n2p(q), radius=0.08, color=YELLOW) for q in roots])
        labs = VGroup(*[MathTex(t, font_size=28, color=YELLOW).next_to(p.n2p(q), d, buff=0.1)
                        for q, t, d in zip(roots, ["1+i\\sqrt3", "-2", "1-i\\sqrt3"], [UR, UL, DR])])
        s = self.stamp(["$z^n=Re^{i\\varphi}\\Rightarrow z_k=\\sqrt[n]{R}\\,e^{\\,i\\frac{\\varphi+2k\\pi}{n}}$",
                        "$k=0,\\dots,n-1$: \\ un **polígono regular**"], "RAÍCES n-ÉSIMAS", size=26)
        s.scale_to_fit_width(min(s.width, 5.8))
        s.move_to([3.9, 1.6, 0])
        self.say("Raíces: z a la n igual a w tiene **n soluciones**, repartidas parejas en un círculo: un polígono regular.",
                 *self.show_stamp(s), Create(circ))
        a3 = apl("EJERCICIO TIPO", ["$z^3=-8=8e^{i\\pi}$: \\ módulo $\\sqrt[3]8=2$,",
                                    "ángulos $\\frac\\pi3,\\ \\pi,\\ \\frac{5\\pi}3$ \\ (saltos de $120^\\circ$)"], size=24, width=5.8)
        a3.move_to([3.9, -1.0, 0])
        self.say("Aplicado: z³ = −8. Módulo 8 y ángulo π. Raíz cúbica del módulo: 2. Ángulos: π/3 y saltos de 120 grados.",
                 FadeIn(a3, shift=UP * 0.2), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), Create(tri))
        self.say("Las tres raíces: 1 + i√3, −2 y 1 − i√3. Dos son conjugadas porque el polinomio tiene coeficientes reales.",
                 FadeIn(labs))
        self.end_scene()


# =====================================================================
class V1_02_Sistemas(V1):
    CH_NUM = "02"
    CH_TITLE = "Sistemas: qué es clasificar"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Sistemas lineales", "clasificar es contar intersecciones", prob=("MUY ALTA", "11 de 14 parciales"))
        ax = ejes([-4, 4, 1], [-3, 3, 1], 7.0, 5.2).shift(LEFT * 3.0 + DOWN * 0.15)
        lam = ValueTracker(-1.0)
        l1 = linea(ax, 1, 1, 2, BLUE, 5)
        l2 = always_redraw(lambda: linea(ax, 1, lam.get_value(), 4, TEAL, 5))

        def inter():
            lv = lam.get_value()
            if abs(lv - 1) < 0.03:
                return VMobject()
            y = 2 / (lv - 1)
            x = 2 - y
            if not (-4 <= x <= 4 and -3 <= y <= 3):
                return VMobject()
            return Dot(ax.c2p(x, y), radius=0.1, color=YELLOW)

        dot = always_redraw(inter)
        a = apl("PRÁCTICO 2 · EJ. 6A", ["$x+y=2,\\quad x+\\lambda y=4$", "Discutir según $\\lambda$."], size=26, width=5.8)
        a.move_to([3.9, 2.1, 0])
        self.say("Con dos incógnitas cada ecuación es una **recta**. Clasificar es contar cuántos puntos tienen en común. Lo vemos directo con el práctico 2.",
                 Create(ax), Create(l1), FadeIn(a))
        self.add(l2, dot)
        sl = Slider("$\\lambda$", lam, -1, 1.6, color=TEAL, width=2.6, decimals=2, size=26).move_to([3.9, 0.75, 0])
        est = {"SCD": T("SCD · se cortan en un punto", 26, YELLOW, SANS, BOLD),
               "SI": T("SI · paralelas, nunca se cortan", 26, RED, SANS, BOLD)}
        for k, v in est.items():
            v.move_to([3.9, 0.05, 0])
            v.add_updater(lambda m, k=k: m.set_opacity(1 if (("SI" if abs(lam.get_value() - 1) < 0.03 else "SCD") == k) else 0))
        self.add(sl, *est.values())
        self.say("Muevo lambda. Mientras lambda no sea 1, las rectas se cortan: una solución. En lambda = 1 quedan **paralelas**.",
                 lam.animate.set_value(1.0), run_time=3.2)
        r = VGroup(L("$\\lambda\\neq1$: \\ **SCD**", 28), L("$\\lambda=1$: \\ $x+y=2$ y $x+y=4$ \\ **SI**", 28),
                   L("nunca SCI: harían falta rectas iguales", 22, SOFT)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        r.move_to([3.9, -1.5, 0])
        self.say("Resultado: SCD si lambda no es 1, incompatible si es 1. Y nunca indeterminado, porque para eso las rectas tendrían que coincidir.",
                 FadeIn(r))
        for v in est.values():
            v.clear_updaters()
        l2.clear_updaters(); dot.clear_updaters()
        self.wipe()

        ops = self.stamp(["$F_i\\leftrightarrow F_j$ \\quad $F_i\\to\\lambda F_i\\ (\\lambda\\neq0)$ \\quad $F_i\\to F_i+\\lambda F_j$",
                          "no cambian las soluciones"], "OPERACIONES ELEMENTALES", size=26)
        ops.move_to([0, 2.3, 0])
        self.say("Con más incógnitas no se dibuja: se **escaleriza**. Tres operaciones que no cambian las soluciones.",
                 *self.show_stamp(ops))
        m = Mat([[1, -1, 5, -2], [2, 1, 4, 2], [2, 4, -2, "c"]], bar=3, size=36).move_to([-2.6, 0.0, 0])
        tag = T("PRÁCTICO 2 · EJ. 1C (c = 10) Y 1E (c = 8)", 18, GREEN, MONO, BOLD).next_to(m, UP, buff=0.25)
        self.say("Aplicado: práctico 2, ejercicios 1c y 1e. Misma matriz, solo cambia el último término.", FadeIn(tag), FadeIn(m))
        m = self.rowop(m, [[1, -1, 5, -2], [0, 3, -6, 6], [0, 6, -12, "c+4"]], r"F_2-2F_1,\ F_3-2F_1",
                       "Ceros debajo del primer pivote.", changed=[1, 2], bar=3, size=36)
        m = self.rowop(m, [[1, -1, 5, -2], [0, 3, -6, 6], [0, 0, 0, "c-8"]], r"F_3-2F_2",
                       "Cero debajo del segundo. La última fila dice: cero igual a c − 8.", changed=[2], bar=3, size=36, focus=True)
        met = metodo(["Fila $(0\\cdots0\\,|\\,k\\neq0)$: \\ **SI**.",
                      "Si no: columna sin pivote = **variable libre**.",
                      "Sin libres: **SCD**. \\ Con libres: **SCI**."], "LEER LA ESCALERA", size=23, width=6.0)
        met.move_to([3.6, 0.3, 0])
        self.say("Se lee así: una fila de ceros con algo distinto de cero a la derecha es incompatible. Si no, cada columna sin pivote es una variable libre.",
                 FadeIn(met))
        res = VGroup(L("$c=10$: \\ $0=2$ \\ **SI**", 26), L("$c=8$: \\ $z$ libre, \\ **SCI**: \\ $(-3z,\\ 2+2z,\\ z)$", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        res.move_to([0, -1.9, 0])
        self.say("Con c = 10, cero igual a dos: no hay solución. Con c = 8, z queda libre: infinitas soluciones, (−3z, 2 + 2z, z).",
                 FadeIn(res))
        self.end_scene()


# =====================================================================
class V1_03_Parametros(V1):
    CH_NUM = "03"
    CH_TITLE = "Parámetros · homogéneos · Rouché-Frobenius"

    def construct(self):
        self.setup_frame()
        met = metodo(["Escalerizá **sin dividir** por nada que tenga el parámetro.",
                      "Los pivotes con parámetro dan los **valores críticos**.",
                      "En cada crítico: **sustituí** y terminá de escalerizar."], "DISCUTIR SEGÚN UN PARÁMETRO", size=24, width=12.4)
        met.move_to([0, 2.05, 0])
        self.say("La pregunta más segura del parcial: discutir según un parámetro. Tres pasos.", FadeIn(met))
        m = Mat([[1, 1, -2, 2], [2, -1, -1, 9], [1, 4, -5, "m"]], bar=3, size=34).move_to([-2.6, -0.65, 0])
        tag = T("1S 2025 · PREGUNTA 3", 18, GREEN, MONO, BOLD).next_to(m, UP, buff=0.2)
        self.say("Aplicado: 1S 2025, pregunta 3. El parámetro m está solo en el término independiente.", FadeIn(tag), FadeIn(m))
        m = self.rowop(m, [[1, 1, -2, 2], [0, -3, 3, 5], [0, 3, -3, "m-2"]], r"F_2-2F_1,\ F_3-F_1",
                       "Ceros en la primera columna.", changed=[1, 2], bar=3, size=34)
        m = self.rowop(m, [[1, 1, -2, 2], [0, -3, 3, 5], [0, 0, 0, "m+3"]], r"F_3+F_2",
                       "Y la última fila queda: cero igual a m + 3.", changed=[2], bar=3, size=34)
        r = VGroup(L("$m=-3$: \\ $0=0$ \\ **SCI**", 26), L("$m\\neq-3$: \\ **SI**", 26), L("nunca SCD ($A$ perdió un pivote)", 22, SOFT),
                   L("Opción (D)", 24, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        r.move_to([3.5, -0.85, 0])
        self.say("Si m = −3, queda cero igual a cero: indeterminado. Si no, incompatible. Nunca determinado, porque la matriz A ya perdió un pivote.",
                 FadeIn(r))
        self.wipe()

        s = self.stamp(["$AX=0$ siempre es compatible ($X=0$).",
                        "Más incógnitas que ecuaciones $\\Rightarrow$ soluciones no triviales.",
                        "Solución general de $AX=b$ \\ = \\ **una particular + las del homogéneo**."], "HOMOGÉNEOS Y ESTRUCTURA", size=26)
        s.move_to([0, 1.9, 0])
        self.say("Dos cosas de teoría que caen en múltiple opción. El homogéneo siempre tiene la solución cero. Y toda solución es una particular más una del homogéneo.",
                 *self.show_stamp(s))
        a = apl("2S 2018 · PREGUNTA 5", [
            "Solución general de $AX=(4,24,28)^t$: \\ $(4,0,0)+\\lambda(-2,1,0)+\\mu(0,0,1)$. \\ ¿Segunda columna de $A$?",
            "$A(4,0,0)^t=4C_1=(4,24,28)^t \\Rightarrow C_1=(1,6,7)$",
            "$A(-2,1,0)^t=0 \\Rightarrow -2C_1+C_2=0 \\Rightarrow C_2=(2,12,14)$ \\quad **Opción (B)**"], size=24, width=12.4)
        a.move_to([0, -0.95, 0])
        self.say("Aplicado, 2S 2018. La parte fija es la particular: A por (4, 0, 0) da b, así que la primera columna es b sobre 4. La parte con lambda es del homogéneo: da la segunda columna, (2, 12, 14).",
                 FadeIn(a, shift=UP * 0.2), focus=True)
        self.wipe()

        rf = self.stamp(["$AX=b$ es compatible $\\iff\\rg(A)=\\rg(A|b)$.",
                         "Compatible y $\\rg(A)=n$: **determinado**. \\ $\\rg(A)<n$: **indeterminado**."], "ROUCHÉ-FROBENIUS", size=28)
        rf.move_to([0, 1.9, 0])
        self.say("Rouché-Frobenius dice lo mismo con rangos: compatible si agregar la columna b no sube el rango, y determinado si el rango es igual al número de incógnitas.",
                 *self.show_stamp(rf))
        a = apl("V/F DE PARCIALES", [
            "$A$ de $5\\times7$: ¿existe $b$ con SCD? \\ **F**: $\\rg\\le5<7$ incógnitas.",
            "15 ecuaciones, 20 incógnitas: ¿siempre compatible? \\ **F**: dos ecuaciones contradictorias.",
            "Más incógnitas que ecuaciones y compatible $\\Rightarrow$ no es única. \\ **V**."], size=24, width=12.4)
        a.move_to([0, -0.85, 0])
        self.say("Aplicado a los verdadero o falso de siempre: cinco por siete nunca es determinado, porque el rango no llega a siete. Y más incógnitas no garantiza que haya solución.",
                 FadeIn(a, shift=UP * 0.2))
        self.end_scene()


# =====================================================================
class V1_04_Matrices(V1):
    CH_NUM = "04"
    CH_TITLE = "Matrices: máquinas que mueven el plano"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Matrices", "qué es lo que estamos haciendo", prob=("TRANSVERSAL", "la imagen que ordena todo"))
        p = full_plane()
        ghost = plano((-8, 8), (-5, 5), unit=1.0).set_opacity(0.22)
        self.add(ghost)
        self.bring_to_front(*self.persist)
        vb = base_vectors()
        li = MathTex(r"\hat\imath", font_size=36, color=I_COL).next_to(vb[0].get_end(), DR, buff=0.05)
        lj = MathTex(r"\hat\jmath", font_size=36, color=J_COL).next_to(vb[1].get_end(), UL, buff=0.05)
        self.say("Qué es lo que hacemos cuando trabajamos con una matriz. Esto es el plano, con sus dos vectores base.",
                 Create(p), GrowArrow(vb[0]), GrowArrow(vb[1]), FadeIn(li), FadeIn(lj), run_time=1.3)
        self.bring_to_front(*self.persist)
        A = [[2, 1], [0, 1]]
        pan = mpanel(mat_cols(A, 40), [-5.3, 2.4, 0])
        self.say("Una matriz dos por dos lo mueve. Sus **columnas** dicen adónde van los vectores base; el resto de la grilla los sigue.",
                 FadeIn(pan), apply_to(p, A), Transform(vb, base_vectors(A)), FadeOut(li), FadeOut(lj), run_time=2.0)
        self.bring_to_front(pan)
        c1 = flecha(ref_plane(), complex(2, 0), I_COL, 6)
        c2a = flecha(ref_plane(), complex(3, 1), J_COL, 6, origin=complex(2, 0))
        c2b = flecha(ref_plane(), complex(4, 2), J_COL, 6, origin=complex(3, 1))
        res = flecha(ref_plane(), complex(4, 2), YELLOW, 7)
        eq = MathTex(r"A\begin{pmatrix}1\\2\end{pmatrix}=1\cdot", r"\begin{pmatrix}2\\0\end{pmatrix}", r"+2\cdot",
                     r"\begin{pmatrix}1\\1\end{pmatrix}", r"=\begin{pmatrix}4\\2\end{pmatrix}", font_size=34)
        eq[1].set_color(I_COL); eq[3].set_color(J_COL); eq[4].set_color(YELLOW)
        eqp = mpanel(eq, [-3.6, -1.9, 0])
        self.say("Multiplicar por un vector es **combinar las columnas** con esos pesos: una vez la primera, dos veces la segunda.",
                 FadeIn(eqp), GrowArrow(c1), GrowArrow(c2a), GrowArrow(c2b), run_time=1.4)
        self.say("Entonces un sistema A X = b pregunta: ¿con qué pesos combino las columnas para llegar a b? Si las columnas no alcanzan para llegar, es incompatible.",
                 GrowArrow(res), focus=True)
        self.wipe(p, ghost)

        self.remove(p)
        catalogo = [([[0, -1], [1, 0]], "GIRO 90°", "Giro de 90 grados."),
                    ([[0, 1], [1, 0]], "SIMETRÍA y = x", "Simetría respecto a y = x: intercambia coordenadas."),
                    ([[1, 1], [0, 1]], "CIZALLA", "Cizalla: desliza las filas horizontales.")]
        for M, nombre, txt in catalogo:
            q = full_plane()
            vb = base_vectors()
            self.add(q, vb)
            self.bring_to_front(*self.persist)
            pan = mpanel(VGroup(T(nombre, 20, GOLD, MONO, BOLD), mat_cols(M, 36)).arrange(DOWN, buff=0.18), [-5.3, 2.2, 0])
            self.say(txt, FadeIn(pan), apply_to(q, M), Transform(vb, base_vectors(M)), run_time=1.4)
            self.play(FadeOut(q), FadeOut(vb), FadeOut(pan), run_time=0.25)
        a = apl("PRÁCTICO 3 · SECCIÓN 3", [
            "Giro $G_\\theta=\\begin{pmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{pmatrix}$: \\ girar $\\theta$ y después $\\psi$ es $G_\\psi G_\\theta=G_{\\theta+\\psi}$.",
            "Multiplicando las matrices salen $\\cos(\\theta+\\psi)$ y $\\sin(\\theta+\\psi)$: las fórmulas de la suma."], size=24, width=12.4)
        a.move_to([0, 0.5, 0])
        self.say("Aplicado, práctico 3: componer dos giros es multiplicar sus matrices. Y al hacer la cuenta aparecen las fórmulas del seno y el coseno de la suma.",
                 FadeIn(a, shift=UP * 0.2))
        tip = self.tip(["Multiplicar por un complejo de módulo 1 es aplicar $G_\\theta$: los complejos son giros escritos como números."],
                       label="EL PUENTE", size=22)
        tip.move_to([0, -1.5, 0])
        self.play(FadeIn(tip), run_time=0.4)
        self.w(1.0)
        self.end_scene()


# =====================================================================
class V1_05_Producto(V1):
    CH_NUM = "05"
    CH_TITLE = "Producto · traspuesta · traza · δ"

    def construct(self):
        self.setup_frame()
        R = [[0, -1], [1, 0]]
        S = [[1, 1], [0, 1]]
        for first, second, n1, n2, prod, pos, txt in [
                (R, S, "R", "S", [[1, -1], [1, 0]], [4.6, 2.3, 0], "Componer es multiplicar, **de derecha a izquierda**: primero el giro R, después la cizalla S."),
                (S, R, "S", "R", [[0, -1], [1, 1]], [4.6, 0.8, 0], "Al revés, primero S y después R: la grilla termina en otro lado.")]:
            q = full_plane()
            vb = base_vectors()
            self.add(q, vb)
            self.bring_to_front(*self.persist)
            lab = mpanel(L(f"primero ${n1}$, después ${n2}$", 28), [-4.5, 2.5, 0])
            self.say(txt, FadeIn(lab), apply_to(q, first), Transform(vb, base_vectors(first)), run_time=1.2)
            self.play(apply_to(q, second), Transform(vb, base_vectors((np.array(second) @ np.array(first)).tolist())), run_time=1.2)
            rp = mpanel(VGroup(MathTex(n2 + n1 + "=", font_size=36), mat_cols(prod, 34)).arrange(RIGHT, buff=0.12), pos)
            self.play(FadeIn(rp), run_time=0.3)
            self.play(FadeOut(q), FadeOut(vb), FadeOut(lab), run_time=0.25)
        s = self.stamp(["$SR\\neq RS$: el producto **no es conmutativo**."], "POR ESO", size=28)
        s.move_to([-1.5, 0.3, 0])
        self.say("El orden importa: el producto de matrices no es conmutativo.", *self.show_stamp(s))
        a = apl("PRÁCTICO 3 · EJ. 5", ["Matrices que conmutan con $\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}$: igualo $AX=XA$ entrada a entrada",
                                         "$\\Rightarrow z=0,\\ x=w$: \\quad $X=\\begin{pmatrix}x&y\\\\0&x\\end{pmatrix}$"], size=24, width=12.4)
        a.move_to([0, -1.55, 0])
        self.say("Aplicado, práctico 3: las que conmutan con esa cizalla. Escribo X genérica, hago los dos productos, igualo, y sale z = 0 y x = w.",
                 FadeIn(a, shift=UP * 0.2))
        self.wipe()

        tr = trampa(["$AB=O$ no implica $A=O$ o $B=O$: \\ $\\begin{pmatrix}0&1\\\\0&0\\end{pmatrix}^2=O$ (aplasta dos veces).",
                     "$AB=AC$ con $A\\neq O$ no implica $B=C$. \\ $(A+B)^2=A^2+AB+BA+B^2$."], width=12.4)
        tr.move_to([0, 2.2, 0])
        self.say("Las trampas que salen de ahí: producto cero sin factores cero, no se puede cancelar, y el binomio lleva AB más BA.",
                 FadeIn(tr))
        self.board_start(top=tr.get_bottom()[1] - 0.25)
        self.push(L("**Traspuesta:** $(AB)^t=B^tA^t$. \\ **Simétrica** $A^t=A$, **antisimétrica** $A^t=-A$ (diagonal nula).", 26),
                  "Traspuesta: la del producto da vuelta el orden. Simétrica y antisimétrica, con diagonal nula.")
        self.push(L("**Traza:** suma de la diagonal. \\ $\\tr(AB)=\\tr(BA)$, \\ pero $\\tr(AB)\\neq\\tr A\\cdot\\tr B$.", 26),
                  "Traza: suma de la diagonal; traza de AB es traza de BA, pero no el producto de las trazas.")
        a = apl("1S 2025 · PREGUNTA 4", ["$\\tr(2B(A+B^t))$ con $A=\\begin{pmatrix}3&-1\\\\2&-3\\end{pmatrix}$, $B=\\begin{pmatrix}-1&-2\\\\0&2\\end{pmatrix}$:",
                                           "$A+B^t=\\begin{pmatrix}2&-1\\\\0&-1\\end{pmatrix}$; diagonal de $B(A+B^t)$: $-2$ y $-2$ \\ $\\Rightarrow$ \\ $2\\cdot(-4)=-8$"], size=23, width=12.4)
        self.push(a, "Aplicado, 1S 2025: para una traza solo hacen falta las entradas de la diagonal. Dos productos fila por columna, y da −8.", anim=FadeIn(a))
        a2 = apl("1S 2023 VESPERTINO · PREGUNTA 3", ["$A\\,\\delta(1,1)$ conserva solo la columna 1 de $A$ \\ $\\Rightarrow$ \\ $\\tr=a_{11}=1+1=2$"],
                 size=23, width=12.4)
        self.push(a2, "Y las matrices delta, con un solo uno: A por delta(1,1) se queda con la primera columna. Traza: a11, que vale 2.", anim=FadeIn(a2))
        self.end_scene()


# =====================================================================
class V1_06_Inversa(V1):
    CH_NUM = "06"
    CH_TITLE = "Inversa: deshacer"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Inversa", "la máquina que deshace", prob=("MUY ALTA", "en los 4 parciales más recientes"))
        A = [[2, 1], [1, 1]]
        Ai = [[1, -1], [-1, 2]]
        q = full_plane()
        vb = base_vectors()
        self.play(Create(q), GrowArrow(vb[0]), GrowArrow(vb[1]), run_time=0.7)
        self.bring_to_front(*self.persist)
        pan = mpanel(VGroup(MathTex("A=", font_size=38), mat_cols(A, 38)).arrange(RIGHT, buff=0.12), [-5.0, 2.4, 0])
        self.say("La inversa es la máquina que **deshace** lo que hizo A.", FadeIn(pan), apply_to(q, A), Transform(vb, base_vectors(A)), run_time=1.5)
        pan2 = mpanel(VGroup(MathTex("A^{-1}=", font_size=38), mat_cols(Ai, 38)).arrange(RIGHT, buff=0.12), [-5.0, 1.0, 0])
        self.say("Aplico la inversa y la grilla vuelve exacta. Si A aplastara el plano, no habría forma de volver: por eso solo las que no aplastan tienen inversa.",
                 FadeIn(pan2), apply_to(q, Ai), Transform(vb, base_vectors()), run_time=1.8)
        f = self.stamp(["$\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}^{-1}=\\dfrac{1}{ad-bc}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}$"], "2×2", size=28)
        f.move_to([3.6, -1.7, 0])
        self.say("En dos por dos hay fórmula: intercambio la diagonal, cambio el signo de la otra, divido por el determinante.",
                 *self.show_stamp(f))
        self.wipe()

        a = apl("PRÁCTICO 4 · EJ. 1A", [
            "$\\begin{pmatrix}-3&-5\\\\2&3\\end{pmatrix}$: \\ $ad-bc=-9+10=1$ \\ $\\Rightarrow$ \\ inversa $\\begin{pmatrix}3&5\\\\-2&-3\\end{pmatrix}$",
            "chequeo, fila 1 por columna 1: \\ $(-3)(3)+(-5)(-2)=1$ ✓"], size=25, width=12.4)
        met = metodo(["Escribí $(A\\,|\\,I)$ y escalerizá las dos mitades juntas.",
                      "Si a la izquierda aparece una fila de ceros: **no es invertible**.",
                      "Si no, llegá a $(I\\,|\\,A^{-1})$ y chequeá una fila por una columna."], "GAUSS-JORDAN (3×3 EN ADELANTE)", size=23, width=12.4)
        pr = memo(["$(AB)^{-1}=B^{-1}A^{-1}$ \\quad $(A^t)^{-1}=(A^{-1})^t$ \\quad $(\\lambda A)^{-1}=\\frac1\\lambda A^{-1}$",
                   "$A+B$ puede no ser invertible aunque $A$ y $B$ lo sean: \\ $I+(-I)=O$"], width=12.4)
        stack(a, met, pr)
        self.say("Aplicado, práctico 4: el determinante da 1, así que la inversa sale directa de la fórmula. Y el chequeo de diez segundos: fila por columna da 1.",
                 FadeIn(a, shift=UP * 0.2))
        self.say("En tres por tres, Gauss-Jordan: la identidad al lado y escalerizar todo junto. Está resuelto completo en el video de ejercicios.",
                 FadeIn(met))
        self.say("Propiedades: la del producto da vuelta el orden, como sacarse zapatos y medias. Y la suma no se lleva con la inversa.",
                 FadeIn(pr))
        self.wipe()

        a = apl("2S 2016 · PREGUNTA 9", ["$\\lambda\\neq0$, $A,B$ invertibles: \\ $(\\lambda AB)^{-1}=\\frac1\\lambda B^{-1}A^{-1}$ \\ **Opción (A)**"], size=26, width=12.4)
        a.move_to([0, 2.3, 0])
        self.say("Aplicado, 2S 2016: el lambda se invierte y el orden se da vuelta.", FadeIn(a))
        self.board_start(top=1.25)
        tag = T("1S 2023 · PREGUNTA 4: INVERSA SIN CUENTAS", 18, GREEN, MONO, BOLD)
        self.push(tag, "Y el truco de la ecuación, de 1S 2023.", anim=FadeIn(tag))
        self.push(L("$A^2-2A+5I=O\\ \\Rightarrow\\ A(A-2I)=-5I$", 30), "Paso la identidad al otro lado y saco A de factor común.")
        self.push(L("$\\Rightarrow\\ A\\cdot\\frac15(2I-A)=I\\ \\Rightarrow\\ A^{-1}=\\frac15(2I-A)$ \\quad **Opción (A)**", 30, YELLOW),
                  "Divido por menos cinco y leo la inversa. Si no te queda la identidad sola del otro lado, no hay conclusión.", focus=True)
        self.end_scene()


# =====================================================================
class V1_07_Rango(V1):
    CH_NUM = "07"
    CH_TITLE = "Rango: cuánto sobrevive"

    def construct(self):
        self.setup_frame()
        ghost = plano((-8, 8), (-5, 5), unit=1.0).set_opacity(0.2)
        q = full_plane()
        vb = base_vectors()
        self.add(ghost, q, vb)
        self.bring_to_front(*self.persist)
        M1 = [[1, 2], [0.5, 4]]
        M2 = [[1, 2], [2, 4]]
        pan = mpanel(VGroup(MathTex("A=", font_size=38), mat_cols([[1, 2], ["t", 4]], 38)).arrange(RIGHT, buff=0.12), [-5.1, 2.4, 0])
        self.add(pan)
        self.say("El rango mide **cuánto sobrevive** del plano. Con t = 1/2 la máquina deforma pero todavía llena el plano: rango 2.",
                 apply_to(q, M1), Transform(vb, base_vectors(M1)), run_time=1.6)
        Mf = np.array(M2, dtype=float) @ np.linalg.inv(np.array(M1, dtype=float))
        labb = boxed(T("t = 2: segunda columna = doble de la primera · rango 1", 24, RED, SANS, BOLD)).move_to([1.4, -1.9, 0])
        self.say("Con t = 2 las columnas quedan alineadas y **todo cae en una recta**: rango 1. Puntos distintos caen al mismo lugar; no se puede deshacer.",
                 ApplyMatrix(Mf, q, about_point=ORIGIN), Transform(vb, base_vectors(M2)), FadeIn(labb), run_time=2.4, focus=True)
        self.wipe()

        d = self.stamp(["$\\rg(A)$ = filas no nulas de **una forma escalonada** de $A$ (= pivotes)"], "RANGO", size=28)
        d.move_to([0, 2.3, 0])
        self.say("La definición para escribir: filas no nulas de una forma **escalonada**. No de A: de la escalonada.", *self.show_stamp(d))
        m = Mat([[1, 2, 3], [4, 5, 6], [7, 8, 9]], size=36).move_to([-3.0, 0.0, 0])
        tag = T("PRÁCTICO 4 · EJ. 2.1B(A)", 18, GREEN, MONO, BOLD).next_to(m, UP, buff=0.2)
        self.say("Aplicado, práctico 4: la famosa del uno al nueve.", FadeIn(tag), FadeIn(m))
        m = self.rowop(m, [[1, 2, 3], [0, -3, -6], [0, -6, -12]], r"F_2-4F_1,\ F_3-7F_1", "Ceros en la primera columna.", changed=[1, 2], size=36)
        m = self.rowop(m, [[1, 2, 3], [0, -3, -6], [0, 0, 0]], r"F_3-2F_2", "La tercera fila se anula: dos pivotes, **rango 2**.", changed=[2], size=36)
        tr = trampa(["Tres filas no nulas en $A$, pero rango 2: \\ la tercera era $2F_2-F_1$."], width=6.0)
        tr.move_to([3.6, -1.6, 0])
        self.play(FadeIn(tr), run_time=0.3)
        self.w(0.6)
        self.wipe()

        pm = metodo(["Igual que en sistemas: escalerizá sin dividir por el parámetro.",
                     "Críticos = donde se anula un pivote (= raíces de $\\det A$ si es cuadrada)."], "RANGO CON PARÁMETRO", size=23, width=12.4)
        pm.move_to([0, 2.2, 0])
        self.say("Rango con parámetro: el mismo método que en sistemas.", FadeIn(pm))
        m = Mat([["k", "1+k"], ["k", 2]], size=38).move_to([-3.2, -0.2, 0])
        tag = T("1S 2025 · PREGUNTA 2", 18, GREEN, MONO, BOLD).next_to(m, UP, buff=0.2)
        self.say("Aplicado, 1S 2025, pregunta 2.", FadeIn(tag), FadeIn(m))
        m = self.rowop(m, [["k", "1+k"], [0, "1-k"]], r"F_2-F_1", "Fila 2 menos fila 1: quedan k y 1 − k en la diagonal.", changed=[1], size=38)
        r = VGroup(L("$k\\neq0,1$: \\ $\\rg=2$", 26), L("$k=1$: $\\begin{pmatrix}1&2\\\\0&0\\end{pmatrix}$ \\ $\\rg=1$", 26),
                   L("$k=0$: $\\begin{pmatrix}0&1\\\\0&1\\end{pmatrix}$ filas iguales, \\ $\\rg=1$", 26), L("dos valores con rango 1: \\ **Opción (B)**", 24, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        r.move_to([3.3, -0.65, 0])
        self.say("Críticos: 0 y 1. En k = 1 se anula la segunda fila. En k = 0, cuidado: la primera columna es cero y las dos filas quedan iguales, así que un paso más la anula. Rango 1 en los dos casos: opción B.",
                 FadeIn(r), focus=True)
        self.end_scene()


# =====================================================================
class V1_08_Determinante(V1):
    CH_NUM = "08"
    CH_TITLE = "Determinante: el factor de área"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Determinantes", "cuánto se estira el área", prob=("MUY ALTA", "9 de 14 · y 8 más de expresiones"))
        a, b, c, d = [ValueTracker(v) for v in (1.0, 0.0, 0.0, 1.0)]
        p = plano((-8, 8), (-5, 5), unit=1.0).set_opacity(0.5)
        self.add(p)
        self.bring_to_front(*self.persist)
        col1 = lambda: complex(a.get_value(), c.get_value())
        col2 = lambda: complex(b.get_value(), d.get_value())
        detv = lambda: a.get_value() * d.get_value() - b.get_value() * c.get_value()

        def par():
            pts = [p.n2p(0), p.n2p(col1()), p.n2p(col1() + col2()), p.n2p(col2())]
            dv = detv()
            col = YELLOW if dv > 0.01 else (RED if dv < -0.01 else GRAY)
            return VGroup(Polygon(*pts, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35),
                          flecha(p, col1(), I_COL, 6), flecha(p, col2(), J_COL, 6))

        pg = always_redraw(par)
        lab = MathTex(r"\det A=ad-bc=", font_size=40)
        num = Num(1.0, num_decimal_places=2, font_size=44, color=YELLOW)
        panel = VGroup(lab, num).arrange(RIGHT, buff=0.15).move_to([-4.2, 2.4, 0])
        num.add_updater(lambda m: m.set_value(detv()).next_to(lab, RIGHT, buff=0.15))
        bgp = SurroundingRectangle(panel, buff=0.2, stroke_width=0).set_fill(BG, 0.9)
        self.say("El cuadradito de los vectores base tiene área 1. El **determinante** es por cuánto multiplica las áreas la máquina.",
                 FadeIn(pg), FadeIn(bgp), FadeIn(panel))
        self.say("Con columnas (3, 0) y (1, 2), el cuadrado se vuelve un paralelogramo de área 6: 3 por 2 menos 1 por 0.",
                 a.animate.set_value(3.0), b.animate.set_value(1.0), d.animate.set_value(2.0), run_time=2.0)
        self.say("Achico d: se aplasta, y en det = 0 es una recta. Paso de largo: queda **dado vuelta**, determinante negativo.",
                 d.animate.set_value(-1.0), run_time=2.6, focus=True)
        self.play(d.animate.set_value(2.0), run_time=0.8)
        pg.clear_updaters(); num.clear_updaters()
        s = self.stamp(["$|\\det A|$ = factor de área \\quad signo = orientación",
                        "$\\det A=0\\iff$ aplasta $\\iff$ no invertible"], "LA IMAGEN", size=26)
        s.scale_to_fit_width(min(s.width, 7.2))
        s.move_to([3.0, -1.8, 0])
        self.say("Eso es todo: factor de área con signo. Cero es aplastar, y aplastar es no tener inversa.", *self.show_stamp(s))
        self.wipe()

        self.board_start(top=2.7)
        self.push(L("$2\\times2$: $ad-bc$. \\ $3\\times3$: Sarrus o **desarrollo por la fila o columna con más ceros**.", 26),
                  "Para calcular: ad menos bc en dos por dos; en tres por tres, Sarrus o desarrollo por la fila con más ceros.")
        self.push(L("Grandes: $F_i\\to F_i+\\lambda F_j$ (no cambia) hasta **triangular** $\\Rightarrow$ producto de la diagonal.", 26),
                  "En las grandes: sumar múltiplos de filas no cambia el determinante; llevás a triangular y multiplicás la diagonal.")
        a1 = apl("PRÁCTICO 5 · EJ. 3A: ¿PARA QUÉ k ES INVERTIBLE?", [
            "$\\begin{vmatrix}k&-k&3\\\\0&k+1&1\\\\k&-8&k-1\\end{vmatrix}=k(k-2)^2$ \\quad $\\Rightarrow$ \\quad invertible $\\iff k\\neq0$ y $k\\neq2$"], size=25, width=12.4)
        self.push(a1, "Aplicado, práctico 5: con parámetro, calculás el determinante, lo **factorizás**, y la matriz es invertible donde no se anula.", anim=FadeIn(a1))
        a2 = apl("1S 2019 · PREGUNTA 5", ["Una $6\\times6$: restando la fila 1 a todas queda triangular, diagonal $1,-2,-2,-2,1,1$ \\ $\\Rightarrow\\det=-8$"],
                 size=24, width=12.4)
        self.push(a2, "Y una seis por seis de 2019: una ronda de restas y quedó triangular. Menos ocho.", anim=FadeIn(a2))
        self.end_scene()


# =====================================================================
class V1_09_DetPropiedades(V1):
    CH_NUM = "09"
    CH_TITLE = "Propiedades del determinante"

    def construct(self):
        self.setup_frame()
        p = plano((-8, 8), (-5, 5), unit=1.0).set_opacity(0.45).shift(RIGHT * 2.2)
        self.add(p)
        self.bring_to_front(*self.persist)
        A0 = np.array([[2.0, 0.5], [0.0, 1.5]])
        M = [ValueTracker(v) for v in A0.flatten()]
        cur = lambda: np.array([[M[0].get_value(), M[1].get_value()], [M[2].get_value(), M[3].get_value()]])

        def par():
            X = cur()
            c1, c2 = complex(X[0, 0], X[1, 0]), complex(X[0, 1], X[1, 1])
            dv = np.linalg.det(X)
            col = YELLOW if dv > 0.01 else (RED if dv < -0.01 else GRAY)
            return VGroup(Polygon(p.n2p(0), p.n2p(c1), p.n2p(c1 + c2), p.n2p(c2), stroke_color=col, stroke_width=3,
                                  fill_color=col, fill_opacity=0.35), flecha(p, c1, I_COL, 6), flecha(p, c2, J_COL, 6))

        pg = always_redraw(par)
        lab = T("área =", 28, INK)
        num = Num(3.0, num_decimal_places=2, font_size=40, color=YELLOW)
        VGroup(lab, num).arrange(RIGHT, buff=0.15).move_to([-4.6, 2.4, 0])
        num.add_updater(lambda m: m.set_value(np.linalg.det(cur())).next_to(lab, RIGHT, buff=0.15))
        self.add(pg, lab, num)

        def regla(tex, y, color=INK):
            r = L(tex, 25, color)
            if r.width > 5.4:
                r.scale_to_fit_width(5.4)
            r.move_to([0, y, 0]).align_to([-6.8, 0, 0], LEFT)
            return boxed(r, 0.85)

        self.say("Las propiedades se ven. Sumar a una columna un múltiplo de otra: se desliza y el área **no cambia**.",
                 FadeIn(regla("**Sumar un múltiplo** de otra: igual", 1.5)), M[1].animate.set_value(2.5), run_time=2.2)
        self.play(M[1].animate.set_value(0.5), run_time=0.6)
        self.say("Multiplicar una fila por lambda estira en una dirección: área por **lambda**.",
                 FadeIn(regla("**Una fila** por $\\lambda$: $\\times\\lambda$", 0.8)), M[0].animate.set_value(4.0), M[1].animate.set_value(1.0), run_time=1.8)
        self.play(M[0].animate.set_value(2.0), M[1].animate.set_value(0.5), run_time=0.6)
        self.say("Toda la matriz por 2 estira las dos direcciones: área por **4**. Lambda a la n, la trampa más cara.",
                 FadeIn(regla("$\\det(\\lambda A)=\\lambda^n\\det A$", 0.1, YELLOW)), *[m.animate.set_value(2 * v) for m, v in zip(M, A0.flatten())],
                 run_time=2.0, focus=True)
        self.play(*[m.animate.set_value(v) for m, v in zip(M, A0.flatten())], run_time=0.6)
        self.say("Intercambiar filas es un espejo: mismo tamaño, **signo opuesto**.",
                 FadeIn(regla("**Intercambiar** filas: cambia el signo", -0.6)), M[0].animate.set_value(0.0), M[2].animate.set_value(2.0),
                 M[1].animate.set_value(1.5), M[3].animate.set_value(0.5), run_time=2.0)
        self.say("Y el producto: si una máquina multiplica las áreas por 3 y otra por 2, juntas por 6.",
                 FadeIn(regla("$\\det(AB)=\\det A\\,\\det B$", -1.3, YELLOW)))
        pg.clear_updaters(); num.clear_updaters()
        self.wipe()

        a = apl("PRÁCTICO 5 · EJ. 2 (det A = 5)", [
            "$(d,e,f;\\ g,h,j;\\ a,b,c)$: cíclica = dos intercambios \\ $\\to5$",
            "$(-a,-b,-c;\\ 2d,2e,2f;\\ -g,-h,-j)$: $(-1)(2)(-1)$ \\ $\\to10$",
            "$(a,b,c;\\ d-3a,\\dots;\\ 2g,2h,2j)$: la resta no cambia, el 2 sí \\ $\\to10$"], size=24, width=12.4)
        b = apl("PRÁCTICO 5 · EJ. 4A (det A = 3, det B = −2, n×n)", [
            "$\\det(2A)=2^n\\cdot3$ \\quad $\\det(A^2)=9$ \\quad $\\det(B^{-1}A)=-\\frac32$ \\quad $\\det(AA^t)=9$ \\quad $\\det(-AB)=(-1)^n(-6)$"],
                size=24, width=12.4)
        tr = trampa(["$\\det(A+B)\\neq\\det A+\\det B$ \\quad $\\det A=0$ no implica una fila de ceros"], width=12.4)
        stack(a, b, tr)
        self.say("Aplicado, práctico 5, con det A = 5. Reordenar cíclico son dos intercambios. Los factores de cada fila multiplican. Restar filas no cambia nada.",
                 FadeIn(a, shift=UP * 0.2))
        self.say("Y con expresiones: el dos sale a la n, la inversa invierte, la traspuesta no cambia, y el menos también sale a la n.",
                 FadeIn(b, shift=UP * 0.2), focus=True)
        self.play(FadeIn(tr), run_time=0.3)
        self.w(0.8)
        self.end_scene()


# =====================================================================
class V1_10_Mapa(V1):
    CH_NUM = "10"
    CH_TITLE = "El mapa del parcial"

    def construct(self):
        self.setup_frame()
        te = self.stamp(["$A$ invertible $\\iff\\rg(A)=n\\iff\\det A\\neq0$",
                         "$\\iff AX=b$ es SCD para todo $b\\iff AX=0$ solo tiene la trivial",
                         "$\\iff$ no aplasta el plano"], "TEOREMA DE LA MATRIZ INVERTIBLE", size=26)
        t = tabla([["te preguntan", "herramienta"],
                   ["discutir un sistema según $a$", "escalerizar $(A|b)$, críticos, sustituir"],
                   ["rango según $a$", "escalerizar; críticos = raíces de $\\det$"],
                   ["entradas de $A^{-1}$", "Gauss-Jordan $(A|I)$ + chequeo"],
                   ["$\\det A=k$, ¿$\\det B$?", "sacar factores, restar filas, contar intercambios"],
                   ["$\\det$ de una expresión", "factorizar respetando el orden, $\\lambda^n$"],
                   ["inversa desde una ecuación", "factor común hasta $A\\cdot(\\dots)=I$"],
                   ["complejos", "polar: módulos multiplican, ángulos suman"]], size=21, h=0.44)
        stack(te, t, buff=0.3)
        self.say("Volvemos al principio: es una sola pregunta. Invertible, rango completo, determinante distinto de cero, sistema determinado: **no aplasta**.",
                 *self.show_stamp(te), focus=True)
        self.say("Y la tabla del parcial: qué te preguntan y con qué herramienta se contesta. Con esto claro, el video de ejercicios es aplicarla siete veces.",
                 FadeIn(t))
        self.say("Éxitos el sábado. **Escalerizá con calma y chequeá siempre.**", focus=True)
        self.end_scene()
