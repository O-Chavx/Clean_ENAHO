# Referencia: ENAHO 2024 (código INEI 966)

## Módulos

| Módulo | Archivo | Una fila por | Filas | Llaves | Factor |
|---|---|---|---|---|---|
| 34 · Sumaria | sumaria-2024.dta | hogar | 33,691 | conglome, vivienda, hogar | factor07 |
| 02 · Miembros | enaho01-2024-200.dta | persona | 117,721 | las tres + codperso | facpob07 |

## Variables usadas

- `pobreza` (sumaria): 1 pobre extremo, 2 pobre no extremo, 3 no pobre. Es categoría: pobre = `pobreza <= 2`, nunca un promedio.
- `mieperho`: miembros del hogar (excluye trabajadores del hogar y pensionistas).
- `estrato`: 1 a 5 urbano, 6 a 8 rural.
- `dominio`: 1-3 costa, 4-6 sierra, 7 selva, 8 Lima Metropolitana.
- `ubigeo`: departamento (2) + provincia (2) + distrito (2). Siempre texto.
- `p203` parentesco · `p204` ¿es miembro del hogar? · `p205` ¿estuvo ausente más de 30 días? · `p206` ¿estuvo presente más de 30 días? · `p207` sexo (1 hombre, 2 mujer) · `p208a` edad.

## Residente habitual

`(p204 == 1 & p205 == 2) | (p204 == 2 & p206 == 1)` → 108,664 personas en 2024.

## Dos formas de ponderar

| Método | Cómo | Pobreza 2024 |
|---|---|---|
| Hogares (oficial INEI) | sumaria, `factor07 * mieperho` | 27.58 % |
| Personas | base de personas, `facpob07` | 27.53 % |

Por departamento o área las diferencias son de hasta 0.5 puntos (Puno 39.9 % vs 40.4 %). Las cifras publicadas por el INEI salen con el método de hogares: desde la base de personas se obtiene con `base.drop_duplicates(["conglome","vivienda","hogar"])` y peso `factor07 * mieperho`.

## Cifras de control 2024 (método de hogares)

Nacional 27.6 % · extrema 5.5 % · urbana 24.8 % · rural 39.3 % · Cusco 18.5 % · Cajamarca 45.0 % · Loreto 43.0 % · Puno 39.9 % · Ica 6.0 % · Moquegua 11.0 % · Madre de Dios 11.1 %.

## Trampas

1. Ceros a la izquierda: conglome «015009», ubigeo «010101». Léelos como texto.
2. La columna del año llega como «aÑo»: normaliza nombres antes de usarlos.
3. No todos son residentes: 117,721 filas → 108,664 residentes.
4. Une con `validate="m:1"` para que un hogar repetido no multiplique personas.
5. Encuestas no son personas: 33,691 hogares representan 34.1 millones con su factor.
6. Códigos, no números: `pobreza`, `estrato`, `p207` son categorías.
