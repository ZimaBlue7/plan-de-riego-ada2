"""
main.py — Punto de entrada de la aplicación Riego Óptimo.

1. Ejecuta la auto-verificación contra los ejemplos del enunciado.
2. Lanza la interfaz gráfica.
"""

import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    """Punto de entrada principal de la aplicación."""
    # 1. Auto-verificación contra ejemplos del enunciado
    from calculos import verificar_ejemplo_enunciado

    print("═══ Verificación de ejemplos del enunciado (§2.3) ═══")
    ok = verificar_ejemplo_enunciado()
    if not ok:
        print("ADVERTENCIA: Algunas verificaciones fallaron. Revise calculos.py.")
    else:
        print("Todas las verificaciones pasaron correctamente.")
    print()

    # 2. Lanzar la GUI
    from gui_ctk import RiegoOptimoApp
    print("Iniciando interfaz gráfica con CustomTkinter...")
    app = RiegoOptimoApp()
    app.mainloop()


if __name__ == '__main__':
    main()
