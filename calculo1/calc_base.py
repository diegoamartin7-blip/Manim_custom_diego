"""
calc_base.py - Infraestructura comun de los 3 videos de Calculo 1 (1er parcial).
Mismo sistema que los videos de Matematica 2 (gaps_base.py):

- Subtitulos karaoke, SIN audio: el texto ES la narracion.
    palabra sin leer = gris, palabra actual = dorado, ya leida = crema,
    **enfasis** = queda en dorado.
- Estilo cuaderno tecnico sobre fondo grafito apagado + grilla tenue,
  sellos rojos de doble borde (definiciones/teoremas), cajas teal (intuicion),
  verdes (ayuda-memoria), barra roja (trampa), acero (metodo).
- Pizarra con auto-scroll:  self.push(mobject, "subtitulo")

Variables de entorno (C1_* o, por costumbre, M2_*):
    C1_PACE  multiplica TODOS los tiempos (1.0 normal, 1.2 = mas lento)
    C1_WPS   palabras por segundo de lectura (default 3.1)
    C1_SNAP  si existe, guarda capturas en snaps/ (solo para control)
"""
import os
import glob
import numpy as np
from manim import *
from manim.animation.animation import prepare_animation
import manimpango

HERE = os.path.dirname(os.path.abspath(__file__))
for _f in glob.glob(os.path.join(HERE, "fonts", "*.ttf")):
    try:
        manimpango.register_font(_f)
    except Exception:
        pass

def _env(name, default):
    return os.environ.get("C1_" + name, os.environ.get("M2_" + name, default))


PACE = float(_env("PACE", "1.0"))
WPS = float(_env("WPS", "3.1"))
SNAP = _env("SNAP", "")

# ---------------- Paleta estilo 3Blue1Brown: negro, limpio ----------
BG = "#000000"
PANEL = "#0E0F11"
GRIDC = "#16181B"
INK = "#FFFFFF"
SOFT = "#BBBBBB"
DIM = "#5A5F66"
GOLD = "#FFD54F"     # palabra actual del karaoke / enfasis
YELLOW = "#FFFF66"
RED = "#FC6255"
TEAL = "#5CD0B3"
BLUE = "#58C4DD"
GREEN = "#83C167"
VIOLET = "#9A72AC"
ORANGE = "#FF862F"
STEEL = "#A6B8C4"
GRID_ON = False      # sin grilla de cuaderno: fondo negro limpio
SANS = "IBM Plex Sans"
MONO = "IBM Plex Mono"

config.background_color = BG

_TPL = TexTemplate()
_TPL.add_to_preamble(r"""
\newcommand{\R}{\mathbb{R}}
\newcommand{\Q}{\mathbb{Q}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\Ss}{S^{*}}
\newcommand{\Si}{S_{*}}
\newcommand{\fl}[1]{\lfloor #1\rfloor}
\newcommand{\eps}{\varepsilon}
""")
MathTex.set_default(tex_template=_TPL)
Tex.set_default(tex_template=_TPL)

CAP_Y = -3.3
CAP_SIZE = 27
CAP_MAXC = 64
BOARD_BOTTOM = -2.42
BOARD_TOP = 3.05


def T(text, size=28, color=INK, font=SANS, weight=NORMAL, **kw):
    # Siempre se genera a 48 y se escala (evita espaciado roto de Pango).
    t = Text(text, font=font, font_size=48, color=color, weight=weight,
             disable_ligatures=True, **kw)
    t.scale(size / 48)
    return t


def M(*tex, size=40, color=INK, **kw):
    return MathTex(*tex, font_size=size, color=color, **kw)


def _segs(s):
    """Parte 'texto $mat$ **enfasis**' en (tipo, texto, enfasis, pegado_a_izq)."""
    out, buf, math, emph, i = [], "", False, False, 0
    while i < len(s):
        if s[i] == "$":
            if buf:
                out.append(("m" if math else "t", buf, emph))
            buf, math = "", not math
            i += 1
        elif not math and s.startswith("**", i):
            if buf:
                out.append(("t", buf, emph))
            buf, emph = "", not emph
            i += 2
        else:
            buf += s[i]
            i += 1
    if buf:
        out.append(("m" if math else "t", buf, emph))
    return out


