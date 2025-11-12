import importlib
import pkgutil
import tkinter as tk
from tkinter import ttk
import sys
from PIL import Image, ImageTk
import conv_

def cargar_conversores():
    modulos = []
    if not hasattr(conv_, "__path__"):
        print("conversores no es un paquete: añade conversores/__init__.py")
        return modulos

    importlib.invalidate_caches()
    print("DEBUG: sys.path =", sys.path)
    print("DEBUG: conv_.__path__ =", list(conv_.__path__))

    for finder, nombre, ispkg in pkgutil.iter_modules(conv_.__path__):
        print("Encontrado módulo:", nombre, "ispkg=", ispkg)
        try:
            modulo = importlib.import_module(f"{conv_.__name__}.{nombre}")
        except Exception as e:
            print(f"  Error importando conversores.{nombre}: {e}")
            continue

        print(f"  Atributos en {nombre}: {dir(modulo)}")
        for attr in dir(modulo):
            if attr.startswith("__"):
                continue
            obj = getattr(modulo, attr)
            print(f"    {attr}: {type(obj)}")  # depuración tipo

            # clases nombradas Conversor*
            if isinstance(obj, type) and attr.startswith("Conversor"):
                print("  Clase encontrada:", attr)
                try:
                    modulos.append(obj())
                except Exception as e:
                    print("    Error instanciando:", e)
            # clases que exponen la interfaz pero no siguen la convención de nombre
            elif isinstance(obj, type) and hasattr(obj, "get_frame") and hasattr(obj, "nombre"):
                print("  Clase que implementa interfaz encontrada (instanciando):", attr)
                try:
                    modulos.append(obj())
                except Exception as e:
                    print("    Error instanciando:", e)
            # objetos ya instanciados que exponen la interfaz
            elif hasattr(obj, "get_frame") and hasattr(obj, "nombre"):
                print("  Objeto conversor encontrado (instancia):", attr)
                try:
                    modulos.append(obj)
                except Exception as e:
                    print("    Error añadiendo objeto:", e)
    return modulos


def main():
    root = tk.Tk()
    root.title("Morph")
    root.geometry("800x400")

    img = Image.open(r"C:\Mio\Git\Pyxego\Morph Test\Gui test\logo.png")  # JPG, PNG, etc.
    img = img.resize((100, 100))  # Redimensionar si quieres
    logo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(root, image=logo)
    logo_label.pack(pady=10)
    root.iconphoto(True, logo)  # logo debe ser PhotoImage


    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    conversores_instancias = cargar_conversores()
    for conversor in conversores_instancias:
        frame = conversor.get_frame(notebook)
        notebook.add(frame, text=conversor.nombre)

    root.mainloop()

if __name__ == "__main__":
    main()
