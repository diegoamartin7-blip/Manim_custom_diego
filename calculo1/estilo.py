"""Estilo "cuaderno técnico" sobre grafito para los videos de Cálculo 1."""
from pathlib import Path

import manimpango
from manim import *

_FONTS = Path(__file__).resolve().parent / "fonts"
for _f in sorted(_FONTS.glob("*.otf")):
    manimpango.register_font(str(_f))

SANS = "IBM Plex Sans"
MONO = "IBM Plex Mono"

FONDO = "#1E2125"
GRILLA = "#272B30"
PANEL = "#272B31"
TINTA = "#ECE6D6"
SUAVE = "#8E897D"
ROJO = "#E0574B"
TEAL = "#3FB0A6"
VERDE = "#8CC063"
ACERO = "#9DB4C0"
NARANJA = "#E8913F"
DORADO = "#F2C230"

config.background_color = FONDO

PLANTILLA = TexTemplate()
PLANTILLA.add_to_preamble(
    r"""
\usepackage{amssymb}
\newcommand{\R}{\mathbb{R}}
\newcommand{\Q}{\mathbb{Q}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\Ss}{S^{*}}
\newcommand{\Si}{S_{*}}
\newcommand{\fl}[1]{\lfloor #1\rfloor}
\newcommand{\eps}{\varepsilon}
"""
)
MathTex.set_default(tex_template=PLANTILLA, color=TINTA)
Tex.set_default(tex_template=PLANTILLA, color=TINTA)

ANCHO = 12.6  # ancho útil de contenido
Y_TOP = 3.05  # borde superior del área de contenido
Y_SUB = -3.42  # centro de la banda de subtítulos


# ---------------------------------------------------------------- texto
def T(s, size=26, color=TINTA, weight=NORMAL, font=SANS, **kw):
    return Text(s, font=font, font_size=size, color=color, weight=weight,
                disable_ligatures=True, **kw)


def Mono(s, size=18, color=SUAVE, weight=NORMAL):
    return T(s, size=size, color=color, weight=weight, font=MONO)


def M(s, size=34, color=TINTA):
    return MathTex(s, font_size=size, color=color)


def L(s, size=26, color=TINTA, weight=NORMAL, msize=None):
    """Línea mixta: texto IBM Plex con tramos $matemática$ intercalados."""
    msize = msize or size * 1.3
    trozos = s.split("$")
    partes = VGroup()
    ancla = []
    for i, tr in enumerate(trozos):
        if i % 2 == 1:
            if tr.strip():
                m = M(tr, size=msize, color=color)
                partes.add(m)
                ancla.append(("m", m, None))
            continue
        if not tr.strip():
            continue
        t = T("|" + tr.strip(), size=size, color=color, weight=weight)
        strut, cuerpo = t[0], VGroup(*t[1:])
        partes.add(cuerpo)
        ancla.append(("t", cuerpo, strut, tr))
    x = 0.0
    ref_y = None
    prev_txt = None
    for item in ancla:
        kind, mob = item[0], item[1]
        if kind == "t":
            strut, raw = item[2], item[3]
            if ref_y is None:
                ref_y = strut.get_center()[1]
            mob.shift(UP * (ref_y - strut.get_center()[1]))
            gap = 0.0 if raw[:1] in ",.;:)" or prev_txt is None and x == 0 else 0.11
            if raw[:1] != " " and prev_txt is not None:
                gap = 0.02 if raw[:1] in ",.;:)" else gap
        else:
            if ref_y is None:
                ref_y = 0.0
            mob.move_to([0, ref_y + 0.02, 0])
            gap = 0.11 if x else 0.0
        mob.shift(RIGHT * (x + gap - mob.get_left()[0]))
        x = mob.get_right()[0]
        prev_txt = kind == "t"
    return partes


def P(*lineas, size=26, buff=0.2, color=TINTA):
    """Párrafo: varias líneas mixtas alineadas a la izquierda."""
    g = VGroup(*[L(l, size=size, color=color) if isinstance(l, str) else l for l in lineas])
    g.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return g


