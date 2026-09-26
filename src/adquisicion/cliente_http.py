"""Cliente HTTP responsable y tolerante a fallos para uso académico."""
from __future__ import annotations

import logging
import re
import time
from urllib.parse import urlparse

import requests

LOGGER = logging.getLogger(__name__)


class ClienteHTTP:
    def __init__(self, timeout: int = 20, pausa: float = 1.0) -> None:
        self.timeout = timeout
        self.pausa = pausa
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (compatible; UCN-ML-LAB01-Academic/1.0; "
                    "+educational-research)"
                )
            }
        )

    def obtener(self, url: str) -> requests.Response:
        if urlparse(url).scheme not in {"http", "https"}:
            raise ValueError(f"URL no HTTP(S): {url}")
        if self.pausa > 0:
            time.sleep(self.pausa)
        respuesta = self.session.get(url, timeout=self.timeout, allow_redirects=True)
        respuesta.raise_for_status()
        return respuesta

    def obtener_html(self, url: str) -> tuple[str, str]:
        respuesta = self.obtener(url)

        # requests puede asumir ISO-8859-1 cuando el servidor no declara charset en
        # Content-Type, aun cuando el propio HTML declare UTF-8. Respetamos primero
        # esa declaración para evitar mojibake en nombres, lugares y entidades.
        cabecera = respuesta.content[:8192].lower()
        declara_utf8 = bool(
            re.search(br"charset\s*=\s*['\"]?utf-?8", cabecera)
        )
        if declara_utf8:
            respuesta.encoding = "utf-8"
        elif respuesta.encoding is None or respuesta.encoding.lower() in {"iso-8859-1", "latin-1"}:
            respuesta.encoding = respuesta.apparent_encoding or "utf-8"

        return respuesta.text, respuesta.url

    def url_final(self, url: str) -> str:
        try:
            _, final = self.obtener_html(url)
            return final
        except requests.RequestException as exc:
            LOGGER.warning("No fue posible resolver redirect de %s: %s", url, exc)
            return url
