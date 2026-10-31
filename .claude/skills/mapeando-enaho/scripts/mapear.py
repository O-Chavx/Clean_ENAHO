"""Mapa coroplético de la pobreza por departamento con la ENAHO.

Uso: uv run .claude/skills/mapeando-enaho/scripts/mapear.py [--anio 2024] [--indicador pobreza]

Une por código (ubigeo[:2] con FIRST_IDDP), nunca por nombre.
"""
import argparse
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

LLAVES_HOGAR = ["conglome", "vivienda", "hogar"]
INDICADORES = {"pobreza": ("pobre", "Pobreza monetaria"), "extrema": ("pobre_extremo", "Pobreza extrema")}
GEOJSON = Path("datos/peru_departamental_simple.geojson")
URL_GEOJSON = (
    "https://raw.githubusercontent.com/d2cml-ai/Data-Science-Python/main/"
    "sessions/06-geoespacial/lab/Data/peru_departamental_simple.geojson"
)


def tasa_departamental(base: pd.DataFrame, ind: str) -> pd.Series:
    """Método oficial del INEI: un registro por hogar, ponderado con factor07 × mieperho.

    Así se replican las cifras publicadas (Cajamarca 45.0 %, Ica 6.0 % en 2024).
    """
    hogares = base.drop_duplicates(LLAVES_HOGAR)
    peso = hogares.factor07 * hogares.mieperho
    num = (hogares[ind] * peso).groupby(hogares.departamento).sum()
    return num / peso.groupby(hogares.departamento).sum() * 100


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--anio", type=int, default=2024)
    ap.add_argument("--indicador", choices=INDICADORES, default="pobreza")
    ap.add_argument("--mapas", type=Path, default=Path("mapas"))
    a = ap.parse_args()

    ruta = Path(f"salidas/personas_{a.anio}.parquet")
    if not ruta.exists():
        sys.exit(f"No existe {ruta}. Corre primero la skill limpiando-enaho.")
    if not GEOJSON.exists():
        sys.exit(f"Falta {GEOJSON}. Bájalo de {URL_GEOJSON}")
    base = pd.read_parquet(ruta)
    ind, titulo = INDICADORES[a.indicador]

    tasa = tasa_departamental(base, ind).rename("tasa").reset_index()
    geo = gpd.read_file(GEOJSON)
    geo["FIRST_IDDP"] = geo.FIRST_IDDP.astype(str).str.zfill(2)
    mapa = geo.merge(tasa, left_on="FIRST_IDDP", right_on="departamento", how="left", validate="1:1")

    # Reglas: 25 departamentos, ninguno sin dato, Lima (15) y Callao (07) separados
    assert len(mapa) == 25, f"Se esperaban 25 departamentos, hay {len(mapa)}"
    sin_dato = mapa.loc[mapa.tasa.isna(), "NOMBDEP"].tolist()
    assert not sin_dato, f"Departamentos sin dato: {sin_dato}"
    assert {"07", "15"} <= set(mapa.FIRST_IDDP), "Lima y Callao deben ir separados"

    fig, ax = plt.subplots(figsize=(7, 9))
    mapa.plot(
        column="tasa", cmap="Blues", vmin=0, vmax=mapa.tasa.max(), linewidth=0.4,
        edgecolor="white", ax=ax, legend=True,
        legend_kwds={"label": "% de personas en pobreza" if a.indicador == "pobreza" else "% de personas en pobreza extrema",
                     "shrink": 0.6},
    )
    ax.set_axis_off()
    ax.set_title(f"{titulo} por departamento, Perú {a.anio}", loc="left", fontsize=13, fontweight="bold")
    fig.text(0.02, 0.02, f"Fuente: INEI, ENAHO {a.anio}. Ponderado con factor07 × mieperho.", fontsize=8, color="#555")

    a.mapas.mkdir(parents=True, exist_ok=True)
    sufijo = "" if a.indicador == "pobreza" else f"_{a.indicador}"
    salida = a.mapas / f"pobreza_departamento{sufijo}.png"
    if a.anio != 2024:
        salida = salida.with_stem(f"{salida.stem}_{a.anio}")
    fig.savefig(salida, dpi=200, bbox_inches="tight")
    mapa.drop(columns="geometry").sort_values("tasa", ascending=False)[["FIRST_IDDP", "NOMBDEP", "tasa"]].round(1).to_csv(
        salida.with_suffix(".csv"), index=False
    )

    orden = mapa.sort_values("tasa", ascending=False)
    print(f"{titulo} por departamento, {a.anio} ({len(mapa)} departamentos con dato):")
    for _, f in orden.iterrows():
        print(f"  {f.FIRST_IDDP} {f.NOMBDEP:<15} {f.tasa:5.1f} %")
    print(f"Mapa guardado en {salida}")


if __name__ == "__main__":
    main()