def L(s, size=26, color=INK, weight=NORMAL, msize=None, emph_color=YELLOW):
    """Linea mixta: texto IBM Plex con $matematica$ y **enfasis** (amarillo).
    Se alinea contra un '|' invisible para que todo comparta linea base."""
    msize = msize or size * 1.36
    out = VGroup()
    x, ref_y, prev_space, extra = 0.0, None, False, 0
    for kind, tr, emph in _segs(s):
        if not tr.strip():
            prev_space = True
            extra += max(0, len(tr) - 1)
            continue
        lead = len(tr) - len(tr.lstrip(" ")) if kind == "t" else 0
        extra += max(0, lead - 1)
        col = emph_color if emph else color
        k = size / 26
        if kind == "m":
            mob = M(tr, size=msize, color=col)
            if ref_y is None:
                ref_y = 0.0
            mob.move_to([0, ref_y + 0.015 * k, 0])
            glued = not prev_space and tr[:1] not in "\\"
            gap = 0.1 * k
        else:
            t = T("|" + tr.strip(), size, col, SANS, BOLD if emph else weight)
            strut, mob = t[0], VGroup(*t[1:])
            if ref_y is None:
                ref_y = strut.get_center()[1]
            mob.shift(UP * (ref_y - strut.get_center()[1]))
            glued = not tr[:1].isspace() and not prev_space
            gap = (0.035 if glued else 0.1) * k
        gap += 0.13 * k * extra
        if not len(out):
            gap = 0.0
        mob.shift(RIGHT * (x + gap - mob.get_left()[0]))
        x = mob.get_right()[0]
        prev_space = tr[-1:].isspace()
        extra = max(0, len(tr) - len(tr.rstrip(" ")) - 1) if kind == "t" else 0
        out.add(mob)
    return out


def Lines(*lines, size=26, color=INK, buff=0.16):
    g = VGroup(*[L(s, size, color) if isinstance(s, str) else s for s in lines])
    return g.arrange(DOWN, aligned_edge=LEFT, buff=buff)


# ---------------- Subtitulos karaoke ----------------
def _tokens(text):
    out, emph = [], False
    for raw in text.split():
        w = raw
        if w.startswith("**"):
            emph = True
            w = w[2:]
        closing = "**" in w
        w = w.replace("**", "")
        if w:
            out.append((w, emph))
        if closing:
            emph = False
    return out


def _wrap(tokens, maxc=CAP_MAXC):
    lines, cur, n = [], [], 0
    for w, e in tokens:
        add = len(w) + (1 if cur else 0)
        if cur and n + add > maxc:
            lines.append(cur)
            cur, n = [], 0
            add = len(w)
        cur.append((w, e))
        n += add
    if cur:
        lines.append(cur)
    return lines


def _word_time(w):
    t = 1.0 / WPS + 0.022 * max(0, len(w) - 5)
    if w[-1] in ".:?!":
        t += 0.22
    elif w[-1] in ",;":
        t += 0.1
    return t * PACE


class Karaoke(Animation):
    """Una sola animacion por pagina de subtitulo (barato de renderizar)."""

    def __init__(self, group, words, colors, starts, ends, run_time, **kw):
        self.words, self.fcol = words, colors
        self.starts, self.ends = starts, ends
        self.state = [None] * len(words)
        super().__init__(group, run_time=run_time, rate_func=linear, **kw)

    def interpolate_mobject(self, alpha):
        t = alpha * self.run_time
        for i, (w, c, s, e) in enumerate(zip(self.words, self.fcol, self.starts, self.ends)):
            col = DIM if t < s else (GOLD if t < e else c)
            if self.state[i] != col:
                w.set_color(col)
                self.state[i] = col


def build_caption(lines):
    rows, words, colors = VGroup(), [], []
    for line in lines:
        s = " ".join(w for w, _ in line)
        t = T(s, CAP_SIZE, DIM)
        nglyph = sum(len(w) for w, _ in line)
        nsub = len(t.submobjects)
        if nsub in (nglyph, len(s)):
            step = 1 if (nsub == len(s) and nsub != nglyph) else 0
            i = 0
            for w, e in line:
                words.append(VGroup(*t.submobjects[i:i + len(w)]))
                colors.append(GOLD if e else INK)
                i += len(w) + step
        else:
            words.append(t)
            colors.append(INK)
        rows.add(t)
    rows.arrange(DOWN, buff=0.13)
    if rows.width > 13.2:
        rows.scale_to_fit_width(13.2)
    rows.move_to([0, CAP_Y, 0])
    return rows, words, colors


