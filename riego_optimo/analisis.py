"""
analisis.py — Utilidades de benchmarking y comparación para Riego Óptimo.

Mide rendimiento (tiempo, memoria) de cada algoritmo y genera
tablas comparativas y métricas de optimalidad.
"""

import time
import tracemalloc
from dataclasses import dataclass
from typing import Optional, Callable

from models import Finca, Solucion
from generador import generar_finca_aleatoria


@dataclass
class MetricasEjecucion:
    """
    Métricas de una ejecución individual de un algoritmo.

    Atributos:
        algoritmo:     Nombre del algoritmo ('FB', 'V', 'PD').
        n:             Tamaño de la finca.
        costo:         Costo total de la solución encontrada.
        tiempo_ms:     Tiempo de ejecución en milisegundos.
        memoria_bytes: Memoria pico utilizada (tracemalloc).
        es_optima:     True/False/None si no se comparó con FB.
        permutacion:   Permutación de la solución.
    """
    algoritmo: str
    n: int
    costo: float
    tiempo_ms: float
    memoria_bytes: int
    es_optima: Optional[bool]
    permutacion: list[int]


def medir_ejecucion(
    fn: Callable,
    finca: Finca,
    algoritmo: str,
    solucion_optima: Optional[Solucion] = None
) -> MetricasEjecucion:
    """
    Ejecuta un algoritmo sobre una finca midiendo tiempo y memoria.

    Args:
        fn: Función del algoritmo (roFB, roV o roPD).
        finca: La finca a resolver.
        algoritmo: Nombre del algoritmo.
        solucion_optima: Solución óptima para comparar (opcional).

    Returns:
        MetricasEjecucion con los resultados medidos.
    """
    tracemalloc.start()
    inicio = time.perf_counter()

    solucion = fn(finca)

    fin = time.perf_counter()
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tiempo_ms = (fin - inicio) * 1000

    es_optima: Optional[bool] = None
    if solucion_optima is not None:
        es_optima = abs(solucion.costo_total - solucion_optima.costo_total) < 1e-9

    return MetricasEjecucion(
        algoritmo=algoritmo,
        n=finca.n,
        costo=solucion.costo_total,
        tiempo_ms=tiempo_ms,
        memoria_bytes=pico,
        es_optima=es_optima,
        permutacion=solucion.permutacion
    )


def comparar_tres_algoritmos(
    finca: Finca, incluir_fb: bool = True
) -> list[MetricasEjecucion]:
    """
    Ejecuta roFB (opcional), roV y roPD sobre la misma finca.

    Usa el resultado de roFB como ground truth para comparar optimalidad.
    Omite roFB si n > 10 por complejidad factorial.
    Captura NotImplementedError para algoritmos no implementados.

    Args:
        finca: La finca a resolver.
        incluir_fb: Si incluir fuerza bruta (auto-deshabilitado si n > 10).

    Returns:
        Lista de MetricasEjecucion, una por algoritmo ejecutado.
    """
    from algoritmos import roFB, roV, roPD

    resultados: list[MetricasEjecucion] = []
    sol_optima: Optional[Solucion] = None

    # Fuerza bruta
    if incluir_fb and finca.n <= 10:
        try:
            m = medir_ejecucion(roFB, finca, 'FB')
            m.es_optima = True
            resultados.append(m)
            # Guardar para comparar
            sol_optima = Solucion(
                permutacion=m.permutacion, costo_total=m.costo,
                resultados=[], tiempo_computo=m.tiempo_ms / 1000, algoritmo='FB'
            )
        except NotImplementedError:
            resultados.append(MetricasEjecucion(
                algoritmo='FB', n=finca.n, costo=float('inf'),
                tiempo_ms=0, memoria_bytes=0, es_optima=None, permutacion=[]
            ))

    # Voraz
    try:
        m = medir_ejecucion(roV, finca, 'V', sol_optima)
        resultados.append(m)
    except NotImplementedError:
        resultados.append(MetricasEjecucion(
            algoritmo='V', n=finca.n, costo=float('inf'),
            tiempo_ms=0, memoria_bytes=0, es_optima=None, permutacion=[]
        ))

    # Programación dinámica
    try:
        m = medir_ejecucion(roPD, finca, 'PD', sol_optima)
        resultados.append(m)
    except NotImplementedError:
        resultados.append(MetricasEjecucion(
            algoritmo='PD', n=finca.n, costo=float('inf'),
            tiempo_ms=0, memoria_bytes=0, es_optima=None, permutacion=[]
        ))

    return resultados


