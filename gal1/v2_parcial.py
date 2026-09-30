"""
VIDEO 2 - LOS EJERCICIOS DEL PARCIAL  (un ejercicio real por tipo, de mayor a menor probabilidad)
  Sistema con parametro (2S 2023) · dos parametros (2S 2022) · rango (1S 2024, 2S 2024)
  Inversa (1S 2025) · det por propiedades (2S 2024, 1S 2025) · det de expresiones (1S 2023)
  Inversa desde una ecuacion (1S 2025, 2S 2024) · complejos · V/F relampago · cierre
Todas las cuentas estan en gal1_teoria/verify.py (sympy).
"""
from gal_base import *

SCENE_ORDER = ["V2_00_Intro", "V2_01_SistemaParam", "V2_02_DosParam", "V2_03_Rango",
               "V2_04_Inversa", "V2_05_DetPropiedades", "V2_06_DetExpresion",
               "V2_07_InversaEcuacion", "V2_08_Complejos", "V2_09_VF", "V2_10_Cierre"]


class V2(GBase, MatScene):
    VIDEO_TAG = "VIDEO 2 · EJERCICIOS DE PARCIAL"


def top(mob, y=2.75):
    return mob.move_to([0, 0, 0]).align_to([0, y, 0], UP)


# =====================================================================
class V2_00_Intro(V2):
    def construct(self):
        self.setup_frame(header=False)
        t1 = T("GAL 1 · IMERL · FING · 2S 2026", 22, SOFT, MONO)
        t2 = T("Los ejercicios del parcial", 64, INK, SANS, BOLD)
        t3 = T("Un ejercicio real por tipo, de mayor a menor probabilidad", 32, BLUE, SANS, BOLD)
        g = VGroup(t1, t2, t3).arrange(DOWN, buff=0.3).shift(UP * 1.7)
        self.play(FadeIn(t1, shift=DOWN * 0.2), Write(t2), FadeIn(t3), run_time=1.3)
        self.say("Video 2: los ejercicios. Cada uno es **de un parcial real**, resuelto como lo escribirías vos.")
        filas = [("MUY ALTA", "Sistema con parámetro · Rango · Inversa · Determinante por propiedades"),
                 ("ALTA", "Determinante de expresiones · Inversa desde una ecuación · Complejos"),
                 ("MEDIA", "Verdadero/falso relámpago · Problema modelado")]
        rows = VGroup(*[VGroup(prob_chip(p), T(t, 23, INK)).arrange(RIGHT, buff=0.35) for p, t in filas])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.scale_to_fit_width(min(rows.width, 12.6)).move_to([0, -0.9, 0])
        self.say("Van en orden de probabilidad. Los cuatro primeros tipos cayeron en **los cuatro parciales más recientes**.",
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.3, run_time=1.8))
        self.say("El ritmo es rápido a propósito. Cuando aparezca la caja naranja, **pausá** e intentá el primer paso. Lo que ya sabés, dejalo correr.")
        self.end_scene()


