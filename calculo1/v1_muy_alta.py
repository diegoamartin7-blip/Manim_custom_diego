"""
VIDEO 1 - PROBABILIDAD MUY ALTA  (libro: capitulos 1 a 5)
  Intro: formato del parcial, ranking, regla del blanco
  Cap 2  Supremo, infimo, maximo, minimo
  Cap 3  Sumas de Darboux
  Cap 4  Integrabilidad (telescopica, existe P?)
  Cap 5  epsilon-delta: el delta maximo
Todas las cuentas salen del libro "Calculo1_1er_parcial_libro.pdf" (verificadas con sympy).
"""
from calc_base import *

SCENE_ORDER = ["V1_00_Intro",
               "V1_01_SupTeoria", "V1_02_SupParcial", "V1_03_SupPractico",
               "V1_04_DarbouxTeoria", "V1_05_DarbouxParcial", "V1_06_DarbouxPractico",
               "V1_07_IntegTeoria", "V1_08_IntegParcial",
               "V1_09_EpsTeoria", "V1_10_EpsParcial", "V1_11_EpsPractico"]


class V1(GBase):
    VIDEO_TAG = "VIDEO 1 · PROBABILIDAD MUY ALTA"


# ---------------------------------------------------------------- utilidades de dibujo
def sup_inf(f, a, b, n=400, extra=()):
    xs = list(np.linspace(a, b, n)) + [a, b] + [x for x in extra if a <= x <= b]
    ys = [f(x) for x in xs]
    return max(ys), min(ys)


def cajas(ax, f, P, kind="sup", color=RED, opacity=0.35, extra=(), stroke=1.5):
    g = VGroup()
    for a, b in zip(P[:-1], P[1:]):
        Mx, mn = sup_inf(f, a, b, extra=extra)
        h = Mx if kind == "sup" else mn
        p0, p1 = ax.c2p(a, 0), ax.c2p(b, h)
        r = Rectangle(width=abs(p1[0] - p0[0]), height=max(abs(p1[1] - p0[1]), 1e-3),
                      stroke_color=color, stroke_width=stroke, fill_color=color, fill_opacity=opacity)
        r.move_to((p0 + p1) / 2)
        g.add(r)
    return g


def linea_num(xmin, xmax, width, y=0.0, color=SOFT):
    nl = NumberLine(x_range=[xmin, xmax, 1], length=width, color=color, stroke_width=2,
                    include_tip=True, tip_length=0.16, tip_width=0.14, include_ticks=False)
    nl.move_to([0, y, 0])
    return nl


def tick(nl, v, txt=None, color=SOFT, size=30, up=False):
    p = nl.n2p(v)
    t = Line(p + DOWN * 0.1, p + UP * 0.1, color=color, stroke_width=2)
    lab = M(txt if txt is not None else f"{v:g}", size=size, color=color)
    lab.next_to(t, UP if up else DOWN, buff=0.1)
    return VGroup(t, lab)


def hueco(p, color=RED, r=0.08):
    return Circle(radius=r, color=color, stroke_width=3).set_fill(BG, 1).move_to(p)


def lleno(p, color=RED, r=0.08):
    return Dot(p, radius=r, color=color)


# =====================================================================
class V1_00_Intro(V1):
    def construct(self):
        self.setup_frame(header=False)
        t1 = T("CDIV · IMERL · FING · 2S 2026", 22, SOFT, MONO)
        t2 = T("Cálculo 1", 76, INK, SANS, BOLD)
        t3 = T("Primer parcial", 44, BLUE, SANS, BOLD)
        t4 = T("Los ejercicios que más probablemente te toquen, resueltos paso a paso.", 26, SOFT)
        g = VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.3).shift(UP * 0.6)
        self.play(FadeIn(t1, shift=DOWN * 0.2), Write(t2), run_time=1.5)
        self.play(FadeIn(t3, shift=UP * 0.2), FadeIn(t4), run_time=0.8)
        self.say("Este video es la versión visual del libro del primer parcial. No repasa toda la teoría pareja: va **directo a los ejercicios** que más probablemente te toquen.")
        self.say("La teoría ya la entendiste en clase. Lo que se entrena acá es otra cosa: **reconocer el tipo de ejercicio** y ejecutar el molde.")
        self.wipe()

        # ---- el formato
        self.board_start()
        a = L("Unos **ocho ejercicios de múltiple opción**, cortos, cada uno sobre una sola idea.", 30)
        self.push(a, "Primero, el formato. En los seis parciales analizados fue casi siempre igual: unos **ocho ejercicios de múltiple opción**, cortos.")
        b = L("La respuesta incorrecta **resta**: $-1$ en la mayoría, $-2$ en 2021.", 30)
        self.push(b, "Y ojo: la respuesta incorrecta **resta**. Menos uno en la mayoría de los años.")
        c = L("Las cuentas entran en cuatro renglones, pero exigen la **definición precisa**.", 30)
        self.push(c, "No hay desarrollo largo. Las cuentas son cortas, pero exigen la definición precisa.")
        s = self.stamp(["Si no podés descartar al menos tres opciones,",
                        "dejarlo **en blanco** vale más que adivinar."], "LA REGLA DEL BLANCO", size=30)
        s.move_to([0, -1.1, 0])
        self.say("De ahí sale la regla del blanco: con penalización, adivinar al azar tiene **esperanza negativa**. Si no descartás tres, en blanco.",
                 *self.show_stamp(s))
        self.wipe()

        # ---- qué apareció y cuántas veces
        datos = [("Sup, ínf, máx, mín", 6, RED), ("Sumas de Darboux", 5, RED),
                 ("Continuidad: hallar el parámetro", 4, ORANGE), ("ε-δ: el δ máximo", 3, RED),
                 ("Propiedades de la integral", 3, ORANGE), ("Integrabilidad: n mínimo, ¿existe P?", 2, RED)]
        tit = T("Cuántas veces apareció en 6 parciales", 30, INK, SANS, BOLD).move_to([0, 2.75, 0])
        barras = VGroup()
        for i, (nom, k, c) in enumerate(datos):
            y = 1.85 - i * 0.68
            lab = T(nom, 24, INK).move_to([-2.6, y, 0], aligned_edge=RIGHT)
            lab.align_to([-0.6, 0, 0], RIGHT)
            bar = Rectangle(width=k * 0.95, height=0.4, stroke_width=0).set_fill(c, 0.85)
            bar.move_to([-0.4, y, 0], aligned_edge=LEFT)
            num = T(f"{k} de 6", 22, c, MONO, BOLD).next_to(bar, RIGHT, buff=0.18)
            barras.add(VGroup(lab, bar, num))
        self.say("Esto es lo que apareció en los parciales de 2021 a 2025, y cuántas veces. **Supremo e ínfimo** salió en los seis.",
                 Write(tit),
                 LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
                               for b in barras], lag_ratio=0.3, run_time=3.5))
        nota = T("+ Bolzano / Weierstrass en varios V/F · y en 2026 el cronograma le dio 2 semanas a límites", 20, SOFT).move_to([0, -2.1, 0])
        self.say("Bolzano y Weierstrass cayeron en verdadero o falso. Y un ajuste para 2026: este año límites tuvo **dos semanas enteras** de teórico, así que entra con probabilidad media.",
                 FadeIn(nota))
        self.wipe()

        # ---- los tres videos
        filas = [("VIDEO 1", "MUY ALTA", RED, "Sup/ínf · Darboux · Integrabilidad · ε-δ"),
                 ("VIDEO 2", "ALTA", ORANGE, "Continuidad con parámetro · Propiedades de la integral · Bolzano"),
                 ("VIDEO 3", "MEDIA", TEAL, "Límites · Lipschitz · Composición · V/F relámpago · Formulario")]
        g = VGroup()
        for v, p, c, txt in filas:
            a = T(v, 24, c, MONO, BOLD)
            b = prob_chip(p)
            d = T(txt, 23, INK)
            g.add(VGroup(a, b, d).arrange(RIGHT, buff=0.35))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([0, 0.7, 0])
        self.say("Los tres videos siguen el ranking del libro, **de mayor a menor probabilidad**. Este es el primero: los cuatro tipos que casi seguro caen.",
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in g], lag_ratio=0.35, run_time=2.2))
        tip = self.tip(["Si el tiempo no te alcanza, cortá desde abajo.",
                        "Cuando aparezca un enunciado: **pausá**, intentá el primer paso, y recién después seguí."],
                       label="CÓMO USARLO", size=23).move_to([0, -1.6, 0])
        self.say("Si el tiempo no te alcanza, cortá desde abajo. Y cada vez que aparezca un enunciado, **pausá** e intentá el primer paso antes de ver la resolución.",
                 FadeIn(tip))
        self.end_scene()


