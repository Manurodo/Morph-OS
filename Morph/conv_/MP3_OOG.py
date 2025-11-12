import os
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

        ttk.Label(frame, text="Directorio entrada:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.entry_dir = ttk.Entry(frame, width=40)
        self.entry_dir.grid(row=0, column=1, padx=5, pady=3)
        if self.dir_in:
            self.entry_dir.insert(0, self.dir_in)

        ttk.Label(frame, text="Directorio salida:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.entry_dir_out = ttk.Entry(frame, width=40)
        self.entry_dir_out.grid(row=1, column=1, padx=5, pady=3)
        if self.dir_out:
            self.entry_dir_out.insert(0, self.dir_out)


        boton = ttk.Button(frame, text="Convertir", command=self.convertir)
        boton.grid(row=2, column=0, columnspan=2, pady=5)

        self.label_result = ttk.Label(frame, text="")
        self.label_result.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        return frame
    
    def convertir(self):
        dir_in = self.entry_dir.get().strip() or "."
        dir_out = self.entry_dir_out.get().strip() or None
        try:
            cambios = self.mp3_ogg(dir_in, dir_out, self.bitrate)
            self.label_result.config(text=cambios)
        except Exception as e:
            self.label_result.config(text=f"Error: {e}")

    def mp3_ogg(self, dir_in, dir_out=None, bitrate="192k"):
            
            if not os.path.isdir(dir_in):
                raise NotADirectoryError(f"No existe la carpeta: {dir_in}")

            # Si no se da carpeta de salida, usar la misma
            if dir_out is None:
                dir_out = dir_in

            # Contador de conversiones
            contador = 0

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
                    except Exception as e:
                        print(f"❌ Error al convertir {archivo}: {e}")

            resultado = f"\n🎵 Conversión completa: {contador} archivos convertidos en '{dir_out}'"
            return resultado