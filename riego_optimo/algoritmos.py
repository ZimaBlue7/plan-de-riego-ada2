"""
algoritmos.py — Stubs de los tres algoritmos para Riego Óptimo.

El estudiante debe implementar:
  - roFB: Fuerza Bruta (Sección 3.1)
  - roV:  Algoritmo Voraz (Sección 3.2)
  - roPD: Programación Dinámica (Sección 3.3)

Cada función recibe una Finca y retorna una Solucion.
"""

import time
from models import Finca, Solucion
from calculos import calcular_costo_total, construir_solucion


def roFB(finca: Finca) -> Solucion:
    """
    FUERZA BRUTA — Sección 3.1

    Genera todas las permutaciones posibles del conjunto de tablones
    y retorna la de menor costo total según la función CR definida en
    la sección 2.2 del enunciado.

    Estrategia:
        Se genera el árbol completo (profundidad) de permutaciones usando backtracking
        recursivo. En cada nivel del árbol se elige un tablón no usado
        aún y se continúa hasta completar una permutación de longitud n.
        Al completarla se evalúa su costo y se actualiza la mejor solución
        encontrada hasta el momento.

    Corrección:
        Al explorar TODAS las permutaciones posibles, se garantiza que
        la solución retornada es siempre la óptima global.

    Complejidad:
        Tiempo : O(n! * n)
    """
    inicio = time.perf_counter()

    n = finca.n
    ids = [t.id for t in finca.tablones]  # lista de ids disponibles

    mejor_costo = [float('inf')]           # lista para poder mutar desde closure
    mejor_perm  = [None]

    # --- generador de permutaciones por backtracking ---

    permutacion_actual = []
    usado = [False] * n   # usado[i] = True si ids[i] ya está en la permutacion_actual

    def backtrack():
        # Caso base: permutación completa
        if len(permutacion_actual) == n:
            costo, _ = calcular_costo_total(finca, permutacion_actual)
            if costo < mejor_costo[0]:
                mejor_costo[0] = costo
                mejor_perm[0]  = permutacion_actual[:]   # copia
            return

        # Paso recursivo: probar cada tablón no usado en la posición actual
        for i in range(n):
            if not usado[i]:
                # Elegir
                usado[i] = True
                permutacion_actual.append(ids[i])

                # Explorar
                backtrack()

                # Deshacer (backtrack)
                permutacion_actual.pop()
                usado[i] = False

    backtrack()

    tiempo_total = time.perf_counter() - inicio

    return construir_solucion(
        finca=finca,
        permutacion=mejor_perm[0],
        algoritmo='FB',
        tiempo_computo=tiempo_total
    )


def roV(finca: Finca) -> Solucion:
    """
    ALGORITMO VORAZ — Sección 3.2

    Criterio Voraz (EDF - Earliest Deadline First):
    Ordena los tablones de forma ascendente según su fecha límite (deadline),
    calculada como: (ts - tr)/p. Al atender primero los tablones que "vencen"
    antes, se intenta minimizar el costo.

    Complejidad esperada: O(n log n)
    Puede o no retornar la solución óptima.

    Args:
        finca: La finca a resolver.

    Returns:
        La Solucion obtenida por el criterio voraz.
    """
    inicio = time.perf_counter()

    deadlines = {}
    for T in finca.tablones:
        deadlines[T.id] = (T.ts - T.tr)/T.p
    
    sorted_tablones = sorted(finca.tablones, key=lambda T: deadlines[T.id])
    permutacion = [T.id for T in sorted_tablones]
    
    tiempo_computo = time.perf_counter() - inicio

    return construir_solucion(finca, permutacion, 'V', tiempo_computo)


def roPD(finca: Finca) -> Solucion:
    """
    PROGRAMACIÓN DINÁMICA — Sección 3.3

    Programación dinámica con máscara de bits sobre subconjuntos de tablones.

    Complejidad esperada: O(n² × 2ⁿ) tiempo, O(n × 2ⁿ) espacio.
    Siempre retorna la solución óptima.

    Args:
        finca: La finca a resolver.

    Returns:
        La Solucion óptima encontrada por PD.

    Raises:
        NotImplementedError: Mientras el estudiante no la implemente.
    """
    # TODO: implementar programación dinámica
    raise NotImplementedError("Pendiente de implementación — Sección 3.3")
