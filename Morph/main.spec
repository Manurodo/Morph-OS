# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules


# ============================================================
# MÓDULOS
# ============================================================

# Todos los módulos de nuestro sistema de conversores
conv_hiddenimports = collect_submodules("conv_")
tkinter_hiddenimports = collect_submodules("tkinter")
pdf2image_hiddenimports = collect_submodules("pdf2image")
pillow_hiddenimports = collect_submodules("PIL")

hiddenimports = (
    conv_hiddenimports
    + tkinter_hiddenimports
    + pdf2image_hiddenimports
    + pillow_hiddenimports
)



# ============================================================
# ANÁLISIS
# ============================================================

a = Analysis(
    ["main.py"],

    pathex=[],

    binaries=[],

    datas=[
        # ----------------------------------------------------
        # CONVERSORES
        # ----------------------------------------------------
        #
        # Se copia físicamente la carpeta porque main.py
        # utiliza pkgutil.iter_modules() para descubrirlos.
        #
        ("conv_", "conv_"),

        # ----------------------------------------------------
        # POPPLER
        # ----------------------------------------------------
        ("bin/poppler", "bin/poppler"),

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------
        ("logo.png", "."),
    ],

    hiddenimports=hiddenimports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[],

    noarchive=False,

    optimize=0,
)


# ============================================================
# PYZ
# ============================================================

pyz = PYZ(
    a.pure
)


# ============================================================
# EJECUTABLE
# ============================================================

exe = EXE(
    pyz,

    a.scripts,

    [],

    exclude_binaries=True,

    name="Morph",

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=True,

    upx_exclude=[],

    console=True,

    disable_windowed_traceback=False,

    argv_emulation=False,

    target_arch=None,

    codesign_identity=None,

    entitlements_file=None,
)


# ============================================================
# COLECCIÓN
# ============================================================

coll = COLLECT(
    exe,

    a.binaries,

    a.datas,

    strip=False,

    upx=True,

    upx_exclude=[],

    name="Morph",
)
