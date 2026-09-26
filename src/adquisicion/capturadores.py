"""Capturadores OOP y fábrica de adaptadores por medio."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Iterable
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .cliente_http import ClienteHTTP


@dataclass(slots=True)
class CapturaWeb:
    html: str
    url_final: str
    titulo: str | None
    fecha_publicacion: str | None
    capturado_en: str
    modo: str = "http_live"


class CapturadorFuente(ABC):
    def __init__(self, cliente: ClienteHTTP) -> None:
        self.cliente = cliente

    @abstractmethod
    def acepta(self, url: str, fuente: str | None = None) -> bool:
        ...

    def obtener_html(self, url: str) -> tuple[str, str]:
        return self.cliente.obtener_html(url)

    def selectores_articulo(self) -> Iterable[str]:
        return ("article", "main")

    def extraer_cuerpo(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        for selector in self.selectores_articulo():
            nodo = soup.select_one(selector)
            if nodo:
                return str(nodo)
        return html

    @staticmethod
    def extraer_metadatos(html: str) -> tuple[str | None, str | None]:
        soup = BeautifulSoup(html, "lxml")
        h1 = soup.find("h1")
        titulo = h1.get_text(" ", strip=True) if h1 else None
        if not titulo and soup.title:
            titulo = soup.title.get_text(" ", strip=True)

        fecha = None
        candidatos = [
            ("meta", {"property": "article:published_time"}, "content"),
            ("meta", {"name": "date"}, "content"),
            ("time", {}, "datetime"),
        ]
        for etiqueta, attrs, atributo in candidatos:
            nodo = soup.find(etiqueta, attrs=attrs)
            if nodo and nodo.get(atributo):
                fecha = str(nodo.get(atributo)).strip()
                break
        return titulo, fecha

    def capturar(self, url: str) -> CapturaWeb:
        html, url_final = self.obtener_html(url)
        titulo, fecha = self.extraer_metadatos(html)
        return CapturaWeb(
            html=html,
            url_final=url_final,
            titulo=titulo,
            fecha_publicacion=fecha,
            capturado_en=datetime.now(timezone.utc).isoformat(),
        )


class CapturadorBioBioChile(CapturadorFuente):
    def acepta(self, url: str, fuente: str | None = None) -> bool:
        return "biobiochile.cl" in urlparse(url).netloc.lower() or (fuente or "").lower().startswith("biobio")

    def selectores_articulo(self) -> Iterable[str]:
        # BioBioChile incluye muchos elementos <article> de tarjetas/recomendaciones antes
        # del cuerpo. El contenedor banners-contenido-nota-* contiene el texto editorial
        # de la noticia y excluye el resumen automático mostrado por el sitio.
        return (
            "[class^='banners-contenido-nota-']",
            ".post-content",
            ".article-content",
            "article",
            "main",
        )


class CapturadorCooperativa(CapturadorFuente):
    def acepta(self, url: str, fuente: str | None = None) -> bool:
        return "cooperativa.cl" in urlparse(url).netloc.lower() or (fuente or "").lower().startswith("cooperativa")

    def selectores_articulo(self) -> Iterable[str]:
        # En cooperativa.cl las páginas no AMP incluyen múltiples <article>
        # (titular, relacionados, tarjetas). El cuerpo editorial estable está en
        # .cuerpo-articulo; en AMP también está disponible.
        return (".cuerpo-articulo", ".contenedor-cuerpo", ".cuerpo", ".article-content", "article", "main")

    def capturar(self, url: str) -> CapturaWeb:
        captura = super().capturar(url)
        if not captura.fecha_publicacion:
            # Algunas variantes AMP/no-AMP no exponen article:published_time.
            # La fecha sí está codificada explícitamente en la URL oficial.
            m = re.search(r"/(20\d{2})-(\d{2})-(\d{2})/", captura.url_final)
            if m:
                captura.fecha_publicacion = "-".join(m.groups())
            else:
                m = re.search(r"/(20\d{2})(\d{2})(\d{2})/", captura.url_final)
                if m:
                    captura.fecha_publicacion = "-".join(m.groups())
        return captura


class CapturadorLaTercera(CapturadorFuente):
    def acepta(self, url: str, fuente: str | None = None) -> bool:
        return "latercera.com" in urlparse(url).netloc.lower() or "tercera" in (fuente or "").lower()

    def selectores_articulo(self) -> Iterable[str]:
        return ("article", "main article", ".article-body", "main")


class CapturadorGenerico(CapturadorFuente):
    def acepta(self, url: str, fuente: str | None = None) -> bool:
        return True


class FabricaCapturadores:
    def __init__(self, cliente: ClienteHTTP | None = None) -> None:
        cliente = cliente or ClienteHTTP()
        self._especificos = [
            CapturadorBioBioChile(cliente),
            CapturadorCooperativa(cliente),
            CapturadorLaTercera(cliente),
        ]
        self.generico = CapturadorGenerico(cliente)

    def para(self, url: str, fuente: str | None = None) -> CapturadorFuente:
        for capturador in self._especificos:
            if capturador.acepta(url, fuente):
                return capturador
        return self.generico
