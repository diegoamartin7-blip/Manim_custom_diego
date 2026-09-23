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
