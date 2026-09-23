"""
VIDEO 3 - PROBABILIDAD MEDIA + CIERRE  (libro: capitulos 9, 10, 11, 12 y 13)
  Cap 9   Calculo de limites
  Cap 10  Lipschitz
  Cap 11  Funciones y composicion
  Cap 12  Verdadero o falso relampago
  Cap 13  Antes de entrar: formulario y checklist
Todas las cuentas salen del libro "Calculo1_1er_parcial_libro.pdf" (verificadas con sympy).
"""
from calc_base import *

SCENE_ORDER = ["V3_00_Intro", "V3_01_Limites", "V3_02_LimitesPractico", "V3_03_Lipschitz",
               "V3_04_Composicion", "V3_05_VF", "V3_06_AntesDeEntrar"]


class V3(GBase):
    VIDEO_TAG = "VIDEO 3 · PROBABILIDAD MEDIA"


def lleno(p, color=BLUE, r=0.08):
    return Dot(p, radius=r, color=color)


def hueco(p, color=BLUE, r=0.08):
    return Circle(radius=r, color=color, stroke_width=3).set_fill(BG, 1).move_to(p)


def lectura(etiqueta, valor_fn, color=INK, decimals=2, size=24):
    n = Num(valor_fn(), num_decimal_places=decimals, font_size=size * 1.3, color=color)
    n.add_updater(lambda m: m.set_value(valor_fn()))
    return VGroup(L(etiqueta, size, color), n).arrange(RIGHT, buff=0.15)


def congelar(*mobs):
    for m in mobs:
        for x in m.get_family():
            x.clear_updaters()


def curva_pts(ax, f, xs, color=BLUE, sw=4):
    return VMobject(color=color, stroke_width=sw).set_points_as_corners([ax.c2p(x, f(x)) for x in xs])


# =====================================================================
class V3_00_Intro(V3):
    def construct(self):
        self.setup_frame(header=False)
        t1 = T("CÁLCULO 1 · PRIMER PARCIAL", 22, SOFT, MONO)
        t2 = T("Video 3", 70, INK, SANS, BOLD)
        t3 = prob_chip("MEDIA")
        t4 = T("Límites · Lipschitz · Composición · V/F relámpago · Antes de entrar", 28, SOFT)
        VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.35).shift(UP * 0.5)
        self.play(FadeIn(t1, shift=DOWN * 0.2), Write(t2), run_time=1.4)
        self.play(FadeIn(t3), FadeIn(t4, shift=UP * 0.2), run_time=0.8)
        self.say("Tercer video: probabilidad **media**, y el cierre. Si llegaste hasta acá con los dos primeros firmes, esto es lo que suma los últimos puntos.")
        self.say("Y al final, lo que tenés que mirar el **miércoles antes de entrar**: el formulario y la checklist.")
        self.end_scene()


