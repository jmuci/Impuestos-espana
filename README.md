# Impuestos-espana

¿A dónde van tus impuestos? ¿Quién paga más? ¿Pagan los ricos? Este tipo de preguntas buscamos responder.

Página en español con gráficos de quién paga los impuestos en España: recaudación por fuente, IRPF por tramos, comunidades autónomas, País Vasco y Navarra, un impuesto al patrimonio, un capítulo sobre los más ricos y otro con la aportación de los 25 mayores patrimonios (impuestos de sus empresas, escenarios de IRPF, estadísticas de Hacienda y las mayores SICAV). Cada cifra lleva su origen entre corchetes: oficial, prensa, académica, estimado o inferido.

Es una sola página estática de scroll continuo (ocho capítulos, menú fijo que sigue la lectura, barra de progreso y aparición suave; respeta `prefers-reduced-motion`), sin dependencias salvo las fuentes de Google Fonts. Los enlaces antiguos tipo `#tramos` siguen llevando al capítulo.

## Estructura

- `index.html`: la página ya generada. Es lo que se publica.
- `src/style.css`, `src/body.html`, `src/app.js`: las fuentes.
- `src/tab8.py`: genera el capítulo 7 ("Top 25: aportación"). Las cifras de los escenarios se calculan ahí, a partir de supuestos explícitos.
- `src/build.py`: regenera `index.html` a partir de las anteriores.

## Regenerar

```
python3 src/build.py
```

Abrir `index.html` en el navegador basta para verla en local.