# ---------------- Escena base ----------------
class GBase(Scene):
    CH_NUM = ""
    CH_TITLE = ""
    VIDEO_TAG = "CÁLCULO 1 · 1er PARCIAL"

    def setup_frame(self, header=True):
        self._cap = None
        self.board = VGroup()
        grid = VGroup()
        if GRID_ON:
            for x in np.arange(-7.0, 7.01, 0.5):
                grid.add(Line([x, -4.2, 0], [x, 4.2, 0], stroke_width=1, color=GRIDC))
            for y in np.arange(-4.0, 4.01, 0.5):
                grid.add(Line([-7.3, y, 0], [7.3, y, 0], stroke_width=1, color=GRIDC))
        # banda negra (tapa lo que baje hasta los subtitulos), sin borde: limpio
        band = Rectangle(width=14.6, height=1.42, stroke_width=0).set_fill(BG, 0.9)
        band.move_to([0, CAP_Y, 0])
        self.add(grid, band)
        self.persist = [grid, band, VGroup()]
        if header:
            self.make_header()

    def make_header(self):
        num = T(self.CH_NUM, 17, BLUE, MONO, BOLD)
        tit = T(self.CH_TITLE.upper(), 17, DIM, MONO)
        h = VGroup(num, tit).arrange(RIGHT, buff=0.22)
        h.to_corner(UL, buff=0.3)
        right = T(self.VIDEO_TAG, 15, DIM, MONO).to_corner(UR, buff=0.3)
        right.match_y(h)
        self.header = VGroup(h, right)
        self.add(self.header)
        self.persist.append(self.header)

    def title_card(self, title, subtitle="", prob=None):
        n = T(f"CAPÍTULO {self.CH_NUM}", 24, BLUE, MONO, BOLD)
        t = T(title, 60, INK, SANS, BOLD)
        if t.width > 12.5:
            t.scale_to_fit_width(12.5)
        rule = Line(LEFT, RIGHT, stroke_width=2, color=BLUE).set_width(t.width)
        parts = [n, t, rule]
        if subtitle:
            parts.append(T(subtitle, 28, SOFT))
        if prob:
            parts.append(prob_chip(*prob))
        g = VGroup(*parts).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        self.play(FadeIn(n, shift=DOWN * 0.2), Write(t), GrowFromCenter(rule),
                  *[FadeIn(p) for p in parts[3:]], run_time=1.6 * PACE)
        self.wait(0.9 * PACE)
        self.play(FadeOut(g), run_time=0.6 * PACE)
        self.make_header()

    def w(self, t=1.0):
        self.wait(t * PACE)

    # ---------- subtitulos ----------
    def say(self, text, *anims, hold=0.5, min_t=0.0, run_time=None, rate_func=None):
        """run_time/rate_func se aplican a las animaciones (no al subtitulo)."""
        if run_time is not None or rate_func is not None:
            anims = [prepare_animation(a) for a in anims]
            for a in anims:
                if run_time is not None:
                    a.run_time = run_time * PACE
                if rate_func is not None:
                    a.rate_func = rate_func
            if run_time is not None:
                min_t = max(min_t, run_time)
        lines = _wrap(_tokens(text))
        pages = [lines[i:i + 2] for i in range(0, len(lines), 2)]
        for pi, page in enumerate(pages):
            grp, words, colors = build_caption(page)
            offset = 0.22 if self._cap is not None else 0.0
            t = offset
            starts, ends = [], []
            flat = [w for line in page for w in line]
            if len(words) == len(flat):
                for (w, _e) in flat:
                    d = _word_time(w)
                    starts.append(t)
                    ends.append(t + d)
                    t += d
            else:
                d = sum(_word_time(w) for w, _ in flat) / max(1, len(words))
                for _ in words:
                    starts.append(t)
                    ends.append(t + d)
                    t += d
            rt = t + hold * PACE
            if pi == 0:
                rt = max(rt, min_t * PACE)
            extra = []
            if self._cap is not None:
                extra.append(FadeOut(self._cap, run_time=0.2))
            if pi == 0:
                extra += list(anims)
            self.play(Karaoke(grp, words, colors, starts, ends, rt), *extra)
            self._cap = grp

    def uncap(self):
        if self._cap is not None:
            self.play(FadeOut(self._cap), run_time=0.3)
            self._cap = None

    # ---------- snapshots de control (M2_SNAP=1) ----------
    def snap(self):
        if not SNAP:
            return
        from PIL import Image
        self._sn = getattr(self, "_sn", 0) + 1
        self.renderer.update_frame(self)
        os.makedirs("snaps", exist_ok=True)
        Image.fromarray(self.renderer.get_frame()).convert("RGB").save(
            f"snaps/{type(self).__name__}_{self._sn:02d}.png")

    # ---------- limpieza ----------
    def wipe(self, *keep, rt=0.6):
        self.snap()
        keep_ids = {id(x) for m in list(self.persist) + list(keep) for x in m.get_family()}
        if self._cap is not None:
            keep_ids.add(id(self._cap))
        gone = [m for m in self.mobjects if id(m) not in keep_ids]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=rt * PACE)
        self.board = VGroup()

    def end_scene(self):
        self.snap()
        self.uncap()
        gone = [m for m in self.mobjects if m not in self.persist[:3]]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=0.7)
        self.wait(0.3)

    # ---------- pizarra con auto-scroll ----------
    def board_start(self, left=-6.55, top=BOARD_TOP, maxw=13.0):
        self.board = VGroup()
        self.b_left, self.b_top, self.b_maxw = left, top, maxw

    def push(self, mob, text=None, *extra, gap=0.3, indent=0.0, anim=None, hold=0.5, min_t=0.0):
        if mob.width > self.b_maxw - indent:
            mob.scale_to_fit_width(self.b_maxw - indent)
        if len(self.board) == 0:
            mob.move_to([0, 0, 0])
            mob.align_to([self.b_left + indent, 0, 0], LEFT)
            mob.align_to([0, self.b_top, 0], UP)
        else:
            mob.next_to(self.board[-1], DOWN, buff=gap)
            mob.align_to([self.b_left + indent, 0, 0], LEFT)
        anims = []
        low = mob.get_bottom()[1]
        if low < BOARD_BOTTOM:
            dy = BOARD_BOTTOM - low + 0.05
            mob.shift(UP * dy)
            keep = VGroup()
            for b in self.board:
                if b.get_top()[1] + dy > self.b_top + 0.15:
                    anims.append(FadeOut(b, shift=UP * dy))
                else:
                    anims.append(b.animate.shift(UP * dy))
                    keep.add(b)
            self.board = keep
        a = anim if anim is not None else Write(mob, run_time=min(2.0, 0.8 + 0.02 * len(mob.submobjects)) * PACE)
        self.board.add(mob)
        if text:
            if anims:
                self.play(*anims, run_time=0.5 * PACE)
            self.say(text, a, *extra, hold=hold, min_t=min_t)
        else:
            self.play(*anims, a, *extra)
        return mob

    # ---------- cajas ----------
    def stamp(self, content, label="RESULTADO", color=RED, buff=0.3, size=26):
        if isinstance(content, (list, tuple)):
            content = Lines(*content, size=size)
        if content.width > 12.6:
            content.scale_to_fit_width(12.6)
        r1 = SurroundingRectangle(content, buff=buff, color=color, stroke_width=2.6)
        r2 = SurroundingRectangle(content, buff=buff + 0.09, color=color, stroke_width=1.2)
        r2.set_fill(BG, 0.96)
        lab = T(label, 15, color, MONO, BOLD)
        lbg = SurroundingRectangle(lab, buff=0.06, stroke_width=0).set_fill(BG, 1)
        L = VGroup(lbg, lab).move_to(r2.get_top()).align_to(r2, LEFT).shift(RIGHT * 0.25)
        return VGroup(r2, r1, content, L)

    def show_stamp(self, s):
        return [FadeIn(s[0]), FadeIn(s[1]), FadeIn(s[3]), FadeIn(s[2])]

    def tip(self, lines, label="ANALOGÍA", color=TEAL, size=23, width=None):
        txt = VGroup(*[L(l, size, INK) if isinstance(l, str) else l for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lab = T(label, 15, color, MONO, BOLD)
        body = VGroup(lab, txt).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        wdt = width or body.width + 0.6
        if body.width > wdt - 0.5:
            body.scale_to_fit_width(wdt - 0.5)
        bg = Rectangle(width=wdt, height=body.height + 0.4, stroke_width=0).set_fill(PANEL, 0.97)
        body.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.3)
        bar = Line(bg.get_corner(UL), bg.get_corner(DL), color=color, stroke_width=7)
        return VGroup(bg, bar, body)

    def hl(self, mob, color=GOLD, buff=0.07):
        return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=2.5)

    def pausa(self, ejercicio, text, secs=4.0):
        """Caja naranja punteada: 'pausá e intentalo'. ejercicio = mobject."""
        tag = T("PAUSÁ E INTENTALO", 16, ORANGE, MONO, BOLD)
        body = VGroup(tag, ejercicio).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        if body.width > 12.4:
            body.scale_to_fit_width(12.4)
        fr = DashedVMobject(SurroundingRectangle(body, buff=0.3, color=ORANGE, stroke_width=2),
                            num_dashes=70)
        self.wipe()
        g = VGroup(fr, body).move_to([0, 0, 0]).align_to([0, 2.9, 0], UP)
        bar = Line(fr.get_corner(DL) + DOWN * 0.2, fr.get_corner(DR) + DOWN * 0.2,
                   color=ORANGE, stroke_width=4)
        self.say(text, FadeIn(g, shift=UP * 0.2), hold=0.2)
        self.add(bar)
        self.play(ShrinkToCenter(bar), run_time=secs * PACE, rate_func=linear)
        self.remove(bar)
        return g

    def check(self, text_ok="CHEQUEO: DERIVANDO VUELVE AL INTEGRANDO ✓"):
        t = T(text_ok, 17, GREEN, MONO, BOLD)
        box = SurroundingRectangle(t, buff=0.12, color=GREEN, stroke_width=2)
        return VGroup(box, t)

    def bullets(self, items, size=25, font=MONO, color=INK, num_color=RED, buff=0.25, numlen=1):
        g = VGroup(*[T(s, size, color, font) for s in items]).arrange(DOWN, aligned_edge=LEFT, buff=buff)
        for m in g:
            m[:numlen].set_color(num_color)
        return g

    def right_tip(self, tip, y):
        return tip.to_edge(RIGHT, buff=0.3).set_y(y)


