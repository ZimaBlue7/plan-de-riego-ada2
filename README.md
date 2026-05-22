# Riego Optimo — Planificador de Riego

Proyecto academico para el curso de Analisis y Diseno de Algoritmos.
Resuelve el problema de encontrar la permutacion de riego que minimiza el costo total CR de una finca.

## Requisitos

- Python 3.11+.
- Dependencias: ver [riego_optimo/requirements.txt](riego_optimo/requirements.txt).

## Ejecucion

```bash
cd riego_optimo
python main.py
```

## Estructura del proyecto

```
riego_optimo/
├── models.py               # Clases de datos
├── calculos.py             # Funciones matematicas de costo
├── algoritmos.py           # Algoritmos (FB, V, PD)
├── io_handler.py           # Lectura/escritura de archivos
├── generador.py            # Generador de fincas aleatorias
├── analisis.py             # Benchmarking y comparacion de rendimiento
├── main.py                 # Punto de entrada de la aplicacion
├── gui_ctk.py              # Interfaz grafica (CustomTkinter)
├── notebook_analisis.ipynb # Cuaderno de analisis
└── procesar_lote.py        # Procesamiento por lotes de tests
```

## Descripcion tecnica de modulos

### models.py

- `Tablon`: parametros `id`, `ts`, `tr`, `p`, `rp` con validaciones.
- `Finca`: contenedor de tablones; propiedad `n` y `get_tablon(id)`.
- `ResultadoTablon`: detalle de costo por tablon con caso aplicado.
- `Solucion`: permutacion, costo total, resultados, tiempo y algoritmo.

### calculos.py

- `calcular_tiempos_inicio(finca, permutacion)`:
  calcula `t[i]` con acumulacion de `tr` segun el orden.
- `determinar_caso(tablon, t_inicio)`:
  caso 1 (t == rp), caso 2 (t != rp y ts - tr >= t), caso 3 (tardio).
- `calcular_costo_individual(tablon, t_inicio)`:
  caso 1: `ts - (t + tr)`
  caso 2: `2 * (ts - (t + tr))`
  caso 3: `2 * p * ((t + tr) - ts)`
- `calcular_costo_total(finca, permutacion)`:
  retorna costo total y lista de `ResultadoTablon`.
- `construir_solucion(finca, permutacion, algoritmo, tiempo_computo)`:
  empaqueta una solucion completa.

### algoritmos.py

- `roFB(finca)`:
  fuerza bruta por backtracking. Complejidad O(n! \* n). Optimo.
- `roV(finca)`:
  voraz EDF con criterio `(ts - tr) / p`. Complejidad O(n log n).
- `roPD(finca)`:
  programacion dinamica por bitmask. Complejidad O(n^2 \* 2^n).

### io_handler.py

- `leer_finca_desde_archivo(path)`:
  formato `n` seguido de `ts,tr,p,rp` por linea.
- `escribir_solucion_a_archivo(solucion, path)`:
  escribe costo en linea 1 y luego los indices en orden.

### gui_ctk.py

Interfaz grafica para cargar entradas, ejecutar algoritmos y visualizar resultados.
Incluye guardado de la mejor solucion en archivo.

### procesar_lote.py

Procesa archivos de `./Tests/tests` o `../Tests/tests` y escribe un consolidado
con costo, permutacion y tiempo por archivo.

## Formato de archivos

### Entrada (finca)

```
5
5,2,1,0
5,1,2,2
10,3,3,0
7,2,4,4
8,4,2,1
```

- Linea 1: numero de tablones (n).
- Lineas 2 a n+1: `ts,tr,p,rp` separados por coma.

### Salida (solucion)

```
<costo_total>
<id_tablon_1>
<id_tablon_2>
...
```

## Ejemplos del enunciado (resumen)

F1:

- PI1 = <2,1,4,3,0> => costo 31
- PI2 = <0,1,4,2,3> => costo 37

F2:

- PI1 = <2,1,4,3,0> => costo 48
- PI2 = <2,1,4,0,3> => costo 46