# =====================================================================
class V2_01_SistemaParam(V2):
    CH_NUM = "R1"
    CH_TITLE = "Sistema con parámetro · 2S 2023"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Sistema con parámetro", "2S 2023 · preguntas 2 y 3", prob=("MUY ALTA", "11 de 14 parciales"))
        e = enun("2S 2023 · PREGUNTAS 2 Y 3", [
            "Discutir según $a\\in\\mathbb{R}$ y resolver para $a=3$:",
            M(r"\left\{\begin{array}{l}x+ay+z=1\\x+2(a-1)y+2z=4\\(a-2)y+az=5\end{array}\right.", size=36)])
        self.pausa(e, "Pausá: escribí la matriz ampliada y hacé el primer paso de escalerización.")
        self.wipe()
        m = Mat([[1, "a", 1, 1], [1, "2a-2", 2, 4], [0, "a-2", "a", 5]], bar=3, size=38).move_to([-2.2, 1.0, 0])
        self.say("La ampliada. Primera regla: **no dividir** por nada que tenga a.", FadeIn(m))
        m = self.rowop(m, [[1, "a", 1, 1], [0, "a-2", 1, 3], [0, "a-2", "a", 5]], r"F_2-F_1",
                       "Fila 2 menos fila 1.", changed=[1], bar=3, size=38)
        m = self.rowop(m, [[1, "a", 1, 1], [0, "a-2", 1, 3], [0, 0, "a-1", 2]], r"F_3-F_2",
                       "Fila 3 menos fila 2: ya está escalonada.", changed=[2], bar=3, size=38)
        piv = VGroup(*[SurroundingRectangle(m.get_entries()[k], color=RED, buff=0.08) for k in (0, 5, 10)])
        note = VGroup(L("pivotes: $1,\\ a-2,\\ a-1$", 28), L("críticos: $a=2$, $a=1$", 28, YELLOW),
                      L("chequeo: $\\det A=(a-1)(a-2)$ ✓", 24, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        note.move_to([3.9, 1.0, 0])
        self.say("Los pivotes con parámetro son a − 2 y a − 1: los **valores críticos** son 2 y 1. Chequeo con el determinante: da (a − 1)(a − 2). Coincide.",
                 Create(piv), FadeIn(note))
        self.board_start(left=-6.5, top=-0.35, maxw=13)
        self.push(L("$a\\neq1,2$: \\ tres pivotes $\\Rightarrow$ **SCD**", 28), "Fuera de los críticos, tres pivotes: compatible determinado.")
        self.push(L("$a=1$: \\ última fila $(0\\ 0\\ 0\\,|\\,2)$ $\\Rightarrow$ $0=2$ \\ **SI**", 28), "Con a = 1, la última fila dice cero igual a dos: incompatible.")
        self.wipe()

        m2 = Mat([[1, 2, 1, 1], [0, 0, 1, 3], [0, 0, 1, 2]], bar=3, size=40).move_to([-2.5, 1.0, 0])
        t2 = T("a = 2", 30, RED, MONO, BOLD).next_to(m2, UP, buff=0.3)
        self.say("Ahora **la trampa**. Con a = 2 sustituyo el número... y se cayó el segundo pivote: la matriz **ya no está escalonada**.",
                 FadeIn(t2), FadeIn(m2), focus=True)
        m2 = self.rowop(m2, [[1, 2, 1, 1], [0, 0, 1, 3], [0, 0, 0, -1]], r"F_3-F_2",
                        "Un paso más: fila 3 menos fila 2 da cero igual a menos uno.", changed=[2], bar=3, size=40)
        r = L("$a=2$: \\ **SI** (dos ecuaciones dicen $z=3$ y $z=2$)", 28).move_to([0, -1.0, 0])
        self.say("Incompatible también. Quien se quedó con la matriz genérica, ve (0, 0, 1 | 2) y dice que es compatible. **Error**.",
                 FadeIn(r), focus=True)
        self.wipe()

        self.board_start(top=2.7)
        self.push(L("$a=3$: \\ $\\left\\{\\begin{array}{l}x+3y+z=1\\\\y+z=3\\\\2z=2\\end{array}\\right.$", 30),
                  "Para a = 3 uso la escalonada: de abajo hacia arriba.")
        self.push(L("$z=1,\\quad y=2,\\quad x=1-6-1=-6$", 30), "z = 1, y = 2, y x da −6.")
        rr = resp("Incompatible para $a=1$ y $a=2$; SCD para los demás. \\ $a=3$: $S=\\{(-6,2,1)\\}$", size=26)
        self.push(rr, "Opción B, y en la pregunta 3, la solución (−6, 2, 1).", anim=FadeIn(rr))
        self.end_scene()


# =====================================================================
class V2_02_DosParam(V2):
    CH_NUM = "R2"
    CH_TITLE = "Dos parámetros · desarrollo 2S 2022"

    def construct(self):
        self.setup_frame()
        e = enun("2S 2022 · DESARROLLO", [
            "$\\alpha x+y+z=\\beta,\\quad x+\\alpha y+z=\\beta,\\quad x+y+\\alpha z=\\beta$.",
            "¿Para qué $\\alpha,\\beta$ es SI, SCI y SCD? Dar las soluciones."])
        self.pausa(e, "Salió como desarrollo, y el mismo sistema salió en 2008. Pausá y pensá qué fila poner arriba.")
        self.wipe()
        m = Mat([[1, 1, "\\alpha", "\\beta"], [1, "\\alpha", 1, "\\beta"], ["\\alpha", 1, 1, "\\beta"]], bar=3, size=38).move_to([-2.0, 1.4, 0])
        self.say("Truco: pongo arriba la fila que empieza con 1, así el pivote es un número.", FadeIn(m))
        m = self.rowop(m, [[1, 1, "\\alpha", "\\beta"], [0, "\\alpha-1", "1-\\alpha", 0], [0, "1-\\alpha", "1-\\alpha^2", "\\beta(1-\\alpha)"]],
                       r"F_2-F_1,\ F_3-\alpha F_1", "Hago ceros en la primera columna. Restar alfa veces la fila 1 es legal: no multiplico la fila que cambia.",
                       changed=[1, 2], bar=3, size=36)
        m = self.rowop(m, [[1, 1, "\\alpha", "\\beta"], [0, "\\alpha-1", "1-\\alpha", 0], [0, 0, "(1-\\alpha)(2+\\alpha)", "\\beta(1-\\alpha)"]],
                       r"F_3+F_2", "Sumo la fila 2 a la 3 y factorizo: (1 − α)(2 + α).", changed=[2], bar=3, size=36)
        self.board_start(left=-6.5, top=-0.1, maxw=13)
        self.push(L("$\\alpha\\neq1,-2$: **SCD**, \\ $x=y=z=\\frac{\\beta}{\\alpha+2}$", 28), "Alfa distinto de 1 y de −2: determinado, con x = y = z = β sobre α + 2.")
        self.push(L("$\\alpha=1$: queda solo $x+y+z=\\beta$ \\ $\\Rightarrow$ **SCI** (2 parámetros), para todo $\\beta$", 28),
                  "Alfa = 1: las tres ecuaciones son la misma. Indeterminado para cualquier beta.")
        self.push(L("$\\alpha=-2$: última fila $(0\\ 0\\ 0\\,|\\,3\\beta)$: \\ $\\beta\\neq0$ **SI**; \\ $\\beta=0$ **SCI**, $\\{(t,t,t)\\}$", 28, YELLOW),
                  "Alfa = −2: la última fila dice cero igual a tres beta. Si beta no es cero, incompatible. Si es cero, indeterminado, con soluciones (t, t, t).",
                  focus=True)
        self.end_scene()


# =====================================================================
class V2_03_Rango(V2):
    CH_NUM = "R3"
    CH_TITLE = "Rango con parámetro · 1S 2024 y 2S 2024"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Rango con parámetro", "1S 2024 · 2S 2024", prob=("MUY ALTA", "en los 3 últimos parciales"))
        e = enun("1S 2024 · PREGUNTA 1", [
            VGroup(L("$A=$", 30), Mat([["a-1", 3, "a+1"], [-1, 1, 1], ["a", 2, -1]], size=32, h_buff=1.1)).arrange(RIGHT, buff=0.15),
            "¿Para cuántos $a$ el rango es 3, y para cuántos es 2?"])
        self.pausa(e, "Pausá: ¿qué fila conviene subir?")
        self.wipe()
        m = Mat([[-1, 1, 1], ["a-1", 3, "a+1"], ["a", 2, -1]], size=38, h_buff=1.2).move_to([-2.2, 1.2, 0])
        self.say("Subo la fila (−1, 1, 1): tiene pivote numérico.", FadeIn(m))
        m = self.rowop(m, [[-1, 1, 1], [0, "a+2", "2a"], [0, "a+2", "a-1"]], r"F_2+(a-1)F_1,\ F_3+aF_1",
                       "Le sumo a las otras filas múltiplos de la primera. Eso siempre es legal.", changed=[1, 2], size=38, h_buff=1.2)
        m = self.rowop(m, [[-1, 1, 1], [0, "a+2", "2a"], [0, 0, "-(a+1)"]], r"F_3-F_2",
                       "Y resto: queda el pivote menos (a + 1).", changed=[2], size=38, h_buff=1.2)
        self.board_start(left=-6.5, top=-0.3, maxw=13)
        self.push(L("$a\\neq-1,-2$: \\ $\\rg=3$", 28), "Fuera de −1 y −2, rango 3.")
        self.push(L("$a=-1$: fila 3 nula $\\Rightarrow\\rg=2$. \\quad $a=-2$: filas $(0,0,-4)$ y $(0,0,1)$ proporcionales $\\Rightarrow\\rg=2$", 26),
                  "En a = −1 se anula la fila 3. En a = −2 se cae el segundo pivote, pero las filas que quedan son proporcionales: rango 2 también.",
                  focus=True)
        rr = resp("Infinitos $a$ con rango 3 y exactamente dos con rango 2. \\ Opción (D).", size=26)
        self.push(rr, "Chequeo: el determinante es −(a + 1)(a + 2). Opción D.", anim=FadeIn(rr))
        self.wipe()

        # 2S 2024: dos parametros
        e2 = enun("2S 2024 · PREGUNTA 1", [
            VGroup(L("$A=$", 30), Mat([[-1, 1, 2], ["a", -1, "-2a+1"], ["-b", "b", "2b+ab+a"]], size=30, h_buff=1.3)).arrange(RIGHT, buff=0.15)])
        e2.scale(0.8)
        top(e2)
        self.say("La versión con dos parámetros, de 2S 2024.", FadeIn(e2))
        m = Mat([[-1, 1, 2], [0, "a-1", 1], [0, 0, "a(b+1)"]], size=34, h_buff=1.2).move_to([-3.6, -1.1, 0])
        lab = op_label(r"F_2+aF_1,\ F_3-bF_1").next_to(m, UP, buff=0.2)
        self.say("Dos pasos y queda escalonada, con pivotes a − 1 y a por (b + 1).", FadeIn(lab), FadeIn(m))
        cas = VGroup(L("$a=1$: filas $(0,0,1)$, $(0,0,b+1)$ $\\Rightarrow\\rg=2$ \\ para todo $b$", 24),
                     L("$a=0$ \\ o \\ $b=-1$: última fila nula $\\Rightarrow\\rg=2$", 24),
                     L("resto: $\\rg=3$", 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.6, -1.1, 0])
        self.say("a = 1 y a = 0 dan rango 2 para cualquier b. **Dos valores de a**: opción B.", FadeIn(cas))
        self.end_scene()


# =====================================================================
class V2_04_Inversa(V2):
    CH_NUM = "R5"
    CH_TITLE = "Inversa y sus entradas · 1S 2025"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Inversa y sus entradas", "1S 2025 · pregunta 5", prob=("MUY ALTA", "en los 4 parciales más recientes"))
        e = enun("1S 2025 · PREGUNTA 5", [
            VGroup(L("$A=$", 30), Mat([[1, 1, 1], [1, 2, -1], [2, 1, 0]], size=32)).arrange(RIGHT, buff=0.15),
            "Si $B=A^{-1}=(b_{ij})$, hallar $b_{11}$, $b_{22}$ y $b_{31}$."])
        self.pausa(e, "Pausá y arrancá Gauss-Jordan: A con la identidad al lado.")
        self.wipe()
        kw = dict(bar=3, size=34, h_buff=0.85)
        m = Mat([[1, 1, 1, 1, 0, 0], [1, 2, -1, 0, 1, 0], [2, 1, 0, 0, 0, 1]], **kw).move_to([-1.2, 0.85, 0])
        self.say("A con la identidad. Escalerizo las dos mitades juntas.", FadeIn(m))
        m = self.rowop(m, [[1, 1, 1, 1, 0, 0], [0, 1, -2, -1, 1, 0], [0, -1, -2, -2, 0, 1]], r"F_2-F_1,\ F_3-2F_1",
                       "Ceros en la primera columna.", changed=[1, 2], **kw)
        m = self.rowop(m, [[1, 1, 1, 1, 0, 0], [0, 1, -2, -1, 1, 0], [0, 0, -4, -3, 1, 1]], r"F_3+F_2",
                       "Cero debajo del segundo pivote.", changed=[2], **kw)
        m = self.rowop(m, [[1, 1, 1, 1, 0, 0], [0, 1, -2, -1, 1, 0], [0, 0, 1, "\\frac34", "-\\frac14", "-\\frac14"]], r"-\tfrac14F_3",
                       "Pivote en 1: divido por −4.", changed=[2], **kw)
        m = self.rowop(m, [[1, 1, 1, 1, 0, 0], [0, 1, 0, "\\frac12", "\\frac12", "-\\frac12"], [0, 0, 1, "\\frac34", "-\\frac14", "-\\frac14"]],
                       r"F_2+2F_3", "Ahora hacia arriba: fila 2 más dos veces la 3.", changed=[1], **kw)
        m = self.rowop(m, [[1, 0, 0, "-\\frac14", "-\\frac14", "\\frac34"], [0, 1, 0, "\\frac12", "\\frac12", "-\\frac12"],
                           [0, 0, 1, "\\frac34", "-\\frac14", "-\\frac14"]],
                       r"F_1-F_2-F_3", "Y fila 1 menos la 2 menos la 3. A la izquierda, la identidad.", changed=[0], **kw)
        ents = m.get_entries()
        marks = VGroup(*[SurroundingRectangle(ents[k], color=YELLOW, buff=0.06) for k in (3, 10, 15)])
        self.say("Leo lo que piden: b once, b veintidós, b treinta y uno.", Create(marks))
        chk = self.check("CHEQUEO: FILA 1 DE A · COLUMNA 1 = −¼ + ½ + ¾ = 1 ✓").move_to([0, -1.05, 0])
        self.say("Y chequeo: fila 1 de A por la primera columna de la inversa da 1. Listo.", FadeIn(chk))
        rr = resp("$b_{11}=-\\frac14,\\ b_{22}=\\frac12,\\ b_{31}=\\frac34$ \\ · \\ Opción (A)", size=28).move_to([0, -1.85, 0])
        self.play(FadeIn(rr), run_time=0.4)
        self.w(0.8)
        self.end_scene()


# =====================================================================
class V2_05_DetPropiedades(V2):
    CH_NUM = "R6"
    CH_TITLE = "Determinante por propiedades"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Determinante por propiedades", "2S 2024 · 1S 2025", prob=("MUY ALTA", "salió en los dos últimos parciales"))
        e = enun("2S 2024 · PREGUNTA 4", [
            VGroup(L("$\\det A=5$, \\ $A=$", 28), Mat([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]], size=30),
                   L("\\quad $B=$", 28), Mat([["2g", "2i", "2h"], ["a+d", "c+f", "b+e"], ["3d", "3f", "3e"]], size=30, h_buff=1.1)
                   ).arrange(RIGHT, buff=0.15),
            "Calcular $\\det B$."])
        self.pausa(e, "Pausá: ¿qué factores se pueden sacar?")
        self.wipe()
        self.board_start(top=2.7)
        self.push(L("$\\det B=2\\cdot3\\begin{vmatrix}g&i&h\\\\a+d&c+f&b+e\\\\d&f&e\\end{vmatrix}$", 30),
                  "Saco 2 de la fila 1 y 3 de la fila 3: un 6 afuera.")
        self.push(L("$\\overset{F_2-F_3}{=}\\ 6\\begin{vmatrix}g&i&h\\\\a&c&b\\\\d&f&e\\end{vmatrix}$", 30),
                  "Fila 2 menos fila 3 deshace la suma, y no cambia nada.")
        self.push(L("$\\overset{C_2\\leftrightarrow C_3}{=}\\ -6\\begin{vmatrix}g&h&i\\\\a&b&c\\\\d&e&f\\end{vmatrix}$ \\quad filas $(g,a,d)\\to(a,d,g)$: cíclica, signo $+$", 30),
                  "Intercambio las columnas 2 y 3: signo menos. Las filas están en orden cíclico: **dos intercambios**, signo más.",
                  focus=True)
        rr = resp("$\\det B=-6\\cdot5=-30$ \\ · \\ Opción (B)", size=28)
        self.push(rr, "Menos seis por cinco: −30.", anim=FadeIn(rr))
        self.wipe()

        e2 = enun("1S 2025 · PREGUNTA 1", [
            VGroup(L("$\\det$", 28), Mat([["a", "b", "c"], [5, -5, 10], [1, 1, 1]], size=28), L("$=-\\frac54$. \\ Calcular \\ $\\det$", 28),
                   Mat([["2a", "-2b", "2c"], [4, 4, 8], [7, -7, 7]], size=28)).arrange(RIGHT, buff=0.12)])
        e2.scale_to_fit_width(min(e2.width, 11.5))
        top(e2)
        self.say("La de 1S 2025: acá hay que normalizar **las dos** matrices.", FadeIn(e2))
        self.board_start(top=e2.get_bottom()[1] - 0.3)
        self.push(L("En $A$ saco 5 de la fila 2: \\ $\\begin{vmatrix}a&b&c\\\\1&-1&2\\\\1&1&1\\end{vmatrix}=-\\frac14$", 28),
                  "En A saco 5 de la fila 2: el determinante chico vale −1/4.")
        self.push(L("En $B$ saco $2,4,7$: \\ $56\\begin{vmatrix}a&-b&c\\\\1&1&2\\\\1&-1&1\\end{vmatrix}\\ \\overset{C_2\\cdot(-1)}{=}\\ -56\\cdot\\left(-\\frac14\\right)=14$", 28, YELLOW),
                  "En B saco 2, 4 y 7: 56. Cambio el signo de la columna del medio: menos 56 por menos un cuarto, **14**.", focus=True)
        self.end_scene()


# =====================================================================
class V2_06_DetExpresion(V2):
    CH_NUM = "R7"
    CH_TITLE = "Determinante de una expresión · 1S 2023"

    def construct(self):
        self.setup_frame()
        e = enun("1S 2023 · PREGUNTA 6", [
            "$A,B$ de $3\\times3$: \\ $\\det(2A)=64$, \\ $\\det(A^2+2AB)=32$, \\ $\\det(A^2+2AB-2BA-4B^2)=24$.",
            "Hallar $\\det(A-2B)$."])
        self.pausa(e, "Pausá. Pista: todo se factoriza.")
        self.wipe()
        top(e, 2.75)
        self.add(e)
        self.board_start(top=1.2)
        self.push(L("$\\det(2A)=2^3\\det A=64\\ \\Rightarrow\\ \\det A=8$", 30),
                  "Primero: el dos sale **al cubo**. det A = 8. Si pusiste dos por det A, ya perdiste la pregunta.", focus=True)
        self.push(L("$A^2+2AB=A(A+2B)\\ \\Rightarrow\\ 8\\det(A+2B)=32\\ \\Rightarrow\\ \\det(A+2B)=4$", 30),
                  "Saco A de factor común a la izquierda: det(A + 2B) = 4.")
        self.push(L("$A^2+2AB-2BA-4B^2=A(A+2B)-2B(A+2B)=(A-2B)(A+2B)$", 30, YELLOW),
                  "La grande: agrupo de a dos y sale (A − 2B)(A + 2B), respetando el orden.")
        rr = resp("$\\det(A-2B)\\cdot4=24\\ \\Rightarrow\\ \\det(A-2B)=6$ \\ · \\ Opción (C)", size=28)
        self.push(rr, "Cuatro por el que busco da 24: **6**.", anim=FadeIn(rr))
        self.wipe()

        e2 = enun("1S 2023 VESPERTINO · PREGUNTA 6", [
            "$\\det A=1,\\ \\det B=3,\\ \\det(B^3A^3B^{-1}+B^4A^2B^{-1})=36$. \\ Hallar $\\det(A+B)$."])
        top(e2)
        self.say("La versión del turno vespertino, con una trampa de orden.", FadeIn(e2))
        self.board_start(top=1.5)
        self.push(L("$B^3A^3B^{-1}+B^4A^2B^{-1}=B^3\\,(A^3+BA^2)\\,B^{-1}=B^3(A+B)A^2B^{-1}$", 30),
                  "Saco B al cubo a la izquierda y B inversa a la derecha. Adentro queda A³ + BA², y el A² sale **por la derecha**.",
                  focus=True)
        self.push(L("$27\\cdot\\det(A+B)\\cdot1\\cdot\\frac13=9\\det(A+B)=36$", 30), "Determinantes: 27 por det(A + B) por 1 por un tercio.")
        rr = resp("$\\det(A+B)=4$ \\ · \\ Opción (B)", size=28)
        self.push(rr, "Da 4.", anim=FadeIn(rr))
        self.end_scene()


# =====================================================================
class V2_07_InversaEcuacion(V2):
    CH_NUM = "R8"
    CH_TITLE = "Inversa desde una ecuación"

    def construct(self):
        self.setup_frame()
        e = enun("1S 2025 · PREGUNTA 6", ["$A^2+3AA^t+2I=O$. \\ ¿Es invertible? ¿Quién es $A^{-1}$?"])
        top(e)
        self.say("Tipo alta probabilidad: la inversa sin hacer cuentas. 1S 2025.", FadeIn(e))
        self.board_start(top=1.7)
        self.push(L("$A^2+3AA^t=-2I$", 32), "Paso la identidad al otro lado.")
        self.push(L("$A\\,(A+3A^t)=-2I$", 32), "A sale a la izquierda de **los dos** términos.")
        self.push(L("$A\\cdot\\left(-\\tfrac12(A+3A^t)\\right)=I$", 32, YELLOW), "Divido por menos dos.")
        rr = resp("Invertible, \\ $A^{-1}=-\\frac12(A+3A^t)$ \\ · \\ Opción (C)", size=28)
        self.push(rr, "Y leo la inversa: opción C.", anim=FadeIn(rr))
        self.wipe()

        e2 = enun("2S 2024 · PREGUNTA 5", [VGroup(L("$A=$", 30), Mat([[1, 0, "\\lambda+1"], ["\\lambda", 1, -1], [0, 0, 1]], size=30, h_buff=1.1)).arrange(RIGHT, buff=0.15),
                                           "¿Para cuántos $\\lambda$ vale $A^{-1}=2I-A$?"])
        e2.scale(0.78)
        top(e2)
        self.say("La otra cara, 2S 2024: ¿para qué lambda la inversa es 2I − A?", FadeIn(e2))
        self.board_start(top=e2.get_bottom()[1] - 0.3)
        self.push(L("$A^{-1}=2I-A\\iff A(2I-A)=I$ \\quad ($\\det A=1$: siempre invertible)", 28),
                  "Traduzco: A por 2I − A tiene que dar la identidad.")
        self.push(VGroup(L("$A(2I-A)=$", 28), Mat([[1, 0, 0], [0, 1, "-\\lambda(\\lambda+1)"], [0, 0, 1]], size=28, h_buff=1.4)).arrange(RIGHT, buff=0.15),
                  "Multiplico: todo da identidad salvo un lugar, menos lambda por lambda más uno.")
        rr = resp("$\\lambda(\\lambda+1)=0$: \\ exactamente dos valores, $\\lambda=0$ y $\\lambda=-1$ \\ · \\ Opción (D)", size=26)
        self.push(rr, "Igualo a cero: dos valores. Opción D.", anim=FadeIn(rr))
        self.end_scene()


# =====================================================================
class V2_08_Complejos(V2):
    CH_NUM = "R11"
    CH_TITLE = "Complejos · ejercicios tipo"

    def construct(self):
        self.setup_frame(header=False)
        self.title_card("Complejos", "ejercicios tipo (no hay parciales viejos)", prob=("ALTA", "nuevo en el programa de este año"))
        e = enun("EJERCICIO TIPO 1", ["Sea $z=\\dfrac{1+i\\sqrt3}{1-i}$. \\ Hallar $|z|$, $\\arg z$ y $z^{12}$."])
        self.pausa(e, "Pausá: pasá numerador y denominador a polar.")
        self.wipe()
        p = plano((-3, 3), (-3, 3), unit=0.8).shift(RIGHT * 3.8 + DOWN * 0.3)
        o = p.n2p(0)
        self.add(p)
        a1 = flecha(p, 1 + np.sqrt(3) * 1j, BLUE)
        a2 = flecha(p, 1 - 1j, TEAL)
        az = flecha(p, np.sqrt(2) * np.exp(1j * 7 * PI / 12), YELLOW)
        self.board_start(left=-6.5, top=2.6, maxw=7.3)
        self.push(L("$1+i\\sqrt3=2\\,e^{i\\pi/3}$ \\quad $1-i=\\sqrt2\\,e^{-i\\pi/4}$", 30),
                  "Arriba: largo 2, ángulo π/3. Abajo: largo √2, cuarto cuadrante, −π/4.", GrowArrow(a1), GrowArrow(a2))
        self.push(L("$z=\\frac{2}{\\sqrt2}\\,e^{i(\\pi/3+\\pi/4)}=\\sqrt2\\,e^{i7\\pi/12}$", 30),
                  "Dividir: los largos se dividen y los ángulos **se restan**. Menos menos π/4 suma.", GrowArrow(az))
        self.push(L("$z^{12}=(\\sqrt2)^{12}\\,e^{i\\,7\\pi}=64\\,e^{i\\pi}=-64$", 30, YELLOW),
                  "De Moivre: √2 a la doce es 64, y doce veces 7π/12 es 7π, o sea π. Da −64.", focus=True)
        rr = resp("$|z|=\\sqrt2,\\ \\arg z=\\frac{7\\pi}{12},\\ z^{12}=-64$", size=26)
        self.push(rr, "Tres datos en tres renglones.", anim=FadeIn(rr))
        self.wipe(p)

        roots = [2 * np.exp(1j * (PI / 4 + k * PI / 2)) for k in range(4)]
        circ = Circle(radius=p.x_axis.unit_size * 2, color=DIM).move_to(o)
        sq = Polygon(*[p.n2p(r) for r in roots], color=RED, stroke_width=3)
        dots = VGroup(*[Dot(p.n2p(r), color=YELLOW, radius=0.08) for r in roots])
        self.board_start(left=-6.5, top=2.6, maxw=7.3)
        self.push(L("**Tipo 2:** \\ $z^4=-16=16\\,e^{i\\pi}$", 30), "Segundo tipo: z a la cuarta igual a −16.", Create(circ))
        self.push(L("$z_k=2\\,e^{i(\\pi+2k\\pi)/4}$: \\ ángulos $\\frac\\pi4,\\frac{3\\pi}4,\\frac{5\\pi}4,\\frac{7\\pi}4$", 30),
                  "Módulo, raíz cuarta de 16: 2. Ángulos: π/4 y saltos de 90 grados.",
                  LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.25), Create(sq))
        rr = resp("$z=\\pm\\sqrt2\\pm i\\sqrt2$: un cuadrado de radio 2", size=26)
        self.push(rr, "Las cuatro raíces: más o menos √2, más o menos i√2. Un cuadrado.", anim=FadeIn(rr))
        self.push(L("**Tipo 3 (práctico 2):** \\ $z_1-z_2=i$, \\ $(1-i)z_1+(1+i)z_2=1$", 28),
                  "Y los sistemas con complejos se resuelven igual que siempre: despejo y sustituyo.")
        self.push(L("$z_1=z_2+i\\ \\Rightarrow\\ 2z_2+1+i=1\\ \\Rightarrow\\ z_2=-\\frac i2,\\ z_1=\\frac i2$", 28, YELLOW),
                  "z₁ = z₂ + i, sustituyo, y sale z₂ = −i/2 y z₁ = i/2.")
        self.end_scene()


