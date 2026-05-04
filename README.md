# Riego Óptimo — Planificador de Riego

Proyecto académico para el curso de **Análisis y Diseño de Algoritmos**.
Resuelve el problema de encontrar la permutación de riego que minimiza el costo total CR de una finca.

---

## Ejecución

```bash
cd riego_optimo
python main.py
```

> **Requisitos:** Python 3.11+ con Tkinter (incluido en la mayoría de instalaciones).
> No se requieren dependencias externas.

---

## Estructura del Proyecto

```
riego_optimo/
├── models.py           # Clases de datos
├── calculos.py         # Funciones matemáticas de costo
├── algoritmos.py       # Algoritmos (stubs #TODO)
├── io_handler.py       # Lectura/escritura de archivos
├── generador.py        # Generador de fincas aleatorias
├── analisis.py         # Benchmarking y comparación
├── main.py             # Punto de entrada
└── gui/
    ├── __init__.py
    ├── app.py           # Ventana principal
    ├── tab_manual.py    # Pestaña de entrada manual
    ├── tab_archivo.py   # Pestaña de archivos
    ├── tab_random.py    # Pestaña de generación aleatoria
    └── tab_resultados.py# Pestaña de resultados
```

---

## Descripción de Funciones por Módulo

### `models.py` — Clases de Datos

| Clase | Descripción |
|-------|-------------|
| `Tablon` | Representa un tablón de la finca con parámetros `id`, `ts` (supervivencia), `tr` (duración riego), `p` (prioridad 1–4), `rp` (tiempo perfecto). Valida automáticamente que `ts > 0`, `tr > 0`, `1 ≤ p ≤ 4` y `0 ≤ rp ≤ ts - tr`. |
| `Finca` | Contenedor de tablones. Propiedad `n` retorna la cantidad. `get_tablon(id)` busca por id. `to_dict()` / `from_dict()` para serialización. |
| `ResultadoTablon` | Resultado del riego de un tablón: `t_inicio`, `t_fin`, `costo`, `caso` (1/2/3), `descripcion` legible. |
| `Solucion` | Solución completa: `permutacion`, `costo_total`, `resultados`, `tiempo_computo`, `algoritmo`. Métodos `es_valida(finca)` y `resumen()`. |

---

### `calculos.py` — Funciones Matemáticas (Sección 2.2)

| Función | Descripción |
|---------|-------------|
| `calcular_tiempos_inicio(finca, permutacion)` | **§2.2** — Calcula el tiempo de inicio `t[i]` de cada tablón en una permutación. El primer tablón comienza en t=0, cada siguiente comienza cuando termina el anterior: `t[πⱼ] = t[πⱼ₋₁] + tr[πⱼ₋₁]`. Retorna `{tablon_id: start_time}`. |
| `determinar_caso(tablon, t_inicio)` | **§2.2** — Determina qué caso de costo aplica: **Caso 1** (riego perfecto: `t == rp`), **Caso 2** (a tiempo pero no perfecto: `t != rp` y `ts-tr ≥ t`), **Caso 3** (tardío). Caso 1 tiene prioridad sobre Caso 2. Retorna `(caso, descripcion)`. |
| `calcular_costo_individual(tablon, t_inicio)` | **§2.2** — Calcula el costo CR de un tablón: Caso 1 → `ts-(t+tr)`, Caso 2 → `2*(ts-(t+tr))`, Caso 3 → `2*p*((t+tr)-ts)`. |
| `calcular_costo_total(finca, permutacion)` | **§2.2** — Suma los costos individuales de todos los tablones en la permutación. Retorna `(costo_total, [ResultadoTablon])`. |
| `construir_solucion(finca, permutacion, algoritmo, tiempo_computo)` | Empaqueta una permutación con su costo y resultados en un objeto `Solucion`. |
| `validar_permutacion(finca, permutacion)` | Verifica que la permutación contenga exactamente los ids `0..n-1` sin repeticiones. |
| `verificar_ejemplo_enunciado()` | **§2.3** — Auto-test contra los 4 ejemplos del enunciado (F1/F2 con Π1/Π2). Imprime PASS/FAIL para cada uno. |

---

### `algoritmos.py` — Algoritmos (Stubs #TODO)

