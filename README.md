# Manim Custom Diego

A collection of [Manim](https://www.manim.community/) animations.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Manim also requires a system LaTeX distribution (for `MathTex`/`Tex`) and
FFmpeg. On Debian/Ubuntu:

```bash
sudo apt-get install ffmpeg texlive texlive-latex-extra texlive-fonts-extra texlive-science
```

## Projects

### `calculo1/` — Cálculo 1, primer parcial (3 videos)

Visualization of the *Cálculo 1 · 1er parcial* study book: the most likely exam
exercises, ordered by probability and solved step by step. 3Blue1Brown-style
black background, karaoke subtitles (no audio), IBM Plex fonts, and live
"parameter sliders" (ε, δ, n, K, a…) that drive the graphs.

| Video | File | Scenes |
|---|---|---|
| 1 · Muy alta | `v1_muy_alta.py` | sup/ínf, Darboux, integrability, ε-δ |
| 2 · Alta | `v2_alta.py` | continuity with a parameter, integral properties, Bolzano |
| 3 · Media | `v3_media.py` | limits, Lipschitz, composition, true/false, formulary |

Shared style and helpers live in `calc_base.py`. On Windows, double-click
`render_preview.bat` (480p) or `render_4k.bat` (final); `render_all.ps1`
renders every scene in parallel and joins each video with ffmpeg. See
`calculo1/LEEME.txt` for options (`-Video`, `-Only`, `-MaxParallel`, `C1_PACE`).

Single scene, from `calculo1/`:

```bash
manim -ql v1_muy_alta.py V1_09_EpsTeoria
```

## Scenes

### `scenes/two_plus_two.py` — `TwoPlusTwo`

A short test animation demonstrating `2 + 2 = 4`: the equation is written out,
two groups of two dots are shown for each addend, the dots animate together
into a single row of four, and the result `4` is revealed and highlighted.

Render it with:

```bash
manim -ql scenes/two_plus_two.py TwoPlusTwo   # low quality, fast preview
manim -qh scenes/two_plus_two.py TwoPlusTwo   # high quality
```

Output is written to `media/videos/two_plus_two/<quality>/TwoPlusTwo.mp4`.
