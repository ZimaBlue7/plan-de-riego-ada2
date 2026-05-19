# Riego Óptimo — Planificador de Riego

Proyecto académico para el curso de **Análisis y Diseño de Algoritmos**.
Resuelve el problema de encontrar la permutación de riego que minimiza el costo total CR de una finca.

---

## Ejecución

```bash
cd riego_optimo
python main.py
```

> **Requisitos:** Python 3.11+ con `customtkinter` instalado en el ambiente virtual.
> La aplicación incluye scripts iniciadores (`play.sh` / `start.sh`) que configuran el ambiente virtual (`venv`) automáticamente e instalan las dependencias necesarias.

---

## Estructura del Proyecto

```
riego_optimo/
├── models.py               # Clases de datos
├── calculos.py             # Funciones matemáticas de costo
├── algoritmos.py           # Algoritmos (stubs #TODO)
├── io_handler.py           # Lectura de archivos de entrada
├── generador.py            # Generador de fincas aleatorias
├── analisis.py             # Benchmarking y comparación de rendimiento
├── main.py                 # Punto de entrada de la aplicación
├── gui_ctk.py              # Interfaz gráfica moderna en CustomTkinter
├── notebook_analisis.ipynb # Cuaderno interactivo de análisis y visualización
└── procesar_lote.py        # Script para procesar lotes de archivos de prueba
```

---

## Descripción de Funciones por Módulo

### `models.py` — Clases de Datos

| Clase | Descripción |
|-------|-------------|
| `Tablon` | Representa un tablón de la finca con parámetros `id`, `ts` (supervivencia), `tr` (duración riego), `p` (prioridad 1–4), `rp` (tiempo perfecto). Valida automáticamente que `ts > 0`, `tr > 0`, `1 ≤ p ≤ 4` y `0 ≤ rp ≤ ts - tr`. |
| `Finca` | Contenedor de tablones. Propiedad `n` retorna la cantidad. `get_tablon(id)` busca por id. |
| `ResultadoTablon` | Resultado del riego de un tablón: `t_inicio`, `t_fin`, `costo`, `caso` (1/2/3), `descripcion` legible. |
| `Solucion` | Solución completa: `permutacion`, `costo_total`, `resultados`, `tiempo_computo`, `algoritmo`. Método `resumen()` para mostrar el detalle formateado en texto. |

---

### `calculos.py` — Funciones Matemáticas (Sección 2.2)

| Función | Descripción |
|---------|-------------|
| `calcular_tiempos_inicio(finca, permutacion)` | **§2.2** — Calcula el tiempo de inicio `t[i]` de cada tablón en una permutación. El primer tablón comienza en t=0, cada siguiente comienza cuando termina el anterior: `t[πⱼ] = t[πⱼ₋₁] + tr[πⱼ₋₁]`. Retorna `{tablon_id: start_time}`. |
| `determinar_caso(tablon, t_inicio)` | **§2.2** — Determina qué caso de costo aplica: **Caso 1** (riego perfecto: `t == rp`), **Caso 2** (a tiempo pero no perfecto: `t != rp` y `ts-tr ≥ t`), **Caso 3** (tardío). Caso 1 tiene prioridad sobre Caso 2. Retorna `(caso, descripcion)`. |
| `calcular_costo_individual(tablon, t_inicio)` | **§2.2** — Calcula el costo CR de un tablón: Caso 1 → `ts-(t+tr)`, Caso 2 → `2*(ts-(t+tr))`, Caso 3 → `2*p*((t+tr)-ts)`. |
| `calcular_costo_total(finca, permutacion)` | **§2.2** — Suma los costos individuales de todos los tablones en la permutación. Retorna `(costo_total, [ResultadoTablon])`. |
| `construir_solucion(finca, permutacion, algoritmo, tiempo_computo)` | Empaqueta una permutación con su costo y resultados en un objeto `Solucion`. |

---

### `algoritmos.py` — Algoritmos (Stubs #TODO)

| Función | Sección | Complejidad | Descripción |
|---------|---------|-------------|-------------|
| `roFB(finca)` | §3.1 | O(n! × n) | **Fuerza Bruta.** Genera todas las n! permutaciones y retorna la de costo mínimo. Siempre óptima. |
| `roV(finca)` | §3.2 | O(n log n) | **Algoritmo Voraz.** El estudiante elige y documenta su criterio greedy. Puede no ser óptima. |
| `roPD(finca)` | §3.3 | O(n² × 2ⁿ) | **Programación Dinámica.** Bitmask DP sobre subconjuntos de tablones. Siempre óptima. |

> ⚠️ Los tres algoritmos lanzan `NotImplementedError` hasta que el estudiante los implemente.

---

### `io_handler.py` — Entrada de Archivos

| Función | Descripción |
|---------|-------------|
| `leer_finca_desde_archivo(path)` | **§3.4.1** — Lee una finca de un `.txt`. Formato: línea 1 = `n`, líneas siguientes = `ts,tr,p,rp`. Reporta errores con número de línea. |

---