| Función | Sección | Complejidad | Descripción |
|---------|---------|-------------|-------------|
| `roFB(finca)` | §3.1 | O(n! × n) | **Fuerza Bruta.** Genera todas las n! permutaciones y retorna la de costo mínimo. Siempre óptima. |
| `roV(finca)` | §3.2 | O(n log n) | **Algoritmo Voraz.** El estudiante elige y documenta su criterio greedy. Puede no ser óptima. |
| `roPD(finca)` | §3.3 | O(n² × 2ⁿ) | **Programación Dinámica.** Bitmask DP sobre subconjuntos de tablones. Siempre óptima. |

> ⚠️ Los tres algoritmos lanzan `NotImplementedError` hasta que el estudiante los implemente.

---

### `io_handler.py` — Entrada/Salida de Archivos

| Función | Descripción |
|---------|-------------|
| `leer_finca_desde_archivo(path)` | **§3.4.1** — Lee una finca de un `.txt`. Formato: línea 1 = `n`, líneas siguientes = `ts,tr,p,rp`. Reporta errores con número de línea. |
| `escribir_solucion_a_archivo(solucion, path)` | **§3.4.2** — Escribe la solución: línea 1 = costo total, líneas siguientes = ids en orden. |
| `leer_solucion_desde_archivo(path)` | Lee una solución previamente guardada. Retorna `(costo, permutacion)`. |
| `exportar_comparacion_csv(resultados, path)` | Exporta benchmark a CSV con columnas: `n, algoritmo, costo, tiempo_ms, es_optima`. |

---

### `generador.py` — Generación de Fincas

| Función | Descripción |
|---------|-------------|
| `generar_finca_aleatoria(n, seed)` | Genera finca con `n` tablones aleatorios. Garantiza `0 ≤ rp ≤ ts-tr`. Rangos: `ts∈[3,20]`, `tr∈[1,ts//2]`, `p∈[1,4]`. Acepta semilla para reproducibilidad. |
| `generar_finca_extrema(n, tipo)` | Genera fincas de casos extremos: `todos_criticos` (p=4, ts≈tr), `todos_perfectos` (rp=0), `gran_prioridad` (p creciente), `supervivencia_corta` (ts muy pequeño). |
| `generar_suite_pruebas(n_values)` | Genera una finca por cada valor de n (default: [3,4,5,6,7,8,10,12,15]). Para benchmarking. |

---

### `analisis.py` — Benchmarking y Métricas

| Función / Clase | Descripción |
|-----------------|-------------|
| `MetricasEjecucion` | Dataclass con: `algoritmo`, `n`, `costo`, `tiempo_ms`, `memoria_bytes`, `es_optima`, `permutacion`. |
| `medir_ejecucion(fn, finca, algoritmo, solucion_optima)` | Ejecuta un algoritmo midiendo tiempo (`perf_counter`) y memoria pico (`tracemalloc`). Compara con solución óptima si se provee. |
| `comparar_tres_algoritmos(finca, incluir_fb)` | Ejecuta FB, V y PD sobre la misma finca. Usa FB como ground truth. Omite FB si `n > 10`. Captura `NotImplementedError`. |
| `benchmark_escalabilidad(n_values, repeticiones)` | Para cada `n`, genera finca y ejecuta los 3 algoritmos. Promedia sobre `repeticiones` ejecuciones. Retorna lista plana de métricas. |
| `calcular_gap_optimalidad(metricas_voraz, metricas_fb)` | Calcula: `(costo_voraz - costo_optimo) / costo_optimo × 100`. |
| `resumen_tabla(lista_metricas)` | Genera tabla ASCII formateada: `Algoritmo | n | Costo | Tiempo (ms) | Memoria (KB) | ¿Óptima?`. |

---

### `gui/app.py` — Ventana Principal