# =====================================================================
class V2_09_VF(V2):
    CH_NUM = "VF"
    CH_TITLE = "Verdadero o falso relámpago"

    def construct(self):
        self.setup_frame()
        items = [
            ("$AB=AC$ y $A\\neq O\\ \\Rightarrow\\ B=C$", False, "$N=\\begin{pmatrix}0&1\\\\0&0\\end{pmatrix}$: $NN=NO$"),
            ("$(A+B)^2=A^2+2AB+B^2$", False, "falta $BA$: solo si conmutan"),
            ("$A,B$ invertibles $\\Rightarrow A+B$ invertible", False, "$I+(-I)=O$"),
            ("$(\\lambda AB)^{-1}=\\frac1\\lambda B^{-1}A^{-1}$", True, "se da vuelta el orden"),
            ("$\\det(2A)=2\\det A$", False, "es $2^n\\det A$"),
            ("$A^2=I\\ \\Rightarrow\\ A$ invertible", True, "$A^{-1}=A$"),
            ("$\\det A=0\\ \\Rightarrow$ fila o columna de ceros", False, "$\\begin{pmatrix}1&2\\\\2&4\\end{pmatrix}$"),
            ("más incógnitas que ecuaciones $\\Rightarrow$ compatible", False, "dos ecuaciones contradictorias"),
            ("rango = filas no nulas de $A$", False, "de la escalonada"),
            ("toda elemental tiene $\\det=1$", False, "$F_i\\to5F_i$: det 5"),
            ("antisimétrica, $n$ impar $\\Rightarrow\\det A=0$", True, "$\\det A=(-1)^n\\det A$"),
            ("$X_1,X_2$ soluciones $\\Rightarrow\\frac12(X_1+X_2)$ solución", True, "$A(\\cdot)=\\frac12b+\\frac12b$"),
        ]
        tit = T("Tapá la respuesta: 12 clásicos en un minuto", 26, SOFT, MONO).to_edge(UP, buff=0.75)
        self.say("Doce verdadero o falso clásicos, a toda velocidad. Si alguno te frena, **pausá ahí**.", FadeIn(tit))
        self.uncap()
        rows = VGroup()
        for k, (afirm, v, why) in enumerate(items):
            a = L(afirm, 25)
            b = T("V" if v else "F", 26, GREEN if v else RED, MONO, BOLD)
            c = L(why, 22, SOFT)
            rows.add(VGroup(a, b, c))
        for half in (0, 1):
            grp = VGroup()
            for k in range(6):
                a, b, c = rows[half * 6 + k]
                y = 1.9 - k * 0.72
                a.move_to([0, y, 0]).align_to([-6.5, 0, 0], LEFT)
                if a.width > 6.6:
                    a.scale_to_fit_width(6.6)
                    a.align_to([-6.5, 0, 0], LEFT)
                b.move_to([0.6, y, 0])
                c.move_to([0, y, 0]).align_to([1.2, 0, 0], LEFT)
                if c.width > 5.4:
                    c.scale_to_fit_width(5.4)
                    c.align_to([1.2, 0, 0], LEFT)
                grp.add(VGroup(a, b, c))
            for k, g in enumerate(grp):
                self.play(FadeIn(g[0], shift=RIGHT * 0.2), run_time=0.35)
                self.w(0.9)
                self.play(FadeIn(g[1], scale=1.4), FadeIn(g[2]), run_time=0.3)
                self.w(0.6)
            self.snap()
            if half == 0:
                self.play(FadeOut(grp), run_time=0.3)
        self.say("Los veinticinco completos, con contraejemplos, están en el apéndice del libro.")
        self.end_scene()


