"""
generador.py — Generador de fincas aleatorias para Riego Óptimo.

Genera fincas aleatorias para pruebas, casos extremos para stress testing,
y suites de pruebas para benchmarking.
"""

import random
from models import Finca, Tablon


def generar_finca_aleatoria(n: int, seed: int = None) -> Finca:
    """
    Genera una finca aleatoria con n tablones.

    Garantiza: 0 <= rp <= ts - tr para todo tablón.
    Rangos:
        ts: entero aleatorio en [3, 20]
        tr: entero aleatorio en [1, ts // 2]
        p:  entero aleatorio en [1, 4]
        rp: entero aleatorio en [0, ts - tr]

    Args:
        n: Número de tablones a generar.
        seed: Semilla para reproducibilidad (opcional).

    Returns:
        Objeto Finca con n tablones generados aleatoriamente.
    """
    if seed is not None:
        random.seed(seed)

    tablones: list[Tablon] = []
    for i in range(n):
        ts = random.randint(3, 20)
        tr = random.randint(1, max(1, ts // 2))
        p = random.randint(1, 4)
        rp = random.randint(0, ts - tr)
        tablones.append(Tablon(id=i, ts=ts, tr=tr, p=p, rp=rp))

    return Finca(tablones=tablones)
