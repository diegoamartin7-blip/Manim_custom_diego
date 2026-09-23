"""
VIDEO 2 - PROBABILIDAD ALTA  (libro: capitulos 6, 7 y 8)
  Cap 6  Continuidad: hallar el parametro
  Cap 7  Propiedades de la integral
  Cap 8  Bolzano, valor medio, Weierstrass
Todas las cuentas salen del libro "Calculo1_1er_parcial_libro.pdf" (verificadas con sympy).
"""
from calc_base import *

SCENE_ORDER = ["V2_00_Intro",
               "V2_01_ContTeoria", "V2_02_ContParcial", "V2_03_ContPractico",
               "V2_04_IntProp", "V2_05_IntPractico",
               "V2_06_BolzTeoria", "V2_07_BolzEjercicios"]


class V2(GBase):
    VIDEO_TAG = "VIDEO 2 · PROBABILIDAD ALTA"


def lleno(p, color=BLUE, r=0.08):
    return Dot(p, radius=r, color=color)


def hueco(p, color=BLUE, r=0.08):
    return Circle(radius=r, color=color, stroke_width=3).set_fill(BG, 1).move_to(p)


def veredicto(ok_, si="CONTINUA", no="DISCONTINUA", size=22):
    return T(si if ok_ else no, size, GREEN if ok_ else RED, MONO, BOLD)


def panel(*filas, buff=0.28):
    return VGroup(*filas).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def lectura(etiqueta, valor_fn, color=INK, decimals=2, size=24):
    n = Num(valor_fn(), num_decimal_places=decimals, font_size=size * 1.3, color=color)
    n.add_updater(lambda m: m.set_value(valor_fn()))
    return VGroup(L(etiqueta, size, color), n).arrange(RIGHT, buff=0.15)


def congelar(*mobs):
    for m in mobs:
        for x in m.get_family():
            x.clear_updaters()


# =====================================================================
class V2_00_Intro(V2):
    def construct(self):
        self.setup_frame(header=False)
        t1 = T("CÁLCULO 1 · PRIMER PARCIAL", 22, SOFT, MONO)
        t2 = T("Video 2", 70, INK, SANS, BOLD)
        t3 = prob_chip("ALTA")
        t4 = T("Continuidad con parámetro · Propiedades de la integral · Bolzano", 28, SOFT)
        g = VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.35).shift(UP * 0.5)
        self.play(FadeIn(t1, shift=DOWN * 0.2), Write(t2), run_time=1.4)
        self.play(FadeIn(t3), FadeIn(t4, shift=UP * 0.2), run_time=0.8)
        self.say("Segundo video: los tres tipos de probabilidad **alta**. Salieron en tres o cuatro de seis parciales, y dos de ellos son los ejercicios **más rápidos** del parcial.")
        self.wipe()
        items = VGroup(
            VGroup(T("06", 26, BLUE, MONO, BOLD), T("Continuidad: hallar el parámetro", 30, INK), T("4 de 6", 22, ORANGE, MONO, BOLD)).arrange(RIGHT, buff=0.4),
            VGroup(T("07", 26, BLUE, MONO, BOLD), T("Propiedades de la integral", 30, INK), T("3 de 6", 22, ORANGE, MONO, BOLD)).arrange(RIGHT, buff=0.4),
            VGroup(T("08", 26, BLUE, MONO, BOLD), T("Bolzano, valor medio, Weierstrass", 30, INK), T("V/F + directo", 22, ORANGE, MONO, BOLD)).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([0, 0.5, 0])
        self.say("El recorrido. En los tres, la idea es la misma: **ver** qué está pasando en la gráfica antes de hacer la cuenta.",
                 LaggedStart(*[FadeIn(i, shift=RIGHT * 0.3) for i in items], lag_ratio=0.3, run_time=2))
        self.end_scene()


# =====================================================================
class V2_01_ContTeoria(V2):
    CH_NUM, CH_TITLE = "06", "Continuidad · la teoría justa"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Continuidad: hallar el parámetro", "Cerrar el salto con una perilla",
                        prob=("ALTA", "4 de 6 parciales · siempre «¿para qué a es continua?»"))
        s = self.stamp(["$f$ es continua en $a\\iff\\lim_{x\\to a}f(x)=f(a)$. Tres cosas a la vez:",
                        "(i) existe $f(a)$;  (ii) existe el límite (laterales iguales);  (iii) son el mismo número."],
                       "CONTINUIDAD EN UN PUNTO", size=26).move_to([0, 2.2, 0])
        self.say("La definición: el límite existe y coincide con el valor. Son **tres condiciones** a la vez, y en el parcial siempre falla una.",
                 *self.show_stamp(s))

        # ---- tipos de discontinuidad, tres mini-gráficas
        def mini(xr, yr):
            return ejes(xr, yr, 3.6, 2.3)
        a1 = mini([-1, 1.2, 1], [-0.2, 1.6, 1])
        a2 = mini([-1, 1.2, 1], [-0.2, 1.6, 1])
        a3 = mini([-0.5, 0.5, 1], [-1.3, 1.3, 1])
        VGroup(a1, a2, a3).arrange(RIGHT, buff=0.7).move_to([0, 0.2, 0])
        e1 = VGroup(a1.plot(lambda x: 0.5 * x + 0.6, x_range=[-0.9, 1.1], color=BLUE, stroke_width=4),
                    hueco(a1.c2p(0, 0.6)), lleno(a1.c2p(0, 1.3), RED))
        e2 = VGroup(a2.plot(lambda x: 0.3 * x + 0.4, x_range=[-0.9, 0], color=BLUE, stroke_width=4),
                    a2.plot(lambda x: 0.3 * x + 1.2, x_range=[0, 1.1], color=BLUE, stroke_width=4),
                    hueco(a2.c2p(0, 0.4)), lleno(a2.c2p(0, 1.2)))
        e3 = a3.plot(lambda x: np.sin(1 / x) if abs(x) > 1e-3 else 0, x_range=[0.012, 0.48, 0.0005], color=BLUE, stroke_width=2)
        e3b = a3.plot(lambda x: np.sin(1 / x), x_range=[-0.48, -0.012, 0.0005], color=BLUE, stroke_width=2)
        n1 = Lines("**Evitable**", "el límite existe, pero $\\neq f(a)$.", "Se arregla con un valor.", size=19).next_to(a1, DOWN, buff=0.2)
        n2 = Lines("**Salto**", "laterales distintos.", "Ningún $f(a)$ lo arregla.", size=19).next_to(a2, DOWN, buff=0.2)
        n3 = Lines("**Esencial**", "algún lateral no existe:", "$\\sin\\frac1x$ en 0.", size=19).next_to(a3, DOWN, buff=0.2)
        self.say("Tres formas de romperse. **Evitable**: el límite existe, pero el punto está corrido. Se arregla moviendo un solo valor.",
                 FadeOut(s), Create(a1), Create(e1), FadeIn(n1))
        self.say("**Salto**: los dos lados llegan a alturas distintas. Mover el valor del punto no sirve: siempre queda un lado sin pegar.",
                 Create(a2), Create(e2), FadeIn(n2))
        self.say("**Esencial**: seno de 1/x oscila infinitas veces cerca del cero. Ningún lado se decide.",
                 Create(a3), Create(e3), Create(e3b), FadeIn(n3))
        self.wipe()

        # ---- la perilla: cerrar un salto con el parámetro
        tit = L("$f(x)=\\begin{cases}x+1 & x<1\\\\ a-x & x\\ge1\\end{cases}$", 26).move_to([3.9, 2.3, 0])
        ax = ejes([-1, 3.2, 1], [-1.5, 4, 1], 7.0, 4.8).move_to([-2.6, 0.1, 0])
        a = ValueTracker(0.8)
        izq = ax.plot(lambda x: x + 1, x_range=[-1, 1], color=BLUE, stroke_width=4)
        der = always_redraw(lambda: ax.plot(lambda x: a.get_value() - x, x_range=[1, 3.1], color=ORANGE, stroke_width=4))
        pi_ = hueco(ax.c2p(1, 2), BLUE)
        pd_ = always_redraw(lambda: lleno(ax.c2p(1, a.get_value() - 1), ORANGE))
        gap = always_redraw(lambda: DashedLine(ax.c2p(1, 2), ax.c2p(1, a.get_value() - 1),
                                               color=RED if abs(a.get_value() - 3) > 0.02 else GREEN, stroke_width=3))
        sl = Slider("a", a, 0, 5, color=ORANGE, decimals=2, width=2.6).move_to([3.9, 1.0, 0])
        li = lectura("izquierda:", lambda: 2.0, BLUE)
        ld = lectura("derecha y valor:", lambda: a.get_value() - 1, ORANGE)
        sal = lectura("salto:", lambda: abs(a.get_value() - 3), RED)
        pan = panel(li, ld, sal).move_to([3.9, -0.6, 0])
        ver = always_redraw(lambda: veredicto(abs(a.get_value() - 3) < 0.02, size=24).move_to([3.9, -1.9, 0]))
        self.say("Ahora el ejercicio del parcial, con perilla. Una función **pegada** en x = 1: una rama a la izquierda, otra a la derecha, y la de la derecha depende de a.",
                 Write(tit), Create(ax), Create(izq), FadeIn(pi_))
        self.add(der, pd_, gap)
        self.say("La perilla a sube y baja la rama naranja. La línea roja punteada es **el salto**.", FadeIn(sl), FadeIn(pan))
        self.add(ver)
        self.say("Subo a... el salto se achica...", a.animate.set_value(2.4), run_time=3)
        self.say("...y en **a = 3** las dos ramas llegan a la misma altura. El salto es cero: continua.", a.animate.set_value(3.0), run_time=2.5)
        self.say("Si me paso, se abre de nuevo del otro lado. Hay **un solo valor** que cierra.", a.animate.set_value(4.3), run_time=2.5)
        self.say("La cuenta es exactamente lo que hizo la perilla: izquierda **igual** a derecha. 2 = a − 1, a = 3.",
                 a.animate.set_value(3.0), run_time=2)
        congelar(pan)
        self.remove(der, pd_, gap, ver)
        self.wipe()

        met = metodo(["Marcá los **puntos de pegado**. En el resto: «cada rama es continua por ser…».",
                      "En cada pegado: límite por izquierda, por derecha y valor asignado.",
                      "Igualá. Un pegado da una ecuación; dos pegados, un sistema.",
                      "Si el límite tiene $0/0$: factorizá. Si es «acotado × algo que va a 0»: da 0.",
                      "**Verificá** sustituyendo."],
                     "PARÁMETRO PARA QUE SEA CONTINUA", size=25).move_to([0, 0.9, 0])
        self.say("El método escrito. Es lo que hizo la perilla, más dos herramientas para cuando el límite no sale directo.",
                 FadeIn(met), min_t=4)
        mm = memo(["Polinomios, $\\sin$, $\\cos$, $e^x$, $\\log$ ($x>0$), $\\sqrt x$ ($x\\ge0$).",
                   "Sumas, productos, cocientes (denominador $\\neq0$) y composiciones de continuas."],
                  label="LO QUE YA SABÉS QUE ES CONTINUO", size=23).move_to([0, -1.7, 0])
        self.say("Y la lista de lo que ya sabés que es continuo: con esto justificás todo lo que **no** es punto de pegado en una frase.", FadeIn(mm))
        self.wipe()

        # ---- acotado por infinitésimo: la máscara que aplasta el ruido
        s2 = self.stamp(["Si $|g(x)|\\le M$ cerca de $a$ y $h(x)\\to0$, entonces $g(x)h(x)\\to0$.",
                         "**No** hace falta que $g$ tenga límite."], "ACOTADO POR INFINITÉSIMO", size=25).move_to([0, 2.45, 0])
        self.say("La otra herramienta clave: **acotado por infinitésimo**.", *self.show_stamp(s2))
        ax = ejes([-0.6, 0.6, 0.2], [-1.3, 1.3, 1], 9.5, 3.8).move_to([0, -0.35, 0])
        t = ValueTracker(0.0)

        def ruido(x):
            if abs(x) < 1e-4:
                return 0.0
            mascara = (1 - t.get_value()) + t.get_value() * abs(x) / 0.6
            return mascara * np.sin(1 / x)
        xs = np.concatenate([np.linspace(-0.6, -0.004, 1400), np.linspace(0.004, 0.6, 1400)])

        def curva():
            ptsL = [ax.c2p(x, ruido(x)) for x in xs[:1400]]
            ptsR = [ax.c2p(x, ruido(x)) for x in xs[1400:]]
            return VGroup(VMobject(color=BLUE, stroke_width=2).set_points_as_corners(ptsL),
                          VMobject(color=BLUE, stroke_width=2).set_points_as_corners(ptsR))
        cv = always_redraw(curva)
        env = always_redraw(lambda: VGroup(
            ax.plot(lambda x: (1 - t.get_value()) + t.get_value() * abs(x) / 0.6, x_range=[-0.6, 0.6], color=YELLOW, stroke_width=2.5),
            ax.plot(lambda x: -((1 - t.get_value()) + t.get_value() * abs(x) / 0.6), x_range=[-0.6, 0.6], color=YELLOW, stroke_width=2.5)))
        sl = Slider("máscara", t, 0, 1, color=YELLOW, decimals=2, width=2.4, size=22).move_to([3.9, -2.2, 0])
        lab = always_redraw(lambda: L("$\\sin\\frac1x$" if t.get_value() < 0.5 else "$x\\sin\\frac1x$", 26, BLUE).move_to([-4.6, -2.2, 0]))
        self.add(cv)
        self.say("Seno de 1/x: un **ruido** que oscila cada vez más rápido cerca del cero, siempre entre −1 y 1. Solo, no tiene límite.",
                 Create(ax), FadeIn(lab))
        self.add(env)
        self.say("Ahora lo multiplico por una **máscara** que se apaga en el cero: una rampa |x|. En amarillo, la envolvente.",
                 FadeIn(sl))
        self.say("Subo la máscara... la envolvente se pellizca en el cero, y el ruido queda **atrapado** adentro.",
                 t.animate.set_value(1.0), run_time=5, rate_func=smooth)
        self.say("Por más frecuencia que tenga el ruido, la máscara lo aplasta a cero. x por seno de 1/x **tiende a 0**.")
        tip = self.tip(["Un noise de amplitud acotada multiplicado por una rampa que se apaga a cero.",
                        "Por más frecuencia que tenga el noise, la máscara lo aplasta."], label="LA IMAGEN", size=21).move_to([0, 1.25, 0])
        self.say("En tu idioma: un noise por una máscara que se apaga. El resultado se apaga.", FadeOut(s2), FadeIn(tip))
        self.remove(cv, env, lab)
        congelar(sl)
        self.end_scene()