# =====================================================================
class V1_01_SupTeoria(V1):
    CH_NUM, CH_TITLE = "02", "Sup, ínf, máx, mín · la teoría justa"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Supremo, ínfimo, máximo, mínimo", "La teoría justa para resolver",
                        prob=("MUY ALTA", "apareció en los 6 parciales"))
        s = self.stamp(["$A\\subset\\R$, $A\\neq\\emptyset$.",
                        "$k$ es **cota superior** de $A$ $\\iff$ $a\\le k$ para todo $a\\in A$.",
                        "$\\sup A$ es la **menor** de las cotas superiores.",
                        "$\\max A$ es una cota superior que **además pertenece** a $A$."],
                       "DEFINICIONES", size=28).move_to([0, 1.3, 0])
        self.say("Las definiciones, literal. Una cota superior es un número que ningún elemento supera. El **supremo** es la menor de todas.",
                 *self.show_stamp(s))
        m = L("Espejo hacia abajo: cota inferior, $\\inf A$ (la **mayor** cota inferior), $\\min A$.", 26).move_to([0, -1.3, 0])
        self.say("Y el **máximo** es una cota superior que además está adentro del conjunto. Para abajo es lo mismo, en espejo.", FadeIn(m))
        self.wipe()

        # ---- A = {2 - 1/2^n}: los puntos se apilan contra el 2
        tit = L("$A=\\left\\{2-\\dfrac{1}{2^n}: n\\in\\N\\right\\}$", 30).move_to([0, 2.5, 0])
        nl = NumberLine(x_range=[0.8, 2.3, 0.5], length=11.5, color=SOFT, stroke_width=2,
                        include_tip=True, tip_length=0.16, include_ticks=False).move_to([0, 0.3, 0])
        t1 = tick(nl, 1, "1")
        t15 = tick(nl, 1.5, "1{,}5")
        self.say("La imagen que tenés que tener. Este conjunto: dos menos uno sobre dos a la n.",
                 Write(tit), Create(nl), FadeIn(t1), FadeIn(t15))
        pts = VGroup(*[Dot(nl.n2p(2 - 1 / 2 ** n), radius=0.07 if n < 6 else 0.05, color=BLUE) for n in range(12)])
        self.say("n = 0 da 1. Después 1,5; 1,75; 1,875... Cada punto recorre **la mitad** de lo que falta hasta el 2.",
                 LaggedStart(*[FadeIn(p, scale=2) for p in pts], lag_ratio=0.35, run_time=4))
        techo = DashedLine(nl.n2p(2) + DOWN * 0.7, nl.n2p(2) + UP * 1.2, color=RED, stroke_width=3)
        tl = T("sup = 2 (no pertenece)", 22, RED, MONO, BOLD).next_to(techo, UP, buff=0.1)
        self.say("Se apilan contra el 2 **sin tocarlo**. El 2 es el techo: supremo. Pero ningún elemento vale 2, así que **no hay máximo**.",
                 Create(techo), FadeIn(tl))
        mn = T("mín = 1", 22, TEAL, MONO, BOLD).next_to(pts[0], DOWN, buff=0.55)
        self.say("Abajo es más fácil: el primer punto, el 1, está en el conjunto y todos los demás son mayores. **Ínfimo y mínimo** valen 1.",
                 Indicate(pts[0], color=TEAL), FadeIn(mn))
        tip = self.tip(["Un bounding box: la cara del box es el supremo. Existe siempre,",
                        "aunque ningún punto la toque. El máximo existe solo si un punto",
                        "está pegado justo en la cara."], label="LA IMAGEN", size=22).move_to([0, -1.75, 0])
        self.say("Pensalo como un bounding box. La cara existe siempre; el máximo existe solo si hay un punto **justo en la cara**.",
                 FadeIn(tip))
        self.wipe(tit, nl, pts)

        # ---- la cota k como perilla: ¿cuándo deja de ser cota?
        k = ValueTracker(2.25)
        kslider = Slider("cota k", k, 1.0, 2.3, color=GREEN, decimals=3).move_to([0, -2.0, 0])

        def es_cota():
            return all(2 - 1 / 2 ** n <= k.get_value() + 1e-9 for n in range(40))

        klinea = always_redraw(lambda: Line(nl.n2p(k.get_value()) + DOWN * 0.6, nl.n2p(k.get_value()) + UP * 0.9,
                                            color=GREEN if es_cota() else RED, stroke_width=5))
        kest = always_redraw(lambda: T("es cota superior" if es_cota() else "ya NO es cota: un punto la supera",
                                       22, GREEN if es_cota() else RED, MONO, BOLD).next_to(nl.n2p(k.get_value()), UP, buff=1.05))
        sobre = always_redraw(lambda: VGroup(*[p.copy().set_color(RED).scale(1.5) for n, p in enumerate(pts)
                                               if 2 - 1 / 2 ** n > k.get_value() + 1e-9]))
        self.add(klinea, kest, sobre)
        self.say("Ahora jugá con una perilla: una cota k. Mientras ningún punto la pase, es verde: **es cota superior**.",
                 FadeIn(kslider))
        self.say("La bajo despacio... 2,1... 2,01... **sigue siendo cota**. Todas estas son cotas superiores.",
                 k.animate.set_value(2.0), run_time=4, rate_func=smooth)
        self.say("Pero apenas la bajo **un pelito** del 2, un punto la pasa y se pone roja. El 2 es la frontera: la **menor** de las cotas. Eso es el supremo.",
                 k.animate.set_value(1.97), run_time=3)
        self.say("Y cuanto más la bajo, **más puntos** la superan.", k.animate.set_value(1.6), run_time=3)
        self.say("Volvamos al 2 exacto: es cota, y cualquier cosa por debajo ya no lo es.", k.animate.set_value(2.0), run_time=2)
        self.remove(klinea, kest, sobre)
        self.play(FadeOut(kslider))

        # ---- caracterizacion a menos de epsilon, animada
        s = self.stamp(["$S=\\sup A\\iff$ (i) $S$ es cota superior y",
                        "(ii) $\\forall\\eps>0\\ \\exists a\\in A:\\ S-\\eps<a\\le S$."],
                       "CARACTERIZACIÓN «A MENOS DE ÉPSILON»", size=26).move_to([0, 2.4, 0])
        self.say("Eso mismo, escrito como se usa en las pruebas: si bajás el techo **ε**, algún punto queda por encima.",
                 FadeOut(tit), *self.show_stamp(s))
        eps = ValueTracker(0.4)
        eslider = Slider("ε", eps, 0, 0.5, color=YELLOW, decimals=3).move_to([0, -2.0, 0])
        self.play(FadeIn(eslider))
        franja = always_redraw(lambda: Rectangle(
            width=abs(nl.n2p(2)[0] - nl.n2p(2 - eps.get_value())[0]), height=0.55,
            stroke_width=0).set_fill(YELLOW, 0.22).move_to(
            (nl.n2p(2) + nl.n2p(2 - eps.get_value())) / 2))
        el = always_redraw(lambda: M(r"2-\eps", size=30, color=YELLOW).next_to(
            nl.n2p(2 - eps.get_value()), DOWN, buff=0.35))

        def adentro():
            e = eps.get_value()
            return VGroup(*[p.copy().set_color(YELLOW).scale(1.4) for n, p in enumerate(pts)
                            if 2 - 1 / 2 ** n > 2 - e])
        hl = always_redraw(adentro)
        cuenta = always_redraw(lambda: T(f"puntos dentro de la franja: infinitos (se ven {len(adentro())})",
                                         20, YELLOW, MONO).move_to([0, -2.75, 0]))
        self.add(franja, el, hl, cuenta)
        self.say("La franja amarilla es de ancho ε, pegada al techo. La achico: 0,1... 0,01...",
                 eps.animate.set_value(0.05), run_time=4)
        self.say("...0,003. Por más que la apriete, **siempre** quedan puntos adentro: los que no se ven siguen ahí, apilados contra el 2.",
                 eps.animate.set_value(0.003), run_time=4, rate_func=rate_functions.ease_in_out_sine)
        self.say("Eso es lo que hace al 2 la **menor** cota: cualquier número por debajo, 2 − ε, ya lo supera algún elemento.",
                 eps.animate.set_value(0.2), run_time=2)
        self.remove(franja, el, hl, cuenta)
        self.play(FadeOut(eslider))
        self.wipe()

        s1 = self.stamp(["Si $A\\neq\\emptyset$ y está acotado superiormente, **existe** $\\sup A\\in\\R$.",
                         "El supremo existe siempre (con esas hipótesis). El máximo, no.",
                         "$\\Q$ no lo cumple: $\\{q\\in\\Q: q\\ge0,\\ q^2<2\\}$ no tiene supremo en $\\Q$."],
                        "AXIOMA DE COMPLETITUD", size=26).move_to([0, 1.9, 0])
        self.say("El axioma de completitud garantiza que el supremo **existe**. El máximo, en cambio, puede faltar. Y en los racionales, ni el supremo está garantizado.",
                 *self.show_stamp(s1))
        det = memo(["(1) una desigualdad **estricta**;",
                    "(2) el conjunto vive en $\\Q$ y el techo es irracional;",
                    "(3) una sucesión monótona que tiende a un valor sin alcanzarlo."],
                   label="DETECTOR DE «HAY SUP PERO NO MÁX»", size=24).move_to([0, -1.0, 0])
        self.say("Y el detector: sospechá que hay supremo pero **no máximo** apenas veas una de estas tres cosas.",
                 FadeIn(det))
        self.wipe()

        met = metodo(["**Simplificá** la expresión del conjunto hasta ver su estructura.",
                      "**Listá** los primeros términos (sucesión) o **despejá** la inecuación.",
                      "**Identificá** el techo y el piso.",
                      "**Preguntá la pertenencia**: ¿algún elemento vale exactamente eso?",
                      "**Escribí las cuatro etiquetas**: sup, máx (o «no existe»), ínf, mín."],
                     "CUALQUIER EJERCICIO DE SUP/ÍNF", size=26).move_to([0, 0.4, 0])
        self.say("El molde para cualquier ejercicio de este tipo. Cinco pasos. El que más se olvida es el cuarto: **preguntar la pertenencia**.",
                 FadeIn(met, shift=UP * 0.2), min_t=5)
        self.end_scene()


# =====================================================================
class V1_02_SupParcial(V1):
    CH_NUM, CH_TITLE = "02", "Sup, ínf · ejercicios de parcial"

    def construct(self):
        self.setup_frame()
        e = enun("PARCIAL 2023-2 · EJ 1",
                 ["Sea $A=\\left\\{\\dfrac{2^{n+1}-1}{2^n}: n\\in\\N\\right\\}$. Hallar $\\sup A$, $\\max A$, $\\inf A$, $\\min A$."],
                 size=28).move_to([0, 2.35, 0])
        self.say("Parcial 2023, ejercicio 1. **Pausá** y pensá el primer paso: ¿qué harías con esa fracción?", FadeIn(e), min_t=3)
        self.board_start(top=1.2)
        a = step(1, "simplifico", M(r"\frac{2^{n+1}-1}{2^n}=\frac{2\cdot 2^n}{2^n}-\frac{1}{2^n}=2-\frac{1}{2^n}", size=44))
        self.push(a, "Paso uno: simplificar. Dos a la n más uno es **dos por dos a la n**, y se cancela. Queda 2 menos 1 sobre 2 a la n.")
        self.say("Este paso **es el ejercicio entero**: escrito así se ve todo. Es el conjunto que acabamos de dibujar.")
        b = step(2, "listo", L("$n=0:\\ 1\\qquad n=1:\\ 1{,}5\\qquad n=2:\\ 1{,}75\\qquad n=3:\\ 1{,}875\\ \\dots$", 26))
        self.push(b, "Paso dos: listar. 1; 1,5; 1,75; 1,875. Crece y se aprieta contra el 2.")
        self.wipe(e)

        self.board_start(top=1.2)
        c = step(3, "techo", Lines("Como $\\frac{1}{2^n}>0$, todo elemento cumple $2-\\frac{1}{2^n}<2$: el 2 es cota superior.",
                                   "Es la menor: dado $\\eps>0$, elijo $n$ con $\\frac{1}{2^n}<\\eps$ y el elemento cae en $(2-\\eps,2)$.", size=25))
        self.push(c, "Paso tres: el techo. Uno sobre dos a la n es positivo, así que todo queda por debajo de 2. Y es la **menor** cota por la caracterización con épsilon.")
        d = step(4, "pertenencia", L("$2-\\frac{1}{2^n}=2$ exigiría $\\frac{1}{2^n}=0$: imposible. $2\\notin A$: **no hay máximo**.", 25))
        self.push(d, "Paso cuatro, el que no se puede saltear: ¿el 2 **pertenece**? Haría falta que uno sobre dos a la n sea cero. Imposible. No hay máximo.")
        f = step(5, "piso", L("La sucesión crece: el menor es el primero, $1$ (en $n=0$). Como $1\\in A$: $\\inf A=\\min A=1$.", 25))
        self.push(f, "Paso cinco, el piso. Como la sucesión crece, el menor es el primero: el 1, que está en A. Ínfimo y mínimo valen 1.")
        r = resp("$\\sup A=2$, no existe $\\max A$;  $\\inf A=\\min A=1$.")
        self.push(r, "Las cuatro etiquetas. Supremo 2 sin máximo; ínfimo y mínimo 1.", anim=FadeIn(r, scale=1.05))
        self.wipe()

        # ---- 2025-1
        e = enun("PARCIAL 2025-1 · EJ 1",
                 ["Sea $A=\\{x\\in\\Q: x\\ge0,\\ x^2\\le2\\}$. Estudiar supremo, máximo, ínfimo y mínimo."],
                 size=28).move_to([0, 2.35, 0])
        self.say("Parcial 2025, ejercicio 1. Mirá **dónde vive** el conjunto: en los racionales. Eso es una alarma del detector.", FadeIn(e), min_t=3)
        self.board_start(top=1.3, maxw=7.4)
        a = step(1, "despejo con cuidado", L("Con $x\\ge0$: $\\ x^2\\le2\\iff0\\le x\\le\\sqrt2$.", 26))
        self.push(a, "Paso uno: despejar. Como x es mayor o igual que cero, puedo tomar raíz **sin romper** la desigualdad.")
        b = step(2, "techo", Lines("$\\sqrt2$ es cota superior, y la menor:", "entre $k<\\sqrt2$ y $\\sqrt2$ hay un racional.", size=25))
        self.push(b, "Raíz de 2 es cota. Y es la menor: si tomás cualquier k más chico, por **densidad de Q** hay un racional entre k y raíz de 2, que está en A.")
        c = step(3, "pertenencia", Lines("$\\sqrt2\\notin\\Q$, y $A\\subset\\Q$.", "Entonces $\\sqrt2\\notin A$: no hay máximo.", size=25))
        self.push(c, "El corazón del ejercicio: raíz de 2 **no es racional**, lo probaste en clase. Entonces no está en A: no hay máximo.")
        d = step(4, "piso", L("$0\\in A$ y es cota inferior: $\\inf A=\\min A=0$.", 25))
        self.push(d, "El piso: el cero es racional, cumple todo, y está en A. Mínimo cero.")
        nl = NumberLine(x_range=[-0.3, 1.9, 1], length=5.2, color=SOFT, include_tip=True,
                        include_ticks=False, tip_length=0.15).move_to([3.7, 0.3, 0])
        seg = Line(nl.n2p(0), nl.n2p(np.sqrt(2)), color=BLUE, stroke_width=7)
        p0 = lleno(nl.n2p(0), TEAL)
        p1 = hueco(nl.n2p(np.sqrt(2)), RED)
        l0 = M("0", size=30, color=TEAL).next_to(p0, DOWN, buff=0.2)
        l1 = M(r"\sqrt2\notin\Q", size=30, color=RED).next_to(p1, UP, buff=0.2)
        self.play(Create(nl), Create(seg), FadeIn(p0), FadeIn(p1), FadeIn(l0), FadeIn(l1))
        r = resp("$\\sup A=\\sqrt2$ sin máximo;  $\\min A=0$.")
        self.push(r, "Respuesta: supremo raíz de 2, **sin máximo**; mínimo cero.", anim=FadeIn(r))
        self.wipe()
        tr = trampa(["Sin la condición $x\\ge0$, la solución de $x^2\\le2$ sería $[-\\sqrt2,\\sqrt2]$",
                     "y el ínfimo cambiaría. **Nunca tomes raíz en una inecuación sin mirar el signo.**"],
                    "EL SIGNO ANTES DE LA RAÍZ", size=26).move_to([0, 0.8, 0])
        self.say("La trampa del ejercicio: si no estuviera x mayor o igual que cero, el conjunto sería **simétrico** y el ínfimo sería menos raíz de 2. Mirá el signo antes de la raíz.",
                 FadeIn(tr))
        self.end_scene()


