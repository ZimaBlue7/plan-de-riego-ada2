import os
import argparse
import sys
import glob
from typing import List

# Asegurar que el directorio actual esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from io_handler import leer_finca_desde_archivo
from algoritmos import roV, roFB, roPD

def procesar_multiples_archivos(rutas_archivos: List[str], ruta_salida: str, algoritmo: str = 'v'):
    """
    Procesa una lista de archivos .txt de fincas y escribe los resultados en un archivo,
    formateado similar a testAll.txt pero incluyendo el tiempo de ejecución.
    """
    algoritmo = algoritmo.lower()
    
    with open(ruta_salida, 'w', encoding='utf-8') as f_out:
        for ruta in sorted(rutas_archivos):
            nombre_archivo = os.path.basename(ruta)
            # Limpiar nombre (quitar _in si lo tiene para que se vea como test1, test2...)
            nombre_base = os.path.splitext(nombre_archivo)[0].replace('_in', '')
            
            try:
                finca = leer_finca_desde_archivo(ruta)
                
                if algoritmo == 'v':
                    solucion = roV(finca)
                    algo_str = 'v'
                elif algoritmo == 'fb':
                    solucion = roFB(finca)
                    algo_str = 'fb'
                elif algoritmo == 'pd':
                    solucion = roPD(finca)
                    algo_str = 'pd'
                else:
                    print(f"Algoritmo desconocido: {algoritmo}")
                    return
                
                # Escribir en formato testAll.txt
                f_out.write(f"=== {nombre_base} ({algo_str}) ===\n")
                f_out.write(f"{solucion.costo_total}\n")
                for tid in solucion.permutacion:
                    f_out.write(f"{tid}\n")
                
                # Escribir el tiempo de ejecución
                f_out.write(f"Tiempo: {solucion.tiempo_computo:.6f}s\n\n")
                
                print(f"Procesado: {ruta} -> Tiempo: {solucion.tiempo_computo:.6f}s")
                
            except Exception as e:
                print(f"Error procesando {ruta}: {e}")
                f_out.write(f"=== {nombre_base} ({algoritmo}) ===\n")
                f_out.write(f"ERROR: {e}\n\n")

def main():
    parser = argparse.ArgumentParser(description="Procesar automáticamente los archivos de ./Tests/tests")
    parser.add_argument('-o', '--output', required=True, help="Ruta del archivo de salida consolidado.")
    parser.add_argument('-a', '--algoritmo', choices=['v', 'fb', 'pd'], default='v', 
                        help="Algoritmo a usar: v (Voraz), fb (Fuerza Bruta), pd (Programación Dinámica)")
    
    args = parser.parse_args()
    
    # Buscar archivos en ../Tests/tests (asumiendo ejecución desde riego_optimo/)
    # o ./Tests/tests (si se ejecuta desde la raíz)
    path_tests = "../Tests/tests"
    if not os.path.exists(path_tests):
        path_tests = "./Tests/tests"
        
    if not os.path.exists(path_tests):
        print(f"❌ Error: No se encontró la carpeta de tests en {path_tests}")
        return

    archivos = glob.glob(os.path.join(path_tests, "*.txt"))
    
    if not archivos:
        print(f"❌ No se encontraron archivos .txt en {path_tests}")
        return

    print(f"Procesando {len(archivos)} archivos de {path_tests} con el algoritmo '{args.algoritmo.upper()}'...")
    procesar_multiples_archivos(archivos, args.output, args.algoritmo)
    print(f"✅ Finalizado. Resultados en: {args.output}")

if __name__ == '__main__':
    main()
