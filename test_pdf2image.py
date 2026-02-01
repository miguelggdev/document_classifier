from pdf2image import convert_from_path

# Ruta a un PDF de prueba dentro de la carpeta docs
pdf_path = "docs/UNAD-2020-2021.pdf"

# Si Poppler no está en el PATH, especifica la ruta manual:
# images = convert_from_path(pdf_path, poppler_path=r"C:\poppler-23.11.0\bin")

# Si ya está en el PATH, basta con:
images = convert_from_path(pdf_path)

print(f"Se generaron {len(images)} páginas como imágenes")

# Guardar la primera página como imagen para verificar
if images:
    images[0].save("pagina1_test.png", "PNG")
    print("✅ Primera página guardada como pagina1_test.png")
else:
    print("⚠️ No se pudo convertir el PDF a imágenes")