def node(label, sub, color, w=2.2):
    t = T(label, 26, color, MONO, BOLD)
    s = T(sub, 18, SOFT)
    g = VGroup(t, s).arrange(DOWN, buff=0.1)
    r = RoundedRectangle(width=max(w, g.width + 0.5), height=1.25, corner_radius=0.15,
                         stroke_color=color, stroke_width=2.5).set_fill(PANEL, 1)
    g.move_to(r)
    return VGroup(r, g)


def parts_table(y, yp, gp, g, size=36):
    """Tabla de 4 lineas de Diego:  y | y'  /  g' | g"""
    cells = [M(r"y=" + y, size=size), M(r"y'=" + yp, size=size),
             M(r"g'=" + gp, size=size), M(r"g=" + g, size=size)]
    for c in cells[:2]:
        c.set_color(BLUE)
    for c in cells[2:]:
        c.set_color(GREEN)
    colw = max(c.width for c in cells) + 0.5
    rowh = max(c.height for c in cells) + 0.35
    for i, c in enumerate(cells):
        r, k = divmod(i, 2)
        c.move_to([k * colw, -r * rowh, 0])
    body = VGroup(*cells)
    frame = SurroundingRectangle(body, buff=0.25, color=SOFT, stroke_width=1.5).set_fill(PANEL, 0.96)
    vline = Line(frame.get_top(), frame.get_bottom(), color=SOFT, stroke_width=1)
    vline.set_x((cells[0].get_right()[0] + cells[1].get_left()[0]) / 2)
    hline = Line(frame.get_left(), frame.get_right(), color=SOFT, stroke_width=1)
    hline.set_y((cells[0].get_bottom()[1] + cells[2].get_top()[1]) / 2)
    l1 = T("SE DERIVA", 13, BLUE, MONO, BOLD).next_to(frame, LEFT, buff=0.12).match_y(cells[0])
    l2 = T("SE INTEGRA", 13, GREEN, MONO, BOLD).next_to(frame, LEFT, buff=0.12).match_y(cells[2])
    return VGroup(frame, vline, hline, body, l1, l2)


