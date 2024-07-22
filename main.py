from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io

def jpg_to_pdf_with_format(jpg_files, output_pdf):
    # Register the font
    pdfmetrics.registerFont(TTFont('TimesRoman', 'TimesNewRoman.ttf'))
    
    # Create a new PDF file with specified formatting
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # Set font and size
    can.setFont("TimesRoman", 12)
    
    # Process each JPEG file
    for jpg_file in jpg_files:
        img = Image.open(jpg_file)
        width, height = img.size
        aspect_ratio = width / height
        new_width = A4[0]
        new_height = A4[0] / aspect_ratio

        if new_height > A4[1]:
            new_height = A4[1]
            new_width = A4[1] * aspect_ratio

        can.drawImage(jpg_file, 0, 0, width=new_width, height=new_height)
        can.showPage()  # Start a new page for the next image
    
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = packet.read()
    
    # Write the PDF to a file
    with open(output_pdf, 'wb') as f:
        f.write(new_pdf)

# Example usage
jpg_files = ['IMG-20240122-WA0026.jpg', 'IMG-20240122-WA0027.jpg']  # List of JPEG files
output_pdf = 'combined.pdf'  # Output PDF file name
jpg_to_pdf_with_format(jpg_files, output_pdf)