# =====================================================================
class V2_10_Cierre(V2):
    CH_NUM = "FIN"
    CH_TITLE = "Problema modelado y checklist"

    def construct(self):
        self.setup_frame()
        e = enun("1S 2023 VESPERTINO · PREGUNTA 1", [
            "30 Philadelphia, 20 New York, 50 California. Tablas: Lagrange $(4,3,5)$, Hausdorff $(2,1,5)$,",
            "Gauss $(6,3,15)$, Kolmogorov $(8,6,10)$. Todas las piezas, 1 Lagrange, al menos una de cada otra."], size=23)
        top(e)
        self.say("Un problema modelado, el del sushi, que también está en el práctico 2.", FadeIn(e))
        self.board_start(top=1.2)
        self.push(L("$H+3G+4K=13,\\quad H+3G+6K=17,\\quad H+3G+2K=9$", 28), "Con L = 1, cada tipo de pieza da una ecuación.")
        self.push(L("Restando: $2K=4\\Rightarrow K=2$; \\ queda $H+3G=5$ con $H,G\\ge1$ enteros $\\Rightarrow G=1,\\ H=2$", 28),
                  "Restando las dos primeras, K = 2. Queda H + 3G = 5, y con enteros positivos solo sirve G = 1, H = 2.")
        tip = self.tip(["En múltiple opción: **sustituí las opciones**. Un minuto."], label="ATAJO", size=24)
        self.push(tip, "Y el atajo: probar las cuatro opciones en las ecuaciones lleva un minuto. Opción D.", anim=FadeIn(tip))
        self.wipe()

        chk = self.stamp([
            "¿Sustituí el valor crítico y **terminé de escalerizar**?",
            "¿$\\det(\\lambda A)$ con $\\lambda^n$?",
            "¿Factoricé respetando **izquierda y derecha**?",
            "¿Chequeé la inversa multiplicando una fila por una columna?",
            "¿Dibujé el complejo para ver el **cuadrante**?"], "ANTES DE MARCAR", size=28)
        chk.move_to([0, 0.5, 0])
        self.say("Y el checklist antes de marcar cada respuesta. Cinco preguntas, cinco segundos cada una.",
                 *self.show_stamp(chk))
        self.say("Eso es todo. El libro tiene la teoría completa y el recetario. **Éxitos el sábado.**", focus=True)
        self.end_scene()
