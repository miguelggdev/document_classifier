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
    """
    Intenta extraer texto digital con PyPDF2.
    Si no encuentra texto, usa OCR con pdf2image + pytesseract.
    """
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    except Exception as e:
        print(f"Error con PyPDF2: {e}")

    # Si no hay texto digital, usar OCR
    if not text.strip():
        try:
            images = convert_from_path(pdf_path)
            for img in images:
                text += pytesseract.image_to_string(img, lang="eng")
        except Exception as e:
            print(f"Error con OCR: {e}")

    return text.strip()

def classify_document(text: str) -> str:
    """
    Envía el texto del documento a GPT-4o para clasificarlo.
    Devuelve la clasificación y justificación en formato JSON.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un clasificador de documentos. Clasifica el texto en categorías como 'Contrato', 'Factura', 'Queja/Reclamo', 'Carta', etc. Devuelve la salida en formato JSON con los campos: fecha, documento, clasificacion, justificacion."},
            {"role": "user", "content": text}
        ],
        temperature=0
    )

    result = response.choices[0].message.content
    return result

def process_pdf(pdf_path: str) -> dict:
    """
    Procesa un PDF: extrae texto y lo clasifica con GPT.
    """
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
    main()