# =====================================================================
class V1_03_SupPractico(V1):
    CH_NUM, CH_TITLE = "02", "Sup, ínf · práctico y demostración"

    def construct(self):
        self.setup_frame()
        e = enun("PRÁCTICO 2.3 · EJ 2 g)",
                 ["Hallar sup, ínf, máx y mín de $A=\\left\\{x\\in\\R:\\dfrac{3x+1}{x-2}\\le0\\right\\}$."], size=28).move_to([0, 2.35, 0])
        self.say("Del práctico: una inecuación con cociente. Primera tentación a evitar: **multiplicar** por x − 2.", FadeIn(e), min_t=2.5)
        tr = trampa(["El signo de $x-2$ es desconocido: multiplicar rompería la desigualdad."], "NO MULTIPLICO", size=24).move_to([0, 1.05, 0])
        self.say("Su signo es desconocido: si es negativo, la desigualdad se da vuelta. Entonces se estudia el **signo del cociente**.", FadeIn(tr))
        tb = tabla([["", "$x<-\\frac13$", "$-\\frac13<x<2$", "$x>2$"],
                    ["$3x+1$", "$-$", "$+$", "$+$"],
                    ["$x-2$", "$-$", "$-$", "$+$"],
                    ["cociente", "$+$", "$-$", "$+$"]], size=24, h=0.58).move_to([0, -1.0, 0])
        self.say("Tabla de signos. El numerador se anula en menos un tercio; el denominador en 2, que queda **excluido**.",
                 FadeIn(tb.rules), FadeIn(tb.rows[0]), FadeIn(tb.rows[1]), FadeIn(tb.rows[2]))
        box = SurroundingRectangle(tb.rows[3][2], color=YELLOW, buff=0.1)
        self.say("Cociente menor o igual que cero: la zona **negativa**, más el punto donde vale cero, que es menos un tercio.",
                 FadeIn(tb.rows[3]), Create(box))
        self.wipe(e)
        nl = linea_num(-1.2, 3.0, 9.0, y=0.6)
        seg = Line(nl.n2p(-1 / 3), nl.n2p(2), color=BLUE, stroke_width=7)
        a = lleno(nl.n2p(-1 / 3), TEAL)
        b = hueco(nl.n2p(2), RED)
        la = M(r"-\tfrac13\in A", size=32, color=TEAL).next_to(a, DOWN, buff=0.25)
        lb = M(r"2\notin A", size=32, color=RED).next_to(b, DOWN, buff=0.25)
        self.say("El conjunto es el intervalo de menos un tercio, cerrado, a 2, **abierto**: el 2 anula el denominador.",
                 Create(nl), Create(seg), FadeIn(a), FadeIn(b), FadeIn(la), FadeIn(lb))
        r = resp("$\\inf A=\\min A=-\\tfrac13$;  $\\sup A=2$, sin máximo.").move_to([0, -1.1, 0])
        self.say("Mínimo menos un tercio. Supremo 2, **sin máximo**.", FadeIn(r))
        self.wipe()

        # ---- múltiple opción
        e = enun("PRÁCTICO 2.3 · EJ 8 (MÚLTIPLE OPCIÓN)",
                 ["$A=\\left\\{\\frac{m}{n}: 0<m<n,\\ m,n\\in\\N\\right\\}$."], size=28).move_to([0, 2.5, 0])
        ops = VGroup(*[L(s, 25) for s in [
            "a) acotado superiormente, tiene supremo pero no máximo.",
            "b) no acotado, sin supremo.",
            "c) tiene supremo que es máximo.",
            "d) no acotado, sin máximo, con supremo.",
            "e) acotado pero sin supremo."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, 0.1, 0])
        self.say("Un múltiple opción del práctico. Acá se entrena **descartar rápido**, que es lo que suma en el parcial.",
                 FadeIn(e), LaggedStart(*[FadeIn(o) for o in ops], lag_ratio=0.15))
        x_e = Line(ops[4].get_left(), ops[4].get_right(), color=RED, stroke_width=3)
        x_d = Line(ops[3].get_left(), ops[3].get_right(), color=RED, stroke_width=3)
        self.say("La e contradice el **axioma de completitud**: acotado siempre tiene supremo. Y la d es imposible: sin cota no hay supremo.",
                 Create(x_e), Create(x_d))
        n1 = L("$m<n\\Rightarrow\\frac{m}{n}<1$: el 1 es cota y **ningún** elemento lo alcanza.", 25)
        n2 = L("Con $m=n-1$: $\\ \\frac{n-1}{n}=1-\\frac1n\\to1$: es la menor cota.", 25)
        VGroup(n1, n2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -2.0, 0])
        self.say("Como m es menor que n, la fracción es menor que 1: el 1 es cota y no se alcanza.", FadeIn(n1))
        self.say("Con m = n − 1, la fracción es 1 − 1/n, que se acerca a 1 todo lo que quieras. Supremo 1, sin máximo: **opción a**.",
                 FadeIn(n2), ops[0].animate.set_color(GREEN))
        self.wipe()

        # ---- la demostración (parcial 2022-2)
        e = enun("PARCIAL 2022-2 · EJ 2 · LA DEMOSTRACIÓN QUE PUEDEN PEDIR",
                 ["$A$ no vacío, acotado superiormente, $\\alpha=\\sup A$.",
                  "Probar: $\\forall\\delta>0\\ \\exists a\\in A:\\ \\alpha-\\delta<a\\le\\alpha$."], size=27).move_to([0, 2.25, 0])
        self.say("La única demostración que salió de este tema. Es la caracterización, y se prueba **por absurdo**.", FadeIn(e), min_t=2.5)
        self.board_start(top=0.95, maxw=7.3)
        p1 = step(1, "hipótesis y tesis", Lines("H: $\\alpha$ es cota superior y es la menor.", "T: en cada franja $(\\alpha-\\delta,\\alpha]$ hay un elemento.", size=23))
        self.push(p1, "Primero separo lo que me regalan de lo que tengo que probar.")
        p2 = step(2, "niego la tesis", L("Existe $\\delta_0>0$ tal que ningún $a$ cumple $\\alpha-\\delta_0<a\\le\\alpha$.", 23))
        self.push(p2, "Niego la tesis: existe un δ₀ para el que la franja queda **vacía**.")
        nl = linea_num(0, 6, 5.2, y=0.2).shift(RIGHT * 3.7)
        pa = tick(nl, 4.6, r"\alpha", RED, up=True)
        pd = tick(nl, 3.2, r"\alpha-\delta_0", YELLOW)
        franja = Rectangle(width=abs(nl.n2p(4.6)[0] - nl.n2p(3.2)[0]), height=0.5, stroke_width=0).set_fill(YELLOW, 0.18)
        franja.move_to((nl.n2p(4.6) + nl.n2p(3.2)) / 2)
        pts = VGroup(*[Dot(nl.n2p(v), radius=0.06, color=BLUE) for v in [0.6, 1.3, 1.9, 2.4, 2.8, 3.1]])
        self.play(Create(nl), FadeIn(pa), FadeIn(pd), FadeIn(franja), FadeIn(pts))
        p3 = step(3, "traduzco", L("Todo $a\\le\\alpha$ y ninguno supera $\\alpha-\\delta_0$: $\\ a\\le\\alpha-\\delta_0$.", 23))
        self.push(p3, "Traduzco: si nadie cae en la franja, **todos** quedan a la izquierda de α − δ₀.")
        p4 = step(4, "contradicción", L("$\\alpha-\\delta_0$ es cota superior y es **menor** que $\\alpha$. Absurdo.", 23))
        self.push(p4, "Entonces α − δ₀ es una cota superior, y es **más chica** que α. Encontré una cota menor que la menor. Absurdo.",
                  Indicate(pd, color=YELLOW, scale_factor=1.3))
        tip = self.tip(["Negar la tesis, traducir, chocar con H.",
                        "Sirve para casi todas las demostraciones", "del curso."], label="EL MOLDE DEL ABSURDO", size=21, width=5.4)
        self.right_tip(tip, -1.5)
        self.say("Guardá la receta: **negar, traducir, chocar** con la hipótesis. Sirve para casi todas las demostraciones del curso.", FadeIn(tip))
        self.wipe()

        ej = VGroup(*[L(s, 26) for s in ["(a) $A=\\{x\\in\\R:|2x-6|<4\\}$",
                                         "(b) $B=\\left\\{\\frac{n-1}{n+1}:n\\in\\N\\right\\}$",
                                         "(c) $C=\\left\\{\\frac{(-1)^n}{n}:n\\ge1\\right\\}$"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        g = self.pausa(ej, "Tu turno. Sup, ínf, máx y mín de estos tres. Pausá el video y hacelo en papel.")
        sol = Lines("(a) $1<x<5$: sup 5, ínf 1, sin máx ni mín.",
                    "(b) $1-\\frac{2}{n+1}$: $\\sup=1$ sin máx; $\\min=-1$ ($n=0$).",
                    "(c) $-1,\\ \\frac12,\\ -\\frac13,\\ \\frac14,\\dots$: $\\max=\\frac12$, $\\min=-1$.", size=24)
        debajo(sol, g)
        self.say("Soluciones, para chequear. En la c, ojo: el máximo es **un medio**, en n = 2, no el 1.", FadeIn(sol))
        self.end_scene()


# =====================================================================
class V1_04_DarbouxTeoria(V1):
    CH_NUM, CH_TITLE = "03", "Sumas de Darboux · la teoría justa"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Sumas de Darboux", "Techo y piso de cada bloque",
                        prob=("MUY ALTA", "5 de 6 parciales · casi siempre con un dibujo"))
        s = self.stamp(["$P=\\{a_0,a_1,\\dots,a_M\\}$ con $a=a_0<a_1<\\dots<a_M=b$.",
                        "$\\Ss(f,P)=\\sum\\sup\\big(f,[a_i,a_{i+1}]\\big)\\,(a_{i+1}-a_i)$",
                        "$\\Si(f,P)=\\sum\\inf\\big(f,[a_i,a_{i+1}]\\big)\\,(a_{i+1}-a_i)$",
                        "Siempre $\\Si\\le\\Ss$: en cada bloque el piso no supera al techo."],
                       "PARTICIÓN Y SUMAS (NOTACIÓN DE CLASE)", size=26).move_to([0, 1.2, 0])
        self.say("La definición. Partís el intervalo en bloques, **no necesariamente iguales**. En cada bloque, techo por ancho da la suma superior; piso por ancho, la inferior.",
                 *self.show_stamp(s), min_t=5)
        self.wipe()

        f = lambda x: 0.25 * (x - 1) ** 3 - 1.0 * (x - 1) + 2.2
        ax = ejes([0, 3.8, 1], [0, 4.2, 1], 9.0, 4.2).move_to([0, 0.6, 0])
        curva = ax.plot(f, x_range=[0.3, 3.5], color=BLUE, stroke_width=4)
        P = [0.3, 1.2, 1.8, 2.9, 3.5]
        sup_c = cajas(ax, f, P, "sup", RED, 0.28)
        inf_c = cajas(ax, f, P, "inf", TEAL, 0.45)
        cortes = VGroup(*[DashedLine(ax.c2p(p, 0), ax.c2p(p, 4.1), color=DIM, stroke_width=1.5) for p in P])
        self.say("Una función cualquiera y una partición con bloques de **anchos distintos**.", Create(ax), Create(curva), Create(cortes))
        self.say("Suma superior: en cada bloque, una caja plana que toca el punto **más alto** de su franja.",
                 LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in sup_c], lag_ratio=0.25, run_time=2))
        self.say("Suma inferior: la caja que toca el punto **más bajo**. Fijate el segundo bloque: el piso está en el medio, no en un extremo.",
                 LaggedStart(*[FadeIn(r) for r in inf_c], lag_ratio=0.25, run_time=2))
        tip = intu(["Voxelizar con ladrillos de ancho desigual. Cada ladrillo de la superior",
                    "toca el punto más alto de su franja; cada uno de la inferior, el más bajo."], size=21).move_to([0, -1.95, 0])
        self.say("Como voxelizar con ladrillos de ancho desigual: arriba sobra volumen, abajo falta.", FadeIn(tip))
        self.play(FadeOut(tip), FadeOut(sup_c), FadeOut(inf_c), FadeOut(cortes))

        # ---- perilla n: refinar en vivo
        a0, b0 = 0.3, 3.5
        n = ValueTracker(3)
        nn = lambda: max(1, int(round(n.get_value())))
        Pn = lambda: [a0 + (b0 - a0) * i / nn() for i in range(nn() + 1)]

        def suma(kind):
            tot = 0.0
            for a, b in zip(Pn()[:-1], Pn()[1:]):
                Mx, mn = sup_inf(f, a, b, n=80)
                tot += (Mx if kind == "sup" else mn) * (b - a)
            return tot
        dx = (b0 - a0) / 4000
        integral = float(sum(f(a0 + (i + 0.5) * dx) for i in range(4000)) * dx)
        sc = always_redraw(lambda: cajas(ax, f, Pn(), "sup", RED, 0.28, stroke=1 if nn() < 25 else 0.4))
        ic = always_redraw(lambda: cajas(ax, f, Pn(), "inf", TEAL, 0.45, stroke=1 if nn() < 25 else 0.4))
        self.add(sc, ic)
        self.bring_to_front(curva)
        panel = VGroup(
            Slider("n bloques", n, 1, 40, color=YELLOW, decimals=0, width=2.6, size=22),
            VGroup(L("$\\Ss=$", 24, RED), Num(suma("sup"), num_decimal_places=3, font_size=30, color=RED)).arrange(RIGHT, buff=0.15),
            VGroup(L("$\\int f=$", 24, BLUE), Num(integral, num_decimal_places=3, font_size=30, color=BLUE)).arrange(RIGHT, buff=0.15),
            VGroup(L("$\\Si=$", 24, TEAL), Num(suma("inf"), num_decimal_places=3, font_size=30, color=TEAL)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.55).move_to([0, -2.05, 0])
        panel[1][1].add_updater(lambda m: m.set_value(suma("sup")))
        panel[3][1].add_updater(lambda m: m.set_value(suma("inf")))
        self.say("Ahora con perilla. **n** es la cantidad de bloques iguales. Abajo, en vivo: la suma superior, la integral, y la inferior.",
                 FadeIn(panel))
        self.say("Subo n: los ladrillos se afinan. La roja **baja**, la teal **sube**, y las dos se aprietan contra la integral.",
                 n.animate.set_value(12), run_time=5, rate_func=linear)
        self.say("Con cuarenta bloques ya casi no se distinguen. Eso es ser **integrable**: la pinza se cierra.",
                 n.animate.set_value(40), run_time=4, rate_func=rate_functions.ease_in_quad)
        self.say("Y si vuelvo a pocos bloques, la pinza se abre: sobra mucho arriba, falta mucho abajo.",
                 n.animate.set_value(2), run_time=3)
        self.remove(sc, ic)
        for m in panel.get_family():
            m.clear_updaters()
        self.wipe()
        tip = self.tip(["Si $P\\subset P'$: $\\Ss$ baja o queda igual, $\\Si$ sube o queda igual.",
                        "Para cualquier par: $\\Si(f,Q)\\le\\Ss(f,P)$ (se prueba pasando por $P\\cup Q$)."],
                       label="REFINAR Y COMPARAR", color=RED, size=24).move_to([0, 0.6, 0])
        self.say("Lo que tenés que saber, escrito: refinar **baja** la superior y **sube** la inferior. Y cualquier inferior queda debajo de cualquier superior.",
                 FadeIn(tip))
        self.wipe()

        met = metodo(["Una fila por bloque: $[a_i,a_{i+1}]$.",
                      "Ancho $a_{i+1}-a_i$. **Nunca asumas que son iguales.**",
                      "Techo $M_i$ = sup de $f$ en **todo** el bloque, extremos incluidos.",
                      "Piso $m_i$ = ínf de $f$ en todo el bloque.",
                      "Aportes $M_i\\cdot$ancho y $m_i\\cdot$ancho. Sumar columnas."],
                     "LA TABLA DE BLOQUES", size=25).move_to([0, 1.3, 0])
        self.say("El método es una tabla. Nunca calcules sumas de Darboux sin la tabla: bloque, ancho, techo, piso, aporte.",
                 FadeIn(met, shift=UP * 0.2), min_t=4)
        tr = trampa(["**1.** Usar $f$ del extremo en vez del sup del bloque: si el pico está en el medio, manda el pico.",
                     "**2.** Multiplicar todo por el mismo ancho.",
                     "**3.** «Compensar» lo de abajo del eje: si $M_i<0$, la caja aporta negativo y listo."],
                    "LOS TRES ERRORES QUE CUESTAN EL EJERCICIO", size=23).move_to([0, -1.55, 0])
        self.say("Y los tres errores que cuestan el ejercicio. El primero es el clásico: usar el valor del extremo cuando **el pico está adentro** del bloque.",
                 FadeIn(tr), min_t=5)
        self.end_scene()


# =====================================================================
DIB = [(0, -1), (1, 0), (2, 1), (3, -2), (4, -0.5), (7, 5), (9, 0), (10, -1)]


def f_dibujo(x):
    xs, ys = zip(*DIB)
    return float(np.interp(x, xs, ys))


class V1_05_DarbouxParcial(V1):
    CH_NUM, CH_TITLE = "03", "Darboux · ejercicio de parcial"

    def construct(self):
        self.setup_frame()
        e = enun("PARCIAL 2024-2 · EJ 3 (MISMO MOLDE EN 2023, 2024-1, 2025)",
                 ["$f:[0,10]\\to\\R$ dada por un bosquejo;  $P=\\{0,1,2,4,9,10\\}$. Hallar $\\Ss(f,P)$."], size=27).move_to([0, 2.55, 0])
        ax = ejes([0, 10.5, 1], [-2.5, 5.5, 1], 6.6, 4.4).move_to([-3.2, -0.4, 0])
        curva = VMobject(color=BLUE, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in DIB])
        xl = xlabels(ax, [1, 2, 4, 7, 9, 10], size=18)
        yl = ylabels(ax, [-2, 1, 5], size=18)
        self.say("El molde que salió **cuatro veces**: un dibujo, una partición irregular, y te piden la suma superior.",
                 FadeIn(e), Create(ax), Create(curva), FadeIn(xl), FadeIn(yl))
        P = [0, 1, 2, 4, 9, 10]
        cortes = VGroup(*[DashedLine(ax.c2p(p, -2.4), ax.c2p(p, 5.3), color=DIM, stroke_width=1.5) for p in P])
        self.say("Marco los cortes. Fijate que los bloques tienen anchos **uno, uno, dos, cinco y uno**.", Create(cortes))
        tb = tabla([["Bloque", "Ancho", "$M_i$", "Aporte"],
                    ["$[0,1]$", "1", "0", "0"],
                    ["$[1,2]$", "1", "1", "1"],
                    ["$[2,4]$", "2", "1", "2"],
                    ["$[4,9]$", "5", "5", "25"],
                    ["$[9,10]$", "1", "0", "0"]], size=23, h=0.52).move_to([3.6, 0.0, 0])
        self.play(FadeIn(tb.rules), FadeIn(tb.rows[0]))
        cs = cajas(ax, f_dibujo, P, "sup", RED, 0.3, extra=[x for x, _ in DIB])
        textos = ["[0,1]: sube de −1 hasta 0. El techo es **0**, aporta cero.",
                  "[1,2]: el pico de altura 1 está en x = 2, que es el extremo del bloque. Techo 1, aporte 1.",
                  "[2,4]: la función **baja hasta −2** ahí adentro... y no importa. El x = 2 también es de este bloque: techo 1, por ancho 2.",
                  "[4,9]: el pico de 5 en x = 7. Techo 5 por ancho **5**: 25.",
                  "[9,10]: baja de 0 a −1. Techo 0."]
        for i in range(5):
            self.say(textos[i], FadeIn(tb.rows[i + 1]), FadeIn(cs[i]))
        hl = SurroundingRectangle(tb.rows[3], color=YELLOW, buff=0.06)
        pk = Dot(ax.c2p(2, 1), color=YELLOW, radius=0.1)
        self.say("El bloque [2, 4] es el que decide el ejercicio: el techo lo pone el **pico de x = 2**, que pertenece al bloque porque es su extremo izquierdo.",
                 Create(hl), FadeIn(pk, scale=2))
        r = resp("$\\Ss=0+1+2+25+0=28$").next_to(tb, DOWN, buff=0.35)
        r.scale_to_fit_width(min(r.width, 5.6)).next_to(tb, DOWN, buff=0.35)
        self.say("Sumo la columna: 28.", FadeIn(r))
        self.end_scene()