# ---------------- Cajas del libro ----------------
PROB_COLORS = {"MUY ALTA": RED, "ALTA": ORANGE, "MEDIA": TEAL, "BAJA": SOFT, "TRANSVERSAL": BLUE}


def prob_chip(nivel, nota=""):
    c = PROB_COLORS.get(nivel, RED)
    t = T(f"PROBABILIDAD: {nivel}", 17, BG, MONO, BOLD)
    r = SurroundingRectangle(t, buff=0.1, stroke_width=0).set_fill(c, 1)
    g = VGroup(r, t)
    if nota:
        g = VGroup(g, T(nota, 18, SOFT, MONO)).arrange(DOWN, buff=0.14)
    return g


def _side_box(lines, label, color, size=23, width=None, fill=0.10):
    txt = VGroup(*[L(l, size, INK) if isinstance(l, str) else l for l in lines])
    txt.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
    lab = T(label, 15, color, MONO, BOLD)
    body = VGroup(lab, txt).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    wdt = width or body.width + 0.6
    if body.width > wdt - 0.5:
        body.scale_to_fit_width(wdt - 0.5)
    bg = Rectangle(width=wdt, height=body.height + 0.4, stroke_width=0)
    bg.set_fill(interpolate_color(ManimColor(BG), ManimColor(color), fill), 1)
    body.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.3)
    bar = Line(bg.get_corner(UL), bg.get_corner(DL), color=color, stroke_width=6)
    return VGroup(bg, bar, body)


