"""Descubrimiento académico de URLs vía RSS público de Google News."""
from __future__ import annotations

import csv
import logging
from pathlib import Path
from urllib.parse import urlencode

from .cliente_http import ClienteHTTP

LOGGER = logging.getLogger(__name__)
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"


class DescubridorGoogleNews:
    """No scrapea news.google.com: consume su RSS público para Chile."""

    def __init__(self, cliente: ClienteHTTP | None = None) -> None:
        self.cliente = cliente or ClienteHTTP()

    def buscar(self, consulta: str, limite: int = 5):
        try:
            import feedparser
        except ImportError as exc:
            raise RuntimeError("Falta feedparser. Cree/active el entorno conda de environment.yml.") from exc

        params = {"q": consulta, "hl": "es-419", "gl": "CL", "ceid": "CL:es-419"}
        url = GOOGLE_NEWS_RSS + "?" + urlencode(params)
        # feedparser puede abrir URL directamente, pero usar bytes obtenidos por nuestro cliente
        # mantiene timeout, User-Agent y manejo de errores bajo un único componente.
        respuesta = self.cliente.obtener(url)
        feed = feedparser.parse(respuesta.content)
        return list(feed.entries)[:limite]

    def resolver_url_final(self, link_google: str) -> str:
        return self.cliente.url_final(link_google)

    def actualizar_urls_csv(self, consultas: Path, urls_csv: Path) -> dict[str, int]:
        filas_existentes: list[dict[str, str]] = []
        urls_existentes: set[str] = set()
        if urls_csv.exists():
            with urls_csv.open(encoding="utf-8", newline="") as f:
                for fila in csv.DictReader(f):
                    filas_existentes.append(fila)
                    urls_existentes.add(fila.get("url", "").strip())

        max_id = 0
        for fila in filas_existentes:
            valor = fila.get("id_noticia", "")
            if valor.startswith("N") and valor[1:].isdigit():
                max_id = max(max_id, int(valor[1:]))

        nuevas: list[dict[str, str]] = []
        with consultas.open(encoding="utf-8", newline="") as f:
            for consulta in csv.DictReader(f):
                q = consulta["consulta"].strip()
                categoria = consulta.get("categoria_busqueda", "").strip()
                limite = int(consulta.get("limite", 5) or 5)
                for entrada in self.buscar(q, limite=limite):
                    enlace = str(getattr(entrada, "link", "")).strip()
                    if not enlace:
                        continue
                    final = self.resolver_url_final(enlace)
                    if final in urls_existentes:
                        continue
                    max_id += 1
                    fuente = getattr(entrada, "source", None)
                    fuente_nombre = "Google News"
                    if isinstance(fuente, dict):
                        fuente_nombre = str(fuente.get("title") or fuente_nombre)
                    nuevas.append(
                        {
                            "id_noticia": f"N{max_id:03d}",
                            "fuente": fuente_nombre,
                            "url": final,
                            "categoria_busqueda": categoria,
                        }
                    )
                    urls_existentes.add(final)

        todas = filas_existentes + nuevas
        urls_csv.parent.mkdir(parents=True, exist_ok=True)
        with urls_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["id_noticia", "fuente", "url", "categoria_busqueda"]
            )
            writer.writeheader()
            writer.writerows(todas)
        LOGGER.info("Descubrimiento: %d URL nuevas; total %d", len(nuevas), len(todas))
        return {"nuevas": len(nuevas), "total": len(todas)}
