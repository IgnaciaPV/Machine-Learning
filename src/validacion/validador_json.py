"""Validación independiente de las salidas del LLM."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from pydantic import ValidationError

from src.modelos import NoticiaEstructurada, NoticiaFuente, ResultadoValidacion


class ValidadorJSON:
    CAMPOS_OBLIGATORIOS = [
        "id_noticia",
        "titulo",
        "fecha_publicacion",
        "fuente",
        "url",
        "resumen",
        "delitos",
        "personas",
        "organizaciones",
        "lugares",
        "objetos",
        "relaciones",
    ]

    @staticmethod
    def _url_comparable(url: str) -> str:
        partes = urlsplit(url.strip())
        path = partes.path.rstrip("/") or "/"
        return urlunsplit((partes.scheme.lower(), partes.netloc.lower(), path, partes.query, ""))

    @staticmethod
    def _entidades(data: dict[str, Any]) -> set[str]:
        valores: set[str] = set()
        for campo in ("delitos", "organizaciones", "lugares"):
            valores.update(str(x).strip().casefold() for x in data.get(campo, []) if str(x).strip())
        for p in data.get("personas", []):
            if isinstance(p, dict) and p.get("nombre"):
                valores.add(str(p["nombre"]).strip().casefold())
        for o in data.get("objetos", []):
            if isinstance(o, dict):
                if o.get("nombre"):
                    valores.add(str(o["nombre"]).strip().casefold())
                if o.get("tipo"):
                    valores.add(str(o["tipo"]).strip().casefold())
        return valores

    def validar(
        self,
        ruta: Path,
        esperado: NoticiaFuente | None = None,
        reporte_dir: Path | None = None,
    ) -> ResultadoValidacion:
        errores: list[str] = []
        advertencias: list[str] = []
        data: dict[str, Any] | None = None

        try:
            texto = Path(ruta).read_text(encoding="utf-8")
            data = json.loads(texto)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errores.append(f"JSON ilegible o sintácticamente inválido: {exc}")

        if isinstance(data, dict):
            faltantes = [c for c in self.CAMPOS_OBLIGATORIOS if c not in data]
            if faltantes:
                errores.append("Campos obligatorios ausentes: " + ", ".join(faltantes))
            try:
                modelo = NoticiaEstructurada.model_validate(data)
                data = modelo.model_dump(mode="json")
            except ValidationError as exc:
                errores.append("Tipos/estructura incompatibles: " + str(exc).replace("\n", " | "))

        if isinstance(data, dict) and not errores:
            if not str(data.get("id_noticia", "")).strip():
                errores.append("id_noticia vacío")
            for campo in ("titulo", "fuente", "url"):
                if data.get(campo) is None or not str(data.get(campo)).strip():
                    errores.append(f"Campo trazable vacío: {campo}")

            if esperado is not None:
                if data.get("id_noticia") != esperado.id_noticia:
                    errores.append(
                        f"id_noticia no coincide con trazabilidad: {data.get('id_noticia')} != {esperado.id_noticia}"
                    )
                if str(data.get("fuente", "")).strip() != esperado.fuente.strip():
                    errores.append("fuente no coincide con data/urls.csv")
                try:
                    if self._url_comparable(str(data.get("url", ""))) != self._url_comparable(esperado.url):
                        errores.append("url no coincide con data/urls.csv")
                except Exception:
                    errores.append("url no pudo compararse con data/urls.csv")

            entidades = self._entidades(data)
            for idx, rel in enumerate(data.get("relaciones", []), start=1):
                if not isinstance(rel, dict):
                    continue
                origen = str(rel.get("origen", "")).strip()
                destino = str(rel.get("destino", "")).strip()
                tipo = str(rel.get("tipo", "")).strip()
                if not origen or not destino or not tipo:
                    errores.append(f"Relación {idx} incompleta")
                    continue
                if not re.fullmatch(r"[A-ZÁÉÍÓÚÜÑ0-9_]+", tipo):
                    advertencias.append(f"Relación {idx} usa tipo no normalizado: {tipo}")
                if origen.casefold() not in entidades:
                    advertencias.append(f"Relación {idx}: origen no aparece entre entidades: {origen}")
                if destino.casefold() not in entidades:
                    advertencias.append(f"Relación {idx}: destino no aparece entre entidades: {destino}")

        resultado = ResultadoValidacion(
            id_noticia=(esperado.id_noticia if esperado else Path(ruta).stem),
            valido=not errores,
            errores=errores,
            advertencias=advertencias,
            ruta=str(ruta),
        )
        if reporte_dir is not None:
            reporte_dir.mkdir(parents=True, exist_ok=True)
            (reporte_dir / f"{resultado.id_noticia}.validation.json").write_text(
                json.dumps(resultado.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
            )
        return resultado