| Método | Descripción |
|--------|-------------|
| `__init__()` | Crea la ventana principal (1100×750), estado compartido, menú, notebook, barra de estado y polling de hilos. |
| `_crear_menu()` | Barra de menú: Archivo (nueva/abrir/guardar/exportar/salir), Ejecutar (FB/V/PD/todos), Ayuda (verificar/acerca de). |
| `_crear_notebook()` | Crea las 4 pestañas: Manual, Archivo, Aleatorio, Resultados. |
| `_crear_barra_estado()` | Barra inferior con: n, algoritmo, costo, tiempo. |
| `actualizar_estado(n, algo, costo, tiempo_ms)` | Actualiza los labels de la barra de estado. |
| `_ejecutar_algo(nombre)` | Ejecuta un algoritmo en hilo de fondo, envía resultado por cola. |
| `_poll_resultados()` | Polling cada 100ms de la cola de resultados de hilos. |
| `set_finca(finca)` | Establece la finca actual y actualiza la barra de estado. |

---

### `gui/tab_manual.py` — Pestaña Manual

| Método | Descripción |
|--------|-------------|
| `_crear_formulario()` | Formulario con campos ts, tr, p (spinbox 1–4), rp y botón "Añadir tablón". |
| `_añadir_tablon()` | Valida entrada, crea Tablon, actualiza tabla y preview. |
| `_crear_tabla()` | Treeview con columnas id/ts/tr/p/rp. Menú contextual (editar/eliminar). Doble-click para editar. |
| `_editar_tablon()` | Abre diálogo modal para editar un tablón existente. |
| `_eliminar_tablon()` | Elimina tablón seleccionado y re-indexa los restantes. |
| `_cargar_ejemplo1()` | Carga la Finca F1 del ejemplo §2.3. |
| `_cargar_ejemplo2()` | Carga la Finca F2 del ejemplo §2.3. |
| `_crear_preview()` | Canvas de barras horizontales: barra gris=ts, barra azul=tr, línea roja=rp. |
| `limpiar()` | Reinicia todos los tablones. |

---

### `gui/tab_archivo.py` — Pestaña Archivo

| Método | Descripción |
|--------|-------------|
| `seleccionar_archivo()` | Diálogo para seleccionar archivo `.txt`. Muestra contenido en preview. |
| `_parsear()` | Llama `leer_finca_desde_archivo`. Muestra errores en rojo o llena la tabla con la finca parseada. |
| `_ejecutar_y_guardar()` | Ejecuta el algoritmo seleccionado y guarda la solución en un `.txt`. |

---

### `gui/tab_random.py` — Pestaña Aleatorio

| Método | Descripción |
|--------|-------------|
| `_generar()` | Genera finca con parámetros del formulario (n, semilla, tipo normal/extremo). Muestra resultado en tabla. |
| `_ejecutar_benchmark()` | Ejecuta `benchmark_escalabilidad` en hilo de fondo con barra de progreso. Al terminar, muestra tabla ASCII y envía datos a la pestaña de resultados. |

---

### `gui/tab_resultados.py` — Pestaña Resultados

| Método | Descripción |
|--------|-------------|
| `mostrar_solucion(solucion)` | Llena la tabla de detalle con colores por caso (verde=1, amarillo=2, rojo=3). Actualiza métricas y gráficos de comparación. |
| `_dibujar_comparacion()` | Dibuja barras agrupadas de costo y tiempo en Canvas. Colores: FB=azul, V=naranja, PD=verde. |
| `mostrar_benchmark(metricas)` | Recibe datos de benchmark y dibuja gráfico de escalabilidad. |
| `_dibujar_escalabilidad()` | Gráfico de líneas (tiempo vs n) con ejes, grid, leyenda. |
| `_exportar()` | Exporta resultados de benchmark a CSV. |

---

### `main.py` — Punto de Entrada

| Función | Descripción |
|---------|-------------|
| `main()` | Ejecuta `verificar_ejemplo_enunciado()` como auto-test, imprime resultados, luego lanza `App().mainloop()`. |

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

### Archivo de Solución (salida — §3.4.2)
```
31.0
2
1
4
3
0
```
- Línea 1: costo total
- Líneas siguientes: id de cada tablón en el orden de riego

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

1. **`roFB(finca)`** — Fuerza bruta con `itertools.permutations`.
2. **`roV(finca)`** — Algoritmo voraz con criterio documentado.
3. **`roPD(finca)`** — Programación dinámica con bitmask.

Todo lo demás (modelos, cálculos, I/O, generador, análisis, GUI) está completamente implementado y funcional.
