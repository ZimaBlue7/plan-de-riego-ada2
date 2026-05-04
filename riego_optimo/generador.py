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


def generar_finca_extrema(n: int, tipo: str) -> Finca:
    """
    Genera fincas con casos extremos para stress testing.

    Args:
        n: Número de tablones.
        tipo: Tipo de caso extremo:
            'todos_criticos'       — p=4 y ts apenas > tr
            'todos_perfectos'      — rp=0, todos quieren ir primero
            'gran_prioridad'       — prioridad creciente monotónicamente
            'supervivencia_corta'  — ts muy pequeño, tr cercano a ts

    Returns:
        Objeto Finca con las características extremas solicitadas.

    Raises:
        ValueError: Si el tipo no es reconocido.
    """
    tablones: list[Tablon] = []

    if tipo == 'todos_criticos':
        for i in range(n):
            tr = random.randint(1, 3)
            ts = tr + 1
            tablones.append(Tablon(id=i, ts=ts, tr=tr, p=4, rp=0))

    elif tipo == 'todos_perfectos':
        for i in range(n):
            ts = random.randint(5, 15)
            tr = random.randint(1, max(1, ts // 3))
            tablones.append(Tablon(id=i, ts=ts, tr=tr, p=random.randint(1, 4), rp=0))

    elif tipo == 'gran_prioridad':
        for i in range(n):
            ts = random.randint(5, 15)
            tr = random.randint(1, max(1, ts // 3))
            p = min(4, (i % 4) + 1)
            rp = random.randint(0, ts - tr)
            tablones.append(Tablon(id=i, ts=ts, tr=tr, p=p, rp=rp))

    elif tipo == 'supervivencia_corta':
        for i in range(n):
            tr = random.randint(1, 2)
            ts = tr + random.randint(0, 1) + 1
            rp = random.randint(0, max(0, ts - tr))
            tablones.append(Tablon(id=i, ts=ts, tr=tr, p=random.randint(2, 4), rp=rp))

    else:
        raise ValueError(
            f"Tipo desconocido: '{tipo}'. Tipos válidos: "
            "todos_criticos, todos_perfectos, gran_prioridad, supervivencia_corta"
        )

    return Finca(tablones=tablones)


def generar_suite_pruebas(
    n_values: list[int] = None
) -> list[tuple[int, Finca]]:
    """
    Genera una finca aleatoria por cada valor de n.

    Args:
        n_values: Lista de tamaños de finca a generar.
                  Por defecto [3, 4, 5, 6, 7, 8, 10, 12, 15].

    Returns:
        Lista de tuplas (n, finca) para benchmarking.
    """
    if n_values is None:
        n_values = [3, 4, 5, 6, 7, 8, 10, 12, 15]

    return [(n, generar_finca_aleatoria(n, seed=n * 42)) for n in n_values]