# =====================================================================
class V2_02_ContParcial(V2):
    CH_NUM, CH_TITLE = "06", "Continuidad · ejercicios de parcial"

    def construct(self):
        self.setup_frame()
        e = enun("PARCIAL 2024-2 · EJ 8",
                 ["$f(x)=(x-1)\\sin\\!\\left(\\dfrac{2x}{x-1}\\right)+\\dfrac\\pi4\\cdot\\dfrac{x^2-1}{x-1}$ si $x\\neq1$,   $f(1)=a$.",
                  "Hallar $a$ para que $f$ sea continua en 1."], size=25).move_to([0, 2.4, 0])
        self.say("Parcial 2024. Parece un monstruo, pero son **las dos herramientas** del capítulo, una en cada término. Pausá y reconocelas.",
                 FadeIn(e), min_t=3)
        self.board_start(top=1.2, maxw=7.0)
        p1 = step(1, "condición", L("Fuera de $x=1$ todo es continuo. Solo importa $a=\\lim_{x\\to1}f$.", 23))
        self.push(p1, "Fuera del 1, todo es composición de continuas. Así que la única condición es: a igual al límite en 1.")
        p2 = step(2, "primer término", L("$|\\sin(\\cdots)|\\le1$ y $(x-1)\\to0$: tiende a $0$.", 23))
        self.push(p2, "Primer término: seno acotado por algo que va a cero. **Acotado por infinitésimo**: tiende a 0. El seno solo no tiene límite, y no importa.")
        p3 = step(3, "segundo término, 0/0", L("$\\dfrac{x^2-1}{x-1}=\\dfrac{(x-1)(x+1)}{x-1}=x+1\\to2$.", 23))
        self.push(p3, "Segundo término: cero sobre cero. Factorizo y cancelo x − 1. Queda x + 1, que tiende a 2. Por π/4: **π/2**.")
        r = resp("$a=\\dfrac\\pi2$")
        self.push(r, "Sumo: 0 + π/2. La respuesta es a = π/2.", anim=FadeIn(r))
        # gráfica a la derecha con perilla a
        ax = ejes([0.4, 1.6, 0.5], [-0.2, 2.8, 1], 5.2, 3.3).move_to([3.9, -0.15, 0])
        f = lambda x: (x - 1) * np.sin(2 * x / (x - 1)) + np.pi / 4 * (x + 1)
        xsL = np.linspace(0.42, 0.998, 700)
        xsR = np.linspace(1.002, 1.58, 700)
        cL = VMobject(color=BLUE, stroke_width=2.5).set_points_as_corners([ax.c2p(x, f(x)) for x in xsL])
        cR = VMobject(color=BLUE, stroke_width=2.5).set_points_as_corners([ax.c2p(x, f(x)) for x in xsR])
        agujero = hueco(ax.c2p(1, np.pi / 2), BLUE, 0.07)
        a = ValueTracker(2.4)
        pa = always_redraw(lambda: lleno(ax.c2p(1, a.get_value()),
                                         GREEN if abs(a.get_value() - np.pi / 2) < 0.02 else RED, 0.09))
        sl = Slider("a", a, 0, 2.8, color=YELLOW, decimals=3, width=2.0, size=22).move_to([3.9, -2.3, 0])
        self.say("Y así se ve: la curva tiembla cerca del 1, pero el temblor **se apaga**. Queda un agujero a altura π/2.",
                 Create(ax), Create(cL), Create(cR), FadeIn(agujero))
        self.add(pa)
        self.say("El valor f(1) = a es un punto suelto. Con la perilla lo muevo hasta **tapar el agujero**: a = π/2, más o menos 1,571.",
                 FadeIn(sl), a.animate.set_value(np.pi / 2), run_time=4)
        self.remove(pa)
        self.add(lleno(ax.c2p(1, np.pi / 2), GREEN, 0.09))
        congelar(sl)
        self.wipe()

        # ---- composición 2024-1
        e = enun("PARCIAL 2024-1 · EJ 2 · COMPOSICIÓN",
                 ["$g(x)=x^2$,   $f_a(x)=x-5$ si $x<a$,   $f_a(x)=x+1$ si $x\\ge a$. ¿Para qué $a$ es $g\\circ f_a$ continua en $\\R$?"], size=24).move_to([0, 2.5, 0])
        self.say("Parcial 2024, primer semestre. Este es **salado**: la respuesta rápida es «nunca», y está mal.", FadeIn(e), min_t=2.5)
        self.board_start(top=1.45, maxw=5.6)
        p1 = step(1, "armo la composición", L("$(g\\circ f_a)(x)=(x-5)^2$ si $x<a$;  $(x+1)^2$ si $x\\ge a$.", 22))
        self.push(p1, "Primero f_a, después g: elevo **cada rama** al cuadrado.")
        p2 = step(2, "único punto conflictivo", L("Izquierda: $(a-5)^2$.  Derecha y valor: $(a+1)^2$.", 22))
        self.push(p2, "El único punto que puede fallar es x = a. Por izquierda llega a (a − 5)², por derecha (a + 1)².")
        ax1 = ejes([-2, 6, 1], [-7, 7, 1], 5.2, 1.55).move_to([3.9, 0.35, 0])
        ax2 = ejes([-2, 6, 1], [0, 30, 10], 5.2, 1.55).move_to([3.9, -1.6, 0])
        la = T("f_a  (salta 6)", 17, SOFT, MONO).next_to(ax1, LEFT, buff=0.1).shift(UP * 0.5)
        lb = T("(f_a)²", 17, SOFT, MONO).next_to(ax2, LEFT, buff=0.1).shift(UP * 0.5)
        a = ValueTracker(4.5)

        def graf():
            av = a.get_value()
            g1 = VGroup(ax1.plot(lambda x: x - 5, x_range=[-2, av], color=BLUE, stroke_width=3),
                        ax1.plot(lambda x: x + 1, x_range=[av, 6], color=ORANGE, stroke_width=3),
                        hueco(ax1.c2p(av, av - 5), BLUE, 0.06), lleno(ax1.c2p(av, av + 1), ORANGE, 0.06))
            ok_ = abs((av - 5) ** 2 - (av + 1) ** 2) < 0.3
            g2 = VGroup(ax2.plot(lambda x: min((x - 5) ** 2, 30), x_range=[-0.47, av], color=BLUE, stroke_width=3),
                        ax2.plot(lambda x: min((x + 1) ** 2, 30), x_range=[av, min(6, 4.4)], color=ORANGE, stroke_width=3),
                        hueco(ax2.c2p(av, min((av - 5) ** 2, 30)), BLUE, 0.06),
                        lleno(ax2.c2p(av, min((av + 1) ** 2, 30)), GREEN if ok_ else ORANGE, 0.07))
            return VGroup(g1, g2)
        gv = always_redraw(graf)
        sl = Slider("a", a, -1, 5, color=YELLOW, decimals=2, width=2.0, size=20).move_to([3.9, 1.55, 0])
        self.add(gv, sl)
        self.say("Con perilla. Arriba, f_a: siempre salta **6 unidades** en x = a. Abajo, su cuadrado.",
                 Create(ax1), Create(ax2), FadeIn(la), FadeIn(lb))
        self.say("Muevo a... abajo, los dos lados llegan a alturas distintas... hasta que en **a = 2** coinciden. ¿Por qué?",
                 a.animate.set_value(2.0), run_time=5)
        self.say("Porque en a = 2 arriba los lados valen **−3 y +3**. Distintos, pero con el mismo cuadrado: 9. El cuadrado **tapa** el salto.")
        p3 = step(3, "igualo y resuelvo", L("$a^2-10a+25=a^2+2a+1\\Rightarrow24=12a\\Rightarrow a=2$.", 22))
        self.push(p3, "La cuenta: desarrollo, los a² se cancelan, y queda a = 2.")
        p4 = step(4, "verifico", L("$(2-5)^2=9=(2+1)^2$ ✓", 22))
        self.push(p4, "Verifico: 9 y 9.")
        congelar(sl)
        self.remove(gv)
        self.add(graf())
        self.wipe()
        tr = trampa(["$f_a$ sola nunca es continua (salta 6 unidades). Pero $-3$ y $+3$ tienen el mismo cuadrado.",
                     "Si decís «$f_a$ es discontinua, entonces $g\\circ f_a$ también», perdés el ejercicio."],
                    "LA COMPOSICIÓN PUEDE ARREGLAR UN SALTO", size=24).move_to([0, 0.8, 0])
        r = resp("$a=2$").next_to(tr, DOWN, buff=0.5)
        self.say("La trampa del ejercicio: **la composición puede arreglar un salto**. Respuesta: a = 2.", FadeIn(tr), FadeIn(r))
        self.end_scene()


