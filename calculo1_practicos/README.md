# Cálculo 1 · Prácticos resueltos

Cuaderno en PDF con todos los ejercicios de los prácticos 1 a 5 que entran al
primer parcial, resueltos paso a paso, con el mismo estilo que el libro del parcial.

- `Calculo1_practicos_resueltos.pdf`: el cuaderno ya compilado.
- Parte 0: todas las propiedades del curso (P1 a P84), de la conmutativa a Weierstrass.
- Cada paso tiene una caja «TEORÍA QUE USO» que cita la propiedad por su número.

Para recompilar (necesita XeLaTeX; las fuentes IBM Plex están en `fonts/`):

```
xelatex main.tex && xelatex main.tex
```

`python verify.py` chequea con sympy los resultados numéricos.
