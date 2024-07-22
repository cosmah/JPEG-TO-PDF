from flask import Flask, request, render_template, send_file
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return "No file part"
    files = request.files.getlist('files[]')
    jpeg_files = []
    for file in files:
        if file and file.filename.endswith('.jpeg'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            jpeg_files.append(filepath)
    
    if jpeg_files:
        output_pdf = convert_jpeg_to_pdf(jpeg_files)
        # Explicitly setting the MIME type and providing a download name
        return send_file(output_pdf, as_attachment=True, mimetype='application/pdf', download_name='output.pdf')
    else:
        return "No valid JPEG files uploaded"

def convert_jpeg_to_pdf(jpeg_files):
    # Register the font
    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'TimesNewRoman.ttf'))
    
    # Create a new PDF file with specified formatting
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # Set font and size
    can.setFont("TimesNewRoman", 12)
    
    # Process each JPEG file
    for jpeg_file in jpeg_files:
        img = Image.open(jpeg_file)
        width, height = img.size
        aspect_ratio = width / height
        new_width = A4[0]
        new_height = A4[0] / aspect_ratio

        if new_height > A4[1]:
            new_height = A4[1]
            new_width = A4[1] * aspect_ratio

        can.drawImage(jpeg_file, 0, 0, width=new_width, height=new_height)
        can.showPage()  # Start a new page for the next image
    
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = io.BytesIO(packet.read())
    new_pdf.seek(0)
    
    return new_pdf

if __name__ == '__main__':
    app.run(debug=True)
