"""Modelos de dominio y esquema estructurado del Laboratorio 01."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


@dataclass(slots=True)
class NoticiaFuente:
    """Noticia trazable a lo largo de todo el pipeline."""

    id_noticia: str
    fuente: str
    url: str
    categoria_busqueda: str = ""
    titulo: str | None = None
    fecha_publicacion: str | None = None
    texto: str | None = None
    ruta_raw: Path | None = None
    ruta_processed: Path | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in ("ruta_raw", "ruta_processed"):
            if data[key] is not None:
                data[key] = str(data[key])
        return data


class PersonaExtraida(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre: str = Field(description="Nombre o referencia tal como aparece en la fuente.")
    rol: str | None = Field(default=None, description="Rol explícito: víctima, detenido, imputado, fiscal, etc.")


class ObjetoExtraido(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tipo: str = Field(description="Tipo general del objeto: arma, sustancia, vehículo, dinero, etc.")
    nombre: str = Field(description="Nombre explícito del objeto.")
    cantidad: float | int | str | None = Field(default=None, description="Cantidad explícita, si aparece.")
    unidad: str | None = Field(default=None, description="Unidad explícita asociada a la cantidad.")


class RelacionExtraida(BaseModel):
    model_config = ConfigDict(extra="forbid")
    origen: str
    tipo: str = Field(description="Relación explícita en MAYÚSCULAS_CON_GUIONES_BAJOS.")
    destino: str


class NoticiaEstructurada(BaseModel):
    """Contrato mínimo de salida exigido por la pauta."""

    model_config = ConfigDict(extra="forbid")
    id_noticia: str
    titulo: str | None = None
    fecha_publicacion: str | None = None
    fuente: str
    url: str
    resumen: str | None = None
    delitos: list[str] = Field(default_factory=list)
    personas: list[PersonaExtraida] = Field(default_factory=list)
    organizaciones: list[str] = Field(default_factory=list)
    lugares: list[str] = Field(default_factory=list)
    objetos: list[ObjetoExtraido] = Field(default_factory=list)
    relaciones: list[RelacionExtraida] = Field(default_factory=list)


@dataclass(slots=True)
class ResultadoValidacion:
    id_noticia: str
    valido: bool
    errores: list[str] = field(default_factory=list)
    advertencias: list[str] = field(default_factory=list)
    ruta: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ResumenPipeline:
    solicitadas: int = 0
    capturadas: int = 0
    limpiadas: int = 0
    json_validos: int = 0
    json_fallidos: int = 0
    notas_generadas: int = 0
    errores: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