# =====================================================================
class V1_06_DarbouxPractico(V1):
    CH_NUM, CH_TITLE = "03", "Darboux · ejercicios del práctico"

    def construct(self):
        self.setup_frame()
        e = enun("PRÁCTICO 3.3 · EJ 4 a)",
                 ["$f(x)=\\fl{x}$ (parte entera),  $P=\\{-1;\\,0;\\,1;\\,1{,}5;\\,3\\}$. Calcular $\\Si(f,P)$ y $\\Ss(f,P)$."], size=27).move_to([0, 2.55, 0])
        ax = ejes([-1.3, 3.4, 1], [-1.5, 3.5, 1], 5.6, 4.0).move_to([-3.5, -0.2, 0])
        esc = VGroup()
        for k in [-1, 0, 1, 2]:
            esc.add(Line(ax.c2p(k, k), ax.c2p(k + 1, k), color=BLUE, stroke_width=5))
            esc.add(lleno(ax.c2p(k, k), BLUE, 0.07), hueco(ax.c2p(k + 1, k), BLUE, 0.07))
        esc.add(lleno(ax.c2p(3, 3), BLUE, 0.07))
        xl = xlabels(ax, [-1, 1, 1.5, 3], ["-1", "1", "1{,}5", "3"], size=17)
        self.say("La parte entera: escalones. Punto lleno, el valor que se alcanza; punto hueco, el que no.",
                 FadeIn(e), Create(ax), FadeIn(esc), FadeIn(xl))
        tr = trampa(["$\\fl{x}$ salta en los enteros. Un bloque cerrado que **termina**",
                     "en un entero incluye ese extremo, con el valor nuevo, más alto."], "LOS EXTREMOS", size=21, width=6.2)
        tr.move_to([3.4, 1.2, 0])
        self.say("La trampa: el bloque [0, 1] es **cerrado**, así que incluye el x = 1, donde la parte entera ya saltó a 1.", FadeIn(tr))
        fl = lambda x: np.floor(x + 1e-12)
        P = [-1, 0, 1, 1.5, 3]
        cs = cajas(ax, fl, P, "sup", RED, 0.3, extra=P)
        self.say("Las cajas de la superior. El último bloque llega hasta 3, y en x = 3 la función vale **3**: ese es el techo.",
                 LaggedStart(*[FadeIn(c) for c in cs], lag_ratio=0.3, run_time=2))
        self.wipe(e, ax, esc, xl, cs)
        tb = tabla([["Bloque", "Ancho", "$M_i$", "$m_i$", "$M_i\\cdot a$", "$m_i\\cdot a$"],
                    ["$[-1,0]$", "1", "0", "$-1$", "0", "$-1$"],
                    ["$[0,1]$", "1", "1", "0", "1", "0"],
                    ["$[1;1{,}5]$", "0,5", "1", "1", "0,5", "0,5"],
                    ["$[1{,}5;3]$", "1,5", "3", "1", "4,5", "1,5"]], size=21, h=0.5).move_to([3.3, 1.0, 0])
        self.say("La tabla completa. Los techos de los bloques que terminan en entero los pone **el extremo derecho**.",
                 FadeIn(tb.rules), LaggedStart(*[FadeIn(r) for r in tb.rows], lag_ratio=0.3, run_time=2.5), min_t=4)
        r = resp("$\\Ss(f,P)=6,\\quad\\Si(f,P)=1$").next_to(tb, DOWN, buff=0.3)
        ch = L("Chequeo: $\\int_{-1}^{3}\\fl{x}\\,dx=-1+0+1+2=2$, y $1\\le2\\le6$ ✓", 22, GREEN).next_to(r, DOWN, buff=0.2)
        self.say("Seis y uno. Y un chequeo que conviene hacer siempre: la integral, que es 2, tiene que quedar **en el medio**.", FadeIn(r), FadeIn(ch))
        self.wipe()

        e = enun("PRÁCTICO 3.3 · EJ 1 b) · EL MÍNIMO EN EL MEDIO",
                 ["$f(x)=x^2$,  $P=\\{-2;\\,-\\tfrac12;\\,\\tfrac12;\\,2\\}$. Calcular $\\Ss$ y $\\Si$."], size=27).move_to([0, 2.55, 0])
        ax = ejes([-2.3, 2.3, 1], [0, 4.4, 1], 5.4, 4.0).move_to([-3.6, -0.2, 0])
        par = ax.plot(lambda x: x * x, x_range=[-2.05, 2.05], color=BLUE, stroke_width=4)
        P = [-2, -0.5, 0.5, 2]
        sc = cajas(ax, lambda x: x * x, P, "sup", RED, 0.25, extra=[0])
        ic = cajas(ax, lambda x: x * x, P, "inf", TEAL, 0.5, extra=[0])
        self.say("Otro clásico. La parábola con un bloque del medio que contiene al **cero**.", FadeIn(e), Create(ax), Create(par))
        self.play(FadeIn(sc), FadeIn(ic))
        z = Dot(ax.c2p(0, 0), color=YELLOW, radius=0.1)
        self.say("En [−½, ½] la parábola baja hasta 0 **adentro** del bloque. El piso es 0, no f de un extremo.", FadeIn(z, scale=2))
        tb = tabla([["Bloque", "Ancho", "$M_i$", "$m_i$", "$M_i\\cdot a$", "$m_i\\cdot a$"],
                    ["$[-2;\\,-0{,}5]$", "1,5", "4", "0,25", "6", "0,375"],
                    ["$[-0{,}5;\\,0{,}5]$", "1", "0,25", "0", "0,25", "0"],
                    ["$[0{,}5;\\,2]$", "1,5", "4", "0,25", "6", "0,375"]], size=21, h=0.58).move_to([3.3, 0.6, 0])
        self.say("La tabla. El bloque del medio aporta 0 a la inferior.",
                 FadeIn(tb.rules), LaggedStart(*[FadeIn(r) for r in tb.rows], lag_ratio=0.3, run_time=2))
        r = resp("$\\Ss=12{,}25,\\quad\\Si=0{,}75$").next_to(tb, DOWN, buff=0.3)
        self.say("12,25 y 0,75. La integral, 16 tercios, más o menos 5,33, queda en el medio.", FadeIn(r))
        self.wipe()

        tip = self.tip(["Cambiar el valor de $f$ en **un** punto cambia las sumas de Darboux de las",
                        "particiones que lo tienen en un bloque. Pero **no** cambia la integral:",
                        "con particiones finas, el bloque «contaminado» se hace tan angosto como quieras."],
                       label="LA LECCIÓN DEL EJ 4 d) y e)", size=24).move_to([0, 1.6, 0])
        self.say("Una lección del mismo práctico: si cambiás f en **un solo punto**, las sumas cambian, pero la integral no.", FadeIn(tip))
        ej = VGroup(*[L(s, 26) for s in ["Con $P=\\{-1;0;1;1{,}5;3\\}$: (a) $f(x)=\\fl{x/2}$   (b) $f(x)=\\fl{2x}$",
                                         "(c) $f(x)=3x-2$ con $P=\\{-2,0,1,2\\}$"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        g = self.pausa(ej, "Tu turno: armá la tabla para cada una.")
        sol = Lines("(a) $\\Ss=1{,}5$, $\\Si=-1$   (b) $\\Ss=12{,}5$, $\\Si=3{,}5$   (c) $\\Ss=1$, $\\Si=-17$", size=24)
        debajo(sol, g)
        self.say("Soluciones. En la c la función es creciente: el techo siempre a la derecha.", FadeIn(sol))
        self.end_scene()


# =====================================================================
class V1_07_IntegTeoria(V1):
    CH_NUM, CH_TITLE = "04", "Integrabilidad · la teoría justa"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Integrabilidad", "La fórmula telescópica y «¿existe P?»",
                        prob=("MUY ALTA", "2024-2 y 2025 trajeron el mismo par de ejercicios"))
        s = self.stamp(["$I_*=\\sup\\{\\Si(f,P)\\}$     $I^*=\\inf\\{\\Ss(f,P)\\}$     (existen por completitud)",
                        "$f$ es **integrable** en $[a,b]\\iff I_*=I^*$, y ese valor es $\\int_a^b f$."],
                       "INTEGRAL INFERIOR, SUPERIOR, INTEGRABLE", size=26).move_to([0, 2.1, 0])
        self.say("La integral inferior es el supremo de todas las sumas inferiores; la superior, el ínfimo de todas las superiores. Integrable es que **coincidan**.",
                 *self.show_stamp(s))
        tip = self.tip(["$\\Ss(f,P)$ es **un número** de **una** partición: una foto.",
                        "$I^*$ es el **mejor** de todos esos números: el ínfimo sobre todas las particiones.",
                        "Por eso siempre $I^*\\le\\Ss(f,P)$, para cualquier $P$."],
                       label="Ss CONTRA I* · TU PREGUNTA DEL CUADERNO", size=23).move_to([0, -0.4, 0])
        self.say("Tu pregunta del cuaderno: la suma superior es una foto, de una partición. La integral superior es **el límite de lo que se puede lograr** afinando.",
                 FadeIn(tip))
        self.wipe()
        s2 = self.stamp(["$f$ integrable $\\iff\\ \\forall\\eps>0\\ \\exists P:\\ \\Ss(f,P)-\\Si(f,P)<\\eps$."],
                        "CRITERIO «A MENOS DE ÉPSILON» (EL QUE SE USA)", size=28).move_to([0, 2.2, 0])
        self.say("El criterio que se usa en los ejercicios: para cada épsilon, **alguna** partición con la diferencia más chica que épsilon.",
                 *self.show_stamp(s2))
        s3 = self.stamp(["**1.** $f$ monótona en $[a,b]$ $\\Rightarrow$ integrable.",
                         "**2.** $f$ continua en $[a,b]$ $\\Rightarrow$ integrable.",
                         "**3.** $f$ acotada con finitas discontinuidades $\\Rightarrow$ integrable.",
                         "Corolario: cambiar $f$ en finitos puntos no cambia ni la integrabilidad ni la integral."],
                        "LOS TRES CRITERIOS", size=25).move_to([0, -0.6, 0])
        self.say("Y los tres criterios para no tener que usar la definición: **monótona, continua, o finitas discontinuidades**.",
                 *self.show_stamp(s3))
        self.wipe()

        # ---- telescópica animada
        tit = T("La fórmula telescópica", 34, INK, SANS, BOLD).move_to([0, 2.7, 0])
        ax = ejes([0.9, 2.5, 1], [0.5, 4.6, 1], 7.0, 4.2).move_to([-2.2, 0.05, 0])
        f = lambda x: x * x
        curva = ax.plot(f, x_range=[1, 2], color=BLUE, stroke_width=4)
        xl = xlabels(ax, [1, 2], ["a", "b"], size=22)
        self.say("Ahora la herramienta que resuelve el ejercicio de n mínimo. Tomo f creciente, x cuadrado en [1, 2], y partición **uniforme**.",
                 Write(tit), Create(ax), Create(curva), FadeIn(xl))
        n = 4
        P = [1 + i / n for i in range(n + 1)]
        difs = VGroup()
        for a, b in zip(P[:-1], P[1:]):
            p0, p1 = ax.c2p(a, f(a)), ax.c2p(b, f(b))
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=RED,
                          stroke_width=1.5, fill_color=RED, fill_opacity=0.4)
            r.move_to((p0 + p1) / 2)
            difs.add(r)
        self.say("En cada bloque, como f crece, el techo está a la derecha y el piso a la izquierda. La diferencia techo menos piso es **esta cajita roja**.",
                 LaggedStart(*[FadeIn(r) for r in difs], lag_ratio=0.3, run_time=2))
        xcol = ax.c2p(2.3, 0)[0]
        destinos = [r.copy().move_to([xcol, r.get_center()[1], 0]) for r in difs]
        self.say("Ahora las **deslizo** todas hacia la derecha, sin cambiarles la altura.",
                 *[Transform(r, d) for r, d in zip(difs, destinos)], run_time=2.5)
        br = Brace(VGroup(*destinos), RIGHT, color=YELLOW)
        bl = M(r"f(b)-f(a)", size=34, color=YELLOW).next_to(br, RIGHT, buff=0.1)
        bw = Brace(VGroup(*destinos), DOWN, color=YELLOW)
        bwl = M(r"\tfrac{b-a}{n}", size=34, color=YELLOW).next_to(bw, DOWN, buff=0.08)
        self.say("Se apilan en **una sola columna**: alto f(b) − f(a), ancho (b − a)/n. Cada caja empieza donde termina la anterior: la suma es **telescópica**.",
                 GrowFromCenter(br), FadeIn(bl), GrowFromCenter(bw), FadeIn(bwl), min_t=5)
        self.play(FadeOut(difs), FadeOut(bw), FadeOut(bwl))

        # ---- perilla n: la columna se afina, el alto no cambia
        n = ValueTracker(4)
        nn = lambda: max(1, int(round(n.get_value())))

        def escena_n():
            g = VGroup()
            P = [1 + i / nn() for i in range(nn() + 1)]
            w = ax.c2p(1 + 1 / nn(), 0)[0] - ax.c2p(1, 0)[0]
            for a, b in zip(P[:-1], P[1:]):
                p0, p1 = ax.c2p(a, f(a)), ax.c2p(b, f(b))
                r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0.8 if nn() < 20 else 0,
                              stroke_color=RED, fill_color=RED, fill_opacity=0.4).move_to((p0 + p1) / 2)
                g.add(r)
            col = Rectangle(width=w, height=ax.c2p(0, 4)[1] - ax.c2p(0, 1)[1], stroke_width=1.5, stroke_color=RED,
                            fill_color=RED, fill_opacity=0.55)
            col.move_to([xcol, (ax.c2p(0, 4)[1] + ax.c2p(0, 1)[1]) / 2, 0])
            g.add(col)
            return g
        viva = always_redraw(escena_n)
        self.add(viva)
        panel = VGroup(Slider("n", n, 1, 30, color=YELLOW, decimals=0, width=2.6, size=24),
                       VGroup(L("$\\Ss-\\Si=\\tfrac{3}{n}=$", 24, RED),
                              Num(0.75, num_decimal_places=3, font_size=32, color=RED)).arrange(RIGHT, buff=0.15)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.4, -1.55, 0])
        panel[1][1].add_updater(lambda m: m.set_value(3 / nn()))
        self.play(FadeIn(panel))
        self.say("Ahora subo n. Las cajitas se afinan, y la columna también: **mismo alto, menos ancho**. La diferencia es 3/n y se va a cero.",
                 n.animate.set_value(30), run_time=6, rate_func=rate_functions.ease_in_sine)
        self.say("Eso es exactamente lo que pide el criterio: para cualquier ε, un n que deje la columna **más angosta** que ε.")
        self.remove(viva)
        panel[1][1].clear_updaters()
        self.wipe()
        s = self.stamp([M(r"\Ss(f,P_n)-\Si(f,P_n)=\frac{b-a}{n}\,\big|f(b)-f(a)\big|", size=50)],
                       "FÓRMULA TELESCÓPICA · f MONÓTONA, PARTICIÓN UNIFORME DE n BLOQUES").move_to([0, 1.8, 0])
        self.say("La fórmula. Vale para f **monótona** y partición **uniforme**. Si f decrece, el valor absoluto la arregla.", *self.show_stamp(s))
        met = metodo(["Verificá que $f$ es **monótona en todo** $[a,b]$. Si no, la fórmula no vale.",
                      "Sustituí $a$, $b$, $f(a)$, $f(b)$.",
                      "Imponé la desigualdad y despejá $n$ ($n>0$: multiplicar no invierte).",
                      "Desigualdad **estricta**: si sale $n>6$, la respuesta es $7$."],
                     "n MÍNIMO", size=25).move_to([0, -1.05, 0])
        self.say("El método de n mínimo, en cuatro pasos. El último es donde se pierden puntos: **n mayor que 6 no es 6**, es 7.",
                 FadeIn(met), min_t=4)
        self.end_scene()


