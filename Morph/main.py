import os
import importlib
import pkgutil
import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path
from PIL import Image, ImageTk

import conv_


def cargar_conversores():
    modulos = []

    if not hasattr(conv_, "__path__"):
        print("ERROR: conv_ no es un paquete")
        return modulos

    importlib.invalidate_caches()

    print("DEBUG: sys.path =", sys.path)
    print("DEBUG: conv_.__path__ =", list(conv_.__path__))

    for ruta in conv_.__path__:
        print("DEBUG: contenido de", ruta)

        try:
            print(os.listdir(ruta))
        except Exception as e:
            print("ERROR listando carpeta:", e)

    for finder, nombre, ispkg in pkgutil.iter_modules(conv_.__path__):

        print("Encontrado módulo:", nombre, "ispkg=", ispkg)

        if ispkg:
            continue

        try:
            modulo = importlib.import_module(
                f"{conv_.__name__}.{nombre}"
            )

        except Exception as e:
            print(
                f"ERROR importando "
                f"{conv_.__name__}.{nombre}: {e}"
            )
            continue

        print(f"Módulo cargado: {nombre}")

        for attr in dir(modulo):

            if attr.startswith("__"):
                continue

            obj = getattr(modulo, attr)

            # Clase Conversor...
            if isinstance(obj, type) and attr.startswith("Conversor"):

                print(f"  Conversor encontrado: {attr}")

                try:
                    modulos.append(obj())
                except Exception as e:
                    print(f"  Error instanciando {attr}: {e}")

            # Clase con interfaz
            elif (
                isinstance(obj, type)
                and hasattr(obj, "get_frame")
                and hasattr(obj, "nombre")
            ):

                print(f"  Conversor encontrado: {attr}")

                try:
                    modulos.append(obj())
                except Exception as e:
                    print(f"  Error instanciando {attr}: {e}")

            # Objeto con interfaz
            elif (
                hasattr(obj, "get_frame")
                and hasattr(obj, "nombre")
            ):

                print(f"  Objeto conversor encontrado: {attr}")

                modulos.append(obj)

    print(
        f"Total de conversores encontrados: "
        f"{len(modulos)}"
    )

    return modulos

def main():

    root = tk.Tk()

    root.title("Morph")
    root.geometry("800x400")

    # --------------------------------
    # Logo
    # --------------------------------

    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    logo_path = base_path / "logo.png"

    img = Image.open(logo_path)
    img = img.resize((100, 100))

    logo = ImageTk.PhotoImage(img)

    logo_label = tk.Label(root, image=logo)
    logo_label.pack(pady=10)

    root.iconphoto(True, logo)

    # --------------------------------
    # Notebook
    # --------------------------------

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # --------------------------------
    # Cargar conversores
    # --------------------------------

    conversores_instancias = cargar_conversores()

    for conversor in conversores_instancias:

        try:
            frame = conversor.get_frame(notebook)

            notebook.add(
                frame,
                text=conversor.nombre
            )

        except Exception as e:
            print(
                f"Error cargando conversor "
                f"{getattr(conversor, 'nombre', '?')}: {e}"
            )

    root.mainloop()


if __name__ == "__main__":
    main()