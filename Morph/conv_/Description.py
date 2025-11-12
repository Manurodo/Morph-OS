import tkinter as tk
from tkinter import ttk

class conv_help:
    nombre = "Ayuda"

    def __init__(self):
        self.conversores_info = {
            "MP3 ↔ OOG": "Convierte archivos de audio entre formatos MP3 y OOG.",
            "PDF ↔ PNG": "Convierte archivos PDF a imágenes PNG y viceversa.",
            "Modificar Archivos": "Renombra archivos en un directorio eliminando letras del nombre y añadiendo un prefijo personalizado.",
            # Añade aquí más conversores según vayas creando
        }

    def get_frame(self, parent):
        frame = ttk.Frame(parent, padding=10)

        # Título
        titulo = ttk.Label(frame, text="Conversores Disponibles", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)

        # Frame scrollable para la lista
        canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Información de cada conversor
        for nombre, descripcion in self.conversores_info.items():
            item_frame = ttk.LabelFrame(scrollable_frame, text=nombre, padding=8)
            item_frame.pack(fill="x", padx=5, pady=5)

            desc_label = ttk.Label(item_frame, text=descripcion, wraplength=300, justify="left")
            desc_label.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return frame