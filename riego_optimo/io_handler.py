"""
io_handler.py — Lectura y escritura de archivos para Riego Óptimo.

Maneja:
- Lectura de fincas desde archivos de texto (sección 3.4.1).
- Escritura de soluciones a archivos de texto (sección 3.4.2).
- Lectura de soluciones previamente guardadas.
- Exportación de comparaciones a CSV.
"""

from models import Finca, Tablon


def leer_finca_desde_archivo(path: str) -> Finca:
    """
    Sección 3.4.1 — Lee una finca desde un archivo de texto.

    Formato esperado:
        Línea 1: n (número de tablones)
        Líneas 2..n+1: ts,tr,p,rp (separados por coma)

    Args:
        path: Ruta al archivo de texto.

    Returns:
        Objeto Finca con los tablones leídos.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el formato es incorrecto, indica el número de línea.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    if not lineas:
        raise ValueError("El archivo está vacío")

    # Línea 1: n
    try:
        n = int(lineas[0].strip())
    except ValueError:
        raise ValueError(
            f"Línea 1: Se esperaba un entero (n), se encontró: '{lineas[0].strip()}'"
        )

    if len(lineas) < n + 1:
        raise ValueError(
            f"Se esperaban {n + 1} líneas ({n} tablones + 1 encabezado), "
            f"pero el archivo tiene {len(lineas)} líneas"
        )

    tablones: list[Tablon] = []
    for i in range(1, n + 1):
        linea = lineas[i].strip()
        if not linea:
            raise ValueError(
                f"Línea {i + 1}: Línea vacía, se esperaban datos del tablón"
            )

        partes = linea.split(",")
        if len(partes) != 4:
            raise ValueError(
                f"Línea {i + 1}: Se esperaban 4 valores (ts,tr,p,rp), "
                f"se encontraron {len(partes)}: '{linea}'"
            )

        try:
            ts, tr, p, rp = (
                int(partes[0]),
                int(partes[1]),
                int(partes[2]),
                int(partes[3]),
            )
        except ValueError:
            raise ValueError(
                f"Línea {i + 1}: Todos los valores deben ser enteros: '{linea}'"
            )

        try:
            tablon = Tablon(id=i - 1, ts=ts, tr=tr, p=p, rp=rp)
        except ValueError as e:
            raise ValueError(f"Línea {i + 1}: {e}")

        tablones.append(tablon)

    return Finca(tablones=tablones)


def escribir_solucion_a_archivo(solucion, path: str) -> None:
    """
    Seccion 3.4.2 - Escribe una solucion a un achivo de texto
    Formato:
        Linea 1: Costo total
        Linea 2..n+1 indice del tablo en orden
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{solucion.costo_total}\n")
        for tid in solucion.permutacion:
            f.write(f"{tid}\n")