# ---------------------------------------------------------------- cajas
def _titulo_caja(txt, color):
    return Mono(txt, size=15, color=color, weight=BOLD)


def caja(contenido, tipo="sello", titulo="", ancho=None, pad=0.28):
    """Cajas del libro: sello (roja doble), tip (teal), memo (verde),
    metodo (acero), trampa (roja lateral), resp (verde), enunciado."""
    colores = {"sello": ROJO, "tip": TEAL, "memo": VERDE, "metodo": ACERO,
               "trampa": ROJO, "resp": VERDE, "enunciado": SUAVE, "pausa": NARANJA}
    c = colores[tipo]
    if tipo == "metodo":
        titulo = "MÉTODO · " + titulo
    if tipo == "trampa":
        titulo = "TRAMPA · " + titulo
    if tipo == "resp":
        titulo = "RESPUESTA"
    cab = _titulo_caja(titulo, c) if titulo and tipo not in ("sello", "enunciado") else None
    cuerpo = VGroup(cab, contenido).arrange(DOWN, aligned_edge=LEFT, buff=0.16) if cab else VGroup(contenido)
    w = max(cuerpo.width + 2 * pad, ancho or 0)
    h = cuerpo.height + 2 * pad
    if tipo == "enunciado":
        h += 0.12
    rect = Rectangle(width=w, height=h, stroke_width=0, fill_opacity=1)
    rect.move_to(cuerpo)
    rect.align_to(cuerpo, LEFT).shift(LEFT * pad)
    if tipo == "enunciado":
        rect.shift(UP * 0.06)
    g = VGroup()
    if tipo == "sello":
        rect.set_fill(interpolate_color(ManimColor(FONDO), ManimColor(ROJO), 0.07))
        rect.set_stroke(ROJO, 1.4)
        interior = rect.copy().set_fill(opacity=0).set_stroke(ROJO, 3.2)
        interior.stretch_to_fit_width(w - 0.14).stretch_to_fit_height(h - 0.14).move_to(rect)
        g.add(rect, interior)
        if titulo:
            tt = _titulo_caja(titulo, ROJO)
            fondo_tt = Rectangle(width=tt.width + 0.24, height=tt.height + 0.12,
                                 stroke_width=0, fill_color=FONDO, fill_opacity=1)
            fondo_tt.move_to(rect.get_corner(UL) + RIGHT * (0.3 + fondo_tt.width / 2))
            tt.move_to(fondo_tt)
            g.add(fondo_tt, tt)
    elif tipo == "enunciado":
        rect.set_fill(PANEL).set_stroke("#3A3F46", 1.2)
        g.add(rect)
        if titulo:
            tt = Mono(titulo, size=15, color=FONDO, weight=BOLD)
            fondo_tt = Rectangle(width=tt.width + 0.2, height=tt.height + 0.12,
                                 stroke_width=0, fill_color=TINTA, fill_opacity=1)
            fondo_tt.move_to(rect.get_corner(UL) + RIGHT * (0.22 + fondo_tt.width / 2))
            tt.move_to(fondo_tt)
            g.add(fondo_tt, tt)
    else:
        mezcla = {"tip": 0.10, "memo": 0.10, "metodo": 0.07, "trampa": 0.11,
                  "resp": 0.13, "pausa": 0.07}[tipo]
        rect.set_fill(interpolate_color(ManimColor(FONDO), ManimColor(c), mezcla))
        if tipo in ("memo", "metodo", "resp"):
            rect.set_stroke(c, 1.2)
        if tipo == "pausa":
            rect = DashedVMobject(rect.copy().set_stroke(c, 1.6), num_dashes=60)
            fill = Rectangle(width=w, height=h, stroke_width=0, fill_opacity=1,
                             fill_color=interpolate_color(ManimColor(FONDO), ManimColor(c), 0.07)).move_to(rect)
            g.add(fill)
        g.add(rect)
        if tipo in ("tip", "memo", "trampa"):
            barra = Line(rect.get_corner(UL), rect.get_corner(DL), stroke_width=6, color=c)
            g.add(barra)
    g.add(cuerpo)
    return g


