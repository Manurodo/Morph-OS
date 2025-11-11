# pip install pdf2image pillow

from pdf2image import convert_from_path
from PIL import Image
import os

def pdf_png(pdf_path, output_folder='./', dpi=300):
    pages = convert_from_path(pdf_path, dpi=dpi)
    for i, page in enumerate(pages):
        filename = os.path.join(output_folder, f"pagina_{i+1}.png")
        page.save(filename, 'PNG')
        print(f"Página {i+1} guardada como {filename}")


def png_pdf(carpeta_png, output_pdf):
    # Lista de imágenes en la carpeta, ordenadas alfabéticamente
    png_files = [f for f in os.listdir(carpeta_png) if f.lower().endswith('.png')]
    png_files.sort()
    
    images = [Image.open(os.path.join(carpeta_png, f)).convert('RGB') for f in png_files]
    
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF generado: {output_pdf}")
    else:
        print("No se encontraron imágenes PNG en la carpeta.")