def memo(lines, label="AYUDA-MEMORIA", **kw):
    return _side_box(lines, label, GREEN, **kw)


def trampa(lines, label="", **kw):
    return _side_box(lines, "TRAMPA" + (" · " + label if label else ""), RED, **kw)


def intu(lines, label="LA IMAGEN", **kw):
    return _side_box(lines, label, TEAL, **kw)


def metodo(pasos, label, size=23, width=None):
    rows = VGroup()
    for i, p in enumerate(pasos, 1):
        n = T(f"{i}", size, STEEL, MONO, BOLD)
        rows.add(VGroup(n, L(p, size, INK)).arrange(RIGHT, buff=0.25, aligned_edge=UP))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    return _side_box([rows], "MÉTODO · " + label, STEEL, size=size, width=width, fill=0.06)


def enun(fuente, lines, size=25, width=None):
    """Enunciado de parcial / practico: etiqueta mono arriba + recuadro gris fino."""
    tag = T(fuente, 15, BG, MONO, BOLD)
    tr = SurroundingRectangle(tag, buff=0.08, stroke_width=0).set_fill(SOFT, 1)
    tagg = VGroup(tr, tag)
    txt = VGroup(*[L(l, size, INK) if isinstance(l, str) else l for l in lines])
    txt.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    wdt = width or min(txt.width + 0.6, 13.2)
    if txt.width > wdt - 0.5:
        txt.scale_to_fit_width(wdt - 0.5)
    fr = Rectangle(width=wdt, height=txt.height + 0.5, color=DIM, stroke_width=1.4)
    txt.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3 + DOWN * 0.04)
    tagg.move_to(fr.get_corner(UL), aligned_edge=LEFT).shift(RIGHT * 0.25)
    return VGroup(fr, txt, tagg)


def resp(content, size=28):
    if isinstance(content, str):
        content = L(content, size, INK, BOLD)
    lab = T("RESPUESTA", 15, GREEN, MONO, BOLD)
    g = VGroup(lab, content).arrange(RIGHT, buff=0.3)
    fr = SurroundingRectangle(g, buff=0.18, color=GREEN, stroke_width=2)
    fr.set_fill(interpolate_color(ManimColor(BG), ManimColor(GREEN), 0.12), 1)
    return VGroup(fr, g)


def paso(n, txt, size=17):
    return T(f"PASO {n} — {txt.upper()}", size, RED, MONO, BOLD)


