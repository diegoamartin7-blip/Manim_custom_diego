"""
VIDEO 1 - TEORIA VISUAL  (de los complejos a los determinantes)
  Intro: el radar del parcial y el hilo conductor
  Complejos: girar y estirar, polar, De Moivre, raices
  Sistemas: rectas que se cruzan, escalerizar, Rouche-Frobenius
  Matrices: maquinas que mueven el plano, composicion, AB != BA
  Inversa y rango: deshacer, aplastar, Gauss-Jordan
  Determinantes: el factor de area
Todas las cuentas estan en gal1_teoria/verify.py (sympy).
"""
from gal_base import *

SCENE_ORDER = ["V1_00_Intro", "V1_01_Complejos", "V1_02_Raices", "V1_03_Sistemas",
               "V1_04_Escalerizar", "V1_05_Matrices", "V1_06_Producto",
               "V1_07_Inversa", "V1_08_Rango", "V1_09_Determinante", "V1_10_DetPropiedades"]


class V1(GBase, MatScene):
    VIDEO_TAG = "VIDEO 1 · TEORÍA VISUAL"


I_COL = GREEN     # i-sombrero (primera columna)
J_COL = RED       # j-sombrero (segunda columna)


REF = None


def ref_plane():
    """Plano fijo (sin deformar) para ubicar flechas: los planos animados se deforman
    y sus n2p ya no sirven como coordenadas."""
    global REF
    if REF is None:
        REF = plano((-8, 8), (-5, 5), unit=1.0)
    return REF


def base_vectors(p, A=((1, 0), (0, 1))):
    """Flechas de las columnas de A sobre el plano p (que tiene que estar sin deformar)."""
    c1 = complex(A[0][0], A[1][0])
    c2 = complex(A[0][1], A[1][1])
    return VGroup(flecha(p, c1, I_COL, 6), flecha(p, c2, J_COL, 6))


def mat_cols(A, size=36):
    """Matriz 2x2 con la columna 1 en verde y la 2 en rojo."""
    m = Mat([[A[0][0], A[0][1]], [A[1][0], A[1][1]]], size=size, h_buff=0.75, v_buff=0.6)
    mcol(m, 0).set_color(I_COL)
    mcol(m, 1).set_color(J_COL)
    return m


def label_panel(mob, corner=UL):
    bg = SurroundingRectangle(mob, buff=0.18, stroke_width=0).set_fill(BG, 0.85)
    return VGroup(bg, mob)


# =====================================================================
class V1_00_Intro(V1):
    def construct(self):
        self.setup_frame(header=False)
        t1 = T("GAL 1 · IMERL · FING · 2S 2026", 22, SOFT, MONO)
        t2 = T("Geometría y Álgebra Lineal 1", 64, INK, SANS, BOLD)
        t3 = T("Primer parcial · sábado 3 de octubre, 15:00", 36, BLUE, SANS, BOLD)
        t4 = T("La teoría que entra, vista como movimiento.", 26, SOFT)
        g = VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.3).shift(UP * 0.6)
        self.play(FadeIn(t1, shift=DOWN * 0.2), Write(t2), run_time=1.5)
        self.play(FadeIn(t3, shift=UP * 0.2), FadeIn(t4), run_time=0.8)
        self.say("Este es el primero de dos videos. Acá va **toda la teoría** del parcial, desde los números complejos hasta los determinantes.")
        self.say("Pero no como lista de fórmulas: cada idea la vamos a **ver moverse**. Si entendés qué hace una matriz con el plano, la mitad de las propiedades salen solas.")
        self.wipe()

        # ---- el radar
        datos = [("Sistema con parámetro", 11, RED), ("Determinante: propiedades o escalerizar", 9, RED),
                 ("Rango (casi siempre con parámetro)", 8, RED), ("Determinante de expresiones", 8, ORANGE),
                 ("Inversa de una matriz numérica", 6, RED), ("Traza y matrices por fórmula", 6, TEAL),
                 ("Inversa a partir de una ecuación", 4, ORANGE)]
        tit = T("En cuántos de los 14 parciales (2016 a 2025) apareció", 28, INK, SANS, BOLD).move_to([0, 2.8, 0])
        barras = VGroup()
        for i, (nom, k, c) in enumerate(datos):
            y = 1.95 - i * 0.6
            lab = T(nom, 22, INK)
            lab.move_to([0, y, 0]).align_to([-0.4, 0, 0], RIGHT)
            bar = Rectangle(width=k * 0.42, height=0.36, stroke_width=0).set_fill(c, 0.85)
            bar.move_to([-0.2, y, 0], aligned_edge=LEFT)
            num = T(f"{k}", 22, c, MONO, BOLD).next_to(bar, RIGHT, buff=0.15)
            barras.add(VGroup(lab, bar, num))
        self.say("Primero, el radar. Leí los catorce primeros parciales de 2016 a 2025 y conté cuántas veces salió cada tipo de ejercicio.",
                 Write(tit),
                 LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
                               for b in barras], lag_ratio=0.25, run_time=3.5))
        caja = SurroundingRectangle(VGroup(barras[0], barras[2], barras[4]), color=GOLD, buff=0.1)
        self.say("Sistemas con parámetro, rango, inversa y determinantes aparecieron en **los cuatro parciales más recientes**. Son la mitad del parcial, y son las más mecánicas.")
        nota = T("Geometría NO entra este año (paro)   ·   Complejos es nuevo: esperá 1 o 2 preguntas", 21, SOFT).move_to([0, -2.2, 0])
        self.say("La geometría no entra este año. Y complejos, que antes no estaba en el programa, seguramente ocupe **una o dos** de las preguntas que antes eran de geometría.",
                 FadeIn(nota))
        self.wipe()

        # ---- el hilo conductor
        nombres = [("COMPLEJOS", "girar y estirar", TEAL), ("SISTEMAS", "cruzar ecuaciones", BLUE),
                   ("MATRICES", "mover el plano", GREEN), ("INVERSA · RANGO", "deshacer · aplastar", ORANGE),
                   ("DETERMINANTE", "factor de área", RED)]
        nodos = VGroup(*[node(a, b, c, w=2.35) for a, b, c in nombres]).arrange(RIGHT, buff=0.32)
        if nodos.width > 13.4:
            nodos.scale_to_fit_width(13.4)
        nodos.move_to([0, 0.9, 0])
        fl = VGroup(*[Arrow(nodos[i].get_right(), nodos[i + 1].get_left(), buff=0.05, color=DIM,
                            stroke_width=3, max_tip_length_to_length_ratio=0.4) for i in range(4)])
        self.say("El camino del curso tiene cinco estaciones. Y hay **un solo hilo** que las une.",
                 LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in nodos], lag_ratio=0.2, run_time=2.4),
                 Create(fl))
        s = self.stamp(["Una matriz es una **máquina que mueve el plano**.",
                        "Sistemas, inversa, rango y determinante son preguntas sobre esa máquina."],
                       "EL HILO", size=28)
        s.move_to([0, -1.3, 0])
        self.say("Una matriz es una máquina que mueve el plano. Resolver un sistema, invertir, calcular el rango o el determinante son **preguntas sobre esa máquina**.",
                 *self.show_stamp(s))
        self.say("El video 2 son los ejercicios de parcial, resueltos paso a paso. Este va primero: la teoría que los hace fáciles.")
        self.end_scene()


