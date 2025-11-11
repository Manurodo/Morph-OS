import os
import time
from utilities.file_modifier import file_modifier
from utilities.MP3_OGG import ogg_mp3, mp3_ogg
from utilities.PDF_PNG import pdf_png, png_pdf

# install poppler and ffmpeg and add to PATH

print("\nSeleccione tipo de herramienta:")
while True:
    print("\n1.✏️  Modificar nombre archivos","","2.📄 Documentos","","3.🎵 Archivos musicales","","H.🛠️  Descripción distintas herramientas","","S.❌  Salir",sep="\n")
    opcion = input("\n|: ")
    if opcion == "1":
        print("\nSeleccione modalidad:")
        while True:
            print("\n1.✏️  Modificar nombre archivos","","M.⬅️  Menú principal",sep="\n")
            opcion_modificar = input("\n|: ")
            if opcion_modificar == "1":
                while True:
                    print("\nIntroduzca directorio")
                    directorio = input("|: ")
                    if os.path.isdir(directorio):
                        break  # Ruta válida, salimos del bucle
                    else:
                        print("Directorio no válido. Intente nuevamente.")
        
                while True:
                    print("\nIntroduzca cadena")
                    cadena = input("|: ")
                    if all(c.isalnum() or c.isspace() for c in cadena):
                        break
                    else:
                        print("❌ No se permiten caracteres especiales. Intente nuevamente.")
                file_modifier(directorio,cadena)
                break
            elif opcion_modificar == "m" or opcion_modificar == "M":
                print("\nSeleccione tipo de herramienta:")
                break

    elif opcion == "2":
        print("\nSeleccione modalidad:")
        while True:
            print("\n1.📄 PDF a PNG","","2.🖼️  PNG a PDF","","M.⬅️  Menú principal",sep="\n")
            opcion_PDF_PNG = input("\n|: ")
            
            if opcion_PDF_PNG == "1":
                while True:
                    print("Introduzca la ruta del archivo PDF:")
                    archivo_pdf = input("|: ")
                    if os.path.exists(archivo_pdf):
                        break  # Ruta válida, salimos del bucle
                    else:
                        print("❌ Archivo no encontrado. Intente nuevamente.")
                
                while True:
                    print("Introduzca la ruta de la carpeta donde se guardarán las imágenes (deje vacío para usar ruta de archivo original):")
                    carpeta_salida = input("|: ")

                    if os.path.isdir(carpeta_salida):
                        break  # Ruta válida o vacía, continuamos
                    else:
                        print("❌ Directorio no válido. Intente nuevamente.")

                carpeta_salida = carpeta_salida if carpeta_salida.strip() else "imagenes_pdf"
                pdf_png(archivo_pdf, carpeta_salida)

            elif opcion_PDF_PNG == "2":
                while True:
                    print("\nIntroduzca la ruta de la carpeta que contiene las imágenes PNG:")
                    carpeta_png = input("|: ")

                    if os.path.isdir(carpeta_png):
                        break  # Ruta válida, salimos del bucle
                    else:
                        print("❌ Directorio no válido. Intente nuevamente.")

                while True:
                    print("Introduzca la ruta con el nombre del archivo PDF de salida (incluya .pdf):")
                    archivo_salida = input("|: ")
                    carpeta = os.path.dirname(archivo_salida) or "."  # "." si no hay carpeta explícita
                    nombre = os.path.basename(archivo_salida)

                    if not os.path.isdir(carpeta):
                        print("❌ Carpeta no válida. Intente nuevamente.")
                    elif not nombre.lower().endswith(".pdf"):
                        print("❌ Archivo no válido. Intente nuevamente.")
                    else:
                        break  # Ruta válida, salimos del bucle

                png_pdf(carpeta_png, archivo_salida)

            elif opcion_PDF_PNG == "m" or opcion_PDF_PNG == "M":
                print("\nSeleccione tipo de herramienta:")
                break

            else:
                print("\n❌ Opción no válida, por favor, seleccione una de las modalidades.")
               
    elif opcion == "3":
        while True:
            print("\nSeleccione modalidad:","","1.🎵 OGG → MP3","","2.🎵 MP3 → OGG","","M.⬅️  Menú principal",sep="\n")
            opcion_ogg_mp3 = input("\n|: ")
            if opcion_ogg_mp3 == "1":
                while True:
                    print(" ")
                    print("Introduzca la ruta de la carpeta que contiene los archivos .ogg:")
                    carpeta_entrada = input("|: ")
                    if os.path.isdir(carpeta_entrada):
                        break  # Ruta válida, salimos del bucle
                    else:
                        print("❌ Directorio no válido. Intente nuevamente.")
                while True:
                    print("Introduzca la ruta de la carpeta donde se guardarán los archivos .mp3 (deje vacío para usar la misma carpeta):")
                    carpeta_salida = input("|: ")
                    if os.path.isdir(carpeta_salida) or carpeta_salida.strip() == "":
                        break  # Ruta válida o vacía, salimos del bucle
                    else:
                        print("❌ Directorio no válido. Intente nuevamente.")
                        carpeta_salida = carpeta_salida if carpeta_salida.strip() else None
                        ogg_mp3(carpeta_entrada, carpeta_salida)
                break
            if opcion_ogg_mp3 == "2":
                while True:
                    print(" ")
                    print("Introduzca la ruta de la carpeta que contiene los archivos .mp3:")
                    carpeta_entrada = input("|: ")
                    if os.path.isdir(carpeta_entrada):
                        break  # Ruta válida, salimos del bucle
                    else:
                        print("❌ Directorio no válido. Intente nuevamente.")
                while True:
                    print("Introduzca la ruta de la carpeta donde se guardarán los archivos .ogg (deje vacío para usar la misma carpeta):")
                    carpeta_salida = input("|: ")
                    if os.path.isdir(carpeta_salida) or carpeta_salida.strip() == "":
                        break  # Ruta válida o vacía, salimos del bucle
                    else:
                        print("❌ Directorio no válido. Intente nuevamente.")
                        carpeta_salida = carpeta_salida if carpeta_salida.strip() else None
                        mp3_ogg(carpeta_entrada, carpeta_salida)
                break
            elif opcion_ogg_mp3 == "m" or opcion_ogg_mp3 == "M":
                print("Seleccione tipo de herramienta:")
                break
            else:
                print("\n❌ Opción no válida, por favor, seleccione una de las modalidades.")
        
            
    elif opcion == "h" or opcion == "H":
        print(" ")
        print("Descripción de las herramientas:")
        print(" ")
        print("1.✏️  Modificar nombre archivos: Permite cambiar el nombre de los archivos en un directorio manteniendo los numeros de este.")
        print("2.📄 PDF a PNG: Convierte un archivo PDF en imágenes PNG.")
        print("3.🎵 OGG a MP3: Convierte archivos de audio OGG a MP3.")
        input("\n⬅️  Presione Enter para volver al menú principal...")
        print("\nSeleccione tipo de herramienta:")

    elif opcion == "s" or opcion == "S":
        print("\nSaliendo del programa. ¡Hasta luego!\n")
        time.sleep(1)
        break

    else:
        print("\n❌Opción no válida. Por favor, seleccione una de las opciones.")