"""
Script para procesar fotos o PDF de un álbum en la carpeta paginas/[ID]/
Uso:
  python scripts/procesar_album.py --id boda-marcos --origen ruta/a/fotos_o_pdf
"""
import os
import sys
import shutil
import argparse
from pathlib import Path

def procesar_album(album_id, origen):
    dest = Path("paginas") / album_id
    dest.mkdir(parents=True, exist_ok=True)
    
    origen_path = Path(origen)
    if not origen_path.exists():
        print(f"Error: La ruta de origen no existe: {origen}")
        sys.exit(1)

    # Caso 1: Archivo PDF
    if origen_path.is_file() and origen_path.suffix.lower() == ".pdf":
        try:
            from pdf2image import convert_from_path
            print(f"Convirtiendo PDF: {origen_path}...")
            images = convert_from_path(str(origen_path), dpi=150)
            for i, img in enumerate(images, start=1):
                out_file = dest / f"{i}.jpg"
                img.save(str(out_file), "JPEG", quality=88)
                print(f"  Página {i} -> {out_file}")
            print(f"\n¡Éxito! {len(images)} páginas creadas en {dest}")
        except ImportError:
            print("pdf2image no está instalado. Instalalo con: pip install pdf2image pillow")
            print(f"Copiando PDF como {dest / 'album.pdf'}...")
            shutil.copy2(origen_path, dest / "album.pdf")

    # Caso 2: Carpeta con imágenes
    elif origen_path.is_dir():
        exts = {".jpg", ".jpeg", ".png", ".webp"}
        files = sorted([f for f in origen_path.iterdir() if f.suffix.lower() in exts])
        if not files:
            print(f"No se encontraron imágenes en {origen_path}")
            sys.exit(1)

        for i, file in enumerate(files, start=1):
            out_file = dest / f"{i}.jpg"
            shutil.copy2(file, out_file)
            print(f"  {file.name} -> {out_file}")
        print(f"\n¡Éxito! {len(files)} fotos copiadas y numeradas en {dest}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesar fotos para webapp-nfc")
    parser.add_argument("--id", required=True, help="Identificador del álbum (ej: boda-marcos)")
    parser.add_argument("--origen", required=True, help="Ruta al archivo PDF o carpeta de fotos")
    args = parser.parse_args()
    procesar_album(args.id, args.origen)