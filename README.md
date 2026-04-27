# Dashboard URA Industries

Dashboard interactivo para seguimiento de avance de proyectos. Detecta atrasos críticos, alertas tempranas, brechas vs. cronograma ideal, y propone planes de acción priorizados.

## 🔄 Cómo actualizar los datos (lo único que necesitas hacer cada semana)

**Solo subes el archivo Excel actualizado y listo.** GitHub se encarga del resto automáticamente.

### Paso a paso

1. Abre tu repositorio en GitHub.
2. Click en el archivo `Base_de_datos_-_Items_URA.xlsx`.
3. Click en el ícono del lápiz (Edit) → click en "Delete" para borrarlo.
4. Click en "Add file" → "Upload files".
5. Arrastra el Excel actualizado.
6. Commit changes.

> ⚠️ **Importante:** el archivo debe llamarse **exactamente** como empezar con `Base_de_datos` y terminar con `.xlsx`. Por ejemplo: `Base_de_datos_-_Items_URA.xlsx`. Si cambias el nombre, GitHub no detectará el cambio y el dashboard no se actualizará.

### ¿Qué pasa después?

Una GitHub Action (un robot automático) detecta el cambio en el Excel y:

1. Lee el archivo
2. Lo convierte automáticamente a `items.json` (con todas las reglas de negocio aplicadas, como reemplazar "Compra insumos" → "Desarrollo")
3. Hace commit del nuevo JSON
4. El dashboard se actualiza solo

Todo el proceso tarda **30-60 segundos**. Puedes seguirlo en la pestaña **"Actions"** del repositorio.

---

## 📁 Estructura del repositorio

```
ura-dashboard/
├── index.html                          ← Dashboard (NO tocar)
├── cronograma.json                     ← Cronograma precargado (NO tocar)
├── items.json                          ← Generado automáticamente (NO tocar)
├── Base_de_datos_-_Items_URA.xlsx      ← ⭐ ESTE ES EL ÚNICO QUE ACTUALIZAS
├── update_items.py                     ← Script de conversión (NO tocar)
├── .github/workflows/
│   └── update-data.yml                 ← Robot que automatiza la conversión
└── README.md
```

---

## 🚀 Despliegue inicial en GitHub Pages (primera vez)

1. **Crear un repositorio nuevo en GitHub** (público para usar GitHub Pages gratis).

2. **Subir todos los archivos del ZIP** a la raíz del repositorio:
   - `index.html`
   - `cronograma.json`
   - `items.json`
   - `Base_de_datos_-_Items_URA.xlsx`
   - `update_items.py`
   - `.github/workflows/update-data.yml` (importante mantener la carpeta)
   - `README.md`

3. **Activar GitHub Pages**:
   - Ve a `Settings` → `Pages`
   - En `Source`, selecciona `Deploy from a branch`
   - Branch: `main` · Folder: `/ (root)`
   - Click `Save`

4. **Activar GitHub Actions** (suele estar activo por defecto):
   - Ve a `Settings` → `Actions` → `General`
   - En `Workflow permissions`, selecciona **Read and write permissions** y guarda. Esto permite que el robot pueda hacer commit del `items.json` regenerado.

5. Espera 1–2 minutos. GitHub te dará una URL del estilo:
   `https://TU-USUARIO.github.io/ura-dashboard/`

6. ✅ Listo. El dashboard estará disponible en esa URL.

> **¿Repositorio privado?** GitHub Pages requiere plan **GitHub Pro** para repos privados. Alternativas gratis con repos privados: **Netlify** o **Vercel** (mismo flujo, drag & drop del repo).

---

## 🛠 Probar localmente antes de subir

Si quieres probar en tu computador:

```bash
# 1. Clonar el repo
git clone https://github.com/TU-USUARIO/ura-dashboard.git
cd ura-dashboard

# 2. (Opcional) regenerar items.json si tocaste el Excel
pip install pandas openpyxl
python update_items.py

# 3. Servir localmente
python -m http.server 8080
```

Abre `http://localhost:8080` en el navegador.

> ⚠️ El dashboard NO funciona si abres `index.html` haciendo doble click (necesita un servidor web por temas de seguridad del navegador).

---

## 🎨 Personalización

- **Colores:** ver bloque `:root` y `[data-theme="dark"]` en `index.html`
- **Umbrales de alerta:** función `renderMatrix()` en `index.html` (actualmente: 15% alerta, 25% crítico)
- **Etapas críticas:** constantes `ETAPAS_MATRIX`, `ONTIME_STAGES` y `PIPELINE_ORDER`
- **Reglas de negocio:** archivo `update_items.py` (ej: el reemplazo de "Compra insumos" → "Desarrollo")

---

## ❓ Solución de problemas

### El dashboard muestra "Error cargando los datos"
- Asegúrate de estar abriéndolo desde la URL de GitHub Pages, no desde tu disco duro local.
- Si lo subiste recientemente, espera 2-3 minutos y refresca con `Ctrl+Shift+R`.

### Subí el Excel pero el dashboard no se actualiza
- Ve a la pestaña **Actions** del repo. Mira si el workflow corrió y si tuvo errores.
- Verifica que el archivo se llame `Base_de_datos*.xlsx` (debe empezar con `Base_de_datos` y terminar en `.xlsx`).
- Verifica en `Settings → Actions → General` que el workflow tenga **Read and write permissions**.

### Quiero forzar una actualización manual
- Ve a la pestaña **Actions** → "Convertir Excel a items.json" → "Run workflow".

---

URA Industries® — Dashboard interno
