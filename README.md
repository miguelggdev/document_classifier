# 📄 Document Classifier con OCR + GPT-4o

Este proyecto permite **clasificar documentos PDF** en categorías como *Contrato*, *Factura*, *Queja/Reclamo*, *Carta*, etc.  
Funciona tanto con PDFs **digitales** (texto embebido) como con PDFs **escaneados** (imágenes), gracias a la combinación de:

- **PyPDF2** → extracción de texto digital.  
- **pdf2image + Pillow** → conversión de PDF a imágenes.  
- **Tesseract OCR (pytesseract)** → reconocimiento de texto en imágenes.  
- **OpenAI GPT‑4o** → clasificación semántica del contenido.  
- **dotenv** → manejo seguro de la API Key.  

---

## 🚀 Requisitos

### 1. Instalar Python
Asegúrate de tener **Python 3.14** o superior instalado en tu sistema.  
Verifica con:
```powershell
python --version
```
### 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

### 3. Instalar dependencias
Con el entorno virtual activado:

python -m pip install --upgrade pip
python -m pip install PyPDF2 pdf2image pillow pytesseract openai python-dotenv tqdm

### 4. Instalar Poppler (para pdf2image)
Descarga Poppler para Windows:
👉 https://github.com/oschwartz10612/poppler-windows/releases (github.com in Bing)

Extrae en C:\Program Files\poppler-xx\bin

Agrega esa ruta al PATH del sistema.

Prueba:
pdftoppm -h

### 5. Instalar Tesseract OCR
Descarga Tesseract para Windows:
👉 https://github.com/UB-Mannheim/tesseract/wiki (github.com in Bing)

Instálalo en:
C:\Program Files\Tesseract-OCR\
Verificar:

tesseract --version

Configura la variable de entorno:
setx TESSDATA_PREFIX "C:\Program Files\Tesseract-OCR\tessdata"

Prueba idiomas disponibles:
