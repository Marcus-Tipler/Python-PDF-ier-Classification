"""
Program developed and conceptualized by Marcus Francis TIPLER.

The idea is to have a program that can easily make PDF reports with classifications.


This Program is consisted of three parts as follows:
1. Collection of Configurations.
2. Collection & Interpretation of Data Files.
3. Output of PDF File.
"""




""" 0.1. Imports & Requirements """
import configparser
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor




""" 0.2. Main Program """
def main():
    cfg_path = "settings.cfg"
    settings = read_settings(cfg_path)
    print_settings(settings)
    generate_pdf(settings)




""" 1. Collection of the CONFIGURATION FILE """
def read_settings(cfg_path):
    parser = configparser.ConfigParser()
    with open(cfg_path, 'r') as f:
        content = '[DEFAULT]\n' + f.read()
    parser.read_string(content)
    s = parser['DEFAULT']
    return {
        'classification': s.get('classification'),
        'classification_color': s.get('classification_color'),
        'classification_angle': int(s.get('classification_angle', '0')),
        'logo_file': s.get('logo_file'),
        'title_color': s.get('title_color'),
        'subtitle_color': s.get('subtitle_color'),
        'text_color': s.get('text_color'),
        'is_header': s.getboolean('is_header', fallback=False),
        'header_title': s.get('header_title'),
        'header_subtitle': s.get('header_subtitle'),
        'header_corner_logo': s.getboolean('header_corner_logo', fallback=False),
        'header_center_logo': s.getboolean('header_center_logo', fallback=False),
        'is_header_classified': s.getboolean('is_header_classified', fallback=False),
        'header_description': s.get('header_description'),
        'is_footer': s.getboolean('is_footer', fallback=False),
        'footer_title': s.get('footer_title'),
        'is_footer_classified': s.getboolean('is_footer_classified', fallback=False),
        'is_ind_footer': s.getboolean('is_ind_footer', fallback=False),
        'footer_ind_left': s.get('footer_ind_left'),
        'footer_ind_middle': s.get('footer_ind_middle'),
        'footer_ind_right': s.get('footer_ind_right'),
    }

def print_settings(settings):
    print("Settings Readout:")
    for key, value in settings.items():
        print(f"{key} = {value}")




""" 3. GENERATE PDF FROM DATA """
def generate_pdf(settings, filename="output.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Classification (centered, rotated)
    if settings['classification']:
        c.saveState()
        c.setFillColor(HexColor(settings['classification_color']))
        c.translate(width/2, height/2)
        c.rotate(int(settings['classification_angle']))
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(0, 0, f"Classification: {settings['classification']}")
        c.restoreState()
        
    # Header
    if settings['is_header']:
        y = height - 60
        if settings['header_center_logo'] and settings['logo_file']:
            c.drawString(50, y, f"[Logo: {settings['logo_file']}]")
            y -= 30
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(HexColor(settings['title_color']))
        c.drawString(50, y, f"Title: {settings['header_title']}")
        y -= 25
        c.setFont("Helvetica", 16)
        c.setFillColor(HexColor(settings['subtitle_color']))
        c.drawString(50, y, f"Subtitle: {settings['header_subtitle']}")
        y -= 25
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor(settings['text_color']))
        c.drawString(50, y, f"Description: {settings['header_description']}")
        y -= 25
        if settings['is_header_classified']:
            c.setFont("Helvetica-Oblique", 10)
            c.setFillColor(HexColor(settings['classification_color']))
            c.drawString(50, y, f"[Header Classification: {settings['classification']}]")

    c.showPage()  # End main page

    # Footer (bottom of page)
    if settings['is_footer']:
        y = 40
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor(settings['title_color']))
        c.drawString(50, y, f"Footer Title: {settings['footer_title']}")
        if settings['is_footer_classified']:
            c.setFont("Helvetica-Oblique", 10)
            c.setFillColor(HexColor(settings['classification_color']))
            c.drawString(250, y, f"[Footer Classification: {settings['classification']}]")
        c.showPage()  # End footer page

    # Individual Page Footer (left, middle, right)
    if settings['is_ind_footer']:
        y = 20
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor(settings['text_color']))
        c.drawString(50, y, f"Left: {settings['footer_ind_left']}")
        c.drawCentredString(width/2, y, f"Middle: {settings['footer_ind_middle']}")
        c.drawRightString(width-50, y, f"Right: {settings['footer_ind_right']}")

    c.showPage()
    c.save()
    print(f"PDF generated: {filename}")




if __name__ == "__main__":
    main()