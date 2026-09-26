"""Orquestación del pipeline completo del Laboratorio 01."""
from __future__ import annotations

import csv
import json
import logging
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.adquisicion import DescubridorGoogleNews, FabricaCapturadores
from src.analisis import ExploradorDatos
from src.conocimiento import EscritorVaultObsidian
from src.extraccion import ExtractorGemini
from src.limpieza import LimpiadorHTML
from src.modelos import NoticiaFuente, ResumenPipeline
from src.validacion import ValidadorJSON

LOGGER = logging.getLogger(__name__)


class PipelineLaboratorio:
    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.data = self.root / "data"
        self.raw_dir = self.data / "raw"
        self.processed_dir = self.data / "processed"
        self.json_dir = self.data / "json"
        self.validation_dir = self.data / "validation"
        self.llm_raw_dir = self.data / "llm_raw"
        self.outputs = self.root / "outputs"
        self.vault = self.root / "obsidian_vault"
        self.docs = self.root / "docs"
        for p in [
            self.raw_dir,
            self.processed_dir,
            self.json_dir,
            self.validation_dir,
            self.llm_raw_dir,
            self.outputs,
            self.vault,
            self.docs,
        ]:
            p.mkdir(parents=True, exist_ok=True)
        self.fabrica = FabricaCapturadores()
        self.limpiador = LimpiadorHTML()
        self.validador = ValidadorJSON()

    def leer_urls(self) -> list[NoticiaFuente]:
        ruta = self.data / "urls.csv"
        if not ruta.exists():
            raise FileNotFoundError(f"No existe {ruta}")
        noticias: list[NoticiaFuente] = []
        ids: set[str] = set()
        urls: set[str] = set()
        with ruta.open(encoding="utf-8", newline="") as f:
            for fila in csv.DictReader(f):
                nid = fila.get("id_noticia", "").strip()
                url = fila.get("url", "").strip()
                fuente = fila.get("fuente", "").strip()
                if not nid or not url or not fuente:
                    raise ValueError(f"Fila incompleta en urls.csv: {fila}")
                if nid in ids:
                    raise ValueError(f"id_noticia duplicado en urls.csv: {nid}")
                if url in urls:
                    LOGGER.warning("URL duplicada en urls.csv: %s", url)
                ids.add(nid)
                urls.add(url)
                noticias.append(
                    NoticiaFuente(
                        id_noticia=nid,
                        fuente=fuente,
                        url=url,
                        categoria_busqueda=fila.get("categoria_busqueda", "").strip(),
                    )
                )
        return noticias

    def descubrir(self) -> dict[str, int]:
        descubridor = DescubridorGoogleNews()
        return descubridor.actualizar_urls_csv(
            self.data / "consultas.csv", self.data / "urls.csv"
        )

    def _meta_path(self, nid: str) -> Path:
        return self.raw_dir / f"{nid}.meta.json"

    def _leer_meta(self, nid: str) -> dict[str, Any]:
        ruta = self._meta_path(nid)
        if ruta.exists():
            try:
                return json.loads(ruta.read_text(encoding="utf-8"))
            except Exception as exc:
                LOGGER.warning("Meta corrupta %s: %s", ruta, exc)
        return {}

    def _guardar_processed(self, noticia: NoticiaFuente, cuerpo: str) -> None:
        ruta = self.processed_dir / f"{noticia.id_noticia}.txt"
        texto = (
            f"ID_NOTICIA: {noticia.id_noticia}\n"
            f"TITULO: {noticia.titulo or ''}\n"
            f"FECHA_PUBLICACION: {noticia.fecha_publicacion or ''}\n"
            f"FUENTE: {noticia.fuente}\n"
            f"URL: {noticia.url}\n"
            "\nCUERPO_NOTICIA:\n"
            f"{cuerpo.strip()}\n"
        )
        ruta.write_text(texto, encoding="utf-8")
        noticia.texto = texto
        noticia.ruta_processed = ruta

    def capturar(self, forzar: bool = False) -> ResumenPipeline:
        noticias = self.leer_urls()
        resumen = ResumenPipeline(solicitadas=len(noticias))
        for noticia in noticias:
            raw_path = self.raw_dir / f"{noticia.id_noticia}.html"
            noticia.ruta_raw = raw_path
            try:
                capturador = self.fabrica.para(noticia.url, noticia.fuente)
                meta: dict[str, Any] = {}
                if raw_path.exists() and not forzar:
                    html = raw_path.read_text(encoding="utf-8")
                    meta = self._leer_meta(noticia.id_noticia)
                    LOGGER.info("%s usa RAW en caché (%s)", noticia.id_noticia, meta.get("modo", "cache"))
                else:
                    try:
                        captura = capturador.capturar(noticia.url)
                        html = captura.html
                        meta = asdict(captura)
                        meta.pop("html", None)
                        raw_path.write_text(html, encoding="utf-8")
                        self._meta_path(noticia.id_noticia).write_text(
                            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
                        )
                    except Exception:
                        if raw_path.exists():
                            html = raw_path.read_text(encoding="utf-8")
                            meta = self._leer_meta(noticia.id_noticia)
                            LOGGER.exception(
                                "%s falló captura live; se conserva snapshot/caché existente", noticia.id_noticia
                            )
                        else:
                            raise

                resumen.capturadas += 1
                articulo_html = capturador.extraer_cuerpo(html)
                limpio = self.limpiador.limpiar_documento(articulo_html)
                noticia.titulo = meta.get("titulo") or limpio.titulo
                noticia.fecha_publicacion = meta.get("fecha_publicacion") or limpio.fecha_publicacion
                if not limpio.cuerpo:
                    raise ValueError("Limpieza produjo cuerpo vacío")
                self._guardar_processed(noticia, limpio.cuerpo)
                resumen.limpiadas += 1
            except Exception as exc:
                LOGGER.exception("Fallo id=%s etapa=capturar url=%s", noticia.id_noticia, noticia.url)
                resumen.errores.append(
                    {
                        "id_noticia": noticia.id_noticia,
                        "etapa": "capturar",
                        "url": noticia.url,
                        "causa": f"{type(exc).__name__}: {exc}",
                    }
                )
        self._guardar_resumen("captura", resumen.to_dict())
        return resumen

    def _cargar_processed(self, noticia: NoticiaFuente) -> NoticiaFuente:
        ruta = self.processed_dir / f"{noticia.id_noticia}.txt"
        if not ruta.exists():
            raise FileNotFoundError(f"No existe texto procesado para {noticia.id_noticia}")
        texto = ruta.read_text(encoding="utf-8")
        noticia.texto = texto
        noticia.ruta_processed = ruta
        for linea in texto.splitlines()[:8]:
            if linea.startswith("TITULO:"):
                noticia.titulo = linea.split(":", 1)[1].strip() or None
            elif linea.startswith("FECHA_PUBLICACION:"):
                noticia.fecha_publicacion = linea.split(":", 1)[1].strip() or None
        return noticia

    def extraer(self, forzar: bool = False) -> ResumenPipeline:
        noticias = self.leer_urls()
        resumen = ResumenPipeline(solicitadas=len(noticias))
        extractor = ExtractorGemini(
            salida_dir=self.json_dir,
            raw_dir=self.llm_raw_dir,
        )
        # Credenciales/SDK/modelo son dependencias sistémicas: si faltan, no se simula éxito por noticia.
        extractor.verificar_disponibilidad()
        for noticia in noticias:
            try:
                self._cargar_processed(noticia)
                ruta_json = self.json_dir / f"{noticia.id_noticia}.json"
                usar_existente = False
                if ruta_json.exists() and not forzar:
                    previo = self.validador.validar(ruta_json, noticia, self.validation_dir)
                    usar_existente = previo.valido
                if not usar_existente:
                    extractor.extraer(noticia)
                validacion = self.validador.validar(ruta_json, noticia, self.validation_dir)
                if validacion.valido:
                    resumen.json_validos += 1
                else:
                    resumen.json_fallidos += 1
                    resumen.errores.append(
                        {
                            "id_noticia": noticia.id_noticia,
                            "etapa": "validacion",
                            "url": noticia.url,
                            "causa": "; ".join(validacion.errores),
                        }
                    )
            except Exception as exc:
                resumen.json_fallidos += 1
                LOGGER.exception("Fallo id=%s etapa=extraer", noticia.id_noticia)
                resumen.errores.append(
                    {
                        "id_noticia": noticia.id_noticia,
                        "etapa": "extraer",
                        "url": noticia.url,
                        "causa": f"{type(exc).__name__}: {exc}",
                    }
                )
        self._guardar_resumen("extraccion", resumen.to_dict())
        return resumen

    def cargar_json_validos(self) -> list[dict[str, Any]]:
        validos: list[dict[str, Any]] = []
        mapa = {n.id_noticia: n for n in self.leer_urls()}
        for ruta in sorted(self.json_dir.glob("N*.json")):
            esperado = mapa.get(ruta.stem)
            if not esperado:
                continue
            resultado = self.validador.validar(ruta, esperado, self.validation_dir)
            if resultado.valido:
                validos.append(json.loads(ruta.read_text(encoding="utf-8")))
        return validos

    def obsidian(self) -> dict[str, Any]:
        noticias = self.cargar_json_validos()
        if not noticias:
            raise RuntimeError("No existen JSON válidos para generar Obsidian")
        escritor = EscritorVaultObsidian(self.vault)
        escritor.escribir_vault(noticias)
        rotos = escritor.auditar_enlaces()
        if rotos:
            raise RuntimeError("Se detectaron enlaces rotos en el vault: " + "; ".join(rotos[:10]))
        md = list(self.vault.rglob("*.md"))
        resultado = {
            "noticias": len(noticias),
            "archivos_markdown": len(md),
            "enlaces_rotos": rotos,
        }
        self._guardar_resumen("obsidian", resultado)
        return resultado

    def analizar(self) -> dict[str, Any]:
        explorador = ExploradorDatos(
            json_dir=self.json_dir,
            output_dir=self.outputs,
            validation_dir=self.validation_dir,
        )
        resumen = explorador.ejecutar()
        self._guardar_resumen("analisis", resumen)
        return resumen

    def pipeline(self, incluir_descubrimiento: bool = True, forzar: bool = False) -> dict[str, Any]:
        resultado: dict[str, Any] = {}
        if incluir_descubrimiento:
            try:
                resultado["descubrir"] = self.descubrir()
            except Exception as exc:
                # Un problema de RSS no invalida un corpus semilla verificado.
                LOGGER.exception("Descubrimiento RSS falló; continúa con data/urls.csv")
                resultado["descubrir"] = {"error": f"{type(exc).__name__}: {exc}"}
        captura = self.capturar(forzar=forzar)
        resultado["capturar"] = captura.to_dict()
        extraccion = self.extraer(forzar=forzar)
        resultado["extraer"] = extraccion.to_dict()
        if extraccion.json_validos:
            resultado["obsidian"] = self.obsidian()
            resultado["analizar"] = self.analizar()
        self._guardar_resumen("pipeline", resultado)
        return resultado

    def _guardar_resumen(self, nombre: str, data: dict[str, Any]) -> None:
        logs = self.root / "logs"
        logs.mkdir(exist_ok=True)
        payload = {
            "etapa": nombre,
            "generado_en": datetime.now(timezone.utc).isoformat(),
            "resultado": data,
        }
        (logs / f"ultimo_{nombre}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
