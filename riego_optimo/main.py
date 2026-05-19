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
    from gui_ctk import RiegoOptimoApp
    print("Iniciando interfaz gráfica con CustomTkinter...")
    app = RiegoOptimoApp()
    app.mainloop()


if __name__ == '__main__':
    main()
