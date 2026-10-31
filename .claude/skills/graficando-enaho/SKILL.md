---
name: graficando-enaho
description: Grafica la pobreza de la ENAHO del INEI en barras ponderadas por área urbana y rural, sexo, grupo de edad o departamento, y guarda PNG en figuras/. Úsala cuando pidan un gráfico, figura, barras o comparación de la pobreza del Perú entre grupos.
argument-hint: [area|sexo|edad|departamento]
allowed-tools: Bash(uv run *)
---

# Graficar la ENAHO

1. Si no existe `salidas/personas_2024.parquet`, usa primero la skill limpiando-enaho.
2. Elige `--por` según el pedido: `area` (urbano/rural), `sexo`, `edad` o `departamento`. Para pobreza extrema agrega `--indicador extrema`. Si el usuario pasó argumento, úsalo: `$0`.
3. Corre exactamente: `uv run ${CLAUDE_SKILL_DIR}/scripts/graficar.py --por <variable>`
4. Responde con las cifras que imprime el script y la ruta del PNG.

## Reglas fijas (ya están en el script; no las cambies si el pedido es otro gráfico)

- Pondera siempre con `facpob07`; nunca cuentes encuestas.
- Barras horizontales que empiezan en cero, ordenadas de menor a mayor (edad, en su orden natural).
- Un solo color; el valor escrito en cada barra con un decimal.
- El título dice qué y cuándo: «Pobreza monetaria por área de residencia, Perú 2024».
- Nota al pie: «Fuente: INEI, ENAHO 2024».
- PNG a 200 dpi en `figuras/`.

Si piden una variable que el script no tiene, copia su estilo en un script nuevo con las mismas reglas, en vez de improvisar otro diseño. Las cifras con `facpob07` pueden diferir hasta 0.1 puntos de las publicadas (urbana 24.7 % frente a 24.8 %); menciónalo si el usuario compara con el INEI.
