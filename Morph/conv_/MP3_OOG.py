import os
from pathlib import Path
from tkinter import filedialog, ttk
from panel import extension
from pydub import AudioSegment
import threading
import sys
from pathlib import Path


class conv_mp3_ogg:
    nombre = "MP3 → OGG"
    
    def __init__(self, dir_in=None, dir_out=None, bitrate="192k"):
        self.dir_in = dir_in
        self.dir_out = dir_out
        self.bitrate = bitrate

    def get_frame(self, parent):
        frame = ttk.Frame(parent)

        self.root = parent.winfo_toplevel()

        button_dir_in = ttk.Button(
            frame,
            text="Seleccionar Carpeta MP3",
            command=self.select_directory_in
        )
        button_dir_in.grid(row=0, column=0, columnspan=2, pady=5)

        if self.dir_in:
            self.entry_dir.insert(0, self.dir_in)

        button_dir_out = ttk.Button(
            frame,
            text="Seleccionar Carpeta OGG",
            command=self.select_directory_out
        )
        button_dir_out.grid(row=1, column=0, columnspan=2, pady=5)

        if self.dir_out:
            self.entry_dir_out.insert(0, self.dir_out)


        self.button_convert = ttk.Button(
            frame, 
            text="Convertir", 
            command=self.convertir
            )
        self.button_convert.grid(row=2, column=0, columnspan=2, pady=5)

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

        self.label_result = ttk.Label(frame, text="")
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
        dir_in = self.dir_in
        dir_out = self.dir_out
        try:
            cambios = self.mp3_ogg(dir_in, dir_out, self.bitrate)
            self.label_result.config(text=cambios)
        except Exception as e:
            self.label_result.config(text=f"Error: {e}")

        # Desactivar botón mientras convierte
        self.button_convert.config(state="disabled")

        self.label_result.config(
            text="Iniciando conversión..."
        )

        # Crear hilo
        hilo = threading.Thread(
            target=self.mp3_ogg,
            args=(self.dir_in, self.dir_out, self.bitrate),
            daemon=True
        )

        hilo.start()

    def get_ffmpeg_path(self):
    
        if getattr(sys, "frozen", False):
            # Estamos ejecutando el .exe
            base_path = Path(sys._MEIPASS)
        else:
            # Estamos ejecutando desde Python
            base_path = Path(__file__).resolve().parent.parent

        ffmpeg_path = (
            base_path
            / "bin"
            / "ffmpeg"
            / "bin"
        )

        return ffmpeg_path

    def mp3_ogg(self, dir_in, dir_out=None, bitrate="192k"):

        try:    
            if not os.path.isdir(dir_in):
                raise NotADirectoryError(f"No existe la carpeta: {dir_in}")

            # Si no se da carpeta de salida, usar la misma
            if dir_out is None:
                dir_out = dir_in

            # Contador de conversiones
            contador = 0

            # Contador de archivos MP3
            ruta_carpeta = Path(dir_in)
            extension = "*.mp3"  

            cantidad = len(list(ruta_carpeta.glob(extension)))

            self.root.after(
                0,
                lambda: self.progress.config(
                    maximum=cantidad,
                    value=0
                )
            )
            

            for archivo in os.listdir(dir_in):
                if archivo.lower().endswith(".mp3"):
                    ruta_entrada = os.path.join(dir_in, archivo)
                    nombre_salida = os.path.splitext(archivo)[0] + ".ogg"
                    ruta_salida = os.path.join(dir_out, nombre_salida)

                    try:
                        audio = AudioSegment.from_file(ruta_entrada, format="mp3")
                        audio.export(ruta_salida, format="ogg", bitrate=bitrate)
                        print(f"✅ Convertido: {archivo} → {nombre_salida}")
                        contador += 1
                        self.root.after(
                            0,
                            self.actualizar_progreso,
                            contador,
                            cantidad   
                        )
                    except Exception as e:
                        print(f"❌ Error al convertir {archivo}: {e}")

            self.root.after(
                0,
                self.conversion_terminada,
                cantidad
            )
            resultado = f"\n🎵 Conversión completa: {contador} archivos convertidos en '{dir_out}'"
            return resultado
        
        except Exception as e:
            print("ERROR:")
            print(e)
            self.root.after(
                0,
                self.error_conversion,
                str(e)
            )

    def actualizar_progreso(self, valor, total):
        self.progress.config(value=valor)
        self.label_result.config(
            text=f"Progreso: {valor}/{total} archivos convertidos"
        )

    def conversion_terminada(self, total):
        self.progress.config(value=total)
        self.label_result.config(
            text=f"Conversión terminada: {total} archivos convertidos"
        )
        self.button_convert.config(state="normal")

    def error_conversion(self, error):
        self.label_result.config(
            text=f"Error: {error}"
        )
        self.button_convert.config(state="normal")