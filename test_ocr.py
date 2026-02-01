import os
import pytesseract
from PIL import Image

# Ruta al ejecutable de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Ruta correcta al tessdata
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

img = Image.open("pagina1_test.png")
texto = pytesseract.image_to_string(img, lang="eng")

print("Texto extraído por OCR:")
print(texto.strip() if texto.strip() else "⚠️ No se detectó texto en la imagen")