# =====================================================================
class V3_01_Limites(V3):
    CH_NUM, CH_TITLE = "09", "Cálculo de límites"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Cálculo de límites", "Qué hacer según lo que aparece",
                        prob=("MEDIA", "casi no apareció, pero en 2026 tuvo dos semanas de teórico"))
        met = metodo(["**Nada raro al sustituir:** el límite es el valor (continuidad).",
                      "**$\\frac00$ con polinomios:** factorizá $(x-a)$ arriba y abajo, cancelá.",
                      "**$\\frac00$ con raíces:** multiplicá y dividí por el conjugado.",
                      "**Senos:** $\\lim_{u\\to0}\\frac{\\sin u}{u}=1$. Acomodá para que el argumento aparezca abajo.",
                      "**Acotado × algo que va a 0:** da 0.",
                      "**Cociente de polinomios en $\\infty$:** mandan los grados.",
                      "**$\\infty-\\infty$ con raíces:** conjugado.",
                      "**Parte entera o valor absoluto:** límites laterales por separado."],
                     "QUÉ HACER SEGÚN LO QUE APARECE", size=23).move_to([0, 0.35, 0])
        self.say("Casi todo límite cae en uno de estos ocho casos. La primera pregunta siempre es: **¿qué aparece cuando sustituyo?**",
                 FadeIn(met, shift=UP * 0.2), min_t=5)
        self.wipe()

        # ---- 0/0: el agujero
        e = enun("PRÁCTICO 4.3 · EJ 1 g) · FACTORIZAR", ["$\\displaystyle\\lim_{x\\to1}\\frac{x^2-1}{x^2-3x+2}$"], size=28).move_to([-3.4, 2.35, 0])
        ax = ejes([-1, 1.8, 1], [-5, 1, 1], 6.0, 4.0).move_to([-3.3, -0.4, 0])
        g = lambda x: (x + 1) / (x - 2)
        c = ax.plot(g, x_range=[-1, 1.5], color=BLUE, stroke_width=4)
        h = hueco(ax.c2p(1, -2), YELLOW, 0.1)
        self.board_start(left=0.6, top=1.6, maxw=6.0)
        a = M(r"\frac{0}{0}\ \to\ \frac{(x-1)(x+1)}{(x-1)(x-2)}=\frac{x+1}{x-2}", size=38)
        self.push(a, "Sustituyo 1: cero sobre cero. Polinomios: **factorizo** el (x − 1) de arriba y de abajo, y lo cancelo.",
                  FadeIn(e), Create(ax), Create(c))
        b = M(r"\to\frac{2}{-1}=-2", size=40)
        self.push(b, "Lo que queda es continuo en 1: sustituyo y da −2.")
        tip = self.tip(["$\\frac00$ no es un número: es un **agujero** en la gráfica.",
                        "La función original es esta curva con un pixel faltante.",
                        "El límite es la altura del agujero."], label="LA IMAGEN", size=21)
        self.push(tip, "Mirá la gráfica: cero sobre cero es un **agujero**. La curva simplificada es idéntica salvo un pixel. El límite es la altura del agujero: −2.",
                  FadeIn(h, scale=2), anim=FadeIn(tip))
        self.wipe()

        # ---- sin u / u con perilla
        tit = L("$\\displaystyle\\lim_{u\\to0}\\frac{\\sin u}{u}=1$", 30).move_to([0, 2.5, 0])
        ax = ejes([-7, 7, 2], [-0.4, 1.3, 0.5], 9.5, 3.4).move_to([0, -0.2, 0])
        s = lambda u: np.sin(u) / u if abs(u) > 1e-6 else 1.0
        c = curva_pts(ax, s, [x for x in np.linspace(-6.8, 6.8, 800) if abs(x) > 1e-3])
        h = hueco(ax.c2p(0, 1), YELLOW, 0.09)
        u = ValueTracker(5.0)
        pt = always_redraw(lambda: lleno(ax.c2p(u.get_value(), s(u.get_value())), ORANGE, 0.1))
        pan = VGroup(Slider("u", u, 0, 6, color=ORANGE, decimals=3, width=2.4, size=22),
                     lectura("$\\frac{\\sin u}{u}=$", lambda: s(u.get_value()), ORANGE, 4, 22)).arrange(RIGHT, buff=0.6).move_to([0, -2.2, 0])
        self.say("El límite de los senos, visto. En u = 0 la expresión no está definida: agujero.", Write(tit), Create(ax), Create(c), FadeIn(h))
        self.add(pt)
        self.play(FadeIn(pan))
        self.say("Acerco u al cero: 1, 0,1, 0,001... el cociente se pega a **1**. De cerca, seno de u es casi u.",
                 u.animate.set_value(0.001), run_time=5, rate_func=rate_functions.ease_out_cubic)
        congelar(pan)
        self.remove(pt)
        self.wipe(tit)
        ej = VGroup(L("(a) $\\displaystyle\\frac{\\sin(2x)}{3x}=\\frac23\\cdot\\frac{\\sin(2x)}{2x}\\to\\frac23\\cdot1=\\frac23$", 28),
                    L("(d) $\\displaystyle\\frac{\\sin(x^2)}{x+x^2}=\\frac{\\sin(x^2)}{x^2}\\cdot\\frac{x}{1+x}\\to1\\cdot0=0$", 28)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        et = T("PRÁCTICO 4.5 · EJ 4 a) y d)", 16, SOFT, MONO, BOLD).next_to(ej, UP, buff=0.35).align_to(ej, LEFT)
        self.say("El truco es **acomodar**: que lo que está adentro del seno aparezca también abajo. En la a, multiplico y divido por 2.", FadeIn(et), FadeIn(ej[0]))
        self.say("En la d, fabrico x² abajo, y lo que sobra, x sobre 1 + x, va a cero.", FadeIn(ej[1]))
        self.end_scene()


# =====================================================================
class V3_02_LimitesPractico(V3):
    CH_NUM, CH_TITLE = "09", "Límites · conjugado, infinito, laterales"

    def construct(self):
        self.setup_frame()
        e = enun("PRÁCTICO 4.3 · EJ 1 i) y j) · CONJUGADO",
                 ["(i) $\\displaystyle\\lim_{x\\to1}\\frac{x-1}{\\sqrt x-1}$     (j) $\\displaystyle\\lim_{x\\to0}\\frac{\\sqrt{1+x}-\\sqrt{1-x}}{x}$"], size=27).move_to([0, 2.4, 0])
        self.say("Cero sobre cero con **raíces**: se multiplica por el conjugado, para que la diferencia de raíces se vuelva diferencia de cuadrados.", FadeIn(e), min_t=3)
        self.board_start(top=1.0)
        a = L("(i) $x-1=(\\sqrt x-1)(\\sqrt x+1)$, así que el cociente es $\\sqrt x+1\\to2$.", 26)
        self.push(a, "En la i ni hace falta: x − 1 **es** una diferencia de cuadrados. Queda raíz de x + 1, que va a 2.")
        b = M(r"\frac{(1+x)-(1-x)}{x\,(\sqrt{1+x}+\sqrt{1-x})}=\frac{2}{\sqrt{1+x}+\sqrt{1-x}}\to\frac22=1", size=38)
        self.push(b, "En la j multiplico arriba y abajo por la suma de las raíces. Arriba queda 2x, cancelo la x, y va a **1**.")
        self.wipe()

        # ---- infinito menos infinito, con perilla
        e = enun("PRÁCTICO 4.4 · EJ 8 a) · ∞ − ∞", ["$\\displaystyle\\lim_{x\\to+\\infty}x-\\sqrt{x^2+x}$"], size=28).move_to([0, 2.45, 0])
        self.say("Infinito menos infinito: dos cosas enormes que casi se cancelan. ¿Qué queda?", FadeIn(e))
        x = ValueTracker(1.0)
        ff = lambda v: v - np.sqrt(v * v + v)
        ax = ejes([0, 60, 10], [-0.8, 0.1, 0.5], 7.0, 3.2).move_to([-2.6, -0.3, 0])
        c = ax.plot(ff, x_range=[0.01, 60], color=BLUE, stroke_width=4)
        asin = DashedLine(ax.c2p(0, -0.5), ax.c2p(60, -0.5), color=YELLOW, stroke_width=2)
        yl = M("-\\tfrac12", size=30, color=YELLOW).next_to(ax.c2p(0, -0.5), LEFT, buff=0.1)
        pt = always_redraw(lambda: lleno(ax.c2p(min(x.get_value(), 60), ff(x.get_value())), ORANGE, 0.1))
        pan = VGroup(lectura("$x=$", lambda: x.get_value(), ORANGE, 0, 24),
                     lectura("$\\sqrt{x^2+x}=$", lambda: np.sqrt(x.get_value() ** 2 + x.get_value()), SOFT, 3, 24),
                     lectura("diferencia $=$", lambda: ff(x.get_value()), ORANGE, 4, 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 0.2, 0])
        self.add(pt)
        self.say("Mirá los números en vivo. x y raíz de x² + x crecen juntos, pero su diferencia **no** se va a cero ni a infinito.",
                 Create(ax), Create(c), FadeIn(pan))
        self.say("Se estaciona en **−½**. Raíz de x² + x es aproximadamente x + ½: el conjugado lo hace exacto.",
                 x.animate.set_value(60), run_time=5, rate_func=rate_functions.ease_in_quad)
        self.play(Create(asin), FadeIn(yl))
        congelar(pan)
        self.remove(pt)
        self.add(lleno(ax.c2p(60, ff(60)), ORANGE, 0.1))
        self.wipe(e)
        a = M(r"\frac{x^2-(x^2+x)}{x+\sqrt{x^2+x}}=\frac{-x}{x+\sqrt{x^2+x}}=\frac{-1}{1+\sqrt{1+\frac1x}}\to-\frac12", size=40).move_to([0, 0.9, 0])
        self.say("La cuenta: conjugado, arriba se cancelan los x², y divido todo por x. Da **−½**.", Write(a))
        g = Lines("**Polinomios en ∞:** mandan los grados.   $\\frac{x^3-10x-1}{10x^2+1}\\to+\\infty$  ·  $\\frac{100x^2+x}{x^3-100x}\\to0$",
                  "**Acotado por infinitésimo:**   $\\frac{\\sin x}{x}\\to0$ cuando $x\\to+\\infty$  ($|\\sin x|\\le1$ y $\\frac1x\\to0$).", size=23).move_to([0, -1.2, 0])
        self.say("Y dos atajos en el infinito: en cocientes de polinomios **mandan los grados**; y la máscara del capítulo 6 sigue funcionando.", FadeIn(g))
        self.wipe()

        # ---- laterales con parte entera
        e = enun("PRÁCTICO 4.3 · EJ 2 c) · PARTE ENTERA", ["$\\displaystyle\\lim_{x\\to0}\\ \\lceil x\\rceil-\\fl{x}$"], size=28).move_to([0, 2.45, 0])
        ax = ejes([-1.5, 1.5, 1], [-0.5, 1.6, 1], 6.0, 3.0).move_to([-3.2, -0.3, 0])
        seg = VGroup(Line(ax.c2p(-1, 1), ax.c2p(0, 1), color=BLUE, stroke_width=5), Line(ax.c2p(0, 1), ax.c2p(1, 1), color=BLUE, stroke_width=5),
                     hueco(ax.c2p(0, 1)), lleno(ax.c2p(0, 0), RED), lleno(ax.c2p(-1, 0), BLUE, 0.06), lleno(ax.c2p(1, 0), BLUE, 0.06))
        cu = Lines("Derecha, $x\\in(0,1)$: $1-0=1$.", "Izquierda, $x\\in(-1,0)$: $0-(-1)=1$.", "Laterales iguales: el límite es **1**,",
                   "aunque en $x=0$ la expresión vale $0$.", size=24).move_to([3.4, -0.2, 0])
        self.say("Con parte entera, **laterales por separado**. A la derecha del 0 vale 1; a la izquierda también. El límite es 1, aunque en el 0 mismo vale 0.",
                 FadeIn(e), Create(ax), FadeIn(seg), FadeIn(cu))
        self.wipe()
        ej = VGroup(*[L(s, 26) for s in ["(a) $\\lim_{x\\to3}\\frac{x^2-9}{x^2-5x+6}$     (b) $\\lim_{x\\to0}\\frac{\\sin(3x)}{5x}$",
                                         "(c) $\\lim_{x\\to+\\infty}\\sqrt{x^2+3x}-x$     (d) $\\lim_{x\\to0}x^2\\cos\\frac1x$"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        g = self.pausa(ej, "Tu turno. Cuatro límites, cuatro casos distintos de la lista.")
        sol = Lines("(a) factorizo: $\\to6$   (b) $\\frac35\\cdot\\frac{\\sin3x}{3x}\\to\\frac35$   (c) conjugado: $\\to\\frac32$   (d) máscara: $0$", size=24)
        debajo(sol, g)
        self.say("Soluciones.", FadeIn(sol), min_t=3)
        self.end_scene()


# =====================================================================
class V3_03_Lipschitz(V3):
    CH_NUM, CH_TITLE = "10", "Lipschitz"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Lipschitz", "Un límite de velocidad para la función",
                        prob=("MEDIA", "apareció en tres prácticos · V/F o demostración corta"))
        s = self.stamp(["$f:I\\to\\R$ es **Lipschitz** si existe $K$ tal que $|f(x)-f(y)|\\le K|x-y|$ para todo $x,y\\in I$."],
                       "DEFINICIÓN", size=27).move_to([0, 2.45, 0])
        self.say("La definición: la función no puede cambiar **más rápido que K** por unidad de x. Es un límite de velocidad.", *self.show_stamp(s))

        # ---- el reloj de arena que se desliza
        ax = ejes([-3.2, 3.2, 1], [-2, 2, 1], 9.0, 3.9).move_to([-1.2, -0.45, 0])
        f = lambda x: 0.6 * np.sin(2 * x) + 0.15 * x
        df = lambda x: 1.2 * np.cos(2 * x) + 0.15
        c = ax.plot(f, x_range=[-3.1, 3.1], color=BLUE, stroke_width=4)
        x0 = ValueTracker(-2.0)
        K = ValueTracker(2.0)
        xs = np.linspace(-3.1, 3.1, 400)

        def cono():
            a, k = x0.get_value(), K.get_value()
            fa = f(a)
            T_ = min(3.5, 1.9 / max(k, 0.01))
            g = VGroup(
                Polygon(ax.c2p(a, fa), ax.c2p(a + T_, fa + k * T_), ax.c2p(a + T_, fa - k * T_),
                        stroke_width=0, fill_color=TEAL, fill_opacity=0.12),
                Polygon(ax.c2p(a, fa), ax.c2p(a - T_, fa + k * T_), ax.c2p(a - T_, fa - k * T_),
                        stroke_width=0, fill_color=TEAL, fill_opacity=0.12),
                DashedLine(ax.c2p(a - T_, fa - k * T_), ax.c2p(a + T_, fa + k * T_), color=TEAL, stroke_width=2),
                DashedLine(ax.c2p(a - T_, fa + k * T_), ax.c2p(a + T_, fa - k * T_), color=TEAL, stroke_width=2))
            malos = VGroup()
            for u, v in zip(xs[:-1], xs[1:]):
                m = (u + v) / 2
                if abs(f(m) - fa) > k * abs(m - a) + 1e-3:
                    malos.add(Line(ax.c2p(u, f(u)), ax.c2p(v, f(v)), color=RED, stroke_width=7))
            g.add(malos, lleno(ax.c2p(a, fa), YELLOW, 0.1))
            return g
        conov = always_redraw(cono)
        pan = VGroup(Slider("K", K, 0, 3, color=TEAL, decimals=2, width=2.0, size=24),
                     Slider("x₀", x0, -3, 3, color=YELLOW, decimals=2, width=2.0, size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([5.3, 0.6, 0])
        ver = always_redraw(lambda: T("K alcanza" if K.get_value() >= 1.35 - 1e-3 else "la curva se escapa", 20,
                                      GREEN if K.get_value() >= 1.35 - 1e-3 else RED, MONO, BOLD).move_to([5.3, -0.7, 0]))
        self.say("La imagen: en cada punto de la curva pongo un **reloj de arena** de pendientes más y menos K. Lipschitz es que la curva entera quede adentro.",
                 FadeOut(s), Create(ax), Create(c), FadeIn(pan))
        self.add(conov, ver)
        self.say("Con K = 2, deslizo el punto por toda la curva: nunca se escapa. **K alcanza**.",
                 x0.animate.set_value(2.5), run_time=5, rate_func=linear)
        self.say("Bajo K: el reloj se cierra... y en los tramos empinados la curva **se sale**, en rojo.",
                 K.animate.set_value(0.8), run_time=3)
        self.say("Muevo el punto: en las zonas planas entra, en las empinadas no. K tiene que ser al menos **la pendiente más brava** de toda la curva.",
                 x0.animate.set_value(-1.5), run_time=4, rate_func=linear)
        self.say("Subo K hasta la pendiente máxima: alcanza en todos lados.", K.animate.set_value(1.4), run_time=2)
        self.remove(conov, ver)
        congelar(pan)
        self.wipe()

        # ---- raíz: ningún K alcanza
        tit = T("√x cerca del 0: ningún K alcanza", 30, INK, SANS, BOLD).move_to([0, 2.6, 0])
        ax = ejes([0, 2.2, 1], [0, 1.6, 1], 7.0, 4.0).move_to([-2.0, -0.3, 0])
        c = ax.plot(np.sqrt, x_range=[0, 2.1], color=BLUE, stroke_width=4)
        xv = ValueTracker(1.5)
        sec = always_redraw(lambda: VGroup(
            Line(ax.c2p(0, 0), ax.c2p(xv.get_value(), np.sqrt(xv.get_value())), color=ORANGE, stroke_width=4),
            lleno(ax.c2p(xv.get_value(), np.sqrt(xv.get_value())), ORANGE, 0.09), lleno(ax.c2p(0, 0), YELLOW, 0.09)))
        rd = VGroup(lectura("$x=$", lambda: xv.get_value(), ORANGE, 4, 24),
                    lectura("pendiente $\\frac{\\sqrt x-0}{x-0}=\\frac1{\\sqrt x}=$", lambda: 1 / np.sqrt(xv.get_value()), ORANGE, 1, 24)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, 0.6, 0])
        self.add(sec)
        self.say("Ahora raíz de x. Uno los puntos 0 y x con un segmento: su pendiente es 1 sobre raíz de x.",
                 Write(tit), Create(ax), Create(c), FadeIn(rd))
        self.say("Acerco x al cero: la pendiente se **dispara**. 10, 100, 1000... Para cualquier K que me des, encuentro un tramo más empinado.",
                 xv.animate.set_value(0.0001), run_time=5, rate_func=rate_functions.ease_out_expo)
        nota = Lines("Tangente vertical en 0:", "continua, pero **no** Lipschitz.", size=24).move_to([3.9, -1.2, 0])
        self.say("Es continua, pero **no Lipschitz**: tiene tangente vertical en el cero.", FadeIn(nota))
        congelar(rd)
        self.remove(sec)
        self.wipe()

        mm = memo(["**Lipschitz ⇒ continua:** dado $\\eps$, sirve $\\delta=\\eps/K$.",
                   "**Continua ⇏ Lipschitz:** $\\sqrt x$ en $[0,1]$.",
                   "**Lipschitz ⇒ integrable:** en un bloque de ancho $h$, $M_i-m_i\\le Kh$."], label="LAS IMPLICANCIAS", size=23).move_to([0, 2.15, 0])
        self.say("Las implicancias. Lipschitz implica continua, con δ = ε/K: es el patrón lineal del capítulo 5 con la pendiente máxima.", FadeIn(mm))
        tb = VGroup(*[L(s, 24) for s in [
            "(a) $3x+7$ en $\\R$: **sí**, $K=3$.",
            "(b) $\\sqrt x$ en $[0,+\\infty)$: **no**, $\\frac1{\\sqrt x}$ sin cota cerca de 0.",
            "(c) $x^2$ en $\\R$: **no**, $|x+y|$ sin cota (en un intervalo acotado, sí).",
            "(d) $2^x$ en $\\R$: **no**, $|2^{x+1}-2^x|=2^x$ sin cota.",
            "(e) signo$(x)$: **no**, ni siquiera es continua."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0, -1.05, 0])
        et = T("PRÁCTICO 2.2 · EJ 8 · ¿CUÁLES SON LIPSCHITZ?", 15, SOFT, MONO, BOLD).next_to(tb, UP, buff=0.18).align_to(tb, LEFT)
        self.say("El ejercicio clásico del práctico. La pregunta siempre es la misma: ¿la pendiente **está acotada** en todo el dominio?",
                 FadeIn(et), LaggedStart(*[FadeIn(t) for t in tb], lag_ratio=0.3, run_time=3), min_t=5)
        self.wipe()

        e = enun("PRÁCTICO 3.4 · EJ 6 a) · LA DEMOSTRACIÓN DEL PIZARRÓN",
                 ["$f$ integrable en $[a,b]$. Probar que $F(x)=\\int_a^xf(t)\\,dt$ es Lipschitz."], size=26).move_to([0, 2.45, 0])
        self.say("Y la demostración que se hizo en el pizarrón. Cuatro renglones.", FadeIn(e))
        self.board_start(top=1.45)
        for i, (t_, b_, sub) in enumerate([
            ("uso que f es acotada", "Integrable implica acotada: $|f(t)|\\le M$.", "Integrable implica acotada: hay un M."),
            ("Chasles", "$F(x)-F(y)=\\int_y^xf(t)\\,dt$.", "Chasles: la diferencia de F es la integral entre y y x."),
            ("acoto", "$|F(x)-F(y)|=\\left|\\int_y^xf\\right|\\le M|x-y|$.", "Acotación: el área cabe en una caja de alto M y ancho |x − y|."),
            ("concluyo", "$F$ es Lipschitz con $K=M$. Y por lo tanto **continua**, aunque $f$ tenga saltos. $\\blacksquare$",
             "F es Lipschitz con K = M. Por eso la integral indefinida es **continua** aunque f salte.")], 1):
            self.push(step(i, t_, L(b_, 25)), sub)
        self.wipe()
        ej = VGroup(*[L(s, 26) for s in ["¿Son Lipschitz? Dar $K$ o mostrar que no.",
                                         "(a) $|x|$ en $\\R$   (b) $\\sin x$ en $\\R$   (c) $F(x)=\\int_0^x\\fl{t}\\,dt$ en $[0,5]$"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        g = self.pausa(ej, "Tu turno.")
        sol = Lines("(a) Sí, $K=1$   (b) Sí, $K=1$   (c) Sí: $|\\fl{t}|\\le5$ en $[0,5]$, así que $K=5$", size=24)
        debajo(sol, g)
        self.say("Soluciones. La c es exactamente la demostración de recién.", FadeIn(sol))
        self.end_scene()


# =====================================================================
class V3_04_Composicion(V3):
    CH_NUM, CH_TITLE = "11", "Funciones y composición"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Funciones y composición", "Nodos en cadena",
                        prob=("BAJA", "una vez directo, pero aparece adentro de continuidad"))

        def nodo(txt, color):
            t = T(txt, 26, color, MONO, BOLD)
            r = RoundedRectangle(width=max(1.6, t.width + 0.6), height=0.9, corner_radius=0.12, stroke_color=color, stroke_width=2.5).set_fill(PANEL, 1)
            return VGroup(r, t.move_to(r))
        x_ = nodo("x", SOFT)
        gn = nodo("g", TEAL)
        fn = nodo("f", ORANGE)
        out = nodo("f(g(x))", YELLOW)
        cadena = VGroup(x_, gn, fn, out).arrange(RIGHT, buff=1.0).move_to([0, 1.5, 0])
        flechas = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=SOFT, stroke_width=3) for a, b in zip(cadena[:-1], cadena[1:])])
        self.say("La composición, como en un editor de nodos: **primero g**, y su salida entra a f. f ∘ g se lee de derecha a izquierda.",
                 LaggedStart(*[FadeIn(n) for n in cadena], lag_ratio=0.3), LaggedStart(*[GrowArrow(a) for a in flechas], lag_ratio=0.3))
        dot = Dot(x_.get_center(), color=YELLOW, radius=0.1)
        self.play(MoveAlongPath(dot, Line(x_.get_center(), out.get_center())), run_time=2 * PACE, rate_func=linear)
        self.remove(dot)
        mm = memo(["$(f+g)(x)=f(x)+g(x)$: dos ramas independientes (un Merge).",
                   "$(f\\circ g)(x)=f(g(x))$: **primero** $g$. En general $f\\circ g\\neq g\\circ f$."], label="SUMA CONTRA COMPOSICIÓN", size=24).move_to([0, -0.5, 0])
        self.say("La suma, en cambio, es un Merge: dos ramas que se juntan. Y el orden de la cadena importa: f ∘ g no es g ∘ f.", FadeIn(mm))
        self.wipe()

        met = metodo(["Escribí la externa con un hueco: $f(\\square)$.",
                      "Meté la interna **entera**, también en las **condiciones** de las ramas.",
                      "Traducí cada condición a $x$. **El punto de quiebre se corre.**"], "COMPONER CON FUNCIONES A TROZOS", size=25).move_to([0, 1.9, 0])
        self.say("Con funciones a trozos, el detalle que se olvida: la interna entra **también en las condiciones**, y los quiebres se mueven.", FadeIn(met))
        e = enun("PRÁCTICO 1.2 · EJ 5 i) · A TROZOS",
                 ["$f(x)=2x+1$ si $x\\le0$,  $x-1$ si $x>0$;    $g(x)=x$ si $x\\le0$,  $2x$ si $x>0$.   Calcular $g\\circ f$."], size=24).move_to([0, 0.15, 0])
        self.say("Ejemplo del práctico: g ∘ f. Primero f; las condiciones de g dependen del **signo de f(x)**.", FadeIn(e))
        self.wipe(e)
        self.play(e.animate.move_to([0, 2.5, 0]))
        cu = Lines("$x\\le0$: $f=2x+1$, que es $\\le0$ si $x\\le-\\frac12$ → $g=2x+1$; si $-\\frac12<x\\le0$ → $g=4x+2$.",
                   "$x>0$: $f=x-1$, que es $\\le0$ si $x\\le1$ → $g=x-1$; si $x>1$ → $g=2x-2$.", size=23).move_to([0, 1.35, 0])
        self.say("Rama por rama: pregunto dónde f(x) es negativa o positiva. Aparecen cortes en **−½** y en **1**.", FadeIn(cu), min_t=4)
        ax = ejes([-2, 2.5, 1], [-3, 3.5, 1], 7.5, 3.0).move_to([-1.4, -1.1, 0])
        piezas = [(lambda x: 2 * x + 1, -2, -0.5, BLUE), (lambda x: 4 * x + 2, -0.5, 0, TEAL),
                  (lambda x: x - 1, 0, 1, ORANGE), (lambda x: 2 * x - 2, 1, 2.2, VIOLET)]
        gr = VGroup(*[ax.plot(fn_, x_range=[a, b], color=c, stroke_width=4) for fn_, a, b, c in piezas])
        q = VGroup(*[DashedLine(ax.c2p(v, -3), ax.c2p(v, 3.3), color=YELLOW, stroke_width=2) for v in (-0.5, 1)])
        ql = VGroup(M("-\\tfrac12", size=28, color=YELLOW).next_to(ax.c2p(-0.5, 3.3), UP, buff=0.05),
                    M("1", size=28, color=YELLOW).next_to(ax.c2p(1, 3.3), UP, buff=0.05))
        nota = Lines("Cuatro ramas.", "Los quiebres **−½** y **1**", "no estaban en ninguna", "de las dos funciones.", size=22).move_to([4.8, -1.1, 0])
        self.say("Cuatro ramas, y los quiebres en −½ y en 1 son **nuevos**: no estaban en ninguna de las dos funciones originales.",
                 Create(ax), LaggedStart(*[Create(p) for p in gr], lag_ratio=0.3), Create(q), FadeIn(ql), FadeIn(nota))
        self.end_scene()


# =====================================================================
VF = [
    ("Si $A$ tiene supremo, tiene máximo.", False, "$(0,1)$: sup 1, sin máx."),
    ("Si $A$ tiene máximo, $\\max A=\\sup A$.", True, "El máx es una cota que pertenece."),
    ("Toda función integrable es continua.", False, "$\\fl{x}$ en $[0,3]$."),
    ("Toda función continua en $[a,b]$ es integrable.", True, "Criterio 2."),
    ("Toda función acotada es integrable.", False, "Dirichlet."),
    ("Monótona en $[a,b]\\Rightarrow$ integrable.", True, "Telescópica."),
    ("Si $|f|$ es integrable, $f$ lo es.", False, "$1$ en $\\Q$, $-1$ fuera: $|f|=1$."),
    ("Si $P\\subset P'$, $\\Ss(f,P')\\le\\Ss(f,P)$.", True, "Refinar baja la superior."),
    ("$\\Si(f,Q)\\le\\Ss(f,P)$ para toda $P,Q$.", True, "Pasando por $P\\cup Q$."),
    ("$f$ integrable $\\Rightarrow G(x)=\\int_a^xf$ continua.", True, "$G$ es Lipschitz."),
    ("$f\\ge0$ y $\\int_a^bf=0\\Rightarrow f\\equiv0$.", False, "$f(0)=1$, $0$ en el resto. (V si $f$ es continua.)"),
    ("Existe $\\lim_{x\\to a}f\\Rightarrow f$ continua en $a$.", False, "Discontinuidad evitable."),
    ("Lipschitz $\\Rightarrow$ continua.", True, "$\\delta=\\eps/K$."),
    ("Continua $\\Rightarrow$ Lipschitz.", False, "$\\sqrt x$ en $[0,1]$."),
    ("$f$ continua en $(0,1)\\Rightarrow$ tiene mínimo.", False, "$x$ en $(0,1)$: ínf 0 sin mín."),
    ("$f$ continua en $[a,b]\\Rightarrow$ acotada.", True, "Weierstrass."),
    ("$f(a)f(b)<0\\Rightarrow$ raíz en $(a,b)$.", False, "Falta continuidad: signo$(x)$ en $[-1,1]$."),
    ("$f\\circ g=g\\circ f$.", False, "$x^2$ y $x+1$."),
    ("El recíproco de un teorema verdadero es verdadero.", False, "Casi nunca. El contrarrecíproco sí."),
]


class V3_05_VF(V3):
    CH_NUM, CH_TITLE = "12", "Verdadero o falso, relámpago"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Verdadero o falso, relámpago", "Tapá la respuesta y contestá antes que el video",
                        prob=("TRANSVERSAL", "los V/F reciclan siempre las mismas trampas"))
        s = self.stamp(["Para **refutar** alcanza un contraejemplo. Para **probar** hace falta un argumento general.",
                        "Primero intentá romperlo con un caso conocido: $\\fl{x}$, Dirichlet, un intervalo abierto,",
                        "$\\sqrt x$ cerca de 0, un conjunto dentro de $\\Q$."], "LA REGLA", size=25).move_to([0, 0.5, 0])
        self.say("La regla de los V/F: para **refutar** alcanza un ejemplo. Tené a mano el kit de contraejemplos: parte entera, Dirichlet, intervalo abierto, raíz cerca de cero, racionales.",
                 *self.show_stamp(s), min_t=5)
        self.wipe()
        self.uncap()
        for i, (af, v, pq) in enumerate(VF, 1):
            num = T(f"{i:02d} / {len(VF)}", 18, DIM, MONO).move_to([0, 2.6, 0])
            a = L(af, 34)
            if a.width > 12.4:
                a.scale_to_fit_width(12.4)
            a.move_to([0, 1.0, 0])
            barra = Line([-2.5, 0.0, 0], [2.5, 0.0, 0], color=ORANGE, stroke_width=5)
            self.play(FadeIn(num), FadeIn(a, shift=UP * 0.15), FadeIn(barra), run_time=0.45 * PACE)
            self.play(ShrinkToCenter(barra), run_time=2.2 * PACE, rate_func=linear)
            self.remove(barra)
            chip_ = T("VERDADERO" if v else "FALSO", 40, GREEN if v else RED, MONO, BOLD).move_to([0, -0.3, 0])
            porque = L(pq, 28, SOFT).next_to(chip_, DOWN, buff=0.35)
            self.play(FadeIn(chip_, scale=1.3), FadeIn(porque), run_time=0.45 * PACE)
            self.wait(1.9 * PACE)
            self.play(FadeOut(VGroup(num, a, chip_, porque)), run_time=0.3 * PACE)
        self.say("Diecinueve afirmaciones. Las que dudaste, volvé a verlas mañana: **son las mismas trampas** que reciclan los parciales.")
        self.end_scene()


# =====================================================================
class V3_06_AntesDeEntrar(V3):
    CH_NUM, CH_TITLE = "13", "Antes de entrar"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Antes de entrar", "El formulario y la checklist del miércoles")
        forms = [
            ("SUP / ÍNF", ["$\\sup A$ = menor cota superior. $\\max A=\\sup A$ solo si pertenece.",
                           "$S=\\sup A\\iff S$ cota y $\\forall\\eps>0\\ \\exists a\\in A: S-\\eps<a$."]),
            ("DARBOUX E INTEGRABILIDAD", ["$\\Ss=\\sum\\sup(\\text{bloque})\\cdot\\text{ancho}$,   $\\Si=\\sum\\inf(\\text{bloque})\\cdot\\text{ancho}$.",
                                          "Integrable $\\iff\\forall\\eps\\ \\exists P:\\Ss-\\Si<\\eps$.   Monótona, uniforme: $\\Ss-\\Si=\\frac{b-a}n|f(b)-f(a)|$."]),
            ("LÍMITE Y CONTINUIDAD", ["$\\forall\\eps>0\\ \\exists\\delta>0: 0<|x-a|<\\delta\\Rightarrow|f(x)-L|<\\eps$. Lineal: $\\delta=\\eps/|m|$. Asimétrico: manda el lado corto.",
                                      "Continua en $a\\iff\\lim_{x\\to a}f=f(a)$.   Acotado × infinitésimo $\\to0$."]),
            ("INTEGRAL", ["Linealidad, Chasles (cualquier orden), $\\int_a^b=-\\int_b^a$, monotonía, $m(b-a)\\le\\int\\le M(b-a)$."]),
            ("TEOREMAS", ["Bolzano: continua en $[a,b]$ y $f(a)f(b)<0\\Rightarrow$ raíz.   Weierstrass: continua en $[a,b]\\Rightarrow$ máx y mín.",
                          "Valor medio: continua $\\Rightarrow f(c)(b-a)=\\int_a^bf$."]),
        ]
        for i in range(0, len(forms), 2):
            grupo = VGroup()
            for lab, lines in forms[i:i + 2]:
                st = self.stamp(lines, lab, size=23)
                grupo.add(st)
            grupo.arrange(DOWN, buff=0.45).move_to([0, 0.5, 0])
            for st in grupo:
                if st.width > 13.2:
                    st.scale_to_fit_width(13.2)
            anims = []
            for st in grupo:
                anims += self.show_stamp(st)
            self.say("El formulario. Esto es lo que se lee el miércoles antes de entrar, y **nada más**." if i == 0 else
                     ("Límite, continuidad y la integral." if i == 2 else "Y los tres teoremas, con sus hipótesis: **cerrado** y **continua**."),
                     *anims, min_t=6)
            self.wipe()

        met = metodo(["**Sup/ínf:** ¿pregunté si el techo pertenece?",
                      "**Darboux:** ¿sup del bloque entero? ¿anchos reales? ¿no compensé negativos?",
                      "**Telescópica:** ¿es monótona en todo el intervalo? ¿el $n$ es el siguiente entero?",
                      "**ε-δ:** ¿el intervalo está centrado? Si no, ¿tomé la distancia menor?",
                      "**Continuidad:** ¿planteé todos los pegados? ¿verifiqué?",
                      "**Integrales:** ¿limpié constantes? ¿di vuelta los extremos? ¿restas de negativos?",
                      "**Teoremas:** ¿intervalo cerrado? ¿función continua?",
                      "**Puntaje:** si no descarto tres opciones, en blanco."], "ANTES DE MARCAR LA OPCIÓN", size=23).move_to([0, 0.3, 0])
        self.say("Y la checklist. Una pregunta por tipo de ejercicio, **antes de marcar** la opción. Cada una es un error que ya viste en estos tres videos.",
                 FadeIn(met, shift=UP * 0.2), min_t=8)
        self.wipe()
        t = T("Suerte el miércoles.", 60, INK, SANS, BOLD).move_to([0, 0.6, 0])
        t2 = T("Pausá, reconocé el molde, ejecutá.", 30, BLUE).next_to(t, DOWN, buff=0.4)
        self.say("Eso es todo. Reconocé el tipo, ejecutá el molde, y **preguntá la pertenencia**. Suerte el miércoles.",
                 Write(t), FadeIn(t2, shift=UP * 0.2))
        self.end_scene()
