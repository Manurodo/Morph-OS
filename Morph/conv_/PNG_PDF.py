from tkinter import ttk
from pdf2image import convert_from_path
from PIL import Image
import os

class conv_png_pdf:
    nombre = "PDF ← PNG"
    
    def __init__(self, dir_png=None, dir_out=None):
        self.dir_png = dir_png
        self.dir_out = dir_out

    def get_frame(self, parent):
        frame = ttk.Frame(parent)

        ttk.Label(frame, text="Directorio PNG:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.entry_png = ttk.Entry(frame, width=40)
        self.entry_png.grid(row=0, column=1, padx=5, pady=3)
        if self.dir_png:
            self.entry_png.insert(0, self.dir_png)

        ttk.Label(frame, text="Directorio Archivo PDF salida:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.entry_output = ttk.Entry(frame, width=40)
        self.entry_output.grid(row=1, column=1, padx=5, pady=3)
        if self.dir_out:
            self.entry_output.insert(0, self.dir_out)

        boton = ttk.Button(frame, text="Convertir", command=self.convertir)
        boton.grid(row=2, column=0, columnspan=2, pady=5)

        self.label_result = ttk.Label(frame, text="")
        self.label_result.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        return frame
    
    def convertir(self):
        dir_png = self.entry_png.get().strip()
        dir_out = self.entry_output.get().strip()
        try:
            cambios = self.png_pdf(dir_png, dir_out)
            self.label_result.config(text=cambios)
        except Exception as e:
            self.label_result.config(text=f"Error: {e}")

    def png_pdf(self, dir_png, dir_out):
        # Intentar encontrar manera para funcionar unicamente con dir_png y guardar el pdf en la misma carpeta
        
        # Lista de imágenes en la carpeta, ordenadas alfabéticamente
        png_files = [f for f in os.listdir(dir_png) if f.lower().endswith('.png')]
        png_files.sort()
        
        images = [Image.open(os.path.join(dir_png, f)).convert('RGB') for f in png_files]
        
        if images:
            images[0].save(dir_out, save_all=True, append_images=images[1:])
            resultado = f"PDF generado en: {dir_out}"
            print(resultado)
            return resultado
        else:
            resultado = "No se encontraron imágenes PNG en la carpeta."
            print(resultado)
            return resultado