# =====================================================================
class V1_01_Complejos(V1):
    CH_NUM = "01"
    CH_TITLE = "Números complejos"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Números complejos", "girar y estirar", prob=("ALTA", "nuevo en el programa de este año"))
        p = plano((-5, 5), (-3, 3), unit=0.72).shift(LEFT * 2.6 + DOWN * 0.15)
        o = p.n2p(0)
        re_l = MathTex(r"\Re", font_size=30, color=SOFT).next_to(p.x_axis.get_end(), DOWN, buff=0.1)
        im_l = MathTex(r"\Im", font_size=30, color=SOFT).next_to(p.y_axis.get_end(), RIGHT, buff=0.1)
        self.say("Un número complejo a + bi es un **punto del plano**: a sobre el eje real, b sobre el eje imaginario.",
                 Create(p), FadeIn(re_l), FadeIn(im_l), run_time=1.5)

        z = 3 + 2j
        az = flecha(p, z, BLUE)
        dz = VGroup(DashedLine(p.n2p(z), p.n2p(3), color=DIM), DashedLine(p.n2p(z), p.n2p(2j), color=DIM))
        lz = MathTex("z=3+2i", font_size=32, color=BLUE).next_to(az.get_end(), UR, buff=0.08)
        lab_a = MathTex("3", font_size=28, color=SOFT).next_to(p.n2p(3), DOWN, buff=0.12)
        lab_b = MathTex("2", font_size=28, color=SOFT).next_to(p.n2p(2j), LEFT, buff=0.12)
        self.say("Por ejemplo z = 3 + 2i, pensado como una **flecha** desde el origen.",
                 GrowArrow(az), Create(dz), FadeIn(lz), FadeIn(lab_a), FadeIn(lab_b))

        # panel derecho
        panel_x = 4.3
        rules = VGroup(
            L("$i^2=-1$", 28),
            L("$|z|=\\sqrt{a^2+b^2}$", 28),
            L("$\\bar z=a-bi$", 28),
            L("$z\\,\\bar z=|z|^2$", 28, YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([panel_x, 1.2, 0])
        mod = Line(o, p.n2p(z), color=GOLD, stroke_width=7)
        self.say("El **módulo** es el largo de la flecha. Pitágoras: √(9 + 4) = √13.",
                 FadeIn(rules[:2]), ShowPassingFlash(mod, time_width=0.6), run_time=1.2)
        zc = flecha(p, z.conjugate(), TEAL)
        lzc = MathTex(r"\bar z=3-2i", font_size=32, color=TEAL).next_to(zc.get_end(), DR, buff=0.08)
        self.say("El **conjugado** refleja en el eje real. Y z por su conjugado da |z|², un real: con eso se divide.",
                 ReplacementTransform(az.copy(), zc), FadeIn(lzc), FadeIn(rules[2:]))
        self.wipe(p, re_l, im_l)

        # ---- suma: paralelogramo
        z, w = 2 + 1j, 1 + 2j
        az = flecha(p, z, BLUE)
        aw = flecha(p, w, TEAL)
        lz = MathTex("z", font_size=34, color=BLUE).next_to(az.get_end(), RIGHT, buff=0.1)
        lw = MathTex("w", font_size=34, color=TEAL).next_to(aw.get_end(), LEFT, buff=0.1)
        self.say("Sumar es **encadenar flechas**: pongo w a continuación de z.",
                 GrowArrow(az), GrowArrow(aw), FadeIn(lz), FadeIn(lw))
        aw2 = flecha(p, z + w, TEAL, origin=z).set_opacity(0.6)
        s = flecha(p, z + w, YELLOW)
        ls = MathTex("z+w", font_size=34, color=YELLOW).next_to(s.get_end(), UR, buff=0.08)
        self.say("La suma es la diagonal del paralelogramo. Vectores del plano, nada nuevo.",
                 ReplacementTransform(aw.copy(), aw2), GrowArrow(s), FadeIn(ls))
        self.wipe(p, re_l, im_l)

        # ---- multiplicar por i: girar 90
        z = 2 + 1j
        az = flecha(p, z, BLUE)
        lz = MathTex("z", font_size=34, color=BLUE).next_to(az.get_end(), RIGHT, buff=0.1)
        self.say("Ahora lo lindo: ¿qué le hace a una flecha **multiplicarla por i**?",
                 GrowArrow(az), FadeIn(lz))
        cols = [YELLOW, ORANGE, VIOLET]
        prev = az
        cur = z
        tags = ["iz", "i^2z=-z", "i^3z=-iz"]
        arcs = VGroup()
        for k in range(3):
            nxt = cur * 1j
            a2 = flecha(p, nxt, cols[k])
            lab = MathTex(tags[k], font_size=30, color=cols[k]).next_to(a2.get_end(), a2.get_end() - o, buff=0.1)
            arc = Arc(radius=0.55, start_angle=np.angle(cur), angle=PI / 2, arc_center=o, color=cols[k], stroke_width=3)
            txt = ("Multiplicar por i **gira 90 grados** sin cambiar el largo: i(2 + i) = −1 + 2i." if k == 0 else
                   "Otra vez: i²z = −z, apunta al revés." if k == 1 else
                   "Y otra. A la cuarta, i⁴ = 1: volvemos al inicio. Las potencias de i se repiten **cada cuatro**.")
            self.say(txt, Rotate(prev.copy().set_color(cols[k]), PI / 2, about_point=o), Create(arc), run_time=1.2)
            self.add(a2)
            self.play(FadeIn(lab), run_time=0.3)
            arcs.add(arc)
            prev, cur = a2, nxt
        self.wipe(p, re_l, im_l)

        # ---- multiplicar por w cualquiera: girar arg w y estirar |w|
        z = 2 + 0.6j
        th = ValueTracker(0.0)
        r = ValueTracker(1.0)
        wv = lambda: r.get_value() * np.exp(1j * th.get_value())
        az = flecha(p, z, BLUE)
        lz = MathTex("z", font_size=34, color=BLUE).next_to(az.get_end(), DOWN, buff=0.1)
        aw = always_redraw(lambda: flecha(p, wv(), TEAL, 5))
        azw = always_redraw(lambda: flecha(p, z * wv(), YELLOW, 6))
        lzw = always_redraw(lambda: MathTex("zw", font_size=32, color=YELLOW).next_to(p.n2p(z * wv()), UR, buff=0.06))
        sl1 = Slider("$\\arg w$", th, 0, 2.2, color=TEAL, width=2.4, decimals=2, size=24).move_to([4.2, 1.7, 0])
        sl2 = Slider("$|w|$", r, 0.5, 1.6, color=TEAL, width=2.4, decimals=2, size=24).move_to([4.2, 1.0, 0])
        rule = VGroup(L("$|zw|=|z|\\,|w|$", 28), L("$\\arg(zw)=\\arg z+\\arg w$", 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rule.move_to([4.2, -0.4, 0])
        self.say("En general, multiplicar por w hace dos cosas a la vez: **gira** el ángulo de w y **estira** por el largo de w.",
                 GrowArrow(az), FadeIn(lz), FadeIn(aw), FadeIn(azw), FadeIn(lzw), FadeIn(sl1), FadeIn(sl2))
        self.say("Muevo el ángulo de w: la amarilla gira exactamente lo mismo.",
                 th.animate.set_value(1.6), run_time=2.5)
        self.say("Agrando |w|: la amarilla se estira en la misma proporción.",
                 r.animate.set_value(1.5), run_time=2.0)
        self.say("Esa es la regla: los módulos **se multiplican**, los ángulos **se suman**.",
                 FadeIn(rule), th.animate.set_value(0.8), r.animate.set_value(0.8), run_time=2.0)
        aw.clear_updaters(); azw.clear_updaters(); lzw.clear_updaters()
        self.wipe(p, re_l, im_l)

        # ---- forma polar
        s = self.stamp(["$z=|z|\\,(\\cos\\theta+i\\sin\\theta)=|z|\\,e^{i\\theta}$",
                        "$re^{i\\theta}\\cdot se^{i\\varphi}=rs\\,e^{i(\\theta+\\varphi)}$",
                        "**De Moivre:** $(re^{i\\theta})^n=r^n e^{in\\theta}$"], "FORMA POLAR", size=30)
        s.scale_to_fit_width(min(s.width, 5.5))
        s.move_to([4.1, 0.9, 0])
        z = -1 + np.sqrt(3) * 1j
        az = flecha(p, z, BLUE)
        arc = Arc(radius=0.6, start_angle=0, angle=np.angle(z), arc_center=o, color=GOLD, stroke_width=3)
        lth = MathTex(r"\theta=\tfrac{2\pi}{3}", font_size=28, color=GOLD).move_to(o + 0.95 * UR + 0.1 * LEFT)
        lz = MathTex(r"-1+i\sqrt3=2e^{i2\pi/3}", font_size=28, color=BLUE).next_to(az.get_end(), UP, buff=0.08)
        self.say("De ahí la **forma polar**: largo y ángulo. Multiplicar es multiplicar largos y sumar ángulos.",
                 *self.show_stamp(s))
        self.say("Ejemplo: −1 + i√3 tiene largo 2, segundo cuadrante, 120 grados.",
                 GrowArrow(az), Create(arc), FadeIn(lth), FadeIn(lz))
        tr = trampa(["$\\arctan\\frac ba$ da lo mismo para $1+i$ y para $-1-i$.",
                     "Dibujá el punto y **ubicá el cuadrante**."], width=5.5)
        tr.move_to([4.1, -1.3, 0])
        self.say("Trampa clásica: el arcotangente no ve el cuadrante; 1 + i y −1 − i le dan igual. **Siempre dibujá el punto.**",
                 FadeIn(tr, shift=UP * 0.2), focus=True)
        self.wipe(p, re_l, im_l)

        # ---- De Moivre: espiral de potencias
        w = 1.12 * np.exp(1j * PI / 6)
        dots = VGroup()
        arrows = VGroup()
        for n in range(0, 10):
            q = w ** n
            dots.add(Dot(p.n2p(q), radius=0.06, color=interpolate_color(ManimColor(TEAL), ManimColor(YELLOW), n / 9)))
        lab = MathTex(r"w=1{,}12\,e^{i\pi/6}", font_size=30, color=TEAL).move_to([4.0, 1.8, 0])
        self.say("De Moivre en imagen: cada vez que multiplico por w giro 30 grados y estiro un poco. Las potencias hacen una **espiral**.",
                 FadeIn(lab), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.25, run_time=3.0))
        path = VMobject(color=YELLOW, stroke_width=2).set_points_smoothly([d.get_center() for d in dots])
        ex = VGroup(L("$(1+i)^{10}=(\\sqrt2\\,e^{i\\pi/4})^{10}$", 28),
                    L("$=32\\,e^{i10\\pi/4}=32\\,e^{i\\pi/2}=32i$", 28, YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ex.scale_to_fit_width(min(ex.width, 5.4))
        ex.move_to([4.1, -0.3, 0])
        self.say("Así (1 + i)¹⁰ sale en dos renglones: largo (√2)¹⁰ = 32, ángulo 10 · 45° = 450°, o sea 90°: da 32i.",
                 Create(path), FadeIn(ex))
        self.end_scene()


# =====================================================================
class V1_02_Raices(V1):
    CH_NUM = "01"
    CH_TITLE = "Raíces n-ésimas"

    def construct(self):
        self.setup_frame()
        p = plano((-3, 3), (-3, 3), unit=0.95).shift(LEFT * 3.0 + DOWN * 0.2)
        o = p.n2p(0)
        self.play(Create(p), run_time=1.0)
        n = ValueTracker(3)
        circ = Circle(radius=p.x_axis.unit_size * 2, color=DIM, stroke_width=2).move_to(o)

        def poly():
            k = int(round(n.get_value()))
            pts = [p.n2p(2 * np.exp(1j * 2 * PI * j / k)) for j in range(k)]
            g = VGroup(Polygon(*pts, color=RED, stroke_width=3))
            for q in pts:
                g.add(Dot(q, radius=0.08, color=YELLOW))
            return g

        pol = always_redraw(poly)
        eq = always_redraw(lambda: MathTex(f"z^{{{int(round(n.get_value()))}}}=2^{{{int(round(n.get_value()))}}}",
                                           font_size=40, color=INK).move_to([3.6, 2.2, 0]))
        self.say("¿Cuántas soluciones tiene z a la n igual a w? Exactamente n, y forman un **polígono regular** centrado en el origen.",
                 Create(circ), FadeIn(pol), FadeIn(eq))
        self.say("n = 3, triángulo. Subo n: cuadrado, pentágono, hexágono. Las raíces se reparten **parejas** en el círculo.",
                 n.animate.set_value(8), run_time=5, rate_func=linear)
        self.play(n.animate.set_value(3), run_time=1.2)
        pol.clear_updaters(); eq.clear_updaters()
        self.wipe(p, circ)

        s = self.stamp(["$z^n=Re^{i\\varphi}\\ \\Longrightarrow\\ z_k=\\sqrt[n]{R}\\;e^{\\,i\\frac{\\varphi+2k\\pi}{n}}$",
                        "$k=0,1,\\dots,n-1$"], "RAÍCES n-ÉSIMAS", size=28)
        s.move_to([3.5, 1.7, 0])
        if s.width > 6.6:
            s.scale_to_fit_width(6.6)
            s.move_to([3.55, 1.7, 0])
        self.say("La receta: módulo = raíz n-ésima del módulo; ángulo = ángulo de w sobre n, **más saltos de 2π/n**.",
                 *self.show_stamp(s), focus=True)
        # ejemplo z^3 = -8
        target = p.n2p(-2)
        a8 = Arrow(o, p.n2p(-2.9), buff=0, color=TEAL, stroke_width=5)
        l8 = MathTex("-8=8e^{i\\pi}", font_size=30, color=TEAL).next_to(a8.get_end(), DOWN, buff=0.35)
        self.say("Ejemplo: z³ = −8. En polar, −8 tiene largo 8 y ángulo π.",
                 GrowArrow(a8), FadeIn(l8))
        roots = [2 * np.exp(1j * (PI + 2 * k * PI) / 3) for k in range(3)]
        labs = ["1+i\\sqrt3", "-2", "1-i\\sqrt3"]
        rd = VGroup(*[Dot(p.n2p(q), radius=0.09, color=YELLOW) for q in roots])
        rl = VGroup(*[MathTex(t, font_size=28, color=YELLOW).next_to(p.n2p(q), d, buff=0.12)
                      for q, t, d in zip(roots, labs, [UR, UL, DR])])
        tri = Polygon(*[p.n2p(q) for q in roots], color=RED, stroke_width=3)
        steps = VGroup(L("módulo $\\sqrt[3]{8}=2$", 26), L("ángulos $\\frac{\\pi}{3},\\ \\pi,\\ \\frac{5\\pi}{3}$", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        steps.move_to([3.5, -0.4, 0])
        self.say("Módulo: raíz cúbica de 8, o sea 2. Ángulos: π/3, y le sumo **120 grados** dos veces.",
                 FadeIn(steps), LaggedStart(*[GrowFromCenter(d) for d in rd], lag_ratio=0.3), Create(tri))
        self.say("Raíces: 1 + i√3, −2 y 1 − i√3. Triángulo equilátero de radio 2. Dos son **conjugadas**: el polinomio tiene coeficientes reales.",
                 FadeIn(rl))
        m = memo(["Si los coeficientes del polinomio son **reales**,",
                  "las raíces complejas vienen de a pares conjugados."], width=6.6)
        m.move_to([3.5, -2.0, 0])
        self.say("Vale siempre: con coeficientes reales, si z₀ es raíz, su conjugado también.",
                 FadeIn(m, shift=UP * 0.2))
        self.end_scene()


# ---------------------------------------------------------------- utilidades
def linea(ax, A, B, C, color=BLUE, sw=4, box=None):
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
    best = max(((p, q) for p in pts for q in pts), key=lambda pq: (pq[0][0] - pq[1][0]) ** 2 + (pq[0][1] - pq[1][1]) ** 2)
    return Line(ax.c2p(*best[0]), ax.c2p(*best[1]), color=color, stroke_width=sw)


def mpanel(m, pos):
    bg = SurroundingRectangle(m, buff=0.2, stroke_width=1.2, color=DIM).set_fill(BG, 0.9)
    return VGroup(bg, m).move_to(pos)


def arrows_for(p, A):
    return base_vectors(p, A)


def apply_to(p, A):
    """ApplyMatrix sobre el plano (centrado en el origen de la escena)."""
    return ApplyMatrix(np.array(A, dtype=float), p, about_point=p.n2p(0))


# =====================================================================
class V1_03_Sistemas(V1):
    CH_NUM = "02"
    CH_TITLE = "Sistemas lineales"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Sistemas lineales", "dónde se cruzan todas", prob=("MUY ALTA", "11 de 14 parciales"))
        ax = ejes([-4, 4, 1], [-3, 3, 1], 7.2, 5.4).shift(LEFT * 2.9 + DOWN * 0.15)
        a = ValueTracker(-1.0)
        b = ValueTracker(0.0)
        l1 = linea(ax, 1, 1, 2, BLUE, 5)
        l2 = always_redraw(lambda: linea(ax, 1, a.get_value(), b.get_value(), TEAL, 5))
        e1 = MathTex("x+y=2", font_size=34, color=BLUE)
        e2 = always_redraw(lambda: MathTex(r"x" + (f"{a.get_value():+.1f}".replace(".", "{,}")) + r"\,y=" +
                                           f"{b.get_value():.1f}".replace(".", "{,}"), font_size=34, color=TEAL))
        sistema = VGroup(e1, MathTex("x+ay=b", font_size=34, color=TEAL)).arrange(DOWN, aligned_edge=LEFT).move_to([4.2, 2.3, 0])
        brace = Brace(sistema, LEFT, color=SOFT)

        def inter():
            av, bv = a.get_value(), b.get_value()
            det = av - 1
            if abs(det) < 0.03:
                return VMobject()
            y = (bv - 2) / det
            x = 2 - y
            if not (-4 <= x <= 4 and -3 <= y <= 3):
                return VMobject()
            return Dot(ax.c2p(x, y), radius=0.1, color=YELLOW)

        dot = always_redraw(inter)
        estados = {
            "SCD": T("SCD · una solución", 30, YELLOW, SANS, BOLD),
            "SI": T("SI · ninguna solución", 30, RED, SANS, BOLD),
            "SCI": T("SCI · infinitas", 30, GREEN, SANS, BOLD),
        }
        for k, v in estados.items():
            v.move_to([4.2, 0.9, 0])

        def estado():
            if abs(a.get_value() - 1) > 0.03:
                return "SCD"
            return "SCI" if abs(b.get_value() - 2) < 0.03 else "SI"

        for k, v in estados.items():
            v.add_updater(lambda m, k=k: m.set_opacity(1 if estado() == k else 0))
        self.say("Con dos incógnitas, cada ecuación es una **recta**. Resolver el sistema es buscar el punto que está en las dos a la vez.",
                 Create(ax), Create(l1), FadeIn(sistema), GrowFromCenter(brace))
        self.add(l2, dot, *estados.values())
        self.say("Si se cortan, hay una sola solución: **compatible determinado**.", Flash(dot, color=YELLOW))
        par = VGroup(Slider("$a$", a, -1, 1.5, color=TEAL, width=2.4, decimals=1, size=26),
                     Slider("$b$", b, -1, 3, color=TEAL, width=2.4, decimals=1, size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        par.move_to([4.2, -0.5, 0])
        self.play(FadeIn(par), run_time=0.4)
        self.say("Ahora muevo el parámetro a. La recta gira... y cuando a llega a 1 queda **paralela**: no se cortan nunca. **Incompatible**.",
                 a.animate.set_value(1.0), run_time=3.2)
        self.say("Con a = 1 muevo b. La paralela se desliza hasta que, en b = 2, las rectas **coinciden**: infinitas soluciones.",
                 b.animate.set_value(2.0), run_time=2.6)
        s = self.stamp(["Un sistema lineal tiene **0, 1 o infinitas** soluciones.", "Nunca exactamente 2."], "CLASIFICACIÓN", size=26)
        s.move_to([4.0, -2.0, 0])
        s.scale_to_fit_width(min(s.width, 5.8))
        self.say("Y no hay otra: cero, una o infinitas. Si hubiera dos, toda la recta que las une serían soluciones.",
                 *self.show_stamp(s))
        for v in estados.values():
            v.clear_updaters()
        l2.clear_updaters(); dot.clear_updaters()
        self.wipe()

        # ---- de ecuaciones a matrices
        sis = MathTex(r"\left\{\begin{array}{l}x-y+5z=-2\\2x+y+4z=2\\2x+4y-2z=c\end{array}\right.", font_size=40)
        m = Mat([[1, -1, 5, -2], [2, 1, 4, 2], [2, 4, -2, "c"]], bar=3, size=38)
        arrow = MathTex(r"\longrightarrow", font_size=50, color=SOFT)
        g = VGroup(sis, arrow, m).arrange(RIGHT, buff=0.5).move_to([0, 0.8, 0])
        self.say("Con tres incógnitas son planos, pero la imagen es la misma. En la práctica se trabaja con la **matriz ampliada**: coeficientes, barra, términos independientes.",
                 Write(sis), run_time=1.2)
        self.play(GrowFromCenter(arrow), ReplacementTransform(sis.copy(), m), run_time=1.0)
        lab = VGroup(L("$A$", 30, SOFT), L("$b$", 30, SOFT))
        yb = m.get_bottom()[1] - 0.35
        lab[0].move_to([VGroup(*[mcol(m, j) for j in range(3)]).get_center()[0], yb, 0])
        lab[1].move_to([mcol(m, 3).get_center()[0], yb, 0])
        self.say("A la izquierda la matriz A, a la derecha la columna b. Todo el capítulo es aprender a **leer** esta matriz.",
                 FadeIn(lab))
        self.end_scene()


# =====================================================================
class V1_04_Escalerizar(V1):
    CH_NUM = "02"
    CH_TITLE = "Escalerizar · Rouché-Frobenius"

    def construct(self):
        self.setup_frame()
        ops = self.stamp(["$F_i\\leftrightarrow F_j$ \\quad intercambiar",
                          "$F_i\\to\\lambda F_i$ \\quad multiplicar por $\\lambda\\neq0$",
                          "$F_i\\to F_i+\\lambda F_j$ \\quad sumar un múltiplo de otra"], "OPERACIONES ELEMENTALES", size=28)
        ops.move_to([0, 1.3, 0])
        self.say("Tres operaciones que **no cambian las soluciones**: intercambiar filas, multiplicar una por un número distinto de cero, y sumarle a una fila un múltiplo de otra.",
                 *self.show_stamp(ops))
        tr = trampa(["Multiplicar por $\\lambda=0$ borra una ecuación.",
                     "Con parámetros: **nunca** multipliques una fila por $a-1$ si $a$ puede valer 1."], width=9.5)
        tr.move_to([0, -1.2, 0])
        self.say("Por eso el lambda tiene que ser distinto de cero. Y con parámetros, multiplicar por a − 1 es **ilegal** si a puede valer 1.",
                 FadeIn(tr, shift=UP * 0.2), focus=True)
        self.wipe()

        # ---- escalerizar el ejemplo
        tit = T("Práctico 2 · ej. 1c y 1e: misma A, distinto b", 24, SOFT, MONO).to_edge(UP, buff=0.75)
        m = Mat([[1, -1, 5, -2], [2, 1, 4, 2], [2, 4, -2, "c"]], bar=3, size=40).move_to([-2.8, 0.6, 0])
        self.say("Escalerizo. La idea: hacer ceros debajo de cada pivote, de izquierda a derecha.",
                 FadeIn(tit), FadeIn(m))
        m = self.rowop(m, [[1, -1, 5, -2], [0, 3, -6, 6], [0, 6, -12, "c+4"]], r"F_2-2F_1,\ F_3-2F_1",
                       "Ceros debajo del primer pivote: fila 2 menos dos veces la 1, fila 3 menos dos veces la 1.",
                       changed=[1, 2], bar=3, size=40)
        m = self.rowop(m, [[1, -1, 5, -2], [0, 3, -6, 6], [0, 0, 0, "c-8"]], r"F_3-2F_2",
                       "Cero debajo del segundo pivote. Y la tercera fila se anula entera a la izquierda.",
                       changed=[2], bar=3, size=40)
        fila = row_box(m, 2, RED)
        self.say("Toda la información está en esa última fila: dice **cero igual a c − 8**.", Create(fila), focus=True)
        c1 = L("$c=10$: \\ $0=2$ \\ $\\Rightarrow$ \\ **incompatible**", 28).move_to([3.0, -1.4, 0])
        c2 = L("$c=8$: \\ $0=0$, $z$ libre \\ $\\Rightarrow$ \\ **SCI**", 28).next_to(c1, DOWN, buff=0.3, aligned_edge=LEFT)
        VGroup(c1, c2).move_to([0, -1.7, 0])
        self.say("Con c = 10 dice cero igual a dos: **no hay solución**.", FadeIn(c1, shift=UP * 0.2))
        self.say("Con c = 8 dice cero igual a cero, y la columna de z no tiene pivote: z es libre, **infinitas soluciones**.",
                 FadeIn(c2, shift=UP * 0.2))
        tip = self.tip(["La matriz $A$ decide si puede haber solución **única**.",
                        "La columna $b$ decide entre **ninguna** e **infinitas**."], label="LO QUE ENSEÑA", size=22)
        tip.to_edge(RIGHT, buff=0.3).set_y(1.9)
        self.say("La lección: la parte izquierda decide si puede haber solución única. La columna b decide entre ninguna e infinitas.",
                 FadeIn(tip))
        self.wipe()

        # ---- parametros
        met = metodo(["Escalerizá **sin dividir** por nada que tenga el parámetro.",
                      "Los pivotes con parámetro marcan los **valores críticos**.",
                      "Fuera de los críticos: todos los pivotes, **SCD**.",
                      "En cada crítico: **sustituí el número** y terminá de escalerizar.",
                      "Chequeo: si $A$ es cuadrada, los críticos son las raíces de $\\det A$."], "DISCUTIR SEGÚN a", size=24, width=11.5)
        met.move_to([0, 0.6, 0])
        self.say("El método para discutir según un parámetro, que es **la pregunta más segura del parcial**: escalerizar sin dividir, encontrar los valores críticos, y analizarlos uno por uno.",
                 FadeIn(met, shift=UP * 0.2))
        tr = trampa(["En el valor crítico la matriz puede **dejar de estar escalonada**: sustituí y seguí."], width=11.5)
        tr.next_to(met, DOWN, buff=0.3)
        self.say("Y el error que más puntos cuesta: en el valor crítico, sustituir el número y **seguir escalerizando**. A veces se cae un pivote del medio y hay que dar un paso más.",
                 FadeIn(tr, shift=UP * 0.2), focus=True)
        self.wipe()

        # ---- Rouche-Frobenius
        rf = self.stamp(["$AX=b$ es **compatible** $\\iff \\rg(A)=\\rg(A|b)$.",
                         "Compatible y $\\rg(A)=n$: **determinado**.",
                         "Compatible y $\\rg(A)<n$: **indeterminado**, con $n-\\rg(A)$ parámetros."],
                        "ROUCHÉ-FROBENIUS (PARA ESCRIBIR TEXTUAL)", size=28)
        rf.move_to([0, 1.2, 0])
        self.say("Todo esto, dicho con el rango, es el **teorema de Rouché-Frobenius**. En 2022 pidieron enunciarlo textual: tenelo en la cabeza así.",
                 *self.show_stamp(rf), focus=True)
        t = tabla([["forma de $A$", "qué puede pasar"],
                   ["$m<n$ (más incógnitas)", "nunca SCD: SI o SCI"],
                   ["$m=n$", "SCD $\\iff \\det A\\neq0$"],
                   ["$m>n$ (más ecuaciones)", "cualquier cosa"]], size=24, h=0.55)
        t.move_to([0, -1.35, 0])
        self.say("Y la tabla rápida: con más incógnitas que ecuaciones, nunca es determinado. Cuadrado, es determinado justo cuando el determinante no es cero.",
                 FadeIn(t))
        self.end_scene()


# =====================================================================
class V1_05_Matrices(V1):
    CH_NUM = "03"
    CH_TITLE = "Matrices: máquinas que mueven el plano"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Matrices", "máquinas que mueven el plano", prob=("TRANSVERSAL", "la idea que ordena todo"))
        p = plano((-8, 8), (-5, 5), unit=1.0, faded=False)
        ghost = plano((-8, 8), (-5, 5), unit=1.0).set_opacity(0.25)
        self.add(ghost)
        self.bring_to_front(*self.persist)
        vb = base_vectors(ref_plane())
        li = MathTex(r"\hat\imath", font_size=36, color=I_COL).next_to(vb[0].get_end(), DR, buff=0.05)
        lj = MathTex(r"\hat\jmath", font_size=36, color=J_COL).next_to(vb[1].get_end(), UL, buff=0.05)
        self.say("Ahora la idea que ordena todo el curso. Esto es el plano, y estos son los dos vectores base: **i sombrero** y **j sombrero**.",
                 Create(p), GrowArrow(vb[0]), GrowArrow(vb[1]), FadeIn(li), FadeIn(lj), run_time=1.5)
        self.bring_to_front(*self.persist)
        A = [[2, 1], [0, 1]]
        mA = mat_cols(A, 40)
        pan = mpanel(mA, [-5.2, 2.5, 0])
        self.say("Una matriz dos por dos es una **máquina que mueve el plano**. Sus columnas dicen adónde van los vectores base.",
                 FadeIn(pan))
        vb2 = base_vectors(ref_plane(), A)
        self.say("La primera columna, (2, 0): ahí cae i sombrero. La segunda, (1, 1): ahí cae j sombrero. Y el resto de la grilla **los sigue**, con las rectas rectas y el origen fijo.",
                 apply_to(p, A), Transform(vb, vb2), FadeOut(li), FadeOut(lj), run_time=2.2)
        self.bring_to_front(pan)
        # AX = combinacion de columnas
        X = (1, 2)
        ax1 = flecha(ref_plane(), complex(2, 0), I_COL, 6)
        c1 = flecha(ref_plane(), complex(2, 0), I_COL, 6)
        c2a = flecha(ref_plane(), complex(3, 1), J_COL, 6, origin=complex(2, 0))
        c2b = flecha(ref_plane(), complex(4, 2), J_COL, 6, origin=complex(3, 1))
        res = flecha(ref_plane(), complex(4, 2), YELLOW, 7)
        eq = MathTex(r"A\begin{pmatrix}1\\2\end{pmatrix}=1\cdot", r"\begin{pmatrix}2\\0\end{pmatrix}", r"+2\cdot",
                     r"\begin{pmatrix}1\\1\end{pmatrix}", r"=\begin{pmatrix}4\\2\end{pmatrix}", font_size=34)
        eq[1].set_color(I_COL); eq[3].set_color(J_COL); eq[4].set_color(YELLOW)
        eqp = mpanel(eq, [-3.6, -1.9, 0])
        self.say("¿Adónde va el punto (1, 2)? Una vez la primera columna **más dos veces la segunda**. Multiplicar una matriz por un vector es **combinar sus columnas**.",
                 FadeIn(eqp), GrowArrow(c1), GrowArrow(c2a), GrowArrow(c2b), run_time=1.6)
        self.say("Por eso un sistema A X = b pregunta: ¿con qué pesos combino las columnas de A para fabricar b?",
                 GrowArrow(res), focus=True)
        self.wipe(p, ghost)

        # ---- catalogo
        catalogo = [
            ([[0, -1], [1, 0]], "Giro de 90 grados: i va a (0, 1), j va a (−1, 0).", "GIRO 90°"),
            ([[0, 1], [1, 0]], "Simetría respecto a y = x: intercambia las coordenadas.", "SIMETRÍA"),
            ([[2, 0], [0, 0.5]], "Escala: estira 2 en horizontal y achica a la mitad en vertical.", "ESCALA"),
            ([[1, 1], [0, 1]], "Cizalla: cada fila horizontal se desliza proporcional a su altura.", "CIZALLA"),
        ]
        self.remove(p)
        for A, txt, nombre in catalogo:
            q = plano((-8, 8), (-5, 5), unit=1.0, faded=False)
            vb = base_vectors(ref_plane())
            self.add(q, vb)
            self.bring_to_front(*self.persist)
            m = mat_cols([[f"{v:g}".replace(".", "{,}") for v in r] for r in A], 40)
            nm = T(nombre, 22, GOLD, MONO, BOLD)
            pan = mpanel(VGroup(nm, m).arrange(DOWN, buff=0.2), [-5.3, 2.3, 0])
            self.say(txt, FadeIn(pan), apply_to(q, A), Transform(vb, base_vectors(ref_plane(), A)), run_time=1.8)
            self.w(0.2)
            self.play(FadeOut(q), FadeOut(vb), FadeOut(pan), run_time=0.3)
        self.say("Girar, reflejar, estirar, deslizar: todo eso es multiplicar por una matriz. Y los complejos eran exactamente esto: **multiplicar por un complejo es un giro con escala**.",
                 FadeIn(plano((-8, 8), (-5, 5), unit=1.0, faded=False)))
        self.end_scene()


# =====================================================================
class V1_06_Producto(V1):
    CH_NUM = "03"
    CH_TITLE = "El producto es componer"

    def construct(self):
        self.setup_frame()
        R = [[0, -1], [1, 0]]
        S = [[1, 1], [0, 1]]
        SR = [[1, -1], [1, 0]]
        RS = [[0, -1], [1, 1]]

        def corrida(first, second, n1, n2, prod, txt1, txt2, pos):
            q = plano((-8, 8), (-5, 5), unit=1.0, faded=False)
            vb = base_vectors(ref_plane())
            self.add(q, vb)
            self.bring_to_front(*self.persist)
            lab = L(f"primero ${n1}$, después ${n2}$", 30)
            pan = mpanel(lab, [-4.3, 2.6, 0])
            self.say(txt1, FadeIn(pan), apply_to(q, first), Transform(vb, base_vectors(ref_plane(), first)), run_time=1.5)
            self.say(txt2, apply_to(q, second), Transform(vb, base_vectors(ref_plane(), np.array(second) @ np.array(first))), run_time=1.5)
            m = mat_cols(prod, 36)
            res = VGroup(MathTex(n2 + n1 + "=", font_size=38), m).arrange(RIGHT, buff=0.15)
            rp = mpanel(res, pos)
            self.play(FadeIn(rp), run_time=0.4)
            return q, vb, pan, rp

        q, vb, pan, rp1 = corrida(R, S, "R", "S", SR, "Componer es multiplicar. Primero giro 90 grados...",
                                  "...y después aplico la cizalla. El resultado es la matriz S por R: **se lee de derecha a izquierda**.",
                                  [4.6, 2.4, 0])
        self.w(0.3)
        self.play(FadeOut(q), FadeOut(vb), FadeOut(pan), run_time=0.3)
        q, vb, pan, rp2 = corrida(S, R, "S", "R", RS, "Ahora al revés: primero la cizalla...",
                                  "...y después el giro. La grilla termina en otro lado.", [4.6, 0.9, 0])
        s = self.stamp(["$SR\\neq RS$: **el producto no es conmutativo**."], "POR ESO", size=28)
        s.scale_to_fit_width(min(s.width, 6.6))
        s.move_to([3.2, -1.3, 0])
        self.say("Mismas dos máquinas, distinto orden, distinto resultado. **El producto de matrices no es conmutativo.**",
                 *self.show_stamp(s), focus=True)
        self.wipe()

        # ---- nilpotente
        N = [[0, 1], [0, 0]]
        q = plano((-8, 8), (-5, 5), unit=1.0, faded=False)
        vb = base_vectors(ref_plane())
        self.add(q, vb)
        self.bring_to_front(*self.persist)
        mN = mat_cols(N, 40)
        pan = mpanel(VGroup(MathTex("N=", font_size=40), mN).arrange(RIGHT, buff=0.15), [-5.0, 2.5, 0])
        self.say("Otra sorpresa. Esta matriz N no es la nula. Mirá lo que hace: **aplasta todo el plano** sobre el eje horizontal.",
                 FadeIn(pan), apply_to(q, N), Transform(vb, base_vectors(ref_plane(), N)), run_time=2.0)
        self.say("La aplico otra vez: lo que quedaba **cae al origen**. N por N es la matriz nula, aunque N no lo sea.",
                 apply_to(q, N), Transform(vb, base_vectors(ref_plane(), [[0, 0], [0, 0]])), run_time=1.8, focus=True)
        tr = trampa(["$AB=O$ **no** implica $A=O$ o $B=O$.",
                     "$AB=AC$ con $A\\neq O$ **no** implica $B=C$ (sí si $A$ es invertible).",
                     "$(A+B)^2=A^2+AB+BA+B^2$: es $A^2+2AB+B^2$ solo si conmutan."], width=10.5)
        tr.move_to([0.8, -0.9, 0])
        self.say("De ahí las tres trampas de verdadero o falso: producto cero sin factores cero, no se puede cancelar, y el binomio tiene **AB más BA**.",
                 FadeIn(tr, shift=UP * 0.2))
        self.wipe()

        # ---- traspuesta y traza
        self.board_start(top=2.8)
        self.push(L("**Traspuesta:** filas $\\leftrightarrow$ columnas. \\ $(AB)^t=B^tA^t$ \\ (se da vuelta el orden)", 28),
                  "La traspuesta cambia filas por columnas, y la del producto **da vuelta el orden**.")
        self.push(L("**Simétrica:** $A^t=A$. \\ **Antisimétrica:** $A^t=-A$ (diagonal nula). \\ $AA^t$ siempre es simétrica.", 28),
                  "Simétrica si es igual a su traspuesta; antisimétrica si es la opuesta, y entonces tiene la diagonal en cero.")
        self.push(L("**Traza:** suma de la diagonal. \\ $\\tr(AB)=\\tr(BA)$, \\ pero $\\tr(AB)\\neq\\tr A\\,\\tr B$.", 28),
                  "La traza es la suma de la diagonal. Traza de AB es traza de BA, pero **no** es el producto de las trazas.")
        self.push(L("Por eso $AB-BA=I_n$ es imposible: traza $0$ a la izquierda, $n$ a la derecha.", 28, YELLOW),
                  "Y el uso famoso: AB − BA nunca puede ser la identidad. La traza de la izquierda es cero y la de la derecha es n.")
        self.push(L("$\\delta(i_0,j_0)\\,A$: copia la fila $j_0$ de $A$ en la fila $i_0$. \\ $A\\,\\delta(i_0,j_0)$: columnas.", 28),
                  "Las matrices delta, con un solo uno, copian una fila, o una columna si multiplican por la derecha. Salieron en 2023.")
        self.end_scene()


# =====================================================================
class V1_07_Inversa(V1):
    CH_NUM = "04"
    CH_TITLE = "Inversa: deshacer el movimiento"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Inversa y rango", "deshacer · aplastar", prob=("MUY ALTA", "inversa y rango en los 4 últimos parciales"))
        A = [[2, 1], [1, 1]]
        Ai = [[1, -1], [-1, 2]]
        q = plano((-8, 8), (-5, 5), unit=1.0, faded=False)
        vb = base_vectors(ref_plane())
        self.play(Create(q), GrowArrow(vb[0]), GrowArrow(vb[1]), run_time=0.8)
        self.bring_to_front(*self.persist)
        pan = mpanel(VGroup(MathTex("A=", font_size=40), mat_cols(A, 40)).arrange(RIGHT, buff=0.15), [-5.0, 2.5, 0])
        self.say("Si A mueve el plano, la **inversa** es la máquina que lo devuelve a su lugar.",
                 FadeIn(pan), apply_to(q, A), Transform(vb, base_vectors(ref_plane(), A)), run_time=1.6)
        pan2 = mpanel(VGroup(MathTex("A^{-1}=", font_size=40), mat_cols(Ai, 40)).arrange(RIGHT, buff=0.15), [-5.0, 1.0, 0])
        self.say("Aplico A inversa: la grilla vuelve exacta. A inversa por A es la identidad.",
                 FadeIn(pan2), apply_to(q, Ai), Transform(vb, base_vectors(ref_plane())), run_time=1.8)
        tip = self.tip(["Para deshacer «primero $B$, después $A$»,", "deshacés $A$ primero: \\ $(AB)^{-1}=B^{-1}A^{-1}$."],
                       label="MEDIAS Y ZAPATOS", size=24)
        tip.move_to([3.6, -1.6, 0])
        self.say("Y la regla del producto: si te pusiste medias y después zapatos, para deshacerlo te sacás **primero los zapatos**. Por eso la inversa de AB es B inversa por A inversa.",
                 FadeIn(tip, shift=UP * 0.2), focus=True)
        self.wipe()

        # ---- Gauss-Jordan
        tit = T("Cómo se calcula: (A | I) → (I | inversa)", 26, SOFT, MONO).to_edge(UP, buff=0.75)
        m = Mat([[2, 1, 1, 0], [1, 1, 0, 1]], bar=2, size=44).move_to([-1.5, 0.8, 0])
        self.say("Para calcularla: escribo A con la identidad al lado y escalerizo **las dos mitades juntas** hasta que la izquierda sea la identidad.",
                 FadeIn(tit), FadeIn(m))
        m = self.rowop(m, [[1, 1, 0, 1], [2, 1, 1, 0]], r"F_1\leftrightarrow F_2", "Subo la fila con 1 adelante.", bar=2, size=44)
        m = self.rowop(m, [[1, 1, 0, 1], [0, -1, 1, -2]], r"F_2-2F_1", "Cero debajo del pivote.", changed=[1], bar=2, size=44)
        m = self.rowop(m, [[1, 1, 0, 1], [0, 1, -1, 2]], r"-F_2", "Pivote en 1.", changed=[1], bar=2, size=44)
        m = self.rowop(m, [[1, 0, 1, -1], [0, 1, -1, 2]], r"F_1-F_2", "Y cero arriba. A la izquierda quedó I: **a la derecha está la inversa**.",
                       changed=[0], bar=2, size=44)
        der = VGroup(*[m.get_entries()[k] for k in (2, 3, 6, 7)])
        self.play(der.animate.set_color(YELLOW), run_time=0.4)
        chk = self.check("CHEQUEO: FILA 1 DE A · COLUMNA 1 = 2·1 + 1·(−1) = 1 ✓").move_to([0, -1.1, 0])
        self.say("Chequeo de diez segundos: fila de A por columna de la inversa. Tiene que dar 1 en la diagonal y 0 afuera.",
                 FadeIn(chk))
        tr = trampa(["Si a la izquierda aparece una **fila de ceros**, $A$ no es invertible: cortá."], width=9)
        tr.move_to([0, -1.9, 0])
        self.play(FadeIn(tr), run_time=0.4)
        self.w(0.8)
        self.wipe()

        # ---- formula 2x2 y ecuacion
        f = self.stamp(["$\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}^{-1}=\\dfrac{1}{ad-bc}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}$"],
                       "FÓRMULA 2×2", size=30)
        f.move_to([-3.2, 1.5, 0])
        self.say("En dos por dos hay fórmula: intercambio la diagonal, cambio el signo de la otra, y divido por el determinante.",
                 *self.show_stamp(f))
        self.board_start(left=0.6, top=2.6, maxw=6.2)
        self.push(L("$A^2-2A+5I=O$", 30), "Y el truco que salió en 2023: una ecuación con A.")
        self.push(L("$A^2-2A=-5I$", 30), "Paso la identidad al otro lado.")
        self.push(L("$A\\,(A-2I)=-5I$", 30), "Saco A de factor común, **del lado correcto**.")
        self.push(L("$A\\cdot\\frac15(2I-A)=I$", 30, YELLOW), "Divido por menos cinco...", focus=False)
        self.push(L("$A^{-1}=\\frac15(2I-A)$", 32, YELLOW), "...y leo la inversa. Si al final no te queda la identidad sola del otro lado, no hay conclusión.",
                  focus=True)
        m2 = memo(["1S 2025: $A^2+3AA^t+2I=O \\Rightarrow A^{-1}=-\\frac12(A+3A^t)$",
                   "2S 2022: $A^4=O \\Rightarrow (I+A+A^2+A^3)^{-1}=I-A$"], width=6.6)
        m2.move_to([-3.2, -1.4, 0])
        self.say("Las otras versiones que salieron: con A traspuesta en 2025, y la de A a la cuarta igual a cero en 2022.",
                 FadeIn(m2, shift=UP * 0.2))
        self.end_scene()


# =====================================================================
class V1_08_Rango(V1):
    CH_NUM = "04"
    CH_TITLE = "Rango: cuánto sobrevive"

    def construct(self):
        self.setup_frame()
        t = ValueTracker(0.5)
        base = plano((-8, 8), (-5, 5), unit=1.0, faded=False)
        Mt = lambda: np.array([[1.0, 2.0], [t.get_value(), 4.0]])
        live = always_redraw(lambda: base.copy().apply_matrix(Mt(), about_point=ORIGIN))
        vbl = always_redraw(lambda: base_vectors(ref_plane(), Mt().tolist()))
        ghost = plano((-8, 8), (-5, 5), unit=1.0).set_opacity(0.18)
        self.add(ghost, live, vbl)
        self.bring_to_front(*self.persist)
        mm = always_redraw(lambda: mpanel(VGroup(MathTex("A=", font_size=38),
                                                 Mat([[1, 2], [f"{t.get_value():.2f}".replace(".", "{,}"), 4]], size=36, h_buff=0.95)
                                                 ).arrange(RIGHT, buff=0.15), [-5.0, 2.5, 0]))
        rg = {2: T("rango 2 · llena el plano", 28, GREEN, SANS, BOLD), 1: T("rango 1 · todo cae en una recta", 28, RED, SANS, BOLD)}
        for k, v in rg.items():
            v.move_to([3.6, 2.6, 0])
            v.add_updater(lambda m, k=k: m.set_opacity(1 if (1 if abs(4 - 2 * t.get_value()) < 0.02 else 2) == k else 0))
        bgr = Rectangle(width=6.4, height=0.7, stroke_width=0).set_fill(BG, 0.85).move_to([3.6, 2.6, 0])
        self.add(mm, bgr, *rg.values())
        self.say("El rango mide **cuánto sobrevive** del plano después de la máquina. Esta matriz tiene un parámetro abajo a la izquierda.")
        self.say("Lo muevo hacia 2. Las dos columnas se van alineando... y en t = 2 la segunda columna es el doble de la primera: el plano entero **se aplasta en una recta**.",
                 t.animate.set_value(2.0), run_time=4.0, rate_func=smooth, focus=True)
        p1 = Dot(ORIGIN + 2 * RIGHT + 0 * UP, color=YELLOW)
        self.say("Rango 1. Y fijate lo grave: puntos distintos caen en el **mismo lugar**. No hay forma de saber de dónde vino cada uno: no se puede deshacer, **no hay inversa**.")
        for v in rg.values():
            v.clear_updaters()
        live.clear_updaters(); vbl.clear_updaters(); mm.clear_updaters()
        self.wipe()

        d = self.stamp(["$\\rg(A)$ = cantidad de **filas no nulas de una forma escalonada** de $A$",
                        "(= cantidad de pivotes; no depende de cómo escalerices)"], "RANGO", size=28)
        d.move_to([0, 2.0, 0])
        self.say("La definición para el parcial: filas no nulas **de una forma escalonada**.", *self.show_stamp(d))
        tr = trampa(["«rango = filas no nulas de $A$» es **falso**: la matriz de unos $3\\times3$ tiene rango 1."], width=10.5)
        tr.next_to(d, DOWN, buff=0.35)
        self.say("De la escalonada, no de A: la matriz de todos unos tiene tres filas no nulas y rango uno.", FadeIn(tr), focus=True)
        pr = memo(["$\\rg(A)\\le\\min(m,n)$ \\qquad $\\rg(A)=\\rg(A^t)$ \\qquad $\\rg(PA)=\\rg(A)$ si $P$ es invertible",
                   "Con parámetro: igual que en sistemas. Críticos = raíces de $\\det A$ si es cuadrada."], width=10.5)
        pr.next_to(tr, DOWN, buff=0.3)
        self.say("Propiedades: a lo sumo el mínimo entre filas y columnas, igual al de la traspuesta, y no cambia al multiplicar por una invertible.",
                 FadeIn(pr))
        self.wipe()

        te = self.stamp(["$A$ invertible", "$\\iff \\rg(A)=n$", "$\\iff$ su escalonada reducida es $I$",
                         "$\\iff AX=0$ solo tiene la solución trivial", "$\\iff AX=b$ es SCD para todo $b$",
                         "$\\iff A$ es producto de elementales", "$\\iff \\det A\\neq0$"],
                        "TEOREMA DE LA MATRIZ INVERTIBLE (n×n)", size=28)
        te.scale_to_fit_height(min(te.height, 4.9))
        te.move_to([0, 0.35, 0]).align_to([-6.6, 0, 0], LEFT)
        tip = self.tip(["Probás la que te resulte **más fácil**", "y te llevás todas las demás gratis."], label="CAJA DE HERRAMIENTAS", size=24)
        tip.next_to(te, RIGHT, buff=0.35)
        if tip.get_right()[0] > 6.9:
            tip.scale_to_fit_width(6.9 - te.get_right()[0] - 0.35).next_to(te, RIGHT, buff=0.35)
        self.say("Todo se junta en un teorema: invertible, rango completo, sistema determinado, determinante distinto de cero... son **la misma cosa dicha de siete formas**.",
                 *self.show_stamp(te), focus=True)
        self.say("En un verdadero o falso, probás la que te quede más cómoda y te llevás las otras gratis.", FadeIn(tip))
        self.end_scene()


# =====================================================================
class V1_09_Determinante(V1):
    CH_NUM = "05"
    CH_TITLE = "Determinante: el factor de área"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Determinantes", "cuánto se estira el área", prob=("MUY ALTA", "9 de 14 · y 8 más de expresiones"))
        a, b, c, d = [ValueTracker(v) for v in (1.0, 0.0, 0.0, 1.0)]
        p = plano((-8, 8), (-5, 5), unit=1.0).set_opacity(0.5)
        self.add(p)
        self.bring_to_front(*self.persist)
        o = p.n2p(0)
        col1 = lambda: complex(a.get_value(), c.get_value())
        col2 = lambda: complex(b.get_value(), d.get_value())
        detv = lambda: a.get_value() * d.get_value() - b.get_value() * c.get_value()

        def par():
            pts = [p.n2p(0), p.n2p(col1()), p.n2p(col1() + col2()), p.n2p(col2())]
            col = YELLOW if detv() > 0.01 else (RED if detv() < -0.01 else GRAY)
            return Polygon(*pts, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35)

        pg = always_redraw(par)
        v1 = always_redraw(lambda: flecha(p, col1(), I_COL, 6))
        v2 = always_redraw(lambda: flecha(p, col2(), J_COL, 6))
        num = Num(1.0, num_decimal_places=2, font_size=44, color=YELLOW)
        num.add_updater(lambda m: m.set_value(detv()))
        lab = MathTex(r"\det A=ad-bc=", font_size=40)
        panel = VGroup(lab, num).arrange(RIGHT, buff=0.15).move_to([-4.2, 2.5, 0])
        num.add_updater(lambda m: m.next_to(lab, RIGHT, buff=0.15))
        bgp = SurroundingRectangle(panel, buff=0.2, stroke_width=0).set_fill(BG, 0.9)
        self.say("El cuadradito que forman los vectores base tiene **área 1**. Miremos qué le pasa cuando una matriz mueve el plano.",
                 FadeIn(pg), FadeIn(v1), FadeIn(v2), FadeIn(bgp), FadeIn(panel))
        self.say("Con la matriz de columnas (3, 0) y (1, 2), el cuadrado se vuelve un paralelogramo de **área 6**. Y 3 por 2 menos 1 por 0 es 6: **el determinante es el factor de área**.",
                 a.animate.set_value(3.0), b.animate.set_value(1.0), d.animate.set_value(2.0), run_time=2.2, focus=True)
        self.say("Ahora achico d. El paralelogramo se aplasta... y en det = 0 **colapsa en una recta**: área cero, la matriz no es invertible.",
                 d.animate.set_value(0.0), run_time=2.5)
        self.say("Sigo: el determinante se hace negativo y el paralelogramo aparece **dado vuelta**, como en un espejo. El signo es la orientación.",
                 d.animate.set_value(-1.2), run_time=2.0)
        self.play(d.animate.set_value(2.0), run_time=1.0)
        s = self.stamp(["$|\\det A|$ = factor por el que se multiplican las **áreas**",
                        "signo = orientación \\quad $\\det A=0 \\iff$ se aplasta $\\iff$ no invertible"], "LA IMAGEN", size=26)
        s.move_to([2.8, -1.7, 0])
        s.scale_to_fit_width(min(s.width, 7.6))
        self.say("Eso es todo el determinante: cuánto estira las áreas, con signo. En tres por tres, los volúmenes.",
                 *self.show_stamp(s))
        for m in (pg, v1, v2):
            m.clear_updaters()
        num.clear_updaters()
        self.wipe()

        # ---- como se calcula
        self.board_start(top=2.8)
        self.push(L("$\\begin{vmatrix}a&b\\\\c&d\\end{vmatrix}=ad-bc$ \\qquad $3\\times3$: Sarrus o desarrollo por una fila", 28),
                  "Para calcularlo: en dos por dos, ad menos bc. En tres por tres, Sarrus o desarrollo por una fila.")
        self.push(L("Desarrollo: $\\det A=\\sum_j(-1)^{i+j}a_{ij}\\det A_{ij}$ \\ por **la fila o columna con más ceros**", 28),
                  "El desarrollo se puede hacer por cualquier fila o columna: elegí **la que tenga más ceros**.")
        self.push(L("Matrices grandes: $F_i\\to F_i+\\lambda F_j$ hasta **triangular** $\\Rightarrow$ producto de la diagonal", 28, YELLOW),
                  "Y para las grandes: fabricá ceros sumando múltiplos de filas, que no cambia el determinante, hasta llegar a una triangular. Ahí es el producto de la diagonal.")
        ej = memo(["1S 2019: una $6\\times6$. Restando la fila 1 a las demás queda triangular:",
                   "diagonal $1,-2,-2,-2,1,1$ \\ $\\Rightarrow$ \\ $\\det=-8$."], width=11)
        ej.move_to([0, -1.5, 0])
        self.say("Así se resolvió una seis por seis en 2019: una sola ronda de restas y quedó triangular.", FadeIn(ej))
        self.end_scene()


# =====================================================================
class V1_10_DetPropiedades(V1):
    CH_NUM = "05"
    CH_TITLE = "Propiedades, vistas"

    def construct(self):
        self.setup_frame()
        p = plano((-8, 8), (-5, 5), unit=1.0).set_opacity(0.45).shift(RIGHT * 2.2)
        self.add(p)
        self.bring_to_front(*self.persist)
        A = np.array([[2.0, 0.5], [0.0, 1.5]])
        M = [ValueTracker(v) for v in A.flatten()]
        cur = lambda: np.array([[M[0].get_value(), M[1].get_value()], [M[2].get_value(), M[3].get_value()]])

        def par():
            X = cur()
            c1, c2 = complex(X[0, 0], X[1, 0]), complex(X[0, 1], X[1, 1])
            dv = np.linalg.det(X)
            col = YELLOW if dv > 0.01 else (RED if dv < -0.01 else GRAY)
            return VGroup(Polygon(p.n2p(0), p.n2p(c1), p.n2p(c1 + c2), p.n2p(c2), stroke_color=col, stroke_width=3,
                                  fill_color=col, fill_opacity=0.35),
                          flecha(p, c1, I_COL, 6), flecha(p, c2, J_COL, 6))

        pg = always_redraw(par)
        num = Num(3.0, num_decimal_places=2, font_size=40, color=YELLOW)
        lab = T("área =", 28, INK)
        area = VGroup(lab, num).arrange(RIGHT, buff=0.15).move_to([-4.6, 2.4, 0])
        num.add_updater(lambda m: m.set_value(np.linalg.det(cur())).next_to(lab, RIGHT, buff=0.15))
        self.add(pg, area)
        rules = VGroup()

        def regla(tex, y, color=INK):
            r = L(tex, 25, color)
            r.move_to([-4.2, y, 0])
            if r.width > 5.4:
                r.scale_to_fit_width(5.4)
            r.align_to([-6.8, 0, 0], LEFT)
            bg = SurroundingRectangle(r, buff=0.1, stroke_width=0).set_fill(BG, 0.85)
            return VGroup(bg, r)

        r1 = regla("**Sumar un múltiplo** de otra: no cambia", 1.5)
        self.say("Las propiedades del determinante se **ven**. Primera: sumarle a una columna un múltiplo de otra. El paralelogramo se desliza... y el área **no cambia**.",
                 FadeIn(r1), M[1].animate.set_value(2.5), run_time=2.5)
        self.play(M[1].animate.set_value(0.5), run_time=0.8)
        r2 = regla("**Multiplicar una fila** por $\\lambda$: $\\times\\lambda$", 0.8)
        self.say("Segunda: multiplicar una fila por lambda estira en una sola dirección. El área se multiplica por **lambda**.",
                 FadeIn(r2), M[0].animate.set_value(4.0), M[1].animate.set_value(1.0), run_time=2.0)
        self.play(M[0].animate.set_value(2.0), M[1].animate.set_value(0.5), run_time=0.8)
        r3 = regla("$\\det(\\lambda A)=\\lambda^n\\det A$", 0.1, YELLOW)
        self.say("Tercera, **la que más se equivoca**: multiplicar toda la matriz por 2 estira las dos direcciones. El área se multiplica por **4**, no por 2. Lambda a la n.",
                 FadeIn(r3), *[m.animate.set_value(2 * v) for m, v in zip(M, A.flatten())], run_time=2.2, focus=True)
        self.play(*[m.animate.set_value(v) for m, v in zip(M, A.flatten())], run_time=0.8)
        r4 = regla("**Intercambiar** filas: cambia el signo", -0.6)
        self.say("Cuarta: intercambiar dos filas es un espejo. El paralelogramo se da vuelta: **mismo tamaño, signo opuesto**.",
                 FadeIn(r4), M[0].animate.set_value(0.0), M[2].animate.set_value(2.0), M[1].animate.set_value(1.5), M[3].animate.set_value(0.5),
                 run_time=2.2)
        self.play(*[m.animate.set_value(v) for m, v in zip(M, A.flatten())], run_time=0.8)
        r5 = regla("$\\det(AB)=\\det A\\cdot\\det B$", -1.3, YELLOW)
        self.say("Y la del producto: si una máquina multiplica las áreas por 3 y otra por 2, hacer una y después la otra las multiplica por **6**.",
                 FadeIn(r5), focus=True)
        num.clear_updaters(); pg.clear_updaters()
        self.wipe()

        tr = trampa(["$\\det(2A)=2\\det A$ \\ es falso: $2^n\\det A$.",
                     "$\\det(A+B)=\\det A+\\det B$ \\ es falso.",
                     "$\\det A=0$ no implica una fila de ceros: $\\begin{pmatrix}1&2\\\\2&4\\end{pmatrix}$."], width=6.3)
        tr.move_to([-3.4, 1.2, 0])
        con = memo(["$\\det A^t=\\det A$ \\quad $\\det A^{-1}=\\frac1{\\det A}$ \\quad $\\det A^k=(\\det A)^k$",
                    "Antisimétrica, $n$ impar: $0$ \\quad Nilpotente: $0$",
                    "$A^2=A$: $0$ o $1$ \\quad $A^2=I$: $\\pm1$"], width=6.3)
        con.move_to([3.3, 1.2, 0])
        self.say("A la izquierda, las tres trampas de verdadero o falso. A la derecha, lo que se sabe del determinante **sin calcularlo**.",
                 FadeIn(tr, shift=UP * 0.2), FadeIn(con, shift=UP * 0.2))
        met = metodo(["Sacá los factores de cada fila y columna (cada uno multiplica).",
                      "Deshacé las sumas con $F_i-\\lambda F_j$ (no cambia). Si no se cancela, partí la fila.",
                      "Reordená hasta llegar a $A$: **cada intercambio cambia el signo**."], "«det A = k, ¿cuánto vale det B?»", size=23, width=12.8)
        met.move_to([0, -1.35, 0])
        self.say("Y el método estrella, que salió en los dos últimos parciales: llevar B hasta A anotando cada factor. Lo resolvemos completo en el video 2.",
                 FadeIn(met, shift=UP * 0.2))
        self.end_scene()
