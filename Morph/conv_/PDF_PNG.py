# pip install pdf2image pillow
from tkinter import ttk
from pdf2image import convert_from_path
from PIL import Image
import os

class conv_pdf_png:
    nombre = "PDF → PNG"
    
    def __init__(self, dir_pdf=None, dir_out=None, dpi=300):
        self.dir_pdf = dir_pdf
        self.dir_out = dir_out
        self.dpi = dpi


    def get_frame(self, parent):
        frame = ttk.Frame(parent)

        ttk.Label(frame, text="Directorio PDF:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.entry_pdf = ttk.Entry(frame, width=40)
        self.entry_pdf.grid(row=0, column=1, padx=5, pady=3)
        if self.dir_pdf:
            self.entry_pdf.insert(0, self.dir_pdf)

        ttk.Label(frame, text="Directorio salida:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
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
        dir_pdf = self.entry_pdf.get().strip()
        dir_out = self.entry_output.get().strip()
        try:
            cambios = self.pdf_png(dir_pdf, dir_out, self.dpi)
            self.label_result.config(text=cambios)
        except Exception as e:
            self.label_result.config(text=f"Error: {e}")

    def pdf_png(self, dir_pdf, dir_out, dpi=300):
        for archivo in os.listdir(dir_pdf):
            if not archivo.lower().endswith(".pdf"):
                continue
            dir_pdf = os.path.join(dir_pdf, archivo)
            pages = convert_from_path(dir_pdf, dpi=dpi)
            for i, page in enumerate(pages):
                filename = os.path.join(dir_out, f"pagina_{i+1}.png")
                page.save(filename, 'PNG')
                print(f"Página {i+1} guardada como {filename}")



