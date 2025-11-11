import os
from pydub import AudioSegment

def ogg_mp3(carpeta_entrada, carpeta_salida=None, bitrate="192k"):
    """
    Convierte todos los archivos .ogg de una carpeta a .mp3.

    Parámetros:
        carpeta_entrada (str): Carpeta donde están los archivos .ogg.
        carpeta_salida (str, opcional): Carpeta donde guardar los .mp3. Si no se indica, se usa la misma.
        bitrate (str, opcional): Calidad del MP3 (por defecto 192 kbps).
    """
    if not os.path.isdir(carpeta_entrada):
        raise NotADirectoryError(f"No existe la carpeta: {carpeta_entrada}")

    # Si no se da carpeta de salida, usar la misma
    if carpeta_salida is None:
        carpeta_salida = carpeta_entrada

    # Crear carpeta de salida si no existe
    os.makedirs(carpeta_salida, exist_ok=True)
    # Contador de conversiones
    convertidos = 0

    for archivo in os.listdir(carpeta_entrada):
        if archivo.lower().endswith(".ogg"):
            ruta_entrada = os.path.join(carpeta_entrada, archivo)
            nombre_salida = os.path.splitext(archivo)[0] + ".mp3"
            ruta_salida = os.path.join(carpeta_salida, nombre_salida)

            try:
                audio = AudioSegment.from_file(ruta_entrada, format="ogg")
                audio.export(ruta_salida, format="mp3", bitrate=bitrate)
                print(f"✅ Convertido: {archivo} → {nombre_salida}")
                convertidos += 1
            except Exception as e:
                print(f"❌ Error al convertir {archivo}: {e}")

    print(f"\n🎵 Conversión completa: {convertidos} archivos convertidos en '{carpeta_salida}'")

print("introduzca directorio entrada carpeta OGG")
directorio_entrada_OGG = input("|: ")
print("introduzca directorio salida carpeta MP3")
directorio_salida_MP3 = input("|: ")

ogg_mp3(directorio_entrada_OGG, directorio_salida_MP3)