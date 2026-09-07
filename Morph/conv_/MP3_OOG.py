import os
import sys
import threading
import tkinter.filedialog as filedialog

from pathlib import Path
from tkinter import ttk

from pydub import AudioSegment


class conv_mp3_ogg:
    nombre = "MP3 → OGG"

    def __init__(self, dir_in=None, dir_out=None, bitrate="192k"):
        self.dir_in = dir_in
        self.dir_out = dir_out
        self.bitrate = bitrate

    def get_frame(self, parent):
        frame = ttk.Frame(parent)

        # Ventana principal
        self.root = parent.winfo_toplevel()

        # Carpeta de entrada

        button_dir_in = ttk.Button(
            frame,
            text="Seleccionar Carpeta MP3",
            command=self.select_directory_in
        )
        button_dir_in.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=5
        )

       
        # Carpeta de salida
     

        button_dir_out = ttk.Button(
            frame,
            text="Seleccionar Carpeta OGG",
            command=self.select_directory_out
        )
        button_dir_out.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=5
        )


        # Convertir


        self.button_convert = ttk.Button(
            frame,
            text="Convertir",
            command=self.convertir
        )
        self.button_convert.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=5
        )

        # Barra de progreso

        self.progress = ttk.Progressbar(
            frame,
            orient="horizontal",
            length=250,
            mode="determinate"
        )
        self.progress.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Resultado
    
        self.label_result = ttk.Label(
            frame,
            text=""
        )
        self.label_result.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=5,
            pady=5
        )

        return frame

    def select_directory_in(self):
        ruta_carpeta = filedialog.askdirectory(
            title="Selecciona una carpeta de entrada"
        )

        if ruta_carpeta:
            self.dir_in = Path(ruta_carpeta)

            self.label_result.config(
                text=f"Entrada: {self.dir_in}"
            )

        else:
            print("No se seleccionó ninguna carpeta.")

    def select_directory_out(self):
        ruta_carpeta = filedialog.askdirectory(
            title="Selecciona una carpeta de salida"
        )

        if ruta_carpeta:
            self.dir_out = Path(ruta_carpeta)

            self.label_result.config(
                text=f"Salida: {self.dir_out}"
            )

        else:
            print("No se seleccionó ninguna carpeta.")

    def convertir(self):

        # Comprobar carpeta de entrada
        if self.dir_in is None:
            self.label_result.config(
                text="Error: selecciona una carpeta de entrada."
            )
            return

        # Si no se selecciona salida, usar entrada
        dir_in = self.dir_in

        if self.dir_out is None:
            dir_out = dir_in
        else:
            dir_out = self.dir_out

        # Desactivar botón
        self.button_convert.config(
            state="disabled"
        )

        self.label_result.config(
            text="Iniciando conversión..."
        )

        # Crear hilo
        hilo = threading.Thread(
            target=self.mp3_ogg,
            args=(dir_in, dir_out, self.bitrate),
            daemon=True
        )

        hilo.start()

    def get_ffmpeg_path(self):

        if getattr(sys, "frozen", False):
            # Ejecutando como .exe
            base_path = Path(sys._MEIPASS)

        else:
            # Ejecutando desde Python
            base_path = Path(__file__).resolve().parent.parent

        ffmpeg_path = (
            base_path
            / "bin"
            / "ffmpeg"
            / "bin"
            / "ffmpeg.exe"
        )

        return ffmpeg_path

    def mp3_ogg(self, dir_in, dir_out=None, bitrate="192k"):

        ffmpeg_path = self.get_ffmpeg_path()

        if not ffmpeg_path.exists():
            raise FileNotFoundError(
                f"No se encontró FFmpeg en:\n{ffmpeg_path}"
            )

        AudioSegment.converter = str(ffmpeg_path)
        
        try:

            # Comprobar entrada
            if not os.path.isdir(dir_in):
                raise NotADirectoryError(
                    f"No existe la carpeta: {dir_in}"
                )

            # Si no hay salida, usar entrada
            if dir_out is None:
                dir_out = dir_in

            # Crear carpeta de salida si no existe
            os.makedirs(
                dir_out,
                exist_ok=True
            )

        
            # Buscar archivos MP3
        

            ruta_carpeta = Path(dir_in)

            archivos_mp3 = list(
                ruta_carpeta.glob("*.mp3")
            )

            cantidad = len(archivos_mp3)

            if cantidad == 0:
                self.root.after(
                    0,
                    self.error_conversion,
                    "No se encontraron archivos MP3."
                )
                return

            #Config barra progreso

            self.root.after(
                0,
                lambda: self.progress.config(
                    maximum=cantidad,
                    value=0
                )
            )

            contador = 0

        
            # Convertir archivos
        
            for ruta_entrada in archivos_mp3:

                nombre_salida = (
                    ruta_entrada.stem + ".ogg"
                )

                ruta_salida = (
                    Path(dir_out) / nombre_salida
                )

                try:

                    audio = AudioSegment.from_file(
                        str(ruta_entrada),
                        format="mp3"
                    )

                    audio.export(
                        str(ruta_salida),
                        format="ogg",
                        bitrate=bitrate
                    )

                    contador += 1

                    print(
                        f"Convertido: "
                        f"{ruta_entrada.name} → "
                        f"{nombre_salida}"
                    )

                    self.root.after(
                        0,
                        self.actualizar_progreso,
                        contador,
                        cantidad
                    )

                except Exception as e:

                    print(
                        f"Error al convertir "
                        f"{ruta_entrada.name}: {e}"
                    )

        
            # Finalizado
        

            self.root.after(
                0,
                self.conversion_terminada,
                contador,
                cantidad,
                str(dir_out)
            )

        except Exception as e:

            print("ERROR:")
            print(e)

            self.root.after(
                0,
                self.error_conversion,
                str(e)
            )

    def actualizar_progreso(
        self,
        valor,
        total
    ):

        self.progress.config(
            value=valor
        )

        self.label_result.config(
            text=f"Progreso: {valor}/{total}"
        )

    def conversion_terminada(
        self,
        convertidos,
        total,
        carpeta
    ):

        self.progress.config(
            value=total
        )

        self.label_result.config(
            text=(
                f"Conversión terminada: "
                f"{convertidos}/{total} archivos"
            )
        )

        self.button_convert.config(
            state="normal"
        )

    def error_conversion(self, error):

        self.label_result.config(
            text=f"Error: {error}"
        )

        self.button_convert.config(
            state="normal"
        )
