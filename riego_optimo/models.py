"""
models.py — Clases de datos para el problema de Riego Óptimo.

Define las estructuras de datos fundamentales:
- Tablon: representa un tablón de la finca con sus parámetros.
- Finca: conjunto de tablones que conforman la finca.
- ResultadoTablon: resultado del riego de un tablón individual.
- Solucion: solución completa con permutación, costo y métricas.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Tablon:
    """
    Representa un tablón de la finca.

    Atributos:
        id: Identificador único del tablón (0-indexed).
        ts: Tiempo de supervivencia del tablón (debe ser > 0).
        tr: Duración del riego del tablón (debe ser > 0).
        p:  Prioridad del tablón (1–4, donde 4 es la más alta).
        rp: Momento perfecto para iniciar el riego (0 <= rp <= ts - tr).

    Validaciones:
        - ts > 0
        - tr > 0
        - 1 <= p <= 4
        - 0 <= rp <= ts - tr
    """
    id: int
    ts: int
    tr: int
    p: int
    rp: int

    def __post_init__(self) -> None:
        """Valida los parámetros del tablón al crear la instancia."""
        if self.ts <= 0:
            raise ValueError(
                f"Tablón {self.id}: ts debe ser > 0, se recibió {self.ts}"
            )
        if self.tr <= 0:
            raise ValueError(
                f"Tablón {self.id}: tr debe ser > 0, se recibió {self.tr}"
            )
        if not (1 <= self.p <= 4):
            raise ValueError(
                f"Tablón {self.id}: p debe estar entre 1 y 4, se recibió {self.p}"
            )
        if not (0 <= self.rp <= self.ts - self.tr):
            raise ValueError(
                f"Tablón {self.id}: rp debe estar entre 0 y {self.ts - self.tr} "
                f"(ts - tr), se recibió {self.rp}"
            )

    def __repr__(self) -> str:
        return (
            f"Tablon(id={self.id}, ts={self.ts}, tr={self.tr}, "
            f"p={self.p}, rp={self.rp})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tablon):
            return NotImplemented
        return (
            self.id == other.id
            and self.ts == other.ts
            and self.tr == other.tr
            and self.p == other.p
            and self.rp == other.rp
        )


@dataclass
class Finca:
    """
    Representa una finca compuesta por múltiples tablones.

    Atributos:
        tablones: Lista de objetos Tablon que conforman la finca.

    Propiedades:
        n: Número de tablones en la finca.

    Métodos:
        get_tablon(id): Retorna el tablón con el id especificado.
    """
    tablones: list[Tablon]

    @property
    def n(self) -> int:
        """Retorna el número de tablones en la finca."""
        return len(self.tablones)

    def get_tablon(self, tablon_id: int) -> Tablon:
        """
        Retorna el tablón con el id especificado.

        Args:
            tablon_id: Identificador del tablón a buscar.

        Returns:
            El objeto Tablon correspondiente.

        Raises:
            ValueError: Si no se encuentra un tablón con ese id.
        """
        for tablon in self.tablones:
            if tablon.id == tablon_id:
                return tablon
        raise ValueError(f"No se encontró tablón con id={tablon_id}")
    def __repr__(self) -> str:
        return f"Finca(n={self.n}, tablones={self.tablones})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Finca):
            return NotImplemented
        return self.tablones == other.tablones


@dataclass
class ResultadoTablon:
    """
    Resultado del riego de un tablón individual dentro de una solución.

    Atributos:
        tablon:      El tablón regado.
        t_inicio:    Momento en que comienza el riego.
        t_fin:       Momento en que termina el riego (t_inicio + tr).
        costo:       Costo individual del riego de este tablón.
        caso:        Caso de costo aplicado (1, 2 o 3).
        descripcion: Explicación legible del caso aplicado.
    """
    tablon: Tablon
    t_inicio: int
    t_fin: int
    costo: float
    caso: int
    descripcion: str

    def __repr__(self) -> str:
        return (
            f"ResultadoTablon(tablon_id={self.tablon.id}, "
            f"t_inicio={self.t_inicio}, t_fin={self.t_fin}, "
            f"costo={self.costo}, caso={self.caso})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResultadoTablon):
            return NotImplemented
        return (
            self.tablon == other.tablon
            and self.t_inicio == other.t_inicio
            and self.t_fin == other.t_fin
            and abs(self.costo - other.costo) < 1e-9
            and self.caso == other.caso
        )


@dataclass
class Solucion:
    """
    Solución completa al problema de riego óptimo.

    Atributos:
        permutacion:    Lista ordenada de ids de tablones (orden de riego).
        costo_total:    Costo total de riego CR.
        resultados:     Lista de ResultadoTablon para cada tablón.
        tiempo_computo: Tiempo en segundos que tomó el algoritmo.
        algoritmo:      Nombre del algoritmo ('FB', 'V' o 'PD').

    Métodos:
        resumen(): Retorna un resumen formateado de la solución.
    """
    permutacion: list[int]
    costo_total: float
    resultados: list[ResultadoTablon]
    tiempo_computo: float
    algoritmo: str
    def resumen(self) -> str:
        """
        Genera un resumen formateado de la solución para visualización.

        Returns:
            Cadena con el resumen detallado de la solución.
        """
        lineas = []
        lineas.append(f"═══ Solución — Algoritmo: {self.algoritmo} ═══")
        lineas.append(f"Permutación: {self.permutacion}")
        lineas.append(f"Costo total: {self.costo_total}")
        lineas.append(f"Tiempo de cómputo: {self.tiempo_computo * 1000:.2f} ms")
        lineas.append("")
        lineas.append(f"{'Pos':<5}{'Tablón':<8}{'t_ini':<7}{'t_fin':<7}"
                      f"{'ts':<5}{'rp':<5}{'Caso':<6}{'Costo':<10}")
        lineas.append("─" * 53)
        for i, r in enumerate(self.resultados):
            lineas.append(
                f"{i:<5}{r.tablon.id:<8}{r.t_inicio:<7}{r.t_fin:<7}"
                f"{r.tablon.ts:<5}{r.tablon.rp:<5}{r.caso:<6}{r.costo:<10.1f}"
            )
        lineas.append("─" * 53)
        lineas.append(f"COSTO TOTAL: {self.costo_total}")
        return "\n".join(lineas)

    def __repr__(self) -> str:
        return (
            f"Solucion(algoritmo={self.algoritmo}, "
            f"costo_total={self.costo_total}, "
            f"permutacion={self.permutacion})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Solucion):
            return NotImplemented
        return (
            self.permutacion == other.permutacion
            and abs(self.costo_total - other.costo_total) < 1e-9
            and self.algoritmo == other.algoritmo
        )
