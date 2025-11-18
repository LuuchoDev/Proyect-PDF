import os
from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    """
    Esta función carga la página web principal (nuestro frontend).
    Flask buscará 'index.html' en la carpeta 'templates'.
    """
    return render_template('index.html')

@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    """
    Esta función genera un archivo PDF a partir de una imagen subida por el usuario.
    Esta es la función principal del backend.
    Se activa cuando el JavaScript le envía las imágenes.
    """
    lista_imagenes_procesadas = []
    archivos_subidos = request.files.getlist('images')

    if not archivos_subidos:
        return "No se han subido imágenes.", 400
    
    try:
        for archivo in archivos_subidos:
            img = Image.open(archivo.stream)

            ## Aseguramos que este en modo RGB
            if img.mode == "RGBA":
                img = img.convert("RGB")
            
            lista_imagenes_procesadas.append(img)
        
        # Guardar las imágenes en un archivo PDF en memoria
        if lista_imagenes_procesadas:
            pdf_buffer = io.BytesIO()
            lista_imagenes_procesadas[0].save(
                pdf_buffer,
                format='PDF',
                save_all=True,
                append_images=lista_imagenes_procesadas[1:]
            )
            pdf_buffer.seek(0)

            # Enviar el archivo PDF generado al usuario
            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name="mi_pdf.pdf",
                mimetype='application/pdf'
            )
    except Exception as e:
        ## Manejo básico de errores
        print(f"Error: {e}")
        return f"Error al procesar las imágenes.", 500

## Iniciar aplicación
if __name__ == '__main__':
    app.run(debug=True)