# =====================================================================
class V2_03_ContPractico(V2):
    CH_NUM, CH_TITLE = "06", "Continuidad · ejercicios del práctico"

    def construct(self):
        self.setup_frame()
        e = enun("PRÁCTICO 4.5 · EJ 3 c) · DOS PEGADOS",
                 ["$f(x)=\\sin(\\pi x)$ si $x<1$;   $ax+b$ si $1\\le x\\le2$;   $x^2$ si $x>2$."], size=26).move_to([0, 2.5, 0])
        self.say("Dos puntos de pegado, dos parámetros. El tramo del medio es una **recta** que tiene que enganchar las dos puntas.",
                 FadeIn(e), min_t=2.5)
        ax = ejes([-0.5, 2.8, 1], [-1.5, 6.5, 2], 6.4, 4.2).move_to([-3.2, -0.3, 0])
        A = ValueTracker(1.0)
        B = ValueTracker(1.0)
        izq = ax.plot(lambda x: np.sin(np.pi * x), x_range=[-0.5, 1], color=BLUE, stroke_width=4)
        der = ax.plot(lambda x: x * x, x_range=[2, 2.5], color=BLUE, stroke_width=4)
        h1, h2 = hueco(ax.c2p(1, 0), BLUE), hueco(ax.c2p(2, 4), BLUE)
        med = always_redraw(lambda: VGroup(
            ax.plot(lambda x: A.get_value() * x + B.get_value(), x_range=[1, 2], color=ORANGE, stroke_width=4),
            lleno(ax.c2p(1, A.get_value() + B.get_value()), ORANGE), lleno(ax.c2p(2, 2 * A.get_value() + B.get_value()), ORANGE)))
        sa = Slider("a", A, -2, 6, color=ORANGE, decimals=2, width=2.2, size=22)
        sb = Slider("b", B, -6, 3, color=ORANGE, decimals=2, width=2.2, size=22)
        pan = panel(sa, sb).move_to([3.8, 1.2, 0])
        self.say("Las ramas de afuera están fijas. La recta del medio se mueve con **dos perillas**: pendiente a y altura b.",
                 Create(ax), Create(izq), Create(der), FadeIn(h1), FadeIn(h2), FadeIn(pan))
        self.add(med)
        self.say("Así no engancha ninguna de las dos puntas.", A.animate.set_value(2.0), run_time=2)
        self.board_start(left=0.6, top=0.2, maxw=6.2)
        p1 = step(1, "en x = 1", L("Izq.: $\\sin\\pi=0$.  Der. y valor: $a+b$.  $\\Rightarrow a+b=0$", 22))
        self.push(p1, "En x = 1: la izquierda llega a seno de π, que es 0. La recta vale a + b. Primera ecuación: a + b = 0.")
        p2 = step(2, "en x = 2", L("Izq. y valor: $2a+b$.  Der.: $4$.  $\\Rightarrow 2a+b=4$", 22))
        self.push(p2, "En x = 2: la recta vale 2a + b, y la parábola llega a 4. Segunda ecuación.")
        p3 = step(3, "sistema", L("Restando: $a=4$, $b=-4$.  Verifico: $4-4=0$ ✓, $8-4=4$ ✓", 22))
        self.push(p3, "Resto las ecuaciones: a = 4, b = −4. Miro la perilla llevarlo ahí...",
                  A.animate.set_value(4.0), B.animate.set_value(-4.0), min_t=4)
        self.say("...y la recta engancha **las dos puntas** a la vez. Un pegado, una ecuación; dos pegados, un sistema.")
        congelar(pan)
        self.remove(med)
        self.add(VGroup(ax.plot(lambda x: 4 * x - 4, x_range=[1, 2], color=GREEN, stroke_width=4)))
        self.wipe()

        # ---- dos valores / familia
        e = enun("PRÁCTICO 4.5 · EJ 3 f) · SALEN DOS VALORES", ["$f(x)=ax^2$ si $x\\le1$;   $a^2x^2-2$ si $x>1$."], size=26).move_to([0, 2.5, 0])
        a = M(r"a=a^2-2\iff a^2-a-2=0\iff(a-2)(a+1)=0", size=42).move_to([0, 1.3, 0])
        r = resp("$a=2$  o  $a=-1$").next_to(a, DOWN, buff=0.35)
        self.say("Puede salir una cuadrática: dos valores de a, **los dos sirven**. En múltiple opción, buscá la opción que tenga ambos.",
                 FadeIn(e), Write(a), FadeIn(r))
        self.wipe()
        e = enun("PRÁCTICO 4.5 · EJ 3 a) · UNA ECUACIÓN, DOS INCÓGNITAS",
                 ["$f(x)=x^2+3x+2$ si $x\\le1$;   $ax^2+bx+1$ si $x>1$."], size=26).move_to([0, 2.5, 0])
        ax = ejes([-2, 2.3, 1], [-1, 20, 5], 6.4, 3.8).move_to([-3.1, -0.4, 0])
        base = ax.plot(lambda x: x * x + 3 * x + 2, x_range=[-2, 1], color=BLUE, stroke_width=4)
        pto = lleno(ax.c2p(1, 6), YELLOW, 0.1)
        fam = VGroup()
        cols = [ORANGE, TEAL, VIOLET, GREEN, RED]
        for i, aa in enumerate([-1.0, 0.0, 1.0, 2.0, 3.0]):
            bb = 5 - aa
            fam.add(ax.plot(lambda x, aa=aa, bb=bb: aa * x * x + bb * x + 1, x_range=[1, 2.1], color=cols[i], stroke_width=3))
        eq = L("En $x=1$: $6=a+b+1\\iff a+b=5$", 26).move_to([3.3, 0.8, 0])
        self.say("Y otro caso: un pegado, **dos incógnitas**. Una sola ecuación: a + b = 5.", FadeIn(e), Create(ax), Create(base), FadeIn(pto), FadeIn(eq))
        self.say("Cada par que suma 5 da una rama que **pasa por el mismo punto**. No hay un valor único: hay una familia entera.",
                 LaggedStart(*[Create(c) for c in fam], lag_ratio=0.3, run_time=3))
        tr = trampa(["Con un pegado y dos parámetros, la respuesta es una **familia**.",
                     "Eso también es una respuesta correcta."], "NO BUSQUES UN VALOR ÚNICO", size=21, width=6.2).move_to([3.4, -1.0, 0])
        self.say("No te quedes buscando un valor único. La familia **es** la respuesta.", FadeIn(tr))
        self.wipe()

        ej = VGroup(*[L(s, 25) for s in ["(a) $f(x)=\\frac{x^2-4}{x-2}$ si $x\\neq2$, $f(2)=k$. Hallar $k$.",
                                         "(b) $f(x)=x^2+a$ si $x\\le2$;  $ax+b$ si $2<x<4$;  $2x$ si $x\\ge4$.",
                                         "(c) $g(x)=x\\sin\\frac1x+a$ si $x\\neq0$,  $g(0)=3$."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        g = self.pausa(ej, "Tu turno. Uno evitable, uno con dos pegados, uno con la máscara.")
        sol = Lines("(a) $x+2\\to4$: $k=4$    (b) $4+a=2a+b$ y $4a+b=8$: $a=\\frac43$, $b=\\frac83$",
                    "(c) $x\\sin\\frac1x\\to0$, así que $a=3$", size=24)
        debajo(sol, g)
        self.say("Soluciones.", FadeIn(sol), min_t=3)
        self.end_scene()


# =====================================================================
class V2_04_IntProp(V2):
    CH_NUM, CH_TITLE = "07", "Propiedades de la integral"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Propiedades de la integral", "Puntos regalados si no te apurás",
                        prob=("ALTA", "3 de 6 · el ejercicio más rápido del parcial"))
        s = self.stamp(["**Linealidad:** $\\int_a^b(\\alpha f+\\beta g)=\\alpha\\int_a^bf+\\beta\\int_a^bg$.",
                        "**Chasles:** $\\int_a^cf=\\int_a^bf+\\int_b^cf$, con $a,b,c$ en **cualquier** orden.",
                        "**Orientación:** $\\int_a^bf=-\\int_b^af$,  $\\int_a^af=0$.     **Constante:** $\\int_a^bk\\,dx=k(b-a)$.",
                        "**Monotonía:** $f\\le g\\Rightarrow\\int_a^bf\\le\\int_a^bg$.   **Acotación:** $m\\le f\\le M\\Rightarrow m(b-a)\\le\\int_a^bf\\le M(b-a)$."],
                       "LAS PROPIEDADES (VISTAS EN CLASE)", size=22).move_to([0, 0.75, 0])
        self.say("Las propiedades vistas en clase. No hay que aprender nada nuevo: hay que **no apurarse** con los signos.",
                 *self.show_stamp(s), min_t=4)
        self.wipe()

        # ---- Chasles visual: áreas que se pegan
        ax = ejes([0, 9, 1], [-1, 3, 1], 11.0, 3.2).move_to([0, 0.6, 0])
        f = lambda x: 1.2 + 0.8 * np.sin(0.9 * x)
        curva = ax.plot(f, x_range=[1, 8.5], color=BLUE, stroke_width=4)
        A1 = ax.get_area(curva, x_range=[2, 4], color=TEAL, opacity=0.45)
        A2 = ax.get_area(curva, x_range=[4, 8], color=ORANGE, opacity=0.45)
        xl = xlabels(ax, [2, 4, 8], size=20)
        l1 = M(r"\int_2^4 f", size=34, color=TEAL).move_to(ax.c2p(3, 0.5))
        l2 = M(r"\int_4^8 f", size=34, color=ORANGE).move_to(ax.c2p(6, 0.5))
        self.say("Chasles, visto: el área de 2 a 8 es el área de 2 a 4 **más** la de 4 a 8. Como pegar dos piezas.",
                 Create(ax), Create(curva), FadeIn(xl), FadeIn(A1), FadeIn(A2), FadeIn(l1), FadeIn(l2))
        tot = Brace(VGroup(A1, A2), DOWN, color=YELLOW).shift(DOWN * 0.3)
        tl = M(r"\int_2^8 f=\int_2^4 f+\int_4^8 f", size=34, color=YELLOW).next_to(tot, DOWN, buff=0.1)
        self.say("Y vale en **cualquier** orden de los puntos: si el tramo va para atrás, el signo se da vuelta y la cuenta sigue cerrando.",
                 GrowFromCenter(tot), Write(tl))
        self.wipe()

        # ---- ejercicio de parcial
        e = enun("PARCIAL 2025-1 · EJ 2", ["$\\int_2^8 2f=6$,   $\\int_2^4f=1$,   $\\int_4^8(f+g)=4$. Hallar $\\int_4^83g$."], size=28).move_to([0, 2.5, 0])
        self.say("Parcial 2025. Pausá y hacé primero **una sola cosa**: sacá las constantes de cada dato.", FadeIn(e), min_t=3)
        nl = NumberLine(x_range=[1, 9, 1], length=6.0, color=SOFT, include_numbers=False).move_to([3.7, -1.9, 0])
        nums = VGroup(*[M(str(v), size=28, color=SOFT).next_to(nl.n2p(v), DOWN, buff=0.12) for v in [2, 4, 8]])
        self.add(nl, nums)
        self.board_start(top=1.5, maxw=6.4)

        def barra(a, b, color, txt, y):
            r = Rectangle(width=nl.n2p(b)[0] - nl.n2p(a)[0], height=0.4, stroke_width=0).set_fill(color, 0.55)
            r.move_to([(nl.n2p(a)[0] + nl.n2p(b)[0]) / 2, y, 0])
            return VGroup(r, M(txt, size=26, color=INK).move_to(r))
        p1 = step(1, "limpio", M(r"\int_2^8 f=3", size=40))
        b1 = barra(2, 8, VIOLET, r"\int_2^8 f=3", -0.9)
        b1.scale_to_fit_height(0.5).move_to([(nl.n2p(2)[0] + nl.n2p(8)[0]) / 2, -0.95, 0])
        self.push(p1, "Paso uno: limpio. La integral de 2f es 6, así que la de f es **3**.", FadeIn(b1))
        p2 = step(2, "Chasles", M(r"3=\int_2^4 f+\int_4^8 f=1+\int_4^8 f\ \Rightarrow\ \int_4^8 f=2", size=40))
        b2 = barra(2, 4, TEAL, "1", -1.45)
        b3 = barra(4, 8, ORANGE, r"\int_4^8 f=2", -1.45)
        self.push(p2, "Paso dos, Chasles: el tramo violeta es el teal más el naranja. 3 = 1 + lo que falta. Lo que falta es **2**.", FadeIn(b2), FadeIn(b3))
        p3 = step(3, "linealidad", M(r"4=\int_4^8 f+\int_4^8 g=2+\int_4^8 g\ \Rightarrow\ \int_4^8 g=2", size=40))
        self.push(p3, "Paso tres, linealidad: la integral de f + g es la suma. 4 = 2 + la de g. La de g es **2**.")
        p4 = step(4, "coeficiente final", M(r"\int_4^8 3g=3\cdot2=6", size=40))
        self.push(p4, "Y recién al final, el coeficiente que pide el enunciado: 3 por 2.")
        r = resp("$6$")
        self.push(r, "Respuesta: 6.", anim=FadeIn(r))
        self.wipe()
        met = metodo(["**Limpiá las constantes** de cada dato: $\\int2f=6\\Rightarrow\\int f=3$.",
                      "Escribí en una **columna** cada integral limpia con sus extremos.",
                      "Unificá la **orientación**: si un dato viene como $\\int_8^4$, pasalo a $-\\int_4^8$.",
                      "Chasles para intervalos superpuestos. Despejá.",
                      "Recién al final, aplicá el coeficiente que pide el enunciado."],
                     "COMBINAR INTEGRALES", size=25).move_to([0, 0.5, 0])
        self.say("El molde, en cinco pasos. Si lo seguís en orden, este ejercicio **no se puede errar**.", FadeIn(met), min_t=4)
        self.end_scene()


# =====================================================================
class V2_05_IntPractico(V2):
    CH_NUM, CH_TITLE = "07", "Propiedades · práctico"

    def construct(self):
        self.setup_frame()
        e = enun("PRÁCTICO 3.6 · EJ 3 · ORIENTACIÓN + ABSURDO",
                 ["$f:[2,8]\\to\\R$ integrable, $\\int_2^8f=20$ y $\\int_8^4f=12$. (a) Calcular $\\int_2^4f$.",
                  "(b) Probar que existen $c,d\\in[2,4]$ con $f(c)\\ge15$ y $f(d)\\le17$."], size=25).move_to([0, 2.4, 0])
        self.say("Del práctico, un ejercicio que junta la orientación con una demostración por absurdo.", FadeIn(e), min_t=2.5)
        self.board_start(top=1.2, maxw=12.5)
        p1 = step(1, "doy vuelta el dato", M(r"\int_8^4 f=12\ \Rightarrow\ \int_4^8 f=-12", size=40))
        self.push(p1, "El dato viene al revés, de 8 a 4. Lo doy vuelta y **cambia el signo**: −12.")
        p2 = step(2, "Chasles", M(r"\int_2^4 f=20-(-12)=32", size=40))
        self.push(p2, "Chasles: 20 menos menos 12. **32**, no 8.")
        tr = trampa(["$20-(-12)=32$, no 8. El error de signo más común de todo el capítulo."], "RESTAR UN NEGATIVO", size=24)
        self.push(tr, "La trampa más común del capítulo: restar un negativo.", anim=FadeIn(tr))
        self.wipe(e)

        # ---- el absurdo, con perilla de techo
        ax = ejes([1.5, 4.5, 1], [0, 22, 5], 6.2, 4.0).move_to([-3.3, -0.35, 0])
        f = lambda x: 16 + 3 * np.sin(np.pi * (x - 2)) - 0.6 * (x - 3)
        curva = ax.plot(f, x_range=[2, 4], color=BLUE, stroke_width=4)
        area = ax.get_area(curva, x_range=[2, 4], color=BLUE, opacity=0.25)
        xl = xlabels(ax, [2, 4], size=20)
        h = ValueTracker(18.0)
        techo = always_redraw(lambda: Rectangle(width=ax.c2p(4, 0)[0] - ax.c2p(2, 0)[0],
                                                height=ax.c2p(0, h.get_value())[1] - ax.c2p(0, 0)[1],
                                                stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.08)
                              .move_to([(ax.c2p(2, 0)[0] + ax.c2p(4, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, h.get_value())[1]) / 2, 0]))
        sl = Slider("techo", h, 10, 20, color=YELLOW, decimals=1, width=2.3, size=22)
        lr = lectura("área máxima $=2\\cdot$techo $=$", lambda: 2 * h.get_value(), YELLOW, 1, 22)
        lv = L("área real $=32$", 22, BLUE)
        pan = panel(sl, lr, lv).move_to([3.6, 0.9, 0])
        ver = always_redraw(lambda: T("entra: puede ser" if 2 * h.get_value() >= 32 else "¡no entra 32! absurdo", 22,
                                      GREEN if 2 * h.get_value() >= 32 else RED, MONO, BOLD).move_to([3.6, -0.6, 0]))
        self.say("Parte b, con imagen. La integral de 2 a 4 es 32: esa es el **área** azul.", Create(ax), Create(curva), FadeIn(area), FadeIn(xl))
        self.add(techo, ver)
        self.say("Supongamos que f queda **debajo de un techo** en todo [2, 4]. Entonces el área cabe en la caja amarilla: 2 por el techo.",
                 FadeIn(pan))
        self.say("Bajo el techo... hasta 16, la caja todavía tiene área 32. Pero si el techo es **15**, la caja tiene 30.",
                 h.animate.set_value(15.0), run_time=4)
        self.say("Un área de 32 no entra en una caja de 30. **Absurdo.** Entonces f no puede estar toda debajo de 15: existe un c con f(c) ≥ 15.")
        p = Lines("Si $f<15$ en todo $[2,4]$: $\\int_2^4f\\le15\\cdot2=30<32$. Absurdo.",
                  "Si $f>17$ en todo $[2,4]$: $\\int_2^4f\\ge17\\cdot2=34>32$. Absurdo. $\\blacksquare$", size=22)
        p.scale_to_fit_width(6.4).move_to([3.6, -1.75, 0])
        self.say("La otra mitad es el espejo: un **piso** de 17 daría área 34, que se pasa de 32.", FadeIn(p))
        congelar(pan)
        self.remove(techo, ver)
        self.wipe()
        tip = self.tip(["$f$ es solo integrable, no continua: el teorema del valor medio no aplica.",
                        "La monotonía de la integral sí, **siempre**."], label="POR QUÉ NO SE USA EL VALOR MEDIO", size=24).move_to([0, 1.6, 0])
        self.say("Ojo: acá **no** se usa el valor medio, porque f es solo integrable. La monotonía de la integral vale siempre.", FadeIn(tip))

        # ---- acotar sin calcular
        e = enun("PRÁCTICO 3.2 · EJ 1 · ACOTAR SIN CALCULAR", ["Probar que $\\dfrac{\\sqrt3}{4}\\le\\displaystyle\\int_0^{1/2}\\sqrt{1-x^2}\\,dx\\le\\dfrac12$."], size=26).move_to([0, -0.5, 0])
        self.say("Otro uso de la misma idea: **acotar** una integral sin calcularla.", FadeIn(e))
        self.wipe(e)
        self.play(e.animate.move_to([0, 2.45, 0]))
        ax = ejes([0, 0.7, 0.5], [0, 1.2, 0.5], 5.0, 3.9).move_to([-3.4, -0.4, 0])
        g = lambda x: np.sqrt(1 - x * x)
        c = ax.plot(g, x_range=[0, 0.5], color=BLUE, stroke_width=4)
        ar = ax.get_area(c, x_range=[0, 0.5], color=BLUE, opacity=0.35)
        top = Rectangle(width=ax.c2p(0.5, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1],
                        stroke_color=RED, stroke_width=2.5).move_to((ax.c2p(0, 0) + ax.c2p(0.5, 1)) / 2)
        bot = Rectangle(width=ax.c2p(0.5, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, g(0.5))[1] - ax.c2p(0, 0)[1],
                        stroke_color=TEAL, stroke_width=0, fill_color=TEAL, fill_opacity=0.45).move_to((ax.c2p(0, 0) + ax.c2p(0.5, g(0.5))) / 2)
        self.board_start(left=0.2, top=1.4, maxw=6.4)
        p1 = step(1, "techo y piso de f", L("$\\sqrt{1-x^2}$ decrece: máx $f(0)=1$, mín $f(\\frac12)=\\frac{\\sqrt3}2$.", 23))
        self.push(p1, "La función decrece en [0, ½]: el techo es f(0) = 1 y el piso f(½) = raíz de 3 sobre 2.", Create(ax), Create(c), FadeIn(ar))
        p2 = step(2, "acotación", L("$\\frac{\\sqrt3}2\\cdot\\frac12\\le\\int\\le1\\cdot\\frac12$, es decir $\\frac{\\sqrt3}4\\le\\int\\le\\frac12$. $\\blacksquare$", 23))
        self.push(p2, "El área queda **entre dos cajas**: la teal de abajo y la roja de arriba. Piso por ancho y techo por ancho.",
                  FadeIn(bot), Create(top))
        self.wipe()

        # ---- área con signo vs Darboux
        e = enun("INTEGRAL POR GEOMETRÍA · ÁREA CON SIGNO",
                 ["$f$: segmento de $(0,0)$ a $(2,2)$, constante 2 hasta $x=4$, baja recto hasta $(6,-2)$. Calcular $\\int_0^6f$ y el área."], size=24).move_to([0, 2.5, 0])
        ax = ejes([0, 6.5, 1], [-2.5, 2.8, 1], 8.0, 3.6).move_to([-1.9, -0.3, 0])
        pts = [(0, 0), (2, 2), (4, 2), (6, -2)]
        pl = VMobject(color=BLUE, stroke_width=4).set_points_as_corners([ax.c2p(*p) for p in pts])
        pos = Polygon(ax.c2p(0, 0), ax.c2p(2, 2), ax.c2p(4, 2), ax.c2p(5, 0), stroke_width=0, fill_color=GREEN, fill_opacity=0.45)
        neg = Polygon(ax.c2p(5, 0), ax.c2p(6, -2), ax.c2p(6, 0), stroke_width=0, fill_color=RED, fill_opacity=0.5)
        self.say("Integral por geometría. Lo que queda **arriba** del eje suma; lo que queda **abajo**, resta.",
                 FadeIn(e), Create(ax), Create(pl))
        self.play(FadeIn(pos), FadeIn(neg))
        cu = Lines("Triángulo: $+2$. Rectángulo: $+4$.", "En $[4,6]$ cruza en 5: $+1$ y $-1$.",
                   "$\\int_0^6f=2+4+1-1=6$", "Área: $2+4+1+1=8$", size=23).move_to([4.6, -0.2, 0])
        self.say("Integral: 2 + 4 + 1 − 1 = 6. Pero **el área** encerrada suma todo en positivo: 8. Preguntate siempre cuál de las dos te piden.",
                 FadeIn(cu))
        tr = trampa(["En la integral lo de abajo **resta**. En $\\Ss(f,P)$ no se compensa nada:",
                     "cada bloque es una caja plana (capítulo 3)."], "INTEGRAL NO ES SUMA DE DARBOUX", size=20, width=5.8).move_to([4.1, -0.3, 0])
        self.say("Y no la confundas con Darboux: en una suma superior **no se compensa** nada.", FadeOut(cu), FadeIn(tr))
        self.wipe()
        ej = VGroup(*[L(s, 25) for s in ["(a) $\\int_0^3f=5$, $\\int_2^3f=1$, $\\int_0^2(f+2g)=10$. Hallar $\\int_2^05g$.",
                                         "(b) Acotar $\\int_0^1\\frac{dx}{1+x^2}$ sin calcularla.",
                                         "(c) $h$ integrable en $[-1,3]$ con $\\int_{-1}^3h=8$. Probar que existe $c$ con $h(c)\\ge1{,}9$."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        g = self.pausa(ej, "Tu turno. Ojo en la a: el extremo final viene al revés.")
        sol = Lines("(a) $\\int_0^2f=4$, $\\int_0^2g=3$: $\\int_2^05g=-15$   (b) $\\frac12\\le\\int\\le1$",
                    "(c) Si $h<1{,}9$ siempre: $\\int\\le1{,}9\\cdot4=7{,}6<8$. Absurdo.", size=24)
        debajo(sol, g)
        self.say("Soluciones. En la a, la orientación da vuelta el signo al final: **−15**.", FadeIn(sol))
        self.end_scene()


# =====================================================================
class V2_06_BolzTeoria(V2):
    CH_NUM, CH_TITLE = "08", "Bolzano, valor medio, Weierstrass"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Bolzano, valor medio, Weierstrass", "Lo continuo no puede saltar",
                        prob=("ALTA", "tema de la última semana · directo y en V/F"))
        s = self.stamp(["**H:** $f$ continua en $[a,b]$ **cerrado** y $f(a)\\cdot f(b)<0$.",
                        "**T:** existe $c\\in(a,b)$ con $f(c)=0$."], "BOLZANO", size=28).move_to([0, 2.3, 0])
        self.say("Bolzano: si una función continua empieza **negativa** y termina **positiva**, en algún lado cruzó el cero.",
                 *self.show_stamp(s))
        ax = ejes([-2.6, 1.6, 1], [-6, 7, 3], 8.0, 3.6).move_to([-1.6, -0.75, 0])
        f = lambda x: x ** 3 - x + 3
        c = ax.plot(f, x_range=[-2.2, 1.35], color=BLUE, stroke_width=4)
        xl = xlabels(ax, [-2, -1, 1], size=20)
        self.say("Mirá x³ − x + 3. Como no puede saltar, para ir de abajo a arriba **tiene** que atravesar el eje.",
                 Create(ax), Create(c), FadeIn(xl))

        # ---- bisección animada: el intervalo se achica hacia la raíz
        lo, hi = ValueTracker(-2.0), ValueTracker(-1.0)
        caja = always_redraw(lambda: Rectangle(width=ax.c2p(hi.get_value(), 0)[0] - ax.c2p(lo.get_value(), 0)[0],
                                               height=ax.c2p(0, 7)[1] - ax.c2p(0, -6)[1], stroke_width=0)
                             .set_fill(YELLOW, 0.14).move_to([(ax.c2p(lo.get_value(), 0)[0] + ax.c2p(hi.get_value(), 0)[0]) / 2,
                                                             (ax.c2p(0, 7)[1] + ax.c2p(0, -6)[1]) / 2, 0]))
        plo = always_redraw(lambda: lleno(ax.c2p(lo.get_value(), f(lo.get_value())), RED, 0.09))
        phi = always_redraw(lambda: lleno(ax.c2p(hi.get_value(), f(hi.get_value())), GREEN, 0.09))
        pan = panel(lectura("$f(p)=$", lambda: f(lo.get_value()), RED, 3, 22),
                    lectura("$f(q)=$", lambda: f(hi.get_value()), GREEN, 3, 22),
                    lectura("ancho $=$", lambda: hi.get_value() - lo.get_value(), YELLOW, 4, 22)).move_to([4.7, -0.4, 0])
        self.add(caja, plo, phi)
        self.say("f(−2) = −3, negativo; f(−1) = 3, positivo. Bolzano garantiza una raíz en la franja amarilla.", FadeIn(pan))
        a_, b_ = -2.0, -1.0
        for _ in range(6):
            m = (a_ + b_) / 2
            if f(a_) * f(m) <= 0:
                b_ = m
                anim = hi.animate.set_value(m)
            else:
                a_ = m
                anim = lo.animate.set_value(m)
            self.play(anim, run_time=0.9 * PACE)
        self.say("Y se puede **apretar**: parto al medio, me quedo con la mitad donde sigue cambiando el signo, y repito. Es una búsqueda binaria: la raíz está cerca de **−1,67**.")
        congelar(pan)
        self.remove(caja, plo, phi)
        self.wipe()

        s2 = self.stamp(["$f$ continua en $[a,b]$ toma **todos** los valores entre $f(a)$ y $f(b)$."], "VALOR INTERMEDIO", size=26).move_to([0, 2.4, 0])
        s3 = self.stamp(["$f$ continua en $[a,b]$ **cerrado y acotado** $\\Rightarrow$ alcanza máximo y mínimo absolutos."],
                        "WEIERSTRASS (SIN PRUEBA EN EL CURSO)", size=26).move_to([0, 0.75, 0])
        s4 = self.stamp(["$f$ continua en $[a,b]\\Rightarrow\\exists c\\in[a,b]:\\ f(c)(b-a)=\\int_a^bf$."], "VALOR MEDIO PARA INTEGRALES", size=26).move_to([0, -1.0, 0])
        self.say("Los otros tres teoremas. Valor intermedio es Bolzano aplicado a f − k.", *self.show_stamp(s2))
        self.say("Weierstrass: continua en un intervalo **cerrado y acotado** alcanza máximo y mínimo.", *self.show_stamp(s3))
        self.say("Y valor medio para integrales: hay un punto donde f vale **el promedio**.", *self.show_stamp(s4))
        self.wipe()

        # ---- valor medio: el agua que se nivela
        ax = ejes([-2.3, 1.4, 1], [0, 2.4, 1], 7.2, 3.9).move_to([-2.2, -0.2, 0])
        g = lambda x: 2 / 3 * (x + 2)
        cv = ax.plot(g, x_range=[-2, 1], color=BLUE, stroke_width=4)
        t = ValueTracker(0.0)
        agua = always_redraw(lambda: ax.get_area(ax.plot(lambda x: (1 - t.get_value()) * g(x) + t.get_value() * 1.0, x_range=[-2, 1]),
                                                 x_range=[-2, 1], color=BLUE, opacity=0.4))
        self.say("El valor medio, como agua. Tengo f(x) = ⅔(x + 2) en [−2, 1]. Su integral es 3: esa área azul.",
                 Create(ax), Create(cv), FadeIn(xlabels(ax, [-2, 1], size=20)))
        self.add(agua)
        sl = Slider("nivelar", t, 0, 1, color=BLUE, decimals=2, width=2.2, size=22).move_to([4.2, 1.2, 0])
        self.say("Ahora dejo que el agua **se nivele**, sin perder volumen. El área no cambia: 3.", FadeIn(sl),
                 t.animate.set_value(1.0), run_time=4, rate_func=smooth)
        nivel = DashedLine(ax.c2p(-2.2, 1), ax.c2p(1.2, 1), color=YELLOW, stroke_width=2.5)
        cpt = lleno(ax.c2p(-0.5, 1), YELLOW, 0.1)
        cl = M("c=-\\tfrac12", size=30, color=YELLOW).next_to(cpt, UP, buff=0.2)
        cu = Lines("Nivel: $\\frac{3}{1-(-2)}=1$.", "Existe $c$ con $f(c)=1$:", "la curva **cruza** el nivel.", size=23).move_to([4.2, -0.4, 0])
        self.say("Queda a altura **1**: el promedio, integral sobre largo. Y como f es continua y va de abajo a arriba del nivel, en algún c **vale exactamente 1**.",
                 Create(nivel), FadeIn(cpt), FadeIn(cl), FadeIn(cu))
        congelar(sl)
        self.remove(agua)
        self.wipe()

        # ---- lo que Bolzano no dice
        a1 = ejes([-1.3, 1.3, 1], [-1.4, 1.4, 1], 4.4, 2.8).move_to([-3.3, 0.3, 0])
        a2 = ejes([-1.3, 1.3, 1], [-0.4, 1.4, 1], 4.4, 2.8).move_to([3.3, 0.3, 0])
        sg = VGroup(a1.plot(lambda x: -1, x_range=[-1.2, 0], color=BLUE, stroke_width=4), a1.plot(lambda x: 1, x_range=[0, 1.2], color=BLUE, stroke_width=4),
                    hueco(a1.c2p(0, -1)), hueco(a1.c2p(0, 1)), lleno(a1.c2p(0, 0)))
        sq = a2.plot(lambda x: x * x, x_range=[-1.15, 1.15], color=BLUE, stroke_width=4)
        n1 = Lines("signo$(x)$: cambia de signo", "y **salta** el cero. Sin continuidad,", "Bolzano no garantiza nada.", size=21).next_to(a1, DOWN, buff=0.25)
        n2 = Lines("$x^2$: tiene raíz **sin** cambiar", "de signo. El recíproco es falso.", size=21).next_to(a2, DOWN, buff=0.25)
        self.say("Lo que Bolzano **no** dice. Sin continuidad, la función puede saltar el cero: el signo pasa de −1 a 1 sin cruzar.",
                 Create(a1), Create(sg), FadeIn(n1))
        self.say("Y el recíproco es falso: x² tiene raíz sin cambiar de signo. Tampoco dice que la raíz sea **única**.",
                 Create(a2), Create(sq), FadeIn(n2))
        self.wipe()
        met = metodo(["Pasá todo a un lado: $h(x)=\\text{izq}-\\text{der}$. Raíz de $h$ = solución.",
                      "Justificá la continuidad de $h$ en una frase.",
                      "Evaluá enteros (o puntos cómodos) hasta que el signo se dé vuelta.",
                      "Escribí: «$h$ continua en $[p,q]$ y $h(p)h(q)<0$; por Bolzano $\\exists c\\in(p,q)$ con $h(c)=0$»."],
                     "BOLZANO EN EL PARCIAL", size=25).move_to([0, 0.5, 0])
        self.say("El método para el parcial. El cuarto paso es la frase que tenés que **escribir**: hipótesis verificadas, y recién ahí la conclusión.",
                 FadeIn(met), min_t=4)
        self.end_scene()


# =====================================================================
class V2_07_BolzEjercicios(V2):
    CH_NUM, CH_TITLE = "08", "Bolzano · ejercicios"

    def construct(self):
        self.setup_frame()
        e = enun("PARCIAL 2024-1 · EJ 6", ["Hallar $n\\in\\Z$ tal que $x^3-x+3=0$ tenga una raíz en $[n,n+1]$."], size=28).move_to([0, 2.5, 0])
        self.say("Parcial 2024. Evaluar enteros hasta que el signo **se dé vuelta**.", FadeIn(e))
        ax = ejes([-3, 2, 1], [-8, 8, 4], 6.0, 3.8).move_to([-3.4, -0.3, 0])
        f = lambda x: x ** 3 - x + 3
        c = ax.plot(f, x_range=[-2.3, 1.4], color=BLUE, stroke_width=3)
        xl = xlabels(ax, [-2, -1, 1], size=18)
        self.play(Create(ax), Create(c), FadeIn(xl))
        x = ValueTracker(1.0)
        punto = always_redraw(lambda: lleno(ax.c2p(x.get_value(), f(x.get_value())), GREEN if f(x.get_value()) > 0 else RED, 0.1))
        guia = always_redraw(lambda: DashedLine(ax.c2p(x.get_value(), 0), ax.c2p(x.get_value(), f(x.get_value())),
                                                color=GREEN if f(x.get_value()) > 0 else RED, stroke_width=2))
        rd = lectura("$f(x)=$", lambda: f(x.get_value()), INK, 2, 24).move_to([3.4, 1.0, 0])
        self.add(guia, punto)
        tabla_v = VGroup()
        self.say("Arranco en 1: f(1) = 3, positivo.", FadeIn(rd))
        for v in [0, -1, -2]:
            x_ = float(v)
            self.play(x.animate.set_value(x_), run_time=1.0 * PACE)
            tv = L(f"$f({v})={int(f(x_))}$", 26, GREEN if f(x_) > 0 else RED)
            tabla_v.add(tv)
            tabla_v.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -0.4, 0])
            self.play(FadeIn(tv), run_time=0.4)
        fr = Rectangle(width=ax.c2p(-1, 0)[0] - ax.c2p(-2, 0)[0], height=3.6, stroke_width=0).set_fill(YELLOW, 0.15).move_to(
            [(ax.c2p(-2, 0)[0] + ax.c2p(-1, 0)[0]) / 2, ax.get_center()[1], 0])
        self.say("En 0 y en −1 sigue positiva... en **−2** se da vuelta: −3. Continua, y cambia de signo entre −2 y −1: Bolzano.", FadeIn(fr))
        r = resp("$n=-2$").move_to([3.4, -2.0, 0])
        self.say("La raíz está en [−2, −1]: n = −2.", FadeIn(r))
        congelar(rd)
        self.remove(guia, punto)
        self.wipe()

        # ---- buscar lejos
        e = enun("PRÁCTICO 5.2 · EJ 1 b) c) · CUANDO LOS VALORES CHICOS NO CAMBIAN DE SIGNO",
                 ["$f(x)=x^5+5x^4+2x+1$. Hallar $n$ con raíz en $[n,n+1]$."], size=26).move_to([0, 2.5, 0])
        self.say("Un caso más salado. f(−1), f(0), f(1): **todos positivos**. ¿Dónde está la raíz?", FadeIn(e), min_t=2.5)
        cu = Lines("El término dominante $x^5$ manda para $x$ muy negativo: ahí tiene que volverse negativo.",
                   "$f(-4)=-1024+1280-8+1=249>0$",
                   "$f(-5)=-3125+3125-10+1=-9<0$", size=26).move_to([0, 0.6, 0])
        r = resp("$n=-5$").next_to(cu, DOWN, buff=0.4)
        self.say("Cuando los valores chicos no cambian de signo, **buscá lejos**. Para x muy negativo, x a la quinta manda y es negativa. En −5 se da vuelta.",
                 FadeIn(cu), FadeIn(r))
        self.wipe()

        # ---- al menos tres soluciones
        e = enun("PRÁCTICO 5.2 · EJ 1 f) · AL MENOS TRES SOLUCIONES", ["Probar que $1-x^4=\\cos x$ tiene al menos tres soluciones."], size=27).move_to([0, 2.5, 0])
        ax = ejes([-1.4, 1.4, 0.5], [-1.2, 0.4, 0.5], 6.4, 3.8).move_to([-3.2, -0.35, 0])
        h = lambda x: 1 - x ** 4 - np.cos(x)
        c = ax.plot(h, x_range=[-1.2, 1.2], color=BLUE, stroke_width=4)
        self.board_start(left=0.4, top=1.45, maxw=6.2)
        p1 = step(1, "función auxiliar", L("$h(x)=1-x^4-\\cos x$, continua y **par**.", 23))
        self.push(p1, "Paso todo a un lado: h(x) = 1 − x⁴ − cos x. Es continua, y además **par**: simétrica respecto al eje vertical.",
                  FadeIn(e), Create(ax), Create(c))
        p2 = step(2, "una gratis", L("$h(0)=1-0-1=0$.", 23))
        z = lleno(ax.c2p(0, 0), YELLOW, 0.1)
        self.push(p2, "Una solución gratis: h(0) = 0.", FadeIn(z))
        p3 = step(3, "cambio de signo", L("$h(\\frac12)\\approx0{,}06>0$,  $h(1)\\approx-0{,}54<0$.", 23))
        pp = VGroup(lleno(ax.c2p(0.5, h(0.5)), GREEN), lleno(ax.c2p(1, h(1)), RED))
        self.push(p3, "Busco cambios de signo lejos del cero: en ½ es positiva, en 1 negativa. Bolzano: raíz entre ½ y 1.", FadeIn(pp))
        p4 = step(4, "simetría", L("Por ser par, también hay raíz en $(-1,-\\frac12)$. $\\blacksquare$", 23))
        pm = VGroup(lleno(ax.c2p(-0.5, h(-0.5)), GREEN), lleno(ax.c2p(-1, h(-1)), RED))
        self.push(p4, "Y la simetría me regala la tercera, del otro lado, **sin hacer ninguna cuenta**.", TransformFromCopy(pp, pm))
        self.wipe()

        # ---- múltiple opción valor medio
        e = enun("PRÁCTICO 5.2 · EJ 7 c) (MÚLTIPLE OPCIÓN)",
                 ["$f$ continua con $\\int_{-2}^1f=3$. Necesariamente: (A) $f\\equiv1$  (B) $f<2$ siempre",
                  "(C) $\\exists\\alpha: f(\\alpha)=-3$   (D) $\\exists\\alpha: f(\\alpha)=1$   (E) $f>\\frac12$ siempre"], size=25).move_to([0, 2.3, 0])
        cu = M(r"f(c)\cdot(1-(-2))=3\ \Rightarrow\ f(c)=1", size=42).move_to([0, 0.7, 0])
        r = resp("(D)").next_to(cu, DOWN, buff=0.35)
        nt = L("Las demás caen con $f(x)=\\frac23(x+2)$: integra 3 y toma valores de 0 a 2.", 23).next_to(r, DOWN, buff=0.35)
        self.say("Múltiple opción: es **exactamente** el agua nivelada de recién. El promedio es 3 sobre 3: 1. Opción D.",
                 FadeIn(e), Write(cu), FadeIn(r))
        self.say("Y las demás se rompen con un contraejemplo: la misma recta del agua.", FadeIn(nt))
        self.wipe()

        # ---- Weierstrass: el máximo que se escapa
        tit = T("¿Hay máximo y mínimo? Weierstrass pide cerrado y acotado", 28, INK, SANS, BOLD).move_to([0, 2.6, 0])
        ax = ejes([-1.3, 1.3, 1], [-0.2, 1.3, 1], 6.4, 3.6).move_to([-3.1, -0.3, 0])
        c = ax.plot(lambda x: x * x, x_range=[-1, 1], color=BLUE, stroke_width=4)
        he = VGroup(hueco(ax.c2p(-1, 1)), hueco(ax.c2p(1, 1)))
        tope = DashedLine(ax.c2p(-1.2, 1), ax.c2p(1.2, 1), color=RED, stroke_width=2)
        xv = ValueTracker(0.3)
        pt = always_redraw(lambda: lleno(ax.c2p(xv.get_value(), xv.get_value() ** 2), YELLOW, 0.1))
        rd = lectura("$x^2=$", lambda: xv.get_value() ** 2, YELLOW, 4, 24).move_to([3.4, 0.8, 0])
        self.say("x² en el intervalo **abierto** (−1, 1). Los extremos están afuera: puntos huecos.",
                 Write(tit), Create(ax), Create(c), FadeIn(he), Create(tope))
        self.add(pt)
        self.play(FadeIn(rd))
        self.say("Persigo el máximo: me acerco al borde... 0,99... 0,9999... el valor se acerca a 1 pero **nunca llega**. Supremo 1, sin máximo.",
                 xv.animate.set_value(0.9995), run_time=5, rate_func=rate_functions.ease_out_cubic)
        tb = Lines("$x^2$ en $(-1,1)$: sup 1 sin máx; mín 0.",
                   "$\\frac1x$ en $(3,5)$: sup $\\frac13$ sin máx; ínf $\\frac15$ sin mín.",
                   "$\\sin x$ en $(0,\\pi)$: máx 1; ínf 0 sin mín.", size=22).move_to([3.4, -1.0, 0])
        self.say("Todas estas son continuas, pero en intervalos **abiertos**. Donde falla la hipótesis, puede faltar máximo o mínimo.", FadeIn(tb))
        congelar(rd)
        self.remove(pt)
        self.wipe()
        ej = VGroup(*[L(s, 25) for s in ["(a) Hallar $n$ con raíz de $x^3+2x-1$ en $[n,n+1]$.",
                                         "(b) Probar que $\\cos x=x$ tiene solución en $[0,\\frac\\pi2]$.",
                                         "(c) $f$ continua con $\\int_0^4f=2$: ¿qué valor toma $f$ seguro?"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        g = self.pausa(ej, "Tu turno. Tres minutos, tres ejercicios.")
        sol = Lines("(a) $f(0)=-1$, $f(1)=2$: $n=0$   (b) $h=\\cos x-x$: $h(0)=1>0$, $h(\\frac\\pi2)=-\\frac\\pi2<0$",
                    "(c) Valor medio: $f(c)\\cdot4=2$, así que $f(c)=\\frac12$", size=24)
        debajo(sol, g)
        self.say("Soluciones. Con esto cerramos el video 2.", FadeIn(sol), min_t=3)
        self.end_scene()
