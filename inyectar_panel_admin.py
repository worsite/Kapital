#!/usr/bin/env python3
import re

# Read current HTML
print("📖 Leyendo HTML actual...")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("🔍 Verificando estado actual...")

# Remove any existing admin panel code to avoid duplication
html = re.sub(r'<!-- KAPITAL ADMIN PANEL.*?</script>\s*', '', html, flags=re.DOTALL)

# Admin panel code to inject (combined and cleaned)
admin_panel_code = '''
<!-- ═══════════════════════════════════════════════
     KAPITAL ADMIN PANEL v2.0
     ═══════════════════════════════════════════════ -->

<style>
/* Admin Panel Styles */
.admin-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.95);
  z-index: 9999;
  display: none;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.admin-overlay.active {
  display: flex;
  opacity: 1;
}

.admin-box {
  background: #1a1a1a;
  border: 2px solid #d4a574;
  border-radius: 12px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 30px;
  color: #f0f0f0;
  font-family: 'Sora', sans-serif;
  box-shadow: 0 0 30px rgba(212, 165, 86, 0.3);
}

.admin-header {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #d4a574;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-close {
  background: #d4a574;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  font-weight: bold;
  color: #000;
  transition: opacity 0.2s;
}

.admin-close:hover {
  opacity: 0.85;
}

.admin-section {
  margin: 20px 0;
  padding: 15px;
  background: #222;
  border-radius: 8px;
  border-left: 3px solid #d4a574;
}

.admin-label {
  font-weight: 500;
  margin-bottom: 8px;
  color: #d4a574;
  display: block;
}

.admin-input,
.admin-select,
.admin-textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  background: #333;
  border: 1px solid #555;
  color: #f0f0f0;
  border-radius: 6px;
  font-family: inherit;
  box-sizing: border-box;
}

.admin-input:focus,
.admin-select:focus,
.admin-textarea:focus {
  outline: none;
  border-color: #d4a574;
  background: #2a2a2a;
}

.admin-button {
  background: #d4a574;
  color: #000;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  margin-right: 10px;
  margin-top: 10px;
  transition: opacity 0.2s;
}

.admin-button:hover {
  opacity: 0.9;
}

.admin-button.danger {
  background: #e74c3c;
  color: white;
}

.admin-success {
  background: #2ecc71;
  color: white;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-weight: 600;
}

.admin-error {
  background: #e74c3c;
  color: white;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-weight: 600;
}

/* Gallery Modal Styles */
.modal-gallery {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.98);
  z-index: 5000;
  display: none;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.modal-gallery.active {
  display: flex;
}

.modal-gallery-image {
  max-width: 90%;
  max-height: 80%;
  object-fit: contain;
  margin: 20px 0;
}

.modal-gallery-nav {
  margin-top: 20px;
  display: flex;
  gap: 20px;
}

.modal-gallery-close {
  position: absolute;
  top: 20px;
  right: 30px;
  font-size: 40px;
  color: #d4a574;
  cursor: pointer;
  background: none;
  border: none;
  transition: opacity 0.2s;
}

.modal-gallery-close:hover {
  opacity: 0.7;
}

.modal-gallery-counter {
  position: absolute;
  top: 20px;
  left: 30px;
  color: #d4a574;
  font-size: 18px;
  font-weight: 500;
}
</style>

<!-- Admin Panel HTML -->
<div class="admin-overlay" id="adminPanel">
  <div class="admin-box">
    <div class="admin-header">
      Panel Administrativo Kapital
      <button class="admin-close" onclick="closeAdmin()">✕</button>
    </div>

    <div id="adminLoginSection">
      <div class="admin-section">
        <label class="admin-label">Usuario</label>
        <input type="text" id="adminUser" class="admin-input" placeholder="kapital01">
        <label class="admin-label">Contraseña</label>
        <input type="password" id="adminPass" class="admin-input" placeholder="••••">
        <button class="admin-button" onclick="loginAdmin()">Acceder</button>
      </div>
    </div>

    <div id="adminContentSection" style="display:none;">
      <div id="successMessage"></div>

      <div class="admin-section">
        <label class="admin-label">Seleccionar Producto</label>
        <select id="productoSelect" class="admin-select" onchange="loadProduct()">
          <option value="">-- Selecciona un producto --</option>
        </select>
      </div>

      <div class="admin-section">
        <label class="admin-label">Nombre del Producto</label>
        <input type="text" id="nombreProducto" class="admin-input" placeholder="Nombre">

        <label class="admin-label">Precio</label>
        <input type="number" id="precioProducto" class="admin-input" placeholder="Precio">

        <label class="admin-label">Descripción</label>
        <textarea id="descProducto" class="admin-textarea" placeholder="Descripción" rows="3"></textarea>

        <label class="admin-label">Categoría</label>
        <select id="categoriaProducto" class="admin-select">
          <option value="camisas">Camisas</option>
          <option value="pantalones">Pantalones</option>
          <option value="hoodies">Hoodies</option>
          <option value="conjuntos">Conjuntos</option>
          <option value="accesorios">Accesorios</option>
          <option value="kapital">Kapital</option>
        </select>

        <button class="admin-button" onclick="saveProduct()">Guardar Cambios</button>
      </div>

      <div class="admin-section">
        <label class="admin-label">Subir Nueva Imagen</label>
        <input type="file" id="imagenInput" class="admin-input" accept="image/*">
        <button class="admin-button" onclick="uploadImage()">Subir Imagen</button>
      </div>
    </div>
  </div>
</div>

<!-- Gallery Modal HTML -->
<div class="modal-gallery" id="modalGaleria">
  <div class="modal-gallery-counter">
    <span id="fotoActual">1</span> / <span id="fotoTotal">1</span>
  </div>
  <button class="modal-gallery-close" onclick="closeGallery()">✕</button>
  <img class="modal-gallery-image" id="imagenModal">
  <div class="modal-gallery-nav">
    <button class="admin-button" onclick="prevImage()">← Anterior</button>
    <button class="admin-button" onclick="nextImage()">Siguiente →</button>
  </div>
</div>

<script>
// ═══════════════════════════════════════════════
// ADMIN PANEL CONFIGURATION
// ═══════════════════════════════════════════════

const SUPABASE_URL = 'https://zperfcjhbhydlmxhoopx.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwZXJmY2poYmh5ZGxteGhvb3B4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczMTk1NDUsImV4cCI6MjEwMjg5NTU0NX0.vb4l7aET1n4hylcjDs7iu2f-5zHtgEvXPgILaQ0aGpA';

// Load Supabase dynamically
let supabase = null;
const script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
script.onload = () => {
  const { createClient } = window.supabase;
  supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
  console.log('✅ Supabase initialized');
};
document.head.appendChild(script);

// Admin Panel State
let adminAuthenticated = false;
let currentProductId = null;
let currentPhotoIndex = 0;
let currentPhotos = [];

// Three-click detection for KAPITAL text
let kapitalClickCount = 0;
let kapitalClickTime = 0;

// ═══════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  console.log('✅ DOM loaded, initializing admin panel...');
  setupKapitalClickDetection();
  setupGalleryClickDetection();
});

// ═══════════════════════════════════════════════
// KAPITAL TEXT CLICK DETECTION (3 clicks trigger admin)
// ═══════════════════════════════════════════════

function setupKapitalClickDetection() {
  // Find all text nodes and elements containing "KAPITAL"
  const allElements = document.querySelectorAll('*');

  for (let elem of allElements) {
    // Check if element contains "KAPITAL" and is visible
    if (elem.childNodes.length === 1 && elem.childNodes[0].nodeType === 3) {
      // Text node
      if (elem.textContent.includes('KAPITAL') || elem.textContent.includes('Kapital')) {
        addClickListener(elem);
      }
    } else if (elem.textContent.includes('KAPITAL') || elem.textContent.includes('Kapital')) {
      // Check if it's a heading or similar
      if (['H1', 'H2', 'H3', 'P', 'SPAN', 'DIV'].includes(elem.tagName)) {
        addClickListener(elem);
      }
    }
  }

  function addClickListener(elem) {
    elem.style.cursor = 'pointer';
    elem.addEventListener('click', (e) => {
      e.stopPropagation();
      const now = Date.now();

      // Reset counter if more than 600ms has passed
      if (now - kapitalClickTime > 600) {
        kapitalClickCount = 0;
      }

      kapitalClickCount++;
      kapitalClickTime = now;

      console.log(`🔐 KAPITAL click: ${kapitalClickCount}/3`);

      if (kapitalClickCount >= 3) {
        openAdmin();
        kapitalClickCount = 0;
      }
    });
  }
}

// ═══════════════════════════════════════════════
// GALLERY IMAGE EXPANSION
// ═══════════════════════════════════════════════

function setupGalleryClickDetection() {
  // Add click listeners to all images after a delay to ensure they're loaded
  setTimeout(() => {
    document.querySelectorAll('img').forEach(img => {
      // Only attach to images that have base64 data or are in product sections
      if (img.src && (img.src.includes('data:image') || img.closest('[data-category]'))) {
        img.style.cursor = 'pointer';
        img.addEventListener('click', (e) => {
          e.stopPropagation();
          const category = img.closest('[data-category]');
          if (category) {
            const key = category.getAttribute('data-category');
            if (typeof productImages !== 'undefined' && productImages[key]) {
              openGallery(productImages[key].galeria, 0);
            }
          }
        });
      }
    });
  }, 1000);
}

// ═══════════════════════════════════════════════
// ADMIN PANEL FUNCTIONS
// ═══════════════════════════════════════════════

function openAdmin() {
  console.log('🔓 Opening admin panel...');
  document.getElementById('adminPanel').classList.add('active');
  document.getElementById('adminLoginSection').style.display = 'block';
  document.getElementById('adminContentSection').style.display = 'none';
}

function closeAdmin() {
  console.log('🔒 Closing admin panel...');
  document.getElementById('adminPanel').classList.remove('active');
  adminAuthenticated = false;
  document.getElementById('adminUser').value = '';
  document.getElementById('adminPass').value = '';
}

function loginAdmin() {
  const user = document.getElementById('adminUser').value;
  const pass = document.getElementById('adminPass').value;

  if (user === 'kapital01' && pass === '123') {
    adminAuthenticated = true;
    document.getElementById('adminLoginSection').style.display = 'none';
    document.getElementById('adminContentSection').style.display = 'block';
    showSuccess('✅ Sesión iniciada correctamente');
    loadProducts();
  } else {
    showError('❌ Usuario o contraseña incorrectos');
  }
}

async function loadProducts() {
  if (!supabase) {
    console.log('⏳ Supabase not ready yet, retrying...');
    setTimeout(loadProducts, 500);
    return;
  }

  console.log('📦 Loading products...');
  const { data, error } = await supabase
    .from('productos')
    .select('id, nombre, categoria, subcategoria');

  if (error) {
    console.error('Error loading products:', error);
    showError('Error cargando productos: ' + error.message);
    return;
  }

  const select = document.getElementById('productoSelect');
  select.innerHTML = '<option value="">-- Selecciona un producto --</option>';

  if (data && data.length > 0) {
    data.forEach(prod => {
      const option = document.createElement('option');
      option.value = prod.id;
      option.textContent = `${prod.nombre} (${prod.categoria}-${prod.subcategoria})`;
      select.appendChild(option);
    });
    console.log(`✅ Loaded ${data.length} products`);
  }
}

async function loadProduct() {
  const id = document.getElementById('productoSelect').value;
  if (!id || !supabase) return;

  console.log('📄 Loading product:', id);
  const { data, error } = await supabase
    .from('productos')
    .select('*')
    .eq('id', id)
    .single();

  if (error) {
    console.error('Error:', error);
    return;
  }

  if (data) {
    currentProductId = data.id;
    document.getElementById('nombreProducto').value = data.nombre || '';
    document.getElementById('precioProducto').value = data.precio || '';
    document.getElementById('descProducto').value = data.descripcion || '';
    document.getElementById('categoriaProducto').value = data.categoria || '';
  }
}

async function saveProduct() {
  if (!adminAuthenticated || !currentProductId || !supabase) return;

  console.log('💾 Saving product:', currentProductId);
  const { error } = await supabase
    .from('productos')
    .update({
      nombre: document.getElementById('nombreProducto').value,
      precio: parseFloat(document.getElementById('precioProducto').value) || 0,
      descripcion: document.getElementById('descProducto').value,
      categoria: document.getElementById('categoriaProducto').value,
      updated_at: new Date()
    })
    .eq('id', currentProductId);

  if (error) {
    console.error('Error:', error);
    showError('Error guardando producto');
  } else {
    showSuccess('✅ Producto guardado correctamente');
  }
}

async function uploadImage() {
  if (!adminAuthenticated || !supabase) {
    showError('Debes estar autenticado');
    return;
  }

  const file = document.getElementById('imagenInput').files[0];
  if (!file) {
    showError('Selecciona una imagen');
    return;
  }

  const fileName = Date.now() + '_' + file.name;
  console.log('📸 Uploading image:', fileName);

  const { data, error } = await supabase.storage
    .from('kapital-imagenes')
    .upload(fileName, file);

  if (error) {
    console.error('Error:', error);
    showError('Error subiendo imagen');
  } else {
    showSuccess('✅ Imagen subida correctamente');
    document.getElementById('imagenInput').value = '';
  }
}

function showSuccess(message) {
  const div = document.getElementById('successMessage');
  div.innerHTML = `<div class="admin-success">${message}</div>`;
  setTimeout(() => div.innerHTML = '', 3000);
}

function showError(message) {
  const div = document.getElementById('successMessage');
  div.innerHTML = `<div class="admin-error">${message}</div>`;
  setTimeout(() => div.innerHTML = '', 5000);
}

// ═══════════════════════════════════════════════
// GALLERY FUNCTIONS
// ═══════════════════════════════════════════════

function openGallery(images, index = 0) {
  console.log('🖼️ Opening gallery with', images.length, 'images at index', index);
  currentPhotos = images;
  currentPhotoIndex = index;
  showPhoto();
  document.getElementById('modalGaleria').classList.add('active');
}

function closeGallery() {
  console.log('🔒 Closing gallery');
  document.getElementById('modalGaleria').classList.remove('active');
}

function showPhoto() {
  if (currentPhotos.length === 0) return;
  const img = currentPhotos[currentPhotoIndex];
  document.getElementById('imagenModal').src = img;
  document.getElementById('fotoActual').textContent = currentPhotoIndex + 1;
  document.getElementById('fotoTotal').textContent = currentPhotos.length;
}

function nextImage() {
  if (currentPhotoIndex < currentPhotos.length - 1) {
    currentPhotoIndex++;
    showPhoto();
  }
}

function prevImage() {
  if (currentPhotoIndex > 0) {
    currentPhotoIndex--;
    showPhoto();
  }
}

// Real-time sync with Supabase (optional)
setTimeout(() => {
  if (supabase) {
    console.log('📡 Setting up real-time listener...');
    supabase
      .channel('productos-cambios')
      .on('postgres_changes',
        { event: '*', schema: 'public', table: 'productos' },
        (payload) => {
          console.log('🔄 Product changes detected:', payload);
          if (adminAuthenticated) {
            loadProducts();
          }
        }
      )
      .subscribe();
  }
}, 2000);

console.log('✅ Admin panel code loaded successfully');
</script>
'''

# Inject before </body>
if '</body>' in html:
    html = html.replace('</body>', admin_panel_code + '\n</body>')
else:
    html += admin_panel_code

# Save
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

final_size = len(html) / (1024 * 1024)
print(f"\n✅ Admin panel injected successfully!")
print(f"📊 File size: {final_size:.2f} MB")
print("\n" + "="*60)
print("🔐 ADMIN PANEL READY")
print("="*60)
print("\n📌 INSTRUCTIONS:")
print("   1. Make 3 RAPID clicks on 'KAPITAL' text")
print("   2. Login with:")
print("      User: kapital01")
print("      Password: 123")
print("   3. Manage products, prices, and images")
print("\n🖼️ GALLERY:")
print("   Click any product image to view in full screen")
print("   Use arrows to navigate between images")
print("   Press X to close")
print("\n" + "="*60)