def benchmark_escalabilidad(
    n_values: list[int],
    repeticiones: int = 3
) -> list[MetricasEjecucion]:
    """
    Para cada n, genera una finca aleatoria y ejecuta los tres algoritmos.
    Omite roFB para n > 10. Promedia sobre `repeticiones` ejecuciones.

    Args:
        n_values: Lista de tamaños de finca.
        repeticiones: Número de repeticiones por medición.

    Returns:
        Lista plana de MetricasEjecucion para todas las combinaciones (n, algoritmo).
    """
    from algoritmos import roFB, roV, roPD

    todos: list[MetricasEjecucion] = []
    algos = [('FB', roFB), ('V', roV), ('PD', roPD)]

    for n in n_values:
        finca = generar_finca_aleatoria(n, seed=n * 42)

        # Obtener óptima si es posible
        sol_optima: Optional[Solucion] = None
        if n <= 10:
            try:
                m = medir_ejecucion(roFB, finca, 'FB')
                sol_optima = Solucion(
                    permutacion=m.permutacion, costo_total=m.costo,
                    resultados=[], tiempo_computo=0, algoritmo='FB'
                )
            except NotImplementedError:
                pass

        for nombre, fn in algos:
            if nombre == 'FB' and n > 10:
                continue

            tiempos = []
            memorias = []
            costo = 0.0
            perm: list[int] = []
            es_opt: Optional[bool] = None

            for _ in range(repeticiones):
                try:
                    m = medir_ejecucion(fn, finca, nombre, sol_optima)
                    tiempos.append(m.tiempo_ms)
                    memorias.append(m.memoria_bytes)
                    costo = m.costo
                    perm = m.permutacion
                    es_opt = m.es_optima
                except NotImplementedError:
                    tiempos.append(0)
                    memorias.append(0)
                    costo = float('inf')
                    perm = []
                    es_opt = None
                    break

            todos.append(MetricasEjecucion(
                algoritmo=nombre, n=n, costo=costo,
                tiempo_ms=sum(tiempos) / max(len(tiempos), 1),
                memoria_bytes=int(sum(memorias) / max(len(memorias), 1)),
                es_optima=es_opt, permutacion=perm
            ))

    return todos


def calcular_gap_optimalidad(
    metricas_voraz: MetricasEjecucion,
    metricas_fb: MetricasEjecucion
) -> float:
    """
    Calcula el gap de optimalidad en porcentaje.
    Gap = (costo_voraz - costo_optimo) / costo_optimo × 100

    Args:
        metricas_voraz: Métricas del algoritmo voraz.
        metricas_fb: Métricas de fuerza bruta (óptimo).

    Returns:
        Porcentaje de gap de optimalidad.
    """
    if metricas_fb.costo == 0:
        return 0.0
    return (metricas_voraz.costo - metricas_fb.costo) / metricas_fb.costo * 100


def resumen_tabla(lista_metricas: list[MetricasEjecucion]) -> str:
    """
    Genera una tabla ASCII formateada con los resultados de benchmark.

    Columnas: Algoritmo | n | Costo | Tiempo (ms) | Memoria (KB) | ¿Óptima?

    Args:
        lista_metricas: Lista de MetricasEjecucion a tabular.

    Returns:
        Cadena con la tabla formateada.
    """
    header = f"{'Algoritmo':<12}{'n':<6}{'Costo':<12}{'Tiempo (ms)':<15}{'Memoria (KB)':<15}{'¿Óptima?':<10}"
    sep = "─" * len(header)
    lineas = [sep, header, sep]

    for m in lista_metricas:
        opt_str = "—"
        if m.es_optima is True:
            opt_str = "Sí"
        elif m.es_optima is False:
            opt_str = "No"

        costo_str = f"{m.costo:.1f}" if m.costo != float('inf') else "N/A"

        lineas.append(
            f"{m.algoritmo:<12}{m.n:<6}{costo_str:<12}"
            f"{m.tiempo_ms:<15.2f}{m.memoria_bytes / 1024:<15.1f}{opt_str:<10}"
        )

    lineas.append(sep)
    return "\n".join(lineas)