def step(n, txt, body, size=17, buff=0.12):
    """Rotulo PASO n + cuerpo (mobject o linea mixta) debajo."""
    if isinstance(body, str):
        body = L(body, 26)
    return VGroup(paso(n, txt, size), body).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def tabla(filas, size=24, h=0.55, head_color=BLUE, pad=0.45):
    """filas[0] = encabezado. Celdas con texto o $math$. Devuelve VGroup con .rows"""
    cells = [[L(c, size, head_color if i == 0 else INK, BOLD if i == 0 else NORMAL)
              for c in f] for i, f in enumerate(filas)]
    ncol = len(filas[0])
    ws = [max(cells[i][j].width for i in range(len(cells))) + pad for j in range(ncol)]
    rows = VGroup()
    for i, f in enumerate(cells):
        row = VGroup()
        x = 0.0
        for j, c in enumerate(f):
            c.move_to([x + ws[j] / 2, -i * h, 0])
            row.add(c)
            x += ws[j]
        rows.add(row)
    W = sum(ws)
    top = Line([0, h / 2, 0], [W, h / 2, 0], stroke_width=1.6, color=SOFT)
    mid = Line([0, -h / 2, 0], [W, -h / 2, 0], stroke_width=1, color=DIM)
    bot = Line([0, -(len(cells) - 0.5) * h, 0], [W, -(len(cells) - 0.5) * h, 0], stroke_width=1.6, color=SOFT)
    g = VGroup(VGroup(top, mid, bot), rows)
    g.rows = rows
    g.rules = VGroup(top, mid, bot)
    return g


def ejes(xr, yr, w, h, **kw):
    return Axes(x_range=xr, y_range=yr, x_length=w, y_length=h,
                axis_config={"color": SOFT, "stroke_width": 2, "tip_length": 0.16,
                             "tip_width": 0.14, "tick_size": 0.05}, **kw)


def xlabels(ax, vals, texts=None, size=20, color=SOFT, buff=0.12):
    g = VGroup()
    for i, v in enumerate(vals):
        s = texts[i] if texts else f"{v:g}".replace(".", ",")
        g.add(M(s, size=size * 1.35, color=color).next_to(ax.x_axis.n2p(v), DOWN, buff=buff))
    return g


def ylabels(ax, vals, texts=None, size=20, color=SOFT, buff=0.12):
    g = VGroup()
    for i, v in enumerate(vals):
        s = texts[i] if texts else f"{v:g}".replace(".", ",")
        g.add(M(s, size=size * 1.35, color=color).next_to(ax.y_axis.n2p(v), LEFT, buff=buff))
    return g


def debajo(mob, ref, buff=0.3, piso=-2.45):
    """Pone mob debajo de ref; si se mete en los subtitulos, lo achica para que entre."""
    mob.next_to(ref, DOWN, buff=buff)
    if mob.get_bottom()[1] < piso:
        alto = ref.get_bottom()[1] - buff - piso
        if alto > 0.3:
            mob.scale_to_fit_height(min(mob.height, alto))
        mob.next_to(ref, DOWN, buff=buff)
    return mob


class Num(DecimalNumber):
    """DecimalNumber con coma decimal (1,25 en vez de 1.25)."""

    def _get_num_string(self, number):
        return super()._get_num_string(number).replace(".", ",")


# ---------------- Slider de parametro (estilo panel de Houdini) ----------------
class Slider(VGroup):
    """Perilla que sigue a un ValueTracker: el parametro se ve moverse en vivo.
    Slider("ε", tracker, 0, 1).move_to(...)  ->  self.add(slider) y animar el tracker."""

    def __init__(self, nombre, tracker, vmin, vmax, color=YELLOW, width=3.4, decimals=2, size=26, **kw):
        super().__init__(**kw)
        self.tracker, self.vmin, self.vmax = tracker, vmin, vmax
        lab = L(nombre, size, color) if "$" in nombre else T(nombre, size, color, SANS, BOLD)
        track = Line(ORIGIN, RIGHT * width, color=DIM, stroke_width=5)
        track.next_to(lab, RIGHT, buff=0.3)
        num = Num(tracker.get_value(), num_decimal_places=decimals, font_size=size * 1.25, color=color)
        num.next_to(track, RIGHT, buff=0.3)
        self.track, self.lab = track, lab

        def pos():
            a = (tracker.get_value() - vmin) / (vmax - vmin)
            return track.point_from_proportion(float(np.clip(a, 0, 1)))

        fill = always_redraw(lambda: Line(track.get_start(), pos(), color=color, stroke_width=5))
        knob = always_redraw(lambda: Dot(pos(), radius=0.1, color=color).set_stroke(BG, 2))
        num.add_updater(lambda m: m.set_value(tracker.get_value()).next_to(track, RIGHT, buff=0.3))
        self.add(lab, track, fill, knob, num)
