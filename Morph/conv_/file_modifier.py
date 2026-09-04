import os
import re
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from pathlib import Path


class conv_file_modifier:
    nombre = "Modificar Archivos"

    def __init__(self, dir_in=None, cadena=None):
        self.dir_in = dir_in
        self.cadena = cadena

    def get_frame(self, parent):
        frame = ttk.Frame(parent)

        # Botón para seleccionar carpeta
        boton_carpeta = ttk.Button(
            frame,
            text="Seleccionar Carpeta",
            command=self.select_directory
        )
        boton_carpeta.grid(row=0, column=0, columnspan=2, pady=5)

        # Prefijo
        ttk.Label(
            frame,
            text="Prefijo:"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=3)

        self.entry_prefijo = ttk.Entry(frame)
        self.entry_prefijo.grid(row=1, column=1, padx=5, pady=3)

        if self.cadena:
            self.entry_prefijo.insert(0, self.cadena)

        # Botón renombrar
        boton = ttk.Button(
            frame,
            text="Renombrar",
            command=self.convertir
        )
        boton.grid(row=2, column=0, columnspan=2, pady=5)

        # Resultado
        self.label_result = ttk.Label(frame, text="")
        self.label_result.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=5,
            pady=5
        )

        return frame

    def select_directory(self):
        ruta_carpeta = filedialog.askdirectory(
            title="Selecciona una carpeta"
        )

        if ruta_carpeta:
            self.dir_in = Path(ruta_carpeta)

            print("Ruta seleccionada:")
            print(self.dir_in)

            self.label_result.config(
                text=f"Carpeta: {self.dir_in}"
            )

        else:
            print("No se seleccionó ninguna carpeta.")

    def convertir(self):
        # Comprobar que se ha seleccionado una carpeta
        if self.dir_in is None:
            self.label_result.config(
                text="Error: selecciona una carpeta primero."
            )
            return
        cadena = self.entry_prefijo.get().strip()

        try:
            cambios = self.file_modifier(
                self.dir_in,
                cadena
            )

            self.label_result.config(
                text=f"Archivos renombrados: {cambios}"
            )

        except Exception as e:
            self.label_result.config(
                text=f"Error: {e}"
            )

    def file_modifier(self, dir_in, cadena):
        if not os.path.isdir(dir_in):
            raise FileNotFoundError(
                f"Directorio no encontrado: {dir_in}"
            )

        contador = 0

        for filename in os.listdir(dir_in):

            nombre, extension = os.path.splitext(filename)

            # Eliminar solamente las letras
            nuevo_nombre = re.sub(
                r'[a-zA-Z]',
                '',
                nombre
            ).lstrip()

            nuevo_nombre_completo = (
                f"{cadena}{nuevo_nombre}{extension}"
            )

            ruta_original = os.path.join(
                dir_in,
                filename
            )

            nueva_ruta = os.path.join(
                dir_in,
                nuevo_nombre_completo
            )

            # Evitar sobrescribir archivos existentes
            if os.path.exists(nueva_ruta):
                continue

            os.rename(
                ruta_original,
                nueva_ruta
            )

            contador += 1

        return contador