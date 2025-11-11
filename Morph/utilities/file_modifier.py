import os
import re

print("introduzca directorio")
directorio = input("|: ")
print("introduzca Nuevo nombre")
cadena = input("|: ")


def file_modifier(directorio,cadena):
    # Recorre todos los archivos en el directorio
    for filename in os.listdir(directorio):
        # Separar el nombre del archivo y la extensión
        nombre, extension = os.path.splitext(filename)
        # Usar regex para eliminar las letras del nombre del archivo
        nuevo_nombre = re.sub(r'[a-zA-Z]', '', nombre).lstrip()
        # Crear el nuevo nombre agregando la cadena al principio
        nuevo_nombre_completo = f"{cadena}{nuevo_nombre}{extension}"
        # Obtener la ruta completa del archivo original y renombrarlo
        ruta_original = os.path.join(directorio, filename)
        nueva_ruta = os.path.join(directorio, nuevo_nombre_completo)
        os.rename(ruta_original, nueva_ruta)
        print(f"Archivo renombrado: {filename} -> {nuevo_nombre_completo}")

file_modifier(directorio,cadena)