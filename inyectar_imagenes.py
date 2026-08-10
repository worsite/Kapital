#!/usr/bin/env python3
import os
import base64
import re

# Mapeo de subcategorías a prefijos de imágenes
CATEGORIAS = {
    'camisas': {
        'oversize': 'Oversize foto',
        'basicas': 'Básicas foto',
        'polos': 'Polos foto',
        'manga-siza': 'Manga Siza foto'
    },
    'pantalones': {
        'bermudas': 'Bermudas foto',
        'pantalonetas': 'Pantalonetas foto',
        'vaqueros': 'Vaqueros foto',
        'jeans': 'Jeans foto'
    },
    'hoodies': {
        'sudaderas': 'Sudaderas foto',
        'crop-tops': 'Crop Tops foto',
        'busos-capota': 'Busos Capota foto'
    },
    'conjuntos': {
        'hombre': 'Conjuntos Hombre foto',
        'mujer': 'Conjuntos Mujer foto'
    },
    'accesorios': {
        'gorras': 'Gorra foto',
        'correas': 'Correa foto',
        'relojes': 'Relojes foto',
        'zapatos': 'Zapatos foto'
    }
}

def convertir_imagenes_a_base64():
    """Convierte todas las imágenes PNG en base64"""
    imagenes = {}
    media_dir = 'media'

    if not os.path.exists(media_dir):
        print(f"❌ Error: No existe la carpeta '{media_dir}'")
        return None

    archivos = [f for f in os.listdir(media_dir) if f.lower().endswith('.png')]

    if not archivos:
        print(f"❌ Error: No hay archivos PNG en la carpeta '{media_dir}'")
        return None

    for archivo in archivos:
        ruta = os.path.join(media_dir, archivo)
        try:
            with open(ruta, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
                imagenes[archivo] = b64
                print(f"✓ {archivo} convertido")
        except Exception as e:
            print(f"❌ Error al convertir {archivo}: {e}")

    return imagenes

def mapear_imagenes_a_categorias(imagenes):
    """Mapea imágenes a sus categorías y subcategorías"""
    catalogo = {}

    for categoria, subcats in CATEGORIAS.items():
        catalogo[categoria] = {}
        for subcat, prefijo in subcats.items():
            imagenes_subcat = []

            for nombre_imagen, b64 in imagenes.items():
                # Comparar ignorando mayúsculas y espacios
                nombre_lower = nombre_imagen.lower().replace(' ', '')
                prefijo_lower = prefijo.lower().replace(' ', '')

                if nombre_lower.startswith(prefijo_lower):
                    imagenes_subcat.append({
                        'nombre': nombre_imagen,
                        'base64': b64
                    })

            if imagenes_subcat:
                # Ordenar por número
                imagenes_subcat.sort(key=lambda x: x['nombre'])
                catalogo[categoria][subcat] = imagenes_subcat
                print(f"✓ {categoria} > {subcat}: {len(imagenes_subcat)} imágenes")
            else:
                print(f"⚠ {categoria} > {subcat}: Sin imágenes")

    return catalogo

def generar_javascript_imagenes(catalogo):
    """Genera el JavaScript con las imágenes mapeadas"""
    js = "\nconst productImages = {\n"

    for categoria, subcats in catalogo.items():
        for subcat, imagenes in subcats.items():
            key = f"{categoria}-{subcat}"
            js += f"  '{key}': [\n"
            for img in imagenes:
                js += f"    'data:image/png;base64,{img['base64']}',\n"
            js += "  ],\n"

    js += "};\n"
    return js

def actualizar_galeria_javascript():
    """Genera la función actualizada de galería"""
    js = """
function showGalleryModal(label) {
  let modal = document.getElementById('galleryModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'galleryModal';
    modal.className = 'gallery-modal-overlay';
    modal.innerHTML = `
      <div class="gallery-modal-content">
        <button class="gallery-modal-close" onclick="closeGalleryModal()">✕</button>
        <h3 class="gallery-modal-title" id="galleryTitle"></h3>
        <p id="galleryInst" style="margin-bottom: 24px; color: var(--ink-2);"></p>
        <div class="gallery-grid" id="galleryGrid"></div>
      </div>
    `;
    document.body.appendChild(modal);
  }

  document.getElementById('galleryTitle').textContent = label;
  document.getElementById('galleryInst').textContent = currentLanguage === 'es' ? 'Haz click en una prenda para seleccionar talla' : 'Click on a product to select size';

  const key = `${currentCategory}-${currentSubcategory}`;
  const images = productImages[key] || [];

  const grid = document.getElementById('galleryGrid');
  grid.innerHTML = '';

  if (images.length === 0) {
    grid.innerHTML = '<p style="color: var(--ink-2);">No hay imágenes disponibles</p>';
  } else {
    images.forEach((imgSrc, index) => {
      const item = document.createElement('div');
      item.className = 'gallery-grid-item';
      item.style.backgroundImage = `url('${imgSrc}')`;
      item.style.backgroundSize = 'cover';
      item.style.backgroundPosition = 'center';
      item.title = `Prenda ${index + 1}`;
      item.onclick = () => selectGalleryItem(index + 1, label);
      grid.appendChild(item);
    });
  }

  modal.classList.add('open');
}
"""
    return js

def main():
    print("\n" + "="*60)
    print("🖼️  INYECTOR DE IMÁGENES - KAPITAL")
    print("="*60 + "\n")

    print("📦 Paso 1: Convirtiendo imágenes a base64...")
    imagenes = convertir_imagenes_a_base64()
    if not imagenes:
        return
    print(f"✓ {len(imagenes)} imágenes convertidas\n")

    print("📋 Paso 2: Mapeando imágenes a categorías...")
    catalogo = mapear_imagenes_a_categorias(imagenes)
    print()

    print("⚙️  Paso 3: Generando código JavaScript...")
    js_images = generar_javascript_imagenes(catalogo)
    js_gallery = actualizar_galeria_javascript()

    print("✓ Código JavaScript generado\n")

    print("📄 Paso 4: Actualizando index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Remover código anterior si existe
    html = re.sub(r'\nconst productImages = \{[\s\S]*?\};', '', html)
    html = re.sub(r'function showGalleryModal\(label\) \{[\s\S]*?\n\}(?=\n\nfunction)', '', html)

    # Inyectar nuevo código antes del </script>
    if '</script>' in html:
        insert_pos = html.rfind('</script>')
        html = html[:insert_pos] + js_images + "\n" + js_gallery + "\n" + html[insert_pos:]

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ index.html actualizado\n")

    print("="*60)
    print("✅ ¡PROCESO COMPLETADO!")
    print("="*60)
    print("\n📋 RESUMEN:")
    total_imgs = sum(len(imgs) for subcat in catalogo.values() for imgs in subcat.values())
    print(f"   Total de imágenes: {total_imgs}\n")

    for cat, subcats in catalogo.items():
        print(f"   📁 {cat.upper()}")
        for subcat, imgs in subcats.items():
            if imgs:
                print(f"      └─ {subcat}: {len(imgs)} imágenes")

    print("\n✨ Próximos pasos:")
    print("   1. git add index.html")
    print("   2. git commit -m 'Agregar imágenes de productos'")
    print("   3. git push origin claude/html-estructura-imagenes-p4n7o6")
    print()

if __name__ == '__main__':
    main()