def paso(n, txt):
    return Mono(f"PASO {n} — {txt.upper()}", size=16, color=ROJO, weight=BOLD)


def resp(contenido):
    if isinstance(contenido, str):
        contenido = L(contenido, size=26, weight=BOLD)
    return caja(contenido, "resp")


def chip(txt, color=ROJO, size=16):
    t = Mono(txt, size=size, color=FONDO, weight=BOLD)
    r = Rectangle(width=t.width + 0.26, height=t.height + 0.16, stroke_width=0,
                  fill_color=color, fill_opacity=1)
    return VGroup(r, t.move_to(r))


def ok():
    return T("✓", size=28, color=VERDE, weight=BOLD)


def tabla(filas, anchos=None, size=22, cab_color=ACERO, h=0.5):
    """Tabla simple: primera fila = encabezado. Celdas: texto o $math$."""
    ncol = len(filas[0])
    celdas = [[L(c, size=size, weight=BOLD if i == 0 else NORMAL,
                 color=cab_color if i == 0 else TINTA) for c in f] for i, f in enumerate(filas)]
    if anchos is None:
        anchos = [max(celdas[i][j].width for i in range(len(filas))) + 0.5 for j in range(ncol)]
    g = VGroup()
    filas_g = VGroup()
    y = 0
    for i, f in enumerate(celdas):
        fila = VGroup()
        x = 0
        for j, c in enumerate(f):
            c.move_to([x + anchos[j] / 2, y, 0])
            fila.add(c)
            x += anchos[j]
        filas_g.add(fila)
        y -= h
    total = sum(anchos)
    lineas = VGroup(
        Line([0, h / 2, 0], [total, h / 2, 0], stroke_width=1.6, color=SUAVE),
        Line([0, -h / 2, 0], [total, -h / 2, 0], stroke_width=1.0, color=SUAVE),
        Line([0, y + h / 2, 0], [total, y + h / 2, 0], stroke_width=1.6, color=SUAVE),
    )
    g.add(lineas, filas_g)
    g.filas = filas_g
    g.lineas = lineas
    return g


