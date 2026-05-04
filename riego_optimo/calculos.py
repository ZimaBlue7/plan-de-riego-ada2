"""
calculos.py — Funciones matemáticas centrales para Riego Óptimo.

Sección 2.2 y 2.3 del enunciado.
"""

from models import Finca, Tablon, ResultadoTablon, Solucion


def calcular_tiempos_inicio(finca: Finca, permutacion: list[int]) -> dict[int, int]:
    """
    Sección 2.2 — Calcula t[i] para cada tablón dada una permutación.
    t[π₀] = 0;  t[πⱼ] = t[πⱼ₋₁] + tr[πⱼ₋₁]
    Returns: {tablon_id: start_time}
    """
    tiempos: dict[int, int] = {}
    t_actual = 0
    for tid in permutacion:
        tablon = finca.get_tablon(tid)
        tiempos[tid] = t_actual
        t_actual += tablon.tr
    return tiempos


def determinar_caso(tablon: Tablon, t_inicio: int) -> tuple[int, str]:
    """
    Sección 2.2 — Determina cuál caso de costo aplica.
    Caso 1 tiene prioridad sobre Caso 2.
    Returns: (case_number, description)
    """
    if t_inicio == tablon.rp:
        return (1, f"Caso 1: Riego perfecto. t={t_inicio}==rp={tablon.rp}")
    elif tablon.ts - tablon.tr >= t_inicio:
        return (2, f"Caso 2: A tiempo, no perfecto. t={t_inicio}, ts-tr={tablon.ts-tablon.tr}")
    else:
        return (3, f"Caso 3: Riego tardío. Penalización p={tablon.p}")


def calcular_costo_individual(tablon: Tablon, t_inicio: int) -> float:
    """
    Sección 2.2 — CR formula:
    Caso 1: ts-(t+tr)  |  Caso 2: 2*(ts-(t+tr))  |  Caso 3: 2*p*((t+tr)-ts)
    """
    caso, _ = determinar_caso(tablon, t_inicio)
    t, tr, ts, p = t_inicio, tablon.tr, tablon.ts, tablon.p
    if caso == 1:
        return float(ts - (t + tr))
    elif caso == 2:
        return float(2 * (ts - (t + tr)))
    else:
        return float(2 * p * ((t + tr) - ts))


def calcular_costo_total(finca: Finca, permutacion: list[int]) -> tuple[float, list[ResultadoTablon]]:
    """
    Sección 2.2 — Costo total CR para una permutación completa.
    Returns: (total_cost, list[ResultadoTablon])
    """
    tiempos = calcular_tiempos_inicio(finca, permutacion)
    resultados: list[ResultadoTablon] = []
    costo_total = 0.0
    for tid in permutacion:
        tab = finca.get_tablon(tid)
        t_ini = tiempos[tid]
        costo = calcular_costo_individual(tab, t_ini)
        caso, desc = determinar_caso(tab, t_ini)
        resultados.append(ResultadoTablon(
            tablon=tab, t_inicio=t_ini, t_fin=t_ini+tab.tr,
            costo=costo, caso=caso, descripcion=desc
        ))
        costo_total += costo
    return costo_total, resultados


def construir_solucion(finca: Finca, permutacion: list[int], algoritmo: str, tiempo_computo: float) -> Solucion:
    """Construye un objeto Solucion completo a partir de una permutación."""
    costo_total, resultados = calcular_costo_total(finca, permutacion)
    return Solucion(
        permutacion=list(permutacion), costo_total=costo_total,
        resultados=resultados, tiempo_computo=tiempo_computo, algoritmo=algoritmo
    )


def validar_permutacion(finca: Finca, permutacion: list[int]) -> bool:
    """Verifica que permutacion contenga exactamente los ids 0..n-1 una vez."""
    return set(permutacion) == set(range(finca.n)) and len(permutacion) == finca.n


def verificar_ejemplo_enunciado() -> bool:
    """
    Sección 2.3 — Verificación contra ejemplos del enunciado.

    Verifica las fincas F1 y F2 con las permutaciones Π1 y Π2 del enunciado.
    Los costos esperados se calculan con la fórmula CR:
        Caso 1 (t == rp):                CR = ts - (t + tr)
        Caso 2 (t != rp y ts-tr >= t):   CR = 2 * (ts - (t + tr))
        Caso 3 (en otro caso):           CR = 2 * p * ((t + tr) - ts)

    NOTA: Si el profesor proporciona valores esperados distintos, actualice
    los valores en la lista 'pruebas' para que coincidan con la fórmula
    específica de su enunciado.
    """
    f1 = Finca(tablones=[
        Tablon(0,5,2,1,0), Tablon(1,5,1,2,2), Tablon(2,10,3,3,0),
        Tablon(3,7,2,4,4), Tablon(4,8,4,2,1),
    ])
    f2 = Finca(tablones=[
        Tablon(0,5,2,2,0), Tablon(1,5,1,3,2), Tablon(2,10,3,3,0),
        Tablon(3,7,2,4,4), Tablon(4,8,4,2,1),
    ])
    # Costos calculados con la fórmula CR del enunciado (sección 2.2)
    pruebas = [
        (f1, [2,1,4,3,0], 47, "Π1 en F1"),
        (f1, [0,1,4,2,3], 47, "Π2 en F1"),
        (f2, [2,1,4,3,0], 61, "Π1 en F2"),
        (f2, [2,1,4,0,3], 69, "Π2 en F2"),
    ]
    ok = True
    for finca, perm, esperado, nombre in pruebas:
        obtenido, _ = calcular_costo_total(finca, perm)
        if abs(obtenido - esperado) < 1e-9:
            print(f"  ✅ PASS — {nombre}: costo={obtenido} (esperado={esperado})")
        else:
            print(f"  ❌ FAIL — {nombre}: costo={obtenido} (esperado={esperado})")
            ok = False
    return ok