### `generador.py` — Generación de Fincas

| Función | Descripción |
|---------|-------------|
| `generar_finca_aleatoria(n, seed)` | Genera finca con `n` tablones aleatorios. Garantiza `0 ≤ rp ≤ ts-tr`. Rangos: `ts∈[3,20]`, `tr∈[1,ts//2]`, `p∈[1,4]`. Acepta semilla para reproducibilidad. |

---

### `analisis.py` — Benchmarking y Métricas

| Función / Clase | Descripción |
|-----------------|-------------|
| `MetricasEjecucion` | Dataclass con: `algoritmo`, `n`, `costo`, `tiempo_ms`, `memoria_bytes`, `es_optima`, `permutacion`. |
| `medir_ejecucion(fn, finca, algoritmo, solucion_optima)` | Ejecuta un algoritmo midiendo tiempo (`perf_counter`) y memoria pico (`tracemalloc`). Compara con solución óptima si se provee. |
| `comparar_tres_algoritmos(finca, incluir_fb)` | Ejecuta FB, V y PD sobre la misma finca. Usa FB como ground truth. Omite FB si `n > 10`. Captura `NotImplementedError`. Utilizado en el análisis interactivo del notebook. |
| `benchmark_escalabilidad(n_values, repeticiones)` | Para cada `n`, genera finca y ejecuta los 3 algoritmos. Promedia sobre `repeticiones` ejecuciones. Retorna lista plana de métricas. Utilizado para las visualizaciones de escalabilidad del notebook. |
| `resumen_tabla(lista_metricas)` | Genera tabla ASCII formateada: `Algoritmo | n | Costo | Tiempo (ms) | Memoria (KB) | ¿Óptima?`. |

---

### `gui_ctk.py` — Interfaz Gráfica (CustomTkinter)

| Método | Descripción |
|--------|-------------|
| `__init__()` | Inicializa la interfaz moderna, barra lateral de configuración (selección de algoritmos y repeticiones de benchmark), y áreas del editor de texto y panel de resultados. |
| `cargar_archivo()` | Permite cargar un archivo `.txt` de finca directamente al editor manual interactivo. |
| `parse_finca_from_editor()` | Procesa y valida el texto del editor interactivo, convirtiéndolo a un objeto `Finca`. |
| `ejecutar_procesamiento()` | Ejecuta el procesamiento de los algoritmos seleccionados en un hilo de fondo (`worker thread`) para evitar congelamientos de la interfaz gráfica. |
| `medir_todo(finca, reps)` | Mide el tiempo y recolecta las soluciones de los algoritmos elegidos para la finca activa. |
| `mostrar_resultados(resultados)` | Muestra los resultados en el panel, indicando costo y tiempo promedio en milisegundos, y desplegando el resumen del mejor orden en formato de texto enriquecido. |

---

### `main.py` — Punto de Entrada

| Función | Descripción |
|---------|-------------|
| `main()` | Lanza la aplicación GUI de CustomTkinter (`RiegoOptimoApp().mainloop()`). |

---

## Formato de Archivos

### Archivo de Finca (entrada — §3.4.1)
```
5
5,2,1,0
5,1,2,2
10,3,3,0
7,2,4,4
8,4,2,1
```
- Línea 1: número de tablones (n)
- Líneas 2 a n+1: `ts,tr,p,rp` separados por coma

---

## Ejemplos del Enunciado (§2.3)

### Finca F1
| id | ts | tr | p | rp |
|----|----|----|---|----|
| 0  | 5  | 2  | 1 | 0  |
| 1  | 5  | 1  | 2 | 2  |
| 2  | 10 | 3  | 3 | 0  |
| 3  | 7  | 2  | 4 | 4  |
| 4  | 8  | 4  | 2 | 1  |

- Π1 = ⟨2,1,4,3,0⟩ → **Costo = 31**
- Π2 = ⟨0,1,4,2,3⟩ → **Costo = 37**

### Finca F2
| id | ts | tr | p | rp |
|----|----|----|---|----|
| 0  | 5  | 2  | 2 | 0  |
| 1  | 5  | 1  | 3 | 2  |
| 2  | 10 | 3  | 3 | 0  |
| 3  | 7  | 2  | 4 | 4  |
| 4  | 8  | 4  | 2 | 1  |

- Π1 = ⟨2,1,4,3,0⟩ → **Costo = 48**
- Π2 = ⟨2,1,4,0,3⟩ → **Costo = 46**

---

## Trabajo del Estudiante

El estudiante debe implementar las tres funciones en `algoritmos.py`:

1. **`roFB(finca)`** — Fuerza bruta con backtracking recursivo para hallar el óptimo global.
2. **`roV(finca)`** — Algoritmo voraz bajo el criterio greedy establecido (EDF).
3. **`roPD(finca)`** — Programación dinámica con bitmask.

Todo lo demás (modelos, cálculos, E/S de archivos, generador aleatorio, suite de análisis de métricas, GUI interactiva con CustomTkinter, cuaderno de Jupyter e inyección de lotes) está completamente implementado y funcional.
