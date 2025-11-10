import os

def agregar_str_al_principio(directorio, cadena):
    # Recorre todos los archivos en el directorio
    for filename in os.listdir(directorio):
        # Separar el nombre del archivo y la extensión
        nombre, extension = os.path.splitext(filename)
        # Crear el nuevo nombre agregando la cadena al principio
        nuevo_nombre_completo = f"{cadena}{nombre}{extension}"
        # Obtener la ruta completa del archivo original y renombrarlo
        ruta_original = os.path.join(directorio, filename)
        nueva_ruta = os.path.join(directorio, nuevo_nombre_completo)
        os.rename(ruta_original, nueva_ruta)
        print(f"Archivo renombrado: {filename} -> {nuevo_nombre_completo}")

# Ejemplo de uso
print("introduzca directorio en formato '/ruta/al/directorio'")
directorio = input("|: ")
print("introduzca str")
cadena = input("|: ")
agregar_str_al_principio(directorio, cadena)
