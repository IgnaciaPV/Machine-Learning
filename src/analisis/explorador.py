"""Data Understanding sobre los JSON validados del laboratorio."""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


class ExploradorDatos:
    CAMPOS = [
        "titulo", "fecha_publicacion", "fuente", "url", "resumen", "delitos",
        "personas", "organizaciones", "lugares", "objetos", "relaciones",
    ]

    def __init__(self, json_dir: Path, output_dir: Path, validation_dir: Path | None = None) -> None:
        self.json_dir = Path(json_dir)
        self.output_dir = Path(output_dir)
        self.fig_dir = self.output_dir / "visualizaciones"
        self.validation_dir = Path(validation_dir) if validation_dir else self.json_dir.parent / "validation"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.fig_dir.mkdir(parents=True, exist_ok=True)
        self.noticias, self.json_invalidos = self._cargar()

    def _cargar(self) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        noticias: list[dict[str, Any]] = []
        invalidos: list[dict[str, str]] = []
        for ruta in sorted(self.json_dir.glob("*.json")):
            try:
                data = json.loads(ruta.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    noticias.append(data)
                else:
                    invalidos.append({"archivo": ruta.name, "error": "raíz JSON no es objeto"})
            except Exception as exc:
                invalidos.append({"archivo": ruta.name, "error": f"{type(exc).__name__}: {exc}"})
        return noticias, invalidos

    @staticmethod
    def _guardar_fig(ruta: Path) -> None:
        plt.tight_layout()
        plt.savefig(ruta, dpi=180, bbox_inches="tight")
        plt.close()

    def noticias_por_fuente(self) -> pd.Series:
        serie = pd.Series([n.get("fuente") or "Sin fuente" for n in self.noticias], dtype="object").value_counts()
        if not serie.empty:
            plt.figure(figsize=(8, 4.5))
            serie.sort_values().plot(kind="barh")
            plt.title("Noticias procesadas por fuente")
            plt.xlabel("Cantidad de noticias")
            plt.ylabel("Fuente")
            self._guardar_fig(self.fig_dir / "01_noticias_por_fuente.png")
        return serie

    def delitos_frecuentes(self) -> pd.Series:
        valores = [d for n in self.noticias for d in n.get("delitos", []) if d]
        serie = pd.Series(valores, dtype="object").value_counts()
        if not serie.empty:
            plt.figure(figsize=(8, 5))
            serie.head(12).sort_values().plot(kind="barh")
            plt.title("Delitos mencionados con mayor frecuencia")
            plt.xlabel("Cantidad de noticias con mención")
            plt.ylabel("Tipo de delito extraído")
            self._guardar_fig(self.fig_dir / "02_delitos_frecuentes.png")
        return serie

    def lugares_frecuentes(self) -> pd.Series:
        valores = [d for n in self.noticias for d in n.get("lugares", []) if d]
        serie = pd.Series(valores, dtype="object").value_counts()
        if not serie.empty:
            plt.figure(figsize=(8, 5))
            serie.head(12).sort_values().plot(kind="barh")
            plt.title("Lugares con mayor cantidad de menciones")
            plt.xlabel("Cantidad de menciones en noticias")
            plt.ylabel("Lugar extraído")
            self._guardar_fig(self.fig_dir / "03_lugares_frecuentes.png")
        return serie

    def delitos_por_lugar(self) -> pd.DataFrame:
        filas: list[dict[str, str]] = []
        for n in self.noticias:
            for delito in sorted(set(n.get("delitos", []))):
                for lugar in sorted(set(n.get("lugares", []))):
                    if delito and lugar:
                        filas.append({"delito": delito, "lugar": lugar})
        if not filas:
            return pd.DataFrame(columns=["lugar", "delito", "co_menciones"])
        df = pd.DataFrame(filas)
        conteo = df.value_counts(["lugar", "delito"]).reset_index(name="co_menciones")
        top_lugares = set(df["lugar"].value_counts().head(8).index)
        plot_df = conteo[conteo["lugar"].isin(top_lugares)]
        if not plot_df.empty:
            piv = plot_df.pivot(index="lugar", columns="delito", values="co_menciones").fillna(0)
            plt.figure(figsize=(10, 5.5))
            piv.plot(kind="bar", stacked=True, ax=plt.gca())
            plt.title("Co-menciones de delitos y lugares por noticia")
            plt.xlabel("Lugar")
            plt.ylabel("Cantidad de co-menciones")
            plt.xticks(rotation=45, ha="right")
            plt.legend(title="Delito", fontsize=7)
            self._guardar_fig(self.fig_dir / "04_delitos_por_lugar.png")
        return conteo

    def entidades_por_noticia(self) -> pd.DataFrame:
        filas = [
            {
                "id_noticia": n.get("id_noticia"),
                "personas": len(n.get("personas", [])),
                "organizaciones": len(n.get("organizaciones", [])),
            }
            for n in self.noticias
        ]
        df = pd.DataFrame(filas)
        if not df.empty:
            ax = df.set_index("id_noticia")[["personas", "organizaciones"]].plot(kind="bar", figsize=(10, 5))
            ax.set_title("Entidades extraídas por noticia")
            ax.set_xlabel("ID de noticia")
            ax.set_ylabel("Cantidad de entidades")
            plt.xticks(rotation=45, ha="right")
            self._guardar_fig(self.fig_dir / "05_entidades_por_noticia.png")
        return df

    def campos_faltantes(self) -> pd.Series:
        total = max(len(self.noticias), 1)
        faltantes: dict[str, int] = {}
        for campo in self.CAMPOS:
            cuenta = 0
            for n in self.noticias:
                valor = n.get(campo)
                if valor is None or valor == "" or valor == [] or valor == {}:
                    cuenta += 1
            faltantes[campo] = cuenta
        serie = pd.Series({k: 100 * v / total for k, v in faltantes.items()}).sort_values(ascending=False)
        if len(self.noticias) > 0:
            plt.figure(figsize=(9, 5))
            serie.sort_values().plot(kind="barh")
            plt.title("Porcentaje de noticias con campo faltante o vacío")
            plt.xlabel("Porcentaje de noticias (%)")
            plt.ylabel("Campo JSON")
            plt.xlim(0, 100)
            self._guardar_fig(self.fig_dir / "06_campos_faltantes.png")
        return serie

    @staticmethod
    def _parse_fecha(valor: Any) -> datetime | None:
        if not valor:
            return None
        texto = str(valor).strip()
        for candidato in (texto, texto[:10]):
            try:
                return datetime.fromisoformat(candidato.replace("Z", "+00:00"))
            except ValueError:
                continue
        return None

    def evolucion_temporal(self) -> pd.Series:
        fechas = [self._parse_fecha(n.get("fecha_publicacion")) for n in self.noticias]
        fechas = [f for f in fechas if f is not None]
        if not fechas:
            return pd.Series(dtype="int64")
        meses = pd.Series([f.strftime("%Y-%m") for f in fechas]).value_counts().sort_index()
        plt.figure(figsize=(8, 4.5))
        meses.plot(kind="line", marker="o")
        plt.title("Evolución temporal del corpus")
        plt.xlabel("Mes de publicación")
        plt.ylabel("Cantidad de noticias")
        plt.xticks(rotation=45, ha="right")
        self._guardar_fig(self.fig_dir / "07_evolucion_temporal.png")
        return meses

    @staticmethod
    def _clave(texto: str) -> str:
        texto = unicodedata.normalize("NFKD", str(texto))
        texto = "".join(c for c in texto if not unicodedata.combining(c))
        return re.sub(r"\W+", " ", texto).strip().casefold()

    def _duplicados(self) -> list[dict[str, Any]]:
        resultados: list[dict[str, Any]] = []
        for campo in ("url", "titulo"):
            indice: dict[str, list[str]] = defaultdict(list)
            for n in self.noticias:
                valor = str(n.get(campo) or "").strip()
                if valor:
                    indice[self._clave(valor)].append(str(n.get("id_noticia")))
            for clave, ids in indice.items():
                if len(ids) > 1:
                    resultados.append({"campo": campo, "clave_normalizada": clave, "ids": ids})
        return resultados

    def _inconsistencias_entidades(self) -> list[dict[str, Any]]:
        variantes: dict[str, set[str]] = defaultdict(set)
        for n in self.noticias:
            for campo in ("delitos", "organizaciones", "lugares"):
                for valor in n.get(campo, []):
                    variantes[self._clave(str(valor))].add(str(valor))
            for p in n.get("personas", []):
                if isinstance(p, dict) and p.get("nombre"):
                    variantes[self._clave(str(p["nombre"]))].add(str(p["nombre"]))
        return [
            {"clave": k, "variantes": sorted(v)}
            for k, v in variantes.items()
            if k and len(v) > 1
        ]

    def _relaciones_dudosas(self) -> list[str]:
        dudas: list[str] = []
        for ruta in sorted(self.validation_dir.glob("*.validation.json")) if self.validation_dir.exists() else []:
            try:
                data = json.loads(ruta.read_text(encoding="utf-8"))
                for adv in data.get("advertencias", []):
                    if "Relación" in adv:
                        dudas.append(f"{ruta.stem}: {adv}")
            except Exception:
                continue
        return dudas

    def ejecutar(self) -> dict[str, Any]:
        por_fuente = self.noticias_por_fuente()
        delitos = self.delitos_frecuentes()
        lugares = self.lugares_frecuentes()
        delitos_lugar = self.delitos_por_lugar()
        entidades = self.entidades_por_noticia()
        faltantes = self.campos_faltantes()
        temporal = self.evolucion_temporal()

        personas_unicas = {
            self._clave(p.get("nombre"))
            for n in self.noticias
            for p in n.get("personas", [])
            if isinstance(p, dict) and p.get("nombre")
        }
        org_unicas = {
            self._clave(o)
            for n in self.noticias
            for o in n.get("organizaciones", [])
            if o
        }
        relaciones = sum(len(n.get("relaciones", [])) for n in self.noticias)
        resumen = {
            "noticias_procesadas": len(self.noticias),
            "json_invalidos": len(self.json_invalidos),
            "fuentes": por_fuente.to_dict(),
            "delitos_frecuentes": delitos.to_dict(),
            "lugares_frecuentes": lugares.to_dict(),
            "personas_unicas": len(personas_unicas),
            "organizaciones_unicas": len(org_unicas),
            "relaciones_extraidas": relaciones,
            "porcentaje_campos_faltantes": {k: round(float(v), 2) for k, v in faltantes.to_dict().items()},
            "noticias_duplicadas": self._duplicados(),
            "entidades_inconsistentes": self._inconsistencias_entidades(),
            "relaciones_dudosas": self._relaciones_dudosas(),
            "json_invalidos_detalle": self.json_invalidos,
        }
        (self.output_dir / "resumen_data_understanding.json").write_text(
            json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        if not delitos_lugar.empty:
            delitos_lugar.to_csv(self.output_dir / "delitos_por_lugar.csv", index=False)
        if not entidades.empty:
            entidades.to_csv(self.output_dir / "entidades_por_noticia.csv", index=False)
        pd.DataFrame({"campo": faltantes.index, "porcentaje_faltante": faltantes.values}).to_csv(
            self.output_dir / "campos_faltantes.csv", index=False
        )

        self._escribir_interpretacion(resumen, temporal)
        return resumen

    def _escribir_interpretacion(self, resumen: dict[str, Any], temporal: pd.Series) -> None:
        fuentes = resumen["fuentes"]
        top_fuente = next(iter(fuentes.items()), ("Sin datos", 0))
        delitos = resumen["delitos_frecuentes"]
        top_delito = next(iter(delitos.items()), ("Sin datos", 0))
        lugares = resumen["lugares_frecuentes"]
        top_lugar = next(iter(lugares.items()), ("Sin datos", 0))
        max_faltante = next(iter(resumen["porcentaje_campos_faltantes"].items()), ("Sin datos", 0.0))
        lineas = [
            "# Data Understanding — interpretación de visualizaciones",
            "",
            f"Se analizaron **{resumen['noticias_procesadas']}** JSON legibles. Se detectaron **{resumen['json_invalidos']}** archivos JSON inválidos.",
            "",
            "## 01. Noticias por fuente",
            f"El gráfico muestra la cobertura por medio. La fuente con más registros es **{top_fuente[0]}** ({top_fuente[1]} noticias). Esto permite identificar concentración de cobertura; no debe interpretarse como mayor incidencia delictual real, porque el corpus depende de la selección de noticias y de la agenda de cada medio.",
            "",
            "## 02. Delitos frecuentes",
            f"El tipo más repetido en la extracción es **{top_delito[0]}** ({top_delito[1]} menciones a nivel de noticia). El patrón describe el corpus periodístico seleccionado, no una tasa delictual poblacional ni estadística policial oficial.",
            "",
            "## 03. Lugares frecuentes",
            f"El lugar con más menciones es **{top_lugar[0]}** ({top_lugar[1]}). La concentración puede reflejar el alcance geográfico definido, la mayor producción noticiosa en comunas urbanas o la selección de fuentes; no demuestra por sí sola mayor riesgo delictual.",
            "",
            "## 04. Delitos por lugar",
            "La visualización apila **co-menciones dentro de una misma noticia**. Sirve para explorar conexiones documentales, pero no implica una relación causal ni reemplaza estadísticas oficiales por comuna.",
            "",
            "## 05. Personas y organizaciones por noticia",
            "El gráfico permite detectar notas densas en entidades y otras con poca información explícita. Valores altos suelen corresponder a operativos u organizaciones; valores bajos pueden reflejar hechos sin identidades publicadas o restricciones editoriales.",
            "",
            "## 06. Campos faltantes",
            f"El mayor porcentaje de ausencia corresponde a **{max_faltante[0]}** ({max_faltante[1]:.1f}%). En campos de personas, objetos o relaciones, una lista vacía puede ser correcta: la regla del laboratorio es no inventar información ausente.",
            "",
            "## 07. Evolución temporal",
            "La serie temporal describe cuándo se publicaron las noticias del corpus. Con una muestra pequeña, no debe interpretarse como tendencia criminal: está afectada por la ventana de recolección y la disponibilidad de artículos.",
            "",
            "## Calidad del corpus",
            f"Duplicados detectados: **{len(resumen['noticias_duplicadas'])}** grupos. Variantes potencialmente inconsistentes de entidades: **{len(resumen['entidades_inconsistentes'])}**. Advertencias de relaciones: **{len(resumen['relaciones_dudosas'])}**.",
            "",
            "Las advertencias requieren revisión humana porque las equivalencias nominales y el respaldo semántico de una relación no pueden resolverse de forma segura mediante similitud textual agresiva.",
        ]
        (self.output_dir / "interpretacion_visualizaciones.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
