"""Utilidades conservadoras para nombres de entidades y archivos Obsidian."""
from __future__ import annotations

import re
import unicodedata


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text)
    return text.strip("_") or "sin_nombre"


def normalizar_visual(text: str) -> str:
    """Normaliza espacios/codificación sin alterar identidad semántica."""
    return " ".join(unicodedata.normalize("NFC", str(text)).split()).strip()


def clave_entidad(text: str) -> str:
    """Clave exacta conservadora: ignora mayúsculas, acentos y espacios, no usa fuzzy matching."""
    value = normalizar_visual(text)
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"[^a-zA-Z0-9]+", " ", value).strip().casefold()
    return value
