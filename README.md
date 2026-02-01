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
`python -m venv .venv
.venv\Scripts\activate`

### 3. Instalar dependencias
Con el entorno virtual activado:

```python
python -m pip install --upgrade pip
python -m pip install PyPDF2 pdf2image pillow pytesseract openai python-dotenv tqdm
```

### 4. Instalar Poppler (para pdf2image)
Descarga Poppler para Windows:
👉 https://github.com/oschwartz10612/poppler-windows/releases

Extrae en C:\Program Files\poppler-xx\bin

Agrega esa ruta al PATH del sistema.

Prueba:
```python
`pdftoppm -h`
```

### 5. Instalar Tesseract OCR
Descarga Tesseract para Windows:
👉 https://github.com/UB-Mannheim/tesseract/wiki

Instálalo en:
C:\Program Files\Tesseract-OCR\
Verificar:

```python
`tesseract --version`
```

Configura la variable de entorno:
```python
`setx TESSDATA_PREFIX "C:\Program Files\Tesseract-OCR\tessdata"`
```

Prueba idiomas disponibles:

```python
`tesseract --list-langs`
```

### 🔑 Configuración de API Key
Crear un archivo .env en la raíz del proyecto:

OPENAI_API_KEY=api_key_aqui

### 📂 Estructura del proyecto

document_classifier/
│
├── docs/                # PDFs de prueba
│   ├── contrato1.pdf
│   └── queja1.pdf
│
├── main.py              # Script principal
├── test_ocr.py          # Script de prueba OCR
├── requirements.txt     # Dependencias
└── .env                 # API Key

### 🧪 Script de prueba OCR (test_ocr.py)

```python
import os
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

img = Image.open("pagina1_test.png")
texto = pytesseract.image_to_string(img, lang="eng")

print("Texto extraído por OCR:")
print(texto.strip() if texto.strip() else "⚠️ No se detectó texto en la imagen")

```
### 🧠 Código principal (main.py)

```python
import os
import json
import datetime
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno (API Key)
load_dotenv()
client = OpenAI()

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    except Exception as e:
        print(f"Error con PyPDF2: {e}")

    if not text.strip():
        try:
            images = convert_from_path(pdf_path)
            for img in images:
                text += pytesseract.image_to_string(img, lang="eng")
        except Exception as e:
            print(f"Error con OCR: {e}")

    return text.strip()

def classify_document(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un clasificador de documentos. Clasifica el texto en categorías como 'Contrato', 'Factura', 'Queja/Reclamo', 'Carta', etc. Devuelve la salida en formato JSON con los campos: fecha, documento, clasificacion, justificacion."},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def process_pdf(pdf_path: str) -> dict:
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return {"error": f"No se pudo extraer texto de {pdf_path}"}

    classification = classify_document(text)
    output = {
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "documento": os.path.basename(pdf_path),
        "resultado": classification
    }
    return output

def main():
    docs_folder = "docs"
    if not os.path.exists(docs_folder):
        print("⚠️ No se encontró la carpeta 'docs'. Crea la carpeta y coloca tus PDFs allí.")
        return

    for file in os.listdir(docs_folder):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(docs_folder, file)
            output = process_pdf(pdf_path)
            print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()`
```

▶️ Ejecución
Con el entorno virtual activado:
```python
`python main.py`
```

Salida

```python
`{"fecha": "2026-02-01 10:34:17", "documento": "contrato-2020-2021.pdf", "resultado": "```json\n{\n  \"fecha\": \"2021-03-12\",\n  \"documento\": \"Certificación de servicios\",\n  \"clasificacion\": \"Contrato\",\n  \"justificacion\": \"El documento certifica la prestación de servicios de una persona bajo una orden de servicio específica, detallando el objeto, plazo de ejecución y valor del contrato, lo cual es característico de un contrato.\"\n}\n```"}`
```

### 📌 Notas importantes
Siempre activa el entorno virtual antes de instalar dependencias o ejecutar el proyecto.

Usa python -m pip install ... para asegurarte de que las librerías se instalan dentro de .venv.

Configura correctamente TESSDATA_PREFIX para que Tesseract encuentre los idiomas.

Si quieres soporte en español, agrega spa.traineddata en la carpeta tessdata y usa lang="spa" en pytesseract.

### 🏆 Contribuciones
Este proyecto fue desarrollado paso a paso, resolviendo problemas de entorno en Windows, configurando OCR y migrando a la nueva API de OpenAI. 
La segunda vearsión se realizará en un entorno Linux.

### 📌 Recursos utilizados
Python  
👉 https://www.python.org/downloads/

PyPDF2 (extracción de texto digital en PDFs)  
👉 https://pypi.org/project/PyPDF2/

pdf2image (conversión de PDF a imágenes)  
👉 https://pypi.org/project/pdf2image/

Pillow (procesamiento de imágenes)  
👉 https://pypi.org/project/Pillow/

pytesseract (OCR con Tesseract)  
👉 https://pypi.org/project/pytesseract/ (pypi.org in Bing)

Tesseract OCR para Windows (UB Mannheim build)  
👉 https://github.com/UB-Mannheim/tesseract/wiki (github.com in Bing)

Modelos de idiomas para Tesseract (tessdata)  
👉 https://github.com/tesseract-ocr/tessdata (github.com in Bing)

Poppler para Windows (necesario para pdf2image)  
👉 https://github.com/oschwartz10612/poppler-windows/releases (github.com in Bing)

OpenAI Python SDK (API GPT‑4o)  
👉 https://pypi.org/project/openai/  
👉 https://github.com/openai/openai-python

python-dotenv (manejo de variables de entorno)  
👉 https://pypi.org/project/python-dotenv/ (pypi.org in Bing)

tqdm (barra de progreso opcional)  
👉 https://pypi.org/project/tqdm/

