#!/usr/bin/env python3
import os
import base64
import re
from PIL import Image
from io import BytesIO

# Configuración
MEDIA_DIR = "media"
HTML_INPUT = "index_backup"
HTML_OUTPUT = "index.html"

# Mapeo de categorías encontradas en las imágenes
CATEGORIAS = [
    "Básicas",
    "Bermudas",
    "Busos Capota",
    "Conjuntos Hombre",
    "Conjuntos Mujer",
    "Gorras",
    "Jeans",
    "Kapital",
    "Manga Siza",
    "Oversize",
    "Pantalonetas",
    "Polos",
    "Relojes",
    "Sudaderas",
    "Zapatos"
]

def comprimir_imagen(ruta_imagen, max_ancho=900, calidad=82):
    """Comprime imagen con Pillow y retorna base64"""
    try:
        img = Image.open(ruta_imagen)

        # Corregir rotación EXIF si existe
        if hasattr(img, '_getexif') and img._getexif() is not None:
            try:
                from PIL.ImageOps import exif_transpose
                img = exif_transpose(img)
            except:
                pass

        # Redimensionar si es necesario
        if img.width > max_ancho:
            ratio = max_ancho / img.width
            nuevo_alto = int(img.height * ratio)
            img = img.resize((max_ancho, nuevo_alto), Image.Resampling.LANCZOS)

        # Convertir a RGB si es necesario (para JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            fondo = Image.new('RGB', img.size, (255, 255, 255))
            fondo.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = fondo

        # Guardar en BytesIO y convertir a base64
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=calidad, optimize=True)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return f"data:image/jpeg;base64,{img_base64}"
    except Exception as e:
        print(f"❌ Error comprimiendo {ruta_imagen}: {e}")
        return None

def obtener_imagenes_por_categoria():
    """Organiza imágenes por categoría"""
    imagenes_por_categoria = {}

    if not os.path.exists(MEDIA_DIR):
        print(f"❌ Error: La carpeta '{MEDIA_DIR}' no existe")
        return None

    archivos = sorted([f for f in os.listdir(MEDIA_DIR) if f.lower().endswith('.png')])

    if not archivos:
        print(f"❌ Error: No hay archivos PNG en '{MEDIA_DIR}'")
        return None

    # Agrupar por categoría
    for archivo in archivos:
        # Detectar categoría (todo antes de "fotoX")
        match = re.match(r'(.+?)\s+foto(\d+)\.png', archivo, re.IGNORECASE)
        if match:
            categoria = match.group(1).strip()
            numero_foto = int(match.group(2))

            if categoria not in imagenes_por_categoria:
                imagenes_por_categoria[categoria] = {}

            ruta_completa = os.path.join(MEDIA_DIR, archivo)
            imagenes_por_categoria[categoria][numero_foto] = {
                'archivo': archivo,
                'ruta': ruta_completa
            }

    return imagenes_por_categoria

def inyectar_imagenes_en_html(imagenes_por_categoria):
    """Inyecta las imágenes en base64 dentro del HTML"""

    # Leer HTML original
    if not os.path.exists(HTML_INPUT):
        print(f"❌ Error: No existe {HTML_INPUT}")
        return False

    with open(HTML_INPUT, 'r', encoding='utf-8') as f:
        html = f.read()

    print("\n" + "="*60)
    print("🖼️  INYECTOR DE IMÁGENES - KAPITAL")
    print("="*60 + "\n")

    print("📦 Paso 1: Comprimiendo y convirtiendo imágenes a base64...")

    # Construir objeto JavaScript con imágenes
    js_images = "const productImages = {\n"

    total_imagenes = 0

    for categoria in sorted(imagenes_por_categoria.keys()):
        fotos = imagenes_por_categoria[categoria]

        # Convertir categoría a ID válido (lowercase, sin espacios, con guiones)
        categoria_id = categoria.lower().replace(' ', '-')

        js_images += f"  '{categoria_id}': {{\n"
        js_images += f"    nombre: '{categoria}',\n"
        js_images += f"    principal: null,\n"
        js_images += f"    galeria: [\n"

        # Procesar fotos en orden
        for numero_foto in sorted(fotos.keys()):
            info = fotos[numero_foto]
            print(f"✓ {info['archivo']} comprimido")

            # Comprimir imagen
            img_base64 = comprimir_imagen(info['ruta'])
            if img_base64:
                js_images += f"      '{img_base64}',\n"
                total_imagenes += 1

                # La foto 1 es la principal
                if numero_foto == 1:
                    js_images = js_images.replace("principal: null,", f"principal: '{img_base64}',")

        js_images += "    ]\n"
        js_images += "  },\n"

    js_images += "};\n"

    print(f"✓ {total_imagenes} imágenes comprimidas\n")

    print("📄 Paso 2: Inyectando en index.html...")

    # Remover código anterior si existe
    html = re.sub(r'const productImages = \{[\s\S]*?\};', '', html)

    # Inyectar nuevo código antes del </script>
    if '</script>' in html:
        insert_pos = html.rfind('</script>')
        html = html[:insert_pos] + "\n" + js_images + "\n" + html[insert_pos:]
    else:
        print("⚠️  No se encontró </script>, agregando al final")
        html += "\n<script>\n" + js_images + "\n</script>"

    # Guardar HTML actualizado
    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)

    print("✓ index.html actualizado\n")

    print("="*60)
    print("✅ ¡PROCESO COMPLETADO!")
    print("="*60)
    print(f"\n📊 RESUMEN:")
    print(f"   Total de imágenes: {total_imagenes}")
    print(f"   Categorías: {len(imagenes_por_categoria)}\n")

    for categoria in sorted(imagenes_por_categoria.keys()):
        fotos = imagenes_por_categoria[categoria]
        print(f"   ✓ {categoria}: {len(fotos)} fotos")

    print(f"\n✨ Archivo guardado: {HTML_OUTPUT}\n")

    return True

def main():
    print("\n🔍 Buscando imágenes...\n")

    imagenes_por_categoria = obtener_imagenes_por_categoria()

    if not imagenes_por_categoria:
        return

    if not inyectar_imagenes_en_html(imagenes_por_categoria):
        return

if __name__ == '__main__':
    main()
