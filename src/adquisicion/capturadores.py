"""Capturadores OOP y fábrica de adaptadores por medio."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
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
        return ("article", ".post-content", ".article-content", "main")


class CapturadorCooperativa(CapturadorFuente):
    def acepta(self, url: str, fuente: str | None = None) -> bool:
        return "cooperativa.cl" in urlparse(url).netloc.lower() or (fuente or "").lower().startswith("cooperativa")

    def selectores_articulo(self) -> Iterable[str]:
        return ("article", ".cuerpo", ".article-content", "main")


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
