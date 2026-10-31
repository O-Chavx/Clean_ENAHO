---
name: limpiando-enaho
description: Limpia los módulos 34 (sumaria) y 02 (miembros) de la ENAHO del INEI y arma una base de personas residentes con pobreza y factor de expansión, validada contra la cifra oficial. Úsala cuando pidan limpiar, unir o analizar la ENAHO, o calcular la pobreza del Perú por región, departamento, área, sexo o edad.
argument-hint: [año]
allowed-tools: Bash(uv run *)
---

# Limpiar la ENAHO

El año es `$0`; si viene vacío, usa 2024.

1. Revisa que existan `datos/966-Modulo34.zip` y `datos/966-Modulo02.zip` (966 = ENAHO 2024). Si faltan, pide al usuario bajarlos de
   `https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo34.zip` y `...966-Modulo02.zip` y guardarlos en `datos/`.
2. Si `salidas/personas_<año>.parquet` y `salidas/validacion.txt` ya existen y la validación dice `VALIDADA`, sáltate el paso 3.
3. Corre exactamente, desde la raíz del repo:
   `uv run ${CLAUDE_SKILL_DIR}/scripts/limpiar.py --anio <año>`
   No reescribas la limpieza a mano ni cambies el filtro, las llaves o los pesos.
4. Lee `salidas/validacion.txt`. Si dice `NO VALIDADA` o la pobreza difiere del INEI en más de 0.1 puntos, detente y reporta qué chequeo falló.
5. Responde con `salidas/personas_<año>.parquet`. Toda cifra va ponderada con `facpob07`, nunca como conteo de encuestas:
   `(pobre * facpob07).sum() / facpob07.sum() * 100`.
   Para una cifra regional que deba coincidir con la publicada por el INEI, usa un registro por hogar ponderado con `factor07 * mieperho` (ver reference.md) e indica qué método usaste.
6. Antes de usar una variable que no está en la base, lee [reference.md](reference.md).

## La base

Una fila por residente habitual (108,664 en 2024). Columnas clave: `conglome, vivienda, hogar, codperso` (texto), `ubigeo` (texto, 6 dígitos), `departamento` (2 dígitos: 15 Lima, 07 Callao), `area` (Urbana/Rural), `pobre`, `pobre_extremo`, `sexo`, `edad`, `grupo_edad`, `facpob07`, `factor07`, `mieperho`.
