import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from typing import List, Optional

from models import Finca, Tablon, Solucion
from io_handler import leer_finca_desde_archivo
from algoritmos import roFB, roV, roPD
from calculos import calcular_costo_total, construir_solucion
import analisis

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RiegoOptimoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Riego Óptimo — Optimizador de Fincas")
        self.geometry("1000x700")

        self.finca_actual: Optional[Finca] = None
        
        # Configuración de Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Opciones y Algoritmos) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Riego Óptimo", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.pack(pady=(20, 10))

        # Sección de Algoritmos
        self.algo_label = ctk.CTkLabel(self.sidebar, text="Algoritmos:", font=ctk.CTkFont(weight="bold"))
        self.algo_label.pack(pady=(20, 5), anchor="w", padx=20)

        self.var_fb = tk.BooleanVar(value=True)
        self.check_fb = ctk.CTkCheckBox(self.sidebar, text="Fuerza Bruta (FB)", variable=self.var_fb)
        self.check_fb.pack(pady=5, anchor="w", padx=30)

        self.var_v = tk.BooleanVar(value=True)
        self.check_v = ctk.CTkCheckBox(self.sidebar, text="Voraz (V)", variable=self.var_v)
        self.check_v.pack(pady=5, anchor="w", padx=30)

        self.var_pd = tk.BooleanVar(value=True)
        self.check_pd = ctk.CTkCheckBox(self.sidebar, text="Prog. Dinámica (PD)", variable=self.var_pd)
        self.check_pd.pack(pady=5, anchor="w", padx=30)

        # Repeticiones
        self.rep_label = ctk.CTkLabel(self.sidebar, text="Repeticiones para promedio:", font=ctk.CTkFont(weight="bold"))
        self.rep_label.pack(pady=(20, 5), anchor="w", padx=20)
        
        self.rep_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 5")
        self.rep_entry.insert(0, "1")
        self.rep_entry.pack(pady=5, padx=20, fill="x")

        # Botón Procesar
        self.btn_procesar = ctk.CTkButton(self.sidebar, text="Procesar Finca", command=self.ejecutar_procesamiento, height=40, font=ctk.CTkFont(weight="bold"))
        self.btn_procesar.pack(pady=40, padx=20, fill="x")

        # --- Contenido Principal ---
        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # Top Bar (Carga de datos)
        self.top_bar = ctk.CTkFrame(self.main_content)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.btn_file = ctk.CTkButton(self.top_bar, text="Cargar desde Archivo .txt", command=self.cargar_archivo)
        self.btn_file.pack(side="left", padx=10, pady=10)

        self.btn_clear = ctk.CTkButton(self.top_bar, text="Limpiar Editor", command=lambda: self.data_editor.delete("0.0", "end"), fg_color="transparent", border_width=1)
        self.btn_clear.pack(side="left", padx=10, pady=10)

        self.info_format = ctk.CTkLabel(self.top_bar, text="Formato Requerido:\nLínea 1: n\nLíneas 2+: ts,tr,p,rp", 
                                        font=ctk.CTkFont(size=11, slant="italic"), text_color="gray")
        self.info_format.pack(side="right", padx=10)

        # Editor Manual
        self.editor_label = ctk.CTkLabel(self.main_content, text="Entrada de Datos (Manual/Editable):", font=ctk.CTkFont(weight="bold"))
        self.editor_label.grid(row=1, column=0, sticky="w", padx=20, pady=(10, 0))

        self.data_editor = ctk.CTkTextbox(self.main_content, font=ctk.CTkFont(family="Courier", size=14))
        self.data_editor.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.data_editor.insert("0.0", "# Formato:\n# n\n# ts,tr,p,rp\n3\n10,2,3,0\n15,5,4,2\n8,3,2,1")

        # --- Resultados ---
        self.results_frame = ctk.CTkScrollableFrame(self.main_content, label_text="Resultados y Métricas")
        self.results_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        self.results_text = ctk.CTkLabel(self.results_frame, text="Los resultados aparecerán aquí...", justify="left", font=ctk.CTkFont(family="Courier", size=12))
        self.results_text.pack(pady=10, padx=10, fill="both")

    def cargar_archivo(self):
        filename = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.data_editor.delete("0.0", "end")
                self.data_editor.insert("0.0", content)
                messagebox.showinfo("Éxito", "Archivo cargado correctamente en el editor.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def parse_finca_from_editor(self) -> Optional[Finca]:
        text = self.data_editor.get("0.0", "end").strip()
        lines = [line.strip() for line in text.split('\n') if line.strip() and not line.strip().startswith('#')]
        
        if not lines:
            messagebox.showwarning("Advertencia", "El editor está vacío.")
            return None

        try:
            n = int(lines[0])
            if len(lines) < n + 1:
                raise ValueError(f"Se esperaban {n} tablones, pero solo hay {len(lines)-1} líneas de datos.")
            
            tablones = []
            for i in range(1, n + 1):
                partes = lines[i].split(',')
                if len(partes) != 4:
                    raise ValueError(f"Línea {i+1}: Se esperaban 4 valores (ts,tr,p,rp), se encontraron {len(partes)}")
                
                ts, tr, p, rp = map(int, partes)
                tablon = Tablon(id=i-1, ts=ts, tr=tr, p=p, rp=rp)
                tablones.append(tablon)
            
            return Finca(tablones=tablones)
        except Exception as e:
            messagebox.showerror("Error de Formato", f"Error al procesar los datos:\n{e}")
            return None

    def ejecutar_procesamiento(self):
        finca = self.parse_finca_from_editor()
        if not finca:
            return

        try:
            reps = int(self.rep_entry.get())
            if reps <= 0: raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "El número de repeticiones debe ser un entero positivo.")
            return

        # Desactivar botón para evitar múltiples clics
        self.btn_procesar.configure(state="disabled", text="Procesando...")
        self.results_text.configure(text="Ejecutando algoritmos...")

        # Ejecutar en un hilo para no congelar la GUI
        def worker():
            try:
                resultados = self.medir_todo(finca, reps)
                self.after(0, lambda: self.mostrar_resultados(resultados))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error en ejecución", str(e)))
            finally:
                self.after(0, lambda: self.btn_procesar.configure(state="normal", text="Procesar Finca"))

        threading.Thread(target=worker, daemon=True).start()

    def medir_todo(self, finca: Finca, reps: int):
        algos_to_run = []
        if self.var_fb.get(): algos_to_run.append(("Fuerza Bruta", roFB))
        if self.var_v.get(): algos_to_run.append(("Voraz", roV))
        if self.var_pd.get(): algos_to_run.append(("Prog. Dinámica", roPD))

        if not algos_to_run:
            raise Exception("Debe seleccionar al menos un algoritmo.")

        results_data = []
        
        for nombre, fn in algos_to_run:
            tiempos = []
            ultima_sol: Optional[Solucion] = None
            error = None
            
            for _ in range(reps):
                try:
                    start = time.perf_counter()
                    ultima_sol = fn(finca)
                    end = time.perf_counter()
                    tiempos.append((end - start) * 1000) # ms
                except NotImplementedError:
                    error = "No implementado"
                    break
                except Exception as e:
                    error = str(e)
                    break
            
            if error:
                results_data.append({
                    "algoritmo": nombre,
                    "error": error
                })
            else:
                avg_time = sum(tiempos) / len(tiempos)
                results_data.append({
                    "algoritmo": nombre,
                    "costo": ultima_sol.costo_total,
                    "tiempo_avg": avg_time,
                    "permutacion": ultima_sol.permutacion,
                    "solucion": ultima_sol
                })
        
        return results_data

    def mostrar_resultados(self, resultados):
        resumen = "═══ RESULTADOS DEL PROCESAMIENTO ═══\n\n"
        
        # Tabla comparativa
        header = f"{'Algoritmo':<20} | {'Costo':<12} | {'Promedio (ms)':<15}\n"
        separator = "-" * 55 + "\n"
        resumen += header + separator
        
        for res in resultados:
            if "error" in res:
                resumen += f"{res['algoritmo']:<20} | {res['error']:<30}\n"
            else:
                resumen += f"{res['algoritmo']:<20} | {res['costo']:<12.2f} | {res['tiempo_avg']:<15.4f}\n"
        
        resumen += "\n" + separator + "\n"
        
        # Detalle de la mejor solución (por costo)
        valid_results = [r for r in resultados if "error" not in r]
        if valid_results:
            mejor = min(valid_results, key=lambda x: x['costo'])
            resumen += f"MEJOR RESULTADO: {mejor['algoritmo']}\n"
            resumen += f"Costo mínimo hallado: {mejor['costo']:.2f}\n"
            resumen += f"Permutación: {mejor['permutacion']}\n\n"
            
            # Si el usuario quiere ver el detalle completo de uno, lo mostramos (del último o mejor)
            resumen += "DETALLE DE EJECUCIÓN (Ejemplo):\n"
            resumen += mejor['solucion'].resumen()
        
        self.results_text.configure(text=resumen)

if __name__ == "__main__":
    app = RiegoOptimoApp()
    app.mainloop()