# ---------------------------------------------------------------- escena base
class Escena(Scene):
    CAP = ""
    NOMBRE = ""

    def setup(self):
        self.sub = None
        grilla = VGroup()
        for x in np.arange(-7.0, 7.01, 0.5):
            grilla.add(Line([x, -4, 0], [x, 4, 0], stroke_width=0.8, color=GRILLA))
        for y in np.arange(-4.0, 4.01, 0.5):
            grilla.add(Line([-7.2, y, 0], [7.2, y, 0], stroke_width=0.8, color=GRILLA))
        self.grilla = grilla
        izq = Mono("CÁLCULO 1 · 1er PARCIAL", size=14)
        der = Mono(self.NOMBRE.upper(), size=14)
        izq.to_corner(UL, buff=0.28)
        der.to_corner(UR, buff=0.28)
        regla = Line([-6.9, 3.5, 0], [6.9, 3.5, 0], stroke_width=1, color="#3A3F46")
        self.cabecera = VGroup(izq, der, regla)
        banda = Rectangle(width=14.3, height=1.0, stroke_width=0, fill_color=FONDO,
                          fill_opacity=0.92).move_to([0, Y_SUB, 0])
        self.banda = banda
        self.add(grilla, self.cabecera, banda)
        self.fijos = {grilla, self.cabecera, banda}

    # ------------------------------------------------------ subtítulos karaoke
    def _armar_sub(self, palabras):
        lineas, act = [], []
        largo = 0
        for p in palabras:
            if act and largo + len(p) + 1 > 68:
                lineas.append(act)
                act, largo = [], 0
            act.append(p)
            largo += len(p) + 1
        if act:
            lineas.append(act)
        grupo = VGroup()
        glifos_por_palabra = []
        for ln in lineas:
            t = T(" ".join(ln), size=24, color=SUAVE)
            k = 0
            for p in ln:
                n = len(p.replace(" ", ""))
                glifos_por_palabra.append(VGroup(*t[k:k + n]))
                k += n
            grupo.add(t)
        grupo.arrange(DOWN, buff=0.12)
        if grupo.width > 13.4:
            grupo.scale_to_fit_width(13.4)
        grupo.move_to([0, Y_SUB, 0])
        grupo.palabras = glifos_por_palabra
        return grupo

    def decir(self, texto, *anims, dur=None, wpm_seg=0.30):
        """Subtítulo karaoke (sin audio): la palabra actual en dorado.
        Las animaciones pasadas se reproducen en paralelo."""
        palabras = texto.split()
        sub = self._armar_sub(palabras)
        if self.sub is not None:
            self.remove(self.sub)
            self.fijos.discard(self.sub)
        self.add(sub)
        self.sub = sub
        self.fijos.add(sub)
        n = len(palabras)
        total = dur if dur is not None else max(1.8, wpm_seg * n + 0.9)
        largo_anims = max((a.get_run_time() for a in anims), default=0)
        total = max(total, largo_anims)
        estado = {"k": -2}

        def pintar(m, alpha):
            k = min(n - 1, int(alpha / 0.88 * n))
            if k == estado["k"]:
                return
            estado["k"] = k
            for i, w in enumerate(m.palabras):
                w.set_color(TINTA if i < k else DORADO if i == k else SUAVE)

        karaoke = UpdateFromAlphaFunc(sub, pintar, run_time=total, rate_func=linear)
        envueltas = []
        for a in anims:
            rt = a.get_run_time()
            envueltas.append(a if rt >= total - 1e-6 else Succession(a, Wait(total - rt)))
        self.play(karaoke, *envueltas)

    def callar(self):
        if self.sub is not None:
            self.remove(self.sub)
            self.fijos.discard(self.sub)
            self.sub = None

    # ------------------------------------------------------ utilidades
    def contenido(self):
        return [m for m in self.mobjects if m not in self.fijos]

    def limpiar(self, run_time=0.6):
        c = self.contenido()
        if c:
            self.play(*[FadeOut(m) for m in c], run_time=run_time)

    def portada(self, num, nombre, prob, nota, color=ROJO):
        etiqueta = VGroup(
            Rectangle(width=2.6, height=0.46, stroke_color=ROJO, stroke_width=1.6),
            Mono(f"CAPÍTULO {num}", size=18, color=ROJO, weight=BOLD),
        )
        etiqueta[1].move_to(etiqueta[0])
        titulo = T(nombre, size=54, weight=BOLD)
        if titulo.width > 12.5:
            titulo.scale_to_fit_width(12.5)
        regla = Line(LEFT, RIGHT, stroke_width=2.4, color=TINTA).set_width(max(titulo.width, 4))
        ch = chip(f"PROBABILIDAD: {prob}", color=color, size=18)
        n = Mono(nota, size=17)
        g = VGroup(etiqueta, titulo, regla, ch, n).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        g.move_to([0, 0.5, 0])
        self.play(FadeIn(etiqueta, shift=RIGHT * 0.3), Write(titulo), run_time=1.2)
        self.play(Create(regla), FadeIn(ch), FadeIn(n), run_time=0.8)
        return g

    def fin(self):
        self.callar()
        self.limpiar(0.8)
        self.wait(0.4)


def ejes(xr, yr, w, h, ticks=True, **kw):
    ax = Axes(
        x_range=xr, y_range=yr, x_length=w, y_length=h,
        axis_config={"color": SUAVE, "stroke_width": 1.6, "include_ticks": ticks,
                     "tick_size": 0.05, "include_tip": True, "tip_length": 0.16,
                     "tip_width": 0.12},
        **kw,
    )
    return ax


def num_eje(ax, valores, eje="x", size=20, color=SUAVE, textos=None):
    g = VGroup()
    for i, v in enumerate(valores):
        s = textos[i] if textos else (f"{v:g}".replace(".", ","))
        m = L(s, size=size, color=color) if "$" in s else T(s, size=size, color=color)
        if eje == "x":
            m.next_to(ax.c2p(v, 0), DOWN, buff=0.12)
        else:
            m.next_to(ax.c2p(0, v), LEFT, buff=0.12)
        g.add(m)
    return g
