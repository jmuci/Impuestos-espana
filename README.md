# Impuestos-espana

¿A dónde van tus impuestos? ¿Quién paga más? ¿Pagan los ricos? Este tipo de preguntas buscamos responder.

Página en español con gráficos de quién paga los impuestos en España: recaudación por fuente, IRPF por tramos, comunidades autónomas, País Vasco y Navarra, un impuesto al patrimonio, una pestaña sobre los más ricos y otra con la aportación de los 25 mayores patrimonios (impuestos de sus empresas, escenarios de IRPF, estadísticas de Hacienda y las mayores SICAV). Cada cifra lleva su origen entre corchetes: oficial, prensa, académica, estimado o inferido.

Es una sola página estática, sin dependencias salvo las fuentes de Google Fonts.

## Estructura

- `index.html`: la página ya generada. Es lo que se publica.
- `src/style.css`, `src/body.html`, `src/app.js`: las fuentes.
- `src/tab8.py`: genera la pestaña 7 ("Top 25: aportación"). Las cifras de los escenarios se calculan ahí, a partir de supuestos explícitos.
- `src/build.py`: regenera `index.html` a partir de las anteriores.

## Regenerar

```
python3 src/build.py
```

Abrir `index.html` en el navegador basta para verla en local.
