# pip install pdf2image pillow

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from pathlib import Path
from pdf2image import convert_from_path, pdfinfo_from_path
import threading
import sys


class conv_pdf_png:
    nombre = "PDF → PNG"

    def __init__(self, dir_pdf=None, dir_out=None, dpi=300):
        self.dir_pdf = dir_pdf
        self.dir_out = dir_out
        self.dpi = dpi

    def get_frame(self, parent):
        frame = ttk.Frame(parent)

        # Guardamos la ventana principal
        self.root = parent.winfo_toplevel()

        # Seleccionar PDF
        boton_pdf = ttk.Button(
            frame,
            text="Seleccionar Archivo PDF",
            command=self.select_file
        )
        boton_pdf.grid(row=0, column=0, columnspan=2, pady=5)

        # Seleccionar carpeta de salida
        boton_out = ttk.Button(
            frame,
            text="Seleccionar Carpeta PNG",
            command=self.select_directory_out
        )
        boton_out.grid(row=1, column=0, columnspan=2, pady=5)

        # Convertir
        self.boton_convertir = ttk.Button(
            frame,
            text="Convertir",
            command=self.convertir
        )
        self.boton_convertir.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=5
        )

        # Barra de progreso
        self.progress = ttk.Progressbar(
            frame,
            orient="horizontal",
            length=250,
            mode="determinate"
        )
        self.progress.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Resultado
        self.label_result = ttk.Label(frame, text="")
        self.label_result.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=5,
            pady=5
        )

        return frame

    def select_file(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Selecciona un archivo PDF",
            filetypes=[
                ("Archivos PDF", "*.pdf"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta_archivo:
            self.dir_pdf = Path(ruta_archivo)

            self.label_result.config(
                text=f"PDF: {self.dir_pdf}"
            )
        else:
            print("No se seleccionó ningún archivo.")

    def select_directory_out(self):
        ruta_carpeta = filedialog.askdirectory(
            title="Selecciona una carpeta de salida"
        )

        if ruta_carpeta:
            self.dir_out = Path(ruta_carpeta)

            self.label_result.config(
                text=f"Salida: {self.dir_out}"
            )
        else:
            print("No se seleccionó ninguna carpeta.")

    def convertir(self):

        if self.dir_pdf is None:
            self.label_result.config(
                text="Error: selecciona un PDF primero."
            )
            return

        if self.dir_out is None:
            self.label_result.config(
                text="Error: selecciona una carpeta de salida."
            )
            return

        # Desactivar botón mientras convierte
        self.boton_convertir.config(state="disabled")

        self.label_result.config(
            text="Iniciando conversión..."
        )

        # Crear hilo
        hilo = threading.Thread(
            target=self.pdf_png,
            args=(self.dir_pdf, self.dir_out, self.dpi),
            daemon=True
        )

        hilo.start()

    def get_poppler_path(self):

        if getattr(sys, "frozen", False):
            # Estamos ejecutando el .exe
            base_path = Path(sys._MEIPASS)
        else:
            # Estamos ejecutando desde Python
            base_path = Path(__file__).resolve().parent.parent

        poppler_path = (
            base_path
            / "bin"
            / "poppler"
            / "Library"
            / "bin"
        )

        return poppler_path

    def pdf_png(self, dir_pdf, dir_out, dpi=300):

        try:

            # Obtener Poppler
            poppler_path = self.get_poppler_path()

            print("Poppler:")
            print(poppler_path)

            # Comprobar que existe
            if not poppler_path.exists():
                raise FileNotFoundError(
                    f"No se encontró Poppler en:\n{poppler_path}"
                )


            # Obtener número de páginas
            info = pdfinfo_from_path(
                str(dir_pdf), 
                poppler_path=str(poppler_path)
            )
            total_paginas = info["Pages"]

            # Configurar barra de progreso
            self.root.after(
                0,
                lambda: self.progress.config(
                    maximum=total_paginas,
                    value=0
                )
            )

            nombre_pdf = Path(dir_pdf).stem

            for i in range(1, total_paginas + 1):

                # Convertir pagina por pagina repetidamente
                pages = convert_from_path(
                    str(dir_pdf),
                    dpi=dpi,
                    first_page=i,
                    last_page=i,
                    poppler_path=str(poppler_path)
                )

                filename = (
                    Path(dir_out)
                    / f"{nombre_pdf}_pagina_{i}.png"
                )

                pages[0].save(
                    filename,
                    "PNG"
                )

                print(
                    f"Página {i}/{total_paginas} guardada"
                )

                # Actualizar interfaz desde el hilo principal
                self.root.after(
                    0,
                    self.actualizar_progreso,
                    i,
                    total_paginas
                )

            # Conversión terminada
            self.root.after(
                0,
                self.conversion_terminada,
                total_paginas
            )

        except Exception as e:

            print("ERROR:")
            print(e)

            self.root.after(
                0,
                self.error_conversion,
                str(e)
            )

    def actualizar_progreso(self, pagina, total):

        self.progress["value"] = pagina

        self.label_result.config(
            text=f"Convirtiendo página {pagina}/{total}"
        )

    def conversion_terminada(self, total):

        self.progress["value"] = total

        self.label_result.config(
            text=f"Conversión terminada: {total} páginas"
        )

        self.boton_convertir.config(
            state="normal"
        )

    def error_conversion(self, error):

        self.label_result.config(
            text=f"Error: {error}"
        )

        self.boton_convertir.config(
            state="normal"
        )