# =====================================================================
class V1_08_IntegParcial(V1):
    CH_NUM, CH_TITLE = "04", "Integrabilidad · ejercicios de parcial"

    def construct(self):
        self.setup_frame()
        e = enun("PARCIAL 2024-2 · EJ 4",
                 ["$f(x)=x^2$ en $[1,2]$, $P_n$ uniforme. Menor $n$ con $\\Ss(f,P_n)-\\Si(f,P_n)<\\frac12$."], size=28).move_to([0, 2.5, 0])
        self.say("Parcial 2024, segundo semestre. Pausá: ¿qué verificás **antes** de usar la fórmula?", FadeIn(e), min_t=2.5)
        self.board_start(top=1.45)
        a = step(1, "hipótesis", L("$x^2$ es creciente en $[1,2]$: todo el intervalo está a la derecha del 0 ✓", 26))
        self.push(a, "Hipótesis: x cuadrado es creciente en [1, 2], porque todo el intervalo está a la derecha del cero.")
        b = step(2, "sustituyo", M(r"\frac{2-1}{n}\,(4-1)=\frac{3}{n}", size=44))
        self.push(b, "Sustituyo: ancho total 1, f(2) − f(1) = 3. La diferencia es 3/n.")
        c = step(3, "despejo", M(r"\frac{3}{n}<\frac12\iff n>6", size=44))
        self.push(c, "Despejo: 3/n menor que un medio, equivale a n mayor que 6.")
        r = resp("$n=7$")
        self.push(r, "Estricta: el primer entero que cumple es el **7**.", anim=FadeIn(r))
        self.wipe()

        e = enun("PARCIAL 2025-1 · EJ 4", ["$f(x)=x^2+1$ en $[1,2]$, diferencia $<\\frac13$."], size=28).move_to([0, 2.5, 0])
        a = M(r"\frac{1}{n}\,(5-2)=\frac{3}{n}<\frac13\iff n>9", size=46).move_to([0, 1.1, 0])
        r = resp("$n=10$").next_to(a, DOWN, buff=0.4)
        self.say("Al año siguiente, casi igual. 3/n menor que un tercio: n mayor que 9, respuesta **10**.", FadeIn(e), Write(a), FadeIn(r))
        mm = memo(["$x^2$ y $x^2+1$ dan la misma cuenta: sumar una constante sube techos",
                   "y pisos por igual, y la diferencia $M_i-m_i$ no cambia."],
                  label="SUMAR UNA CONSTANTE NO CAMBIA NADA", size=24).move_to([0, -1.4, 0])
        self.say("Fijate que el +1 **no cambió nada**: sube techos y pisos por igual.", FadeIn(mm))
        self.wipe()

        # ---- ¿existe P?
        e = enun("PARCIAL 2024-2 · EJ 5",
                 ["$f(x)=2x$ en $[0,2]$. ¿Es integrable? ¿Existe $P$ con $\\Ss(f,P)=4$? ¿Existe $Q$ con $\\Si(f,Q)=3$?"], size=26).move_to([0, 2.55, 0])
        self.say("El otro ejercicio del par. Este es **salado**: parece fácil y se lo contesta mal.", FadeIn(e), min_t=2.5)
        ax = ejes([0, 2.3, 1], [0, 4.6, 1], 5.2, 3.9).move_to([-3.6, -0.3, 0])
        f = lambda x: 2 * x
        rec = ax.plot(f, x_range=[0, 2], color=BLUE, stroke_width=4)
        tri = Polygon(ax.c2p(0, 0), ax.c2p(2, 0), ax.c2p(2, 4), stroke_width=0, fill_color=BLUE, fill_opacity=0.25)
        self.board_start(left=-0.2, top=1.5, maxw=6.6)
        p1 = step(1, "integrable", L("Monótona: integrable. $\\int_0^2 2x\\,dx=\\frac{2\\cdot4}{2}=4$", 24))
        self.push(p1, "Integrable, porque es monótona. Y la integral es el área del triángulo: **4**.", Create(ax), Create(rec), FadeIn(tri))
        n = ValueTracker(2)
        cs = always_redraw(lambda: cajas(ax, f, [2 * i / int(n.get_value()) for i in range(int(n.get_value()) + 1)],
                                         "sup", RED, 0.3))
        self.add(cs)
        p2 = step(2, "¿Ss = 4? NO", Lines("En cada bloque la caja sobresale sobre la curva:", "sobra un triangulito **por fino que sea**. $\\Ss>4$ siempre.", size=24))
        self.push(p2, "¿Suma superior igual a 4? Mirá las cajas: en **cada** bloque sobra un triangulito arriba de la recta.")
        self.say("Refino: los triangulitos se achican, la suma baja hacia 4... pero **nunca llega**. Siempre queda algo sobrando.",
                 n.animate.set_value(16), run_time=4, rate_func=linear)
        tip = self.tip(["4 es el **ínfimo** de las sumas superiores, pero no es mínimo.",
                        "Igual que $\\sqrt2$ es supremo sin máximo de $\\{x\\in\\Q:x^2\\le2\\}$."], label="EL MISMO FENÓMENO DEL CAP. 2", size=21)
        self.push(tip, "Es el mismo fenómeno del capítulo 2: el 4 es **ínfimo sin mínimo**. Si contestás «sí, con una partición muy fina», confundiste ínfimo con mínimo.", anim=FadeIn(tip))
        self.remove(cs)
        self.wipe(e)
        ax2 = ejes([0, 2.3, 1], [0, 4.6, 1], 5.2, 3.9).move_to([-3.6, -0.15, 0])
        rec2 = ax2.plot(f, x_range=[0, 2], color=BLUE, stroke_width=4)
        Q = [0, 0.5, 1, 1.5, 2]
        ic = cajas(ax2, f, Q, "inf", TEAL, 0.5)
        xl = xlabels(ax2, Q, ["0", "0{,}5", "1", "1{,}5", "2"], size=18)
        self.board_start(left=-0.2, top=1.4, maxw=6.6)
        p3 = step(3, "¿Si = 3? SÍ, y hay que exhibirla", Lines("$Q=\\{0,\\frac12,1,\\frac32,2\\}$: pisos $0,1,2,3$.",
                                                              "$\\Si(f,Q)=\\frac12(0+1+2+3)=3$ ✓", size=25))
        self.push(p3, "¿Suma inferior igual a 3? Sí, y hay que **mostrar** la partición. Cuatro bloques de un medio: pisos 0, 1, 2 y 3.",
                  Create(ax2), Create(rec2), FadeIn(xl), LaggedStart(*[FadeIn(c) for c in ic], lag_ratio=0.25))
        r = resp(Lines("Integrable;  no existe $P$ con $\\Ss=4$;", "sí existe $Q$ con $\\Si=3$.", size=24))
        self.push(r, "Un medio por seis: 3. Respuesta completa: integrable, **no** existe P, **sí** existe Q.", anim=FadeIn(r))
        self.wipe()

        e = enun("PARCIAL 2025-1 · EJ 5 (MOLDE)",
                 ["$h$ coincide con $3x$ en $[0,2]$ salvo en $x=1$ y $x=2$. ¿Integrable? ¿$\\int_0^2 h$?"], size=27).move_to([0, 2.3, 0])
        a = L("Acotada con dos discontinuidades: integrable (criterio 3).", 27).move_to([0, 1.0, 0])
        b = L("Por el corolario, $\\int_0^2 h=\\int_0^2 3x\\,dx=\\frac{2\\cdot6}{2}=6$.", 27).next_to(a, DOWN, buff=0.3)
        r = resp("Integrable, integral $6$.").next_to(b, DOWN, buff=0.4)
        self.say("El molde de 2025: una función que coincide con 3x salvo en dos puntos. Finitas discontinuidades: **integrable**.", FadeIn(e), FadeIn(a))
        self.say("Y cambiar finitos puntos **no cambia la integral**: es la de 3x, el triángulo, 6.", FadeIn(b), FadeIn(r))
        self.wipe()
        ej = VGroup(*[L(s, 25) for s in ["(a) $f(x)=\\sqrt x$ en $[1,4]$: menor $n$ con $\\Ss-\\Si<\\frac1{10}$.",
                                         "(b) $f(x)=\\frac1x$ en $[1,2]$: menor $n$ con diferencia $<\\frac1{100}$.",
                                         "(c) Para $f(x)=2x$ en $[0,2]$: ¿existe $P$ con $\\Si(f,P)=4$?"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        g = self.pausa(ej, "Tu turno. Ojo con la b: la función **decrece**.")
        sol = Lines("(a) $\\frac3n<\\frac1{10}$: $n=31$   (b) $\\frac1{2n}<\\frac1{100}$: $n=51$",
                    "(c) No: $\\Si<4$ siempre. 4 es supremo de las inferiores, no se alcanza.", size=24)
        debajo(sol, g)
        self.say("Soluciones. En la b, el valor absoluto de f(b) − f(a) es un medio.", FadeIn(sol))
        self.end_scene()


# =====================================================================
class V1_09_EpsTeoria(V1):
    CH_NUM, CH_TITLE = "05", "ε-δ · la teoría justa"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("ε-δ: el δ máximo", "Te dan la tolerancia de salida; vos das la de entrada",
                        prob=("MUY ALTA", "salió en los tres últimos parciales"))
        s = self.stamp(["$\\lim_{x\\to x_0}f(x)=L\\in\\R$  sii",
                        "$\\forall\\eps>0\\ \\exists\\delta>0:\\quad 0<|x-x_0|<\\delta,\\ x\\in I\\ \\Longrightarrow\\ |f(x)-L|<\\eps.$"],
                       "DEFINICIÓN DE LÍMITE (COMO LA DIO LA PROFESORA)", size=27).move_to([0, 2.1, 0])
        self.say("La definición, como la dio la profesora. El orden es sagrado: **primero** te dan el épsilon, **después** vos conseguís el delta.",
                 *self.show_stamp(s))
        mm = memo(["$|x-a|<r\\iff x\\in(a-r,a+r)=E(a,r)$.",
                   "$0<|x-a|<r$: el mismo intervalo **sin el centro**, $E^*(a,r)$.",
                   "El límite no mira qué pasa **en** $a$."], label="ENTORNOS", size=25).move_to([0, -0.6, 0])
        self.say("El 0 < |x − a| saca al centro: el límite **nunca mira** qué pasa exactamente en a.", FadeIn(mm))
        self.wipe()

        ax = ejes([0, 2.6, 1], [0, 4.2, 1], 7.2, 5.0).move_to([-2.4, -0.1, 0])
        f = lambda x: 2 * x
        curva = ax.plot(f, x_range=[0, 1.9], color=BLUE, stroke_width=4)
        pto = Dot(ax.c2p(1, 2), color=INK, radius=0.06)
        guias = VGroup(DashedLine(ax.c2p(1, 0), ax.c2p(1, 2), color=DIM), DashedLine(ax.c2p(0, 2), ax.c2p(1, 2), color=DIM))
        la = M("a", size=32, color=SOFT).next_to(ax.c2p(1, 0), DOWN, buff=0.12)
        lL = M("L", size=32, color=SOFT).next_to(ax.c2p(0, 2), LEFT, buff=0.12)
        self.say("La imagen: f(x) = 2x, cerca de a = 1, con límite L = 2.", Create(ax), Create(curva), FadeIn(guias), FadeIn(pto), FadeIn(la), FadeIn(lL))
        e = ValueTracker(0.8)
        d = ValueTracker(0.4)
        X0, X1 = 0, 2.6
        banda = always_redraw(lambda: Rectangle(width=ax.c2p(X1, 0)[0] - ax.c2p(X0, 0)[0],
                                                height=ax.c2p(0, 2 * e.get_value())[1] - ax.c2p(0, 0)[1],
                                                stroke_width=0).set_fill(RED, 0.16).move_to(
            [(ax.c2p(X0, 0)[0] + ax.c2p(X1, 0)[0]) / 2, ax.c2p(0, 2)[1], 0]))
        bordes = always_redraw(lambda: VGroup(
            DashedLine(ax.c2p(X0, 2 + e.get_value()), ax.c2p(X1, 2 + e.get_value()), color=RED, stroke_width=2),
            DashedLine(ax.c2p(X0, 2 - e.get_value()), ax.c2p(X1, 2 - e.get_value()), color=RED, stroke_width=2)))
        franja = always_redraw(lambda: Rectangle(width=ax.c2p(2 * d.get_value(), 0)[0] - ax.c2p(0, 0)[0],
                                                 height=ax.c2p(0, 4.1)[1] - ax.c2p(0, 0)[1],
                                                 stroke_width=0).set_fill(TEAL, 0.22).move_to(
            [ax.c2p(1, 0)[0], (ax.c2p(0, 0)[1] + ax.c2p(0, 4.1)[1]) / 2, 0]))

        def tramo():
            lo, hi = 1 - d.get_value(), 1 + d.get_value()
            g = VGroup()
            xs = np.linspace(lo, hi, 60)
            for x0, x1 in zip(xs[:-1], xs[1:]):
                xm = (x0 + x1) / 2
                ok_ = abs(f(xm) - 2) < e.get_value()
                g.add(Line(ax.c2p(x0, f(x0)), ax.c2p(x1, f(x1)), color=GREEN if ok_ else RED, stroke_width=8))
            return g
        tramo_v = always_redraw(tramo)

        def veredicto():
            bien = 2 * d.get_value() <= e.get_value() + 1e-9
            return T("el δ SIRVE" if bien else "el δ NO sirve: la curva se sale", 22,
                     GREEN if bien else RED, MONO, BOLD).move_to([3.5, 2.3, 0])
        ver = always_redraw(veredicto)
        sl_e = Slider("ε", e, 0, 1.0, color=RED, decimals=2, width=2.6).move_to([3.5, 0.9, 0])
        sl_d = Slider("δ", d, 0, 0.8, color=TEAL, decimals=2, width=2.6).move_to([3.5, 0.1, 0])
        dmax = VGroup(L("$\\delta_{\\max}=\\tfrac{\\eps}{2}=$", 24, YELLOW),
                      Num(0.4, num_decimal_places=2, font_size=32, color=YELLOW)).arrange(RIGHT, buff=0.15)
        dmax.move_to([3.5, -0.7, 0])
        dmax[1].add_updater(lambda m: m.set_value(e.get_value() / 2))
        self.add(banda, bordes)
        self.say("El cliente te da una **banda roja** alrededor de L, de alto 2ε: la tolerancia de salida. Es la perilla roja.", FadeIn(sl_e))
        self.add(franja, tramo_v, ver)
        self.say("Vos respondés con una **franja teal** alrededor de a: la perilla δ. La curva sobre la franja se pinta **verde** si cae dentro de la banda, **roja** si se sale.",
                 FadeIn(sl_d))
        self.say("Agrando δ... hasta que la curva **toca el borde** de la banda. Pasado ese punto, se sale: el δ ya no sirve.",
                 d.animate.set_value(0.65), run_time=4, rate_func=linear)
        self.say("Lo achico de nuevo: vuelve a entrar. Achicar δ **nunca rompe** nada. El problema es agrandarlo de más.",
                 d.animate.set_value(0.25), run_time=3)
        self.add(dmax)
        self.say("El δ máximo es el borde exacto: la franja **más ancha** que todavía funciona. Para esta recta, ε/2.",
                 d.animate.set_value(0.4), run_time=2)
        self.say("Ahora el cliente **aprieta**: achica ε. Mi δ de antes se sale... así que tengo que achicarlo también.",
                 e.animate.set_value(0.35), run_time=3)
        self.say("Lo ajusto al nuevo máximo, ε/2. Sirve de nuevo.", d.animate.set_value(0.175), run_time=2)
        self.say("Y así para **cualquier** ε: si el cliente aprieta más, yo achico más. Que eso se pueda hacer siempre es que **exista el límite**.",
                 e.animate.set_value(0.08), d.animate.set_value(0.04), run_time=4)
        tip = self.tip(["Control de calidad: el cliente fija la tolerancia de salida (ε),",
                        "vos respondés con la tolerancia de entrada (δ)."], label="LA IMAGEN", size=21, width=6.0).move_to([3.75, -1.7, 0])
        self.say("Control de calidad: ε es lo que exige el cliente, δ es lo que vos podés garantizar en la entrada.", FadeIn(tip))
        self.remove(banda, bordes, franja, tramo_v, ver, dmax)
        self.wipe()

        met = metodo(["Escribí $|f(x)-L|<\\eps$ con los números.",
                      "Despejá **hacia atrás** con pasos reversibles ($\\iff$) hasta el **conjunto** de $x$ que cumplen.",
                      "Si queda $|x-a|<c$, entonces $\\delta_{\\max}=c$.",
                      "Si queda un intervalo **no centrado** en $a$: medí la distancia a cada borde. **Manda la menor.**"],
                     "δ MÁXIMO DADO UN ε", size=25).move_to([0, 1.1, 0])
        self.say("El método. Despejás **hacia atrás**, desde la condición de llegada hasta el conjunto de x que sirven.",
                 FadeIn(met), min_t=4)
        mm = memo(["Si $f(x)=mx+n$: $\\ |f(x)-L|=|m|\\,|x-a|$, así que $\\delta_{\\max}=\\dfrac{\\eps}{|m|}$. La pendiente divide."],
                  label="PATRÓN LINEAL", size=25).move_to([0, -1.7, 0])
        self.say("Y un atajo para las lineales: **la pendiente divide**. δ máximo es ε sobre |m|.", FadeIn(mm))
        self.end_scene()


# =====================================================================
class V1_10_EpsParcial(V1):
    CH_NUM, CH_TITLE = "05", "ε-δ · ejercicios de parcial"

    def construct(self):
        self.setup_frame()
        e = enun("PARCIAL 2024-2 · EJ 7", ["$f(x)=2x$,  $\\lim_{x\\to1}f(x)=2$. Máximo $\\delta$ para $\\eps=\\frac13$."], size=28).move_to([0, 2.5, 0])
        self.say("Parcial 2024. El caso lineal, puro.", FadeIn(e))
        self.board_start(top=1.45)
        a = step(1, "condición de llegada", M(r"|2x-2|<\tfrac13", size=44))
        self.push(a, "Escribo la condición de llegada con los números.")
        b = step(2, "factorizo", M(r"|2x-2|=2\,|x-1|", size=44))
        self.push(b, "Saco el 2 de factor común: aparece |x − 1|, que es lo que quiero despejar.")
        c = step(3, "despejo", M(r"2|x-1|<\tfrac13\iff|x-1|<\tfrac16", size=44))
        self.push(c, "Divido por 2 y queda la forma |x − a| < algo. Ese algo **es** el δ máximo.")
        r = resp("$\\delta_{\\max}=\\frac16$")
        self.push(r, "Un sexto. Patrón lineal: ε sobre la pendiente, un tercio sobre 2.", anim=FadeIn(r))
        self.wipe()
        e = enun("PARCIAL 2025-1 · EJ 7", ["$f(x)=2x$,  $a=2$,  $L=4$,  $\\eps=\\frac12$."], size=28).move_to([0, 2.4, 0])
        a = M(r"|2x-4|<\tfrac12\iff2|x-2|<\tfrac12\iff|x-2|<\tfrac14", size=44).move_to([0, 1.0, 0])
        b = L("Patrón lineal: $\\frac{1/2}{2}=\\frac14$ ✓", 26, GREEN).next_to(a, DOWN, buff=0.35)
        r = resp("$\\delta_{\\max}=\\frac14$").next_to(b, DOWN, buff=0.35)
        self.say("2025: el mismo molde. Medio sobre dos: **un cuarto**. Dos parciales seguidos, mismos puntos regalados.", FadeIn(e), Write(a), FadeIn(b), FadeIn(r))
        self.wipe()

        e = enun("PARCIAL 2024-1 · EJ 8 · EL DIFÍCIL",
                 ["$f(x)=\\fl{x}$. Máximo $\\delta$ tal que $x\\in E^*(3{,}8;\\delta)\\Rightarrow f(x)\\in E(3;0{,}5)$."], size=28).move_to([0, 2.5, 0])
        self.say("Y el difícil. Parte entera, y el punto 3,8 **no está en el medio** de nada. Pausá.", FadeIn(e), min_t=3)
        self.board_start(top=1.45, maxw=7.0)
        a = step(1, "qué pide la llegada", L("$E(3;0{,}5)=(2{,}5;\\,3{,}5)$. Necesito $\\fl{x}$ ahí.", 24))
        self.push(a, "La llegada: el entorno de 3 con radio medio, el intervalo de 2,5 a 3,5.")
        b = step(2, "la salida es entera", L("El único entero en $(2{,}5;3{,}5)$ es el 3: $\\ \\fl{x}=3$.", 24))
        self.push(b, "Pero la parte entera **solo da enteros**. El único entero en ese intervalo es el 3.")
        c = step(3, "a conjunto de x", L("$\\fl{x}=3\\iff3\\le x<4$:  las $x$ admisibles son $[3,4)$.", 24))
        self.push(c, "Parte entera igual a 3: x entre 3 y 4, con el 4 afuera.")
        nl = NumberLine(x_range=[2.6, 4.4, 1], length=5.6, color=SOFT, include_tip=True, include_ticks=False,
                        tip_length=0.15).move_to([3.7, 0.4, 0])
        zona = Rectangle(width=nl.n2p(4)[0] - nl.n2p(3)[0], height=0.3, stroke_width=0).set_fill(GREEN, 0.35).move_to((nl.n2p(3) + nl.n2p(4)) / 2)
        z3 = VGroup(Line(nl.n2p(3) + DOWN * 0.22, nl.n2p(3) + UP * 0.22, color=GREEN, stroke_width=3), M("3", size=30).next_to(nl.n2p(3), DOWN, buff=0.3))
        z4 = VGroup(DashedLine(nl.n2p(4) + DOWN * 0.22, nl.n2p(4) + UP * 0.22, color=GREEN, stroke_width=3), M("4", size=30).next_to(nl.n2p(4), DOWN, buff=0.3))
        c38 = Dot(nl.n2p(3.8), color=RED, radius=0.08)
        l38 = M("3{,}8", size=28, color=RED).next_to(c38, DOWN, buff=0.3)
        self.play(Create(nl), FadeIn(zona), FadeIn(z3), FadeIn(z4), FadeIn(c38), FadeIn(l38))
        d = step(4, "lado más apretado", L("Del 3,8 al borde izquierdo: $0{,}8$. Al derecho: $0{,}2$. Manda $0{,}2$.", 24))
        izq = DoubleArrow(nl.n2p(3), nl.n2p(3.8), buff=0, color=SOFT, stroke_width=3, tip_length=0.15).shift(UP * 0.55)
        der = DoubleArrow(nl.n2p(3.8), nl.n2p(4), buff=0, color=RED, stroke_width=3, tip_length=0.12).shift(UP * 0.55)
        li = M("0{,}8", size=28, color=SOFT).next_to(izq, UP, buff=0.08)
        ld = M("0{,}2", size=28, color=RED).next_to(der, UP, buff=0.08)
        self.push(d, "Ahora, el lado más apretado. El entorno es **simétrico**: si me paso de 0,2 hacia la derecha, llego al 4 y la parte entera salta a 4.",
                  GrowFromCenter(izq), GrowFromCenter(der), FadeIn(li), FadeIn(ld))
        sim = Rectangle(width=nl.n2p(4)[0] - nl.n2p(3.6)[0], height=0.14, stroke_width=0).set_fill(TEAL, 0.9).move_to((nl.n2p(3.6) + nl.n2p(4)) / 2).shift(DOWN * 0.9)
        sl = T("δ = 0,2 para cada lado", 20, TEAL, MONO, BOLD).next_to(sim, DOWN, buff=0.12)
        self.play(FadeIn(sim), FadeIn(sl))
        r = resp("$\\delta_{\\max}=0{,}2$")
        self.push(r, "δ máximo: **0,2**. El entorno simétrico entra entero en [3, 4) solo si mide 0,2 para cada lado.", anim=FadeIn(r))
        self.end_scene()


# =====================================================================
class V1_11_EpsPractico(V1):
    CH_NUM, CH_TITLE = "05", "ε-δ · el asimétrico y las demostraciones"

    def construct(self):
        self.setup_frame()
        e = enun("PRÁCTICO 4.2 · EJ 1 b) · EL ASIMÉTRICO",
                 ["$f(x)=\\frac1x$,  $a=1$. Hallar el $\\delta$ máximo en función de $\\eps$ (con $0<\\eps<1$)."], size=27).move_to([0, 2.55, 0])
        self.say("Del práctico. La función no es lineal y el intervalo de x que sirven **no queda centrado**. Es el ejemplo perfecto del paso 4.", FadeIn(e), min_t=2.5)
        ax = ejes([0.3, 2.4, 1], [0, 2.4, 1], 5.4, 4.2).move_to([-3.6, -0.5, 0])
        f = lambda x: 1 / x
        curva = ax.plot(f, x_range=[0.45, 2.3], color=BLUE, stroke_width=4)
        ep = 0.4
        banda = Rectangle(width=ax.c2p(2.4, 0)[0] - ax.c2p(0.3, 0)[0], height=ax.c2p(0, 2 * ep)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0).set_fill(RED, 0.18).move_to([(ax.c2p(0.3, 0)[0] + ax.c2p(2.4, 0)[0]) / 2, ax.c2p(0, 1)[1], 0])
        x1, x2 = 1 / (1 + ep), 1 / (1 - ep)
        zona = Rectangle(width=ax.c2p(x2, 0)[0] - ax.c2p(x1, 0)[0], height=0.16, stroke_width=0).set_fill(GREEN, 0.8)
        zona.move_to([(ax.c2p(x1, 0)[0] + ax.c2p(x2, 0)[0]) / 2, ax.c2p(0, 0)[1], 0])
        g1 = DashedLine(ax.c2p(x1, 0), ax.c2p(x1, 1 + ep), color=GREEN)
        g2 = DashedLine(ax.c2p(x2, 0), ax.c2p(x2, 1 - ep), color=GREEN)
        c1 = Dot(ax.c2p(1, 0), color=RED, radius=0.07)
        self.board_start(left=-0.3, top=1.45, maxw=6.8)
        p1 = step(1, "llegada", M(r"\left|\tfrac1x-1\right|<\eps\iff1-\eps<\tfrac1x<1+\eps", size=38))
        self.push(p1, "Llegada: 1/x entre 1 − ε y 1 + ε.", Create(ax), Create(curva), FadeIn(banda))
        p2 = step(2, "invierto (todo positivo)", M(r"\frac{1}{1+\eps}<x<\frac{1}{1-\eps}", size=40))
        self.push(p2, "Invierto. Como todo es positivo, al invertir **se da vuelta** el orden.", Create(g1), Create(g2), FadeIn(zona), FadeIn(c1))
        p3 = step(3, "distancias desde a = 1", Lines("Izq: $1-\\frac1{1+\\eps}=\\frac{\\eps}{1+\\eps}$    Der: $\\frac1{1-\\eps}-1=\\frac{\\eps}{1-\\eps}$",
                                                     "Como $1+\\eps>1-\\eps$, la izquierda es la **menor**.", size=23))
        self.push(p3, "Mirá el dibujo: la zona verde se estira más a la derecha. La distancia a la **izquierda** es la menor, y esa manda.")
        r = resp("$\\delta_{\\max}=\\frac{\\eps}{1+\\eps}$")
        self.push(r, "δ máximo: ε sobre 1 + ε. Para ε = 0,01 da más o menos 0,0099.", anim=FadeIn(r))
        self.wipe()

        # ---- perilla ε: el intervalo se deforma, manda siempre el lado corto
        ax = ejes([0.2, 3.2, 1], [0, 2.6, 1], 8.0, 4.6).move_to([-2.0, 0.2, 0])
        curva = ax.plot(f, x_range=[0.39, 3.1], color=BLUE, stroke_width=4)
        ep = ValueTracker(0.3)
        xa = lambda: 1 / (1 + ep.get_value())
        xb = lambda: 1 / (1 - ep.get_value())
        banda = always_redraw(lambda: Rectangle(width=ax.c2p(3.2, 0)[0] - ax.c2p(0.2, 0)[0],
                                                height=ax.c2p(0, 2 * ep.get_value())[1] - ax.c2p(0, 0)[1],
                                                stroke_width=0).set_fill(RED, 0.16).move_to(
            [(ax.c2p(0.2, 0)[0] + ax.c2p(3.2, 0)[0]) / 2, ax.c2p(0, 1)[1], 0]))

        def zonas():
            y0 = ax.c2p(0, 0)[1]
            izq = Line([ax.c2p(xa(), 0)[0], y0 - 0.25, 0], [ax.c2p(1, 0)[0], y0 - 0.25, 0], color=YELLOW, stroke_width=8)
            der = Line([ax.c2p(1, 0)[0], y0 - 0.25, 0], [ax.c2p(xb(), 0)[0], y0 - 0.25, 0], color=DIM, stroke_width=8)
            sim = Line([ax.c2p(1 - (1 - xa()), 0)[0], y0 + 0.05, 0], [ax.c2p(1 + (1 - xa()), 0)[0], y0 + 0.05, 0],
                       color=TEAL, stroke_width=6)
            g1 = DashedLine(ax.c2p(xa(), 0), ax.c2p(xa(), 1 + ep.get_value()), color=GREEN, stroke_width=2)
            g2 = DashedLine(ax.c2p(xb(), 0), ax.c2p(xb(), 1 - ep.get_value()), color=GREEN, stroke_width=2)
            return VGroup(g1, g2, izq, der, sim)
        zv = always_redraw(zonas)
        panel = VGroup(Slider("ε", ep, 0, 0.6, color=RED, decimals=2, width=2.2, size=24),
                       VGroup(T("izquierda", 20, YELLOW, MONO, BOLD), Num(0, 3, font_size=30, color=YELLOW)).arrange(RIGHT, buff=0.2),
                       VGroup(T("derecha", 20, SOFT, MONO, BOLD), Num(0, 3, font_size=30, color=SOFT)).arrange(RIGHT, buff=0.2),
                       VGroup(T("δ máx", 20, TEAL, MONO, BOLD), Num(0, 3, font_size=30, color=TEAL)).arrange(RIGHT, buff=0.2)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.6, 0])
        panel[1][1].add_updater(lambda m: m.set_value(1 - xa()))
        panel[2][1].add_updater(lambda m: m.set_value(xb() - 1))
        panel[3][1].add_updater(lambda m: m.set_value(1 - xa()))
        self.add(banda)
        self.say("Mirá cómo se deforma con una perilla. Banda roja de alto 2ε alrededor de 1; abajo, la zona de x que sirven.",
                 Create(ax), Create(curva), FadeIn(panel))
        self.add(zv)
        self.say("Amarillo, el lado izquierdo; gris, el derecho. La curva es más **empinada** a la izquierda, así que ahí el margen es más corto.")
        self.say("Agrando ε: los dos lados crecen, pero el derecho **se dispara**. El δ, en teal, sigue atado al lado corto.",
                 ep.animate.set_value(0.55), run_time=4)
        self.say("Achico ε: los dos lados se parecen cada vez más, porque de cerca **la curva parece una recta**. Pero el corto sigue mandando.",
                 ep.animate.set_value(0.05), run_time=4)
        self.remove(banda, zv)
        for m in panel.get_family():
            m.clear_updaters()
        self.wipe()
        tr = trampa(["El intervalo de $x$ admisibles no está centrado en 1. Si respondés con la",
                     "distancia derecha, algún $x$ a la izquierda se escapa de la banda."], "NO ES δ = ε", size=25).move_to([0, 1.9, 0])
        self.say("La trampa: responder con el lado largo. Algún x del lado corto **se escapa** de la banda.", FadeIn(tr))

        e = enun("MOLDE GENERAL · CUADRÁTICA", ["Probar por definición que $\\lim_{x\\to2}x^2=4$."], size=27).move_to([0, 0.2, 0])
        self.say("Y si te piden **demostrar** un límite para un ε genérico, este es el molde con una cuadrática.", FadeIn(e))
        self.wipe(e)
        self.play(e.animate.move_to([0, 2.5, 0]))
        self.board_start(top=1.5)
        a = step(1, "factorizo", L("$|x^2-4|=|x-2|\\,|x+2|$. El primer factor lo controlo con $\\delta$; el segundo molesta.", 24))
        self.push(a, "Factorizo. |x − 2| lo controla δ. El |x + 2| molesta: hay que acotarlo.")
        b = step(2, "me autolimito", L("Pido $\\delta\\le1$. Entonces $1<x<3$ y $|x+2|<5$.", 24))
        self.push(b, "El truco: me autolimito a δ ≤ 1. Entonces x queda entre 1 y 3, y |x + 2| menor que 5.")
        c = step(3, "encadeno", L("$|x^2-4|<5\\delta$. Alcanza con $5\\delta\\le\\eps$.", 24))
        self.push(c, "Encadeno: todo queda menor que 5δ. Alcanza con que 5δ no supere ε.")
        d = step(4, "elijo", L("$\\delta=\\min\\{1,\\frac\\eps5\\}$. Con eso $0<|x-2|<\\delta\\Rightarrow|x^2-4|<\\eps$. $\\blacksquare$", 24))
        self.push(d, "Elijo δ como el **mínimo** entre 1 y ε/5: cumple las dos condiciones a la vez.")
        self.wipe()
        ej = VGroup(*[L(s, 25) for s in ["(a) $f(x)=3x-1$, $a=1$, $\\eps=0{,}3$.",
                                         "(b) $f(x)=\\fl{x}$, entorno de $2{,}7$, llegada $E(2;0{,}5)$.",
                                         "(c) $f(x)=\\sqrt x$, $a=4$, $\\eps=0{,}1$."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        g = self.pausa(ej, "Tu turno: δ máximo en cada caso. Uno lineal, uno con parte entera, uno asimétrico.")
        sol = Lines("(a) $\\delta=0{,}1$   (b) $x\\in[2,3)$, distancias 0,7 y 0,3: $\\delta=0{,}3$",
                    "(c) $3{,}61<x<4{,}41$: distancias 0,39 y 0,41: $\\delta=0{,}39$", size=24)
        debajo(sol, g)
        self.say("Soluciones. En las tres manda **la distancia menor**.", FadeIn(sol))
        self.end_scene()
