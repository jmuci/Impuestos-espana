# Impuestos-espana

¿A dónde van tus impuestos? ¿Quién paga más? ¿Pagan los ricos? Este tipo de preguntas buscamos responder.

Página en español con gráficos de quién paga los impuestos en España: recaudación por fuente, IRPF por tramos, comunidades autónomas, País Vasco y Navarra, un impuesto al patrimonio y una pestaña sobre los más ricos. Cada cifra lleva su origen entre corchetes: oficial, prensa, académica, estimado o inferido.

Es una sola página estática, sin dependencias salvo las fuentes de Google Fonts.

## Estructura

- `index.html`: la página ya generada. Es lo que se publica.
- `src/style.css`, `src/body.html`, `src/app.js`: las fuentes.
- `src/build.py`: regenera `index.html` a partir de las tres anteriores.

## Regenerar

```
python3 src/build.py
```

Abrir `index.html` en el navegador basta para verla en local.
