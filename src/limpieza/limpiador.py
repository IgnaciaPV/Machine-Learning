"""Limpieza conservadora de HTML para preservar evidencia semántica."""
from __future__ import annotations

import html as html_lib
import re
from collections import Counter
from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass(slots=True)
class TextoLimpio:
    titulo: str | None
    fecha_publicacion: str | None
    cuerpo: str


class LimpiadorHTML:
    ETIQUETAS_RUIDO = ("script", "style", "nav", "footer", "aside", "form", "noscript")
    LARGO_MINIMO_LINEA = 40
    PATRONES_RUIDO = (
        r"^suscr[ií]bete\b",
        r"^s[ií]guenos\b",
        r"^revisa nuestra p[aá]gina",
        r"^¿?encontraste un error",
        r"^ver resumen$",
        r"^visitas$",
        r"^en vivo$",
        r"^publicidad$",
        r"^noticia patrocinada$",
    )

    def _soup(self, html: str) -> BeautifulSoup:
        try:
            return BeautifulSoup(html, "lxml")
        except Exception:
            return BeautifulSoup(html, "html.parser")

    @staticmethod
    def _normalizar_espacios(texto: str) -> str:
        texto = html_lib.unescape(texto)
        texto = texto.replace("\xa0", " ").replace("\t", " ")
        texto = re.sub(r"[ \f\v]+", " ", texto)
        texto = re.sub(r"\s+([,.;:!?])", r"\1", texto)
        return texto.strip()

    def _es_ruido(self, linea: str) -> bool:
        bajo = linea.casefold().strip()
        return any(re.search(p, bajo, re.IGNORECASE) for p in self.PATRONES_RUIDO)

    @staticmethod
    def _extraer_fecha(soup: BeautifulSoup) -> str | None:
        for selector, atributo in [
            ('meta[property="article:published_time"]', "content"),
            ('meta[name="date"]', "content"),
            ("time[datetime]", "datetime"),
        ]:
            nodo = soup.select_one(selector)
            if nodo and nodo.get(atributo):
                return str(nodo.get(atributo)).strip()
        # Snapshots académicos usan meta explícito.
        nodo = soup.select_one('meta[name="ucn:fecha_publicacion"]')
        if nodo and nodo.get("content"):
            return str(nodo.get("content")).strip()
        return None

    def limpiar_documento(self, html: str) -> TextoLimpio:
        soup = self._soup(html)
        for etiqueta in soup.find_all(self.ETIQUETAS_RUIDO):
            etiqueta.decompose()
        for selector in [
            ".advertisement", ".ads", ".ad", ".social-share", ".related", ".recomendados",
            "[aria-label='Publicidad']", "[data-ad]",
        ]:
            for nodo in soup.select(selector):
                nodo.decompose()

        h1 = soup.find("h1")
        titulo = self._normalizar_espacios(h1.get_text(" ", strip=True)) if h1 else None
        if not titulo and soup.title:
            titulo = self._normalizar_espacios(soup.title.get_text(" ", strip=True))
        fecha = self._extraer_fecha(soup)

        articulo = soup.find("article") or soup.find("main") or soup.body or soup
        lineas_crudas = [self._normalizar_espacios(x) for x in articulo.get_text("\n").splitlines()]
        lineas_crudas = [x for x in lineas_crudas if x]

        # Eliminar duplicados exactos frecuentes sin borrar una repetición significativa única.
        conteo = Counter(lineas_crudas)
        vistos: set[str] = set()
        lineas: list[str] = []
        for linea in lineas_crudas:
            if self._es_ruido(linea):
                continue
            if len(linea) < self.LARGO_MINIMO_LINEA and linea != titulo:
                continue
            clave = linea.casefold()
            if conteo[linea] > 1 and clave in vistos:
                continue
            vistos.add(clave)
            lineas.append(linea)

        if titulo:
            lineas = [ln for ln in lineas if ln.casefold() != titulo.casefold()]
        cuerpo = "\n".join(lineas).strip()
        return TextoLimpio(titulo=titulo, fecha_publicacion=fecha, cuerpo=cuerpo)

    def limpiar(self, html: str) -> str:
        return self.limpiar_documento(html).cuerpo
