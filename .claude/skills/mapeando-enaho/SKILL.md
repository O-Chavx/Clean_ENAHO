---
name: mapeando-enaho
description: Hace un mapa coroplético de la pobreza de la ENAHO del INEI por departamento del Perú, uniendo por código de ubigeo con el GeoJSON de los 25 departamentos, y lo guarda en mapas/. Úsala cuando pidan un mapa de la pobreza, pobreza por departamento o región en un mapa, o un coroplético del Perú.
allowed-tools: Bash(uv run *)
---

# Mapear la ENAHO

1. Si no existe `salidas/personas_2024.parquet`, usa primero la skill limpiando-enaho.
2. Si falta `datos/peru_departamental_simple.geojson`, bájalo de
   `https://raw.githubusercontent.com/d2cml-ai/Data-Science-Python/main/sessions/06-geoespacial/lab/Data/peru_departamental_simple.geojson`.
3. Corre exactamente: `uv run ${CLAUDE_SKILL_DIR}/scripts/mapear.py` (para pobreza extrema, `--indicador extrema`).
4. Responde con la ruta del mapa, los tres departamentos con más pobreza y los tres con menos. La tabla completa queda en `mapas/pobreza_departamento.csv`.

## Reglas fijas (ya están en el script)

- Une por código: `ubigeo[:2]` con `FIRST_IDDP`. Nunca por nombre: «APURIMAC» no es «Apurímac».
- Exige 25 departamentos y ninguno sin dato; si falla, revisa la unión, no la quites.
- Lima (15) y Callao (07) van separados.
- Un solo color de claro a oscuro (`Blues`), desde 0; nunca arcoíris.
- Leyenda con la unidad: % de personas.
- Pondera como el INEI (un registro por hogar, `factor07 × mieperho`), para que el mapa replique las cifras oficiales: Cajamarca 45.0 %, Loreto 43.0 %, Puno 39.9 %, Ica 6.0 %.
