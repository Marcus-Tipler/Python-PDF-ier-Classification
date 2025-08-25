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
import markdown
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib import colors
import os




""" 0.2. Main Program """
def main():
    cfg_path = "settings.cfg"
    settings = read_settings(cfg_path)
    print_settings(settings)

    # PDF Printing pages
    generate_pdf_from_md("./config/content/content.md", "output.pdf")





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




def md_to_html(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite', 'attr_list'])
    return html


def parse_html_to_pdf_elements(html, base_path):
    soup = BeautifulSoup(html, 'html.parser')
    styles = getSampleStyleSheet()
    elements = []

    for tag in soup.children:
        if tag.name == 'h1':
            elements.append(Paragraph(tag.text, styles['Title']))
        elif tag.name == 'h2':
            elements.append(Paragraph(tag.text, styles['Heading2']))
        elif tag.name == 'h3':
            elements.append(Paragraph(tag.text, styles['Heading3']))
        elif tag.name == 'p':
            elements.append(Paragraph(tag.text, styles['BodyText']))
        elif tag.name == 'pre':
            code_style = ParagraphStyle('Code', fontName='Courier', fontSize=10, backColor=colors.lightgrey)
            elements.append(Paragraph(tag.text, code_style))
        elif tag.name == 'img':
            img_path = os.path.join(base_path, tag['src'])
            elements.append(Image(img_path, width=400, height=200))
        elif tag.name == 'table':
            data = []
            for row in tag.find_all('tr'):
                data.append([cell.text for cell in row.find_all(['td', 'th'])])
            table = Table(data)
            table.setStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            elements.append(table)
        elif tag.name is None and tag.string.strip():
            elements.append(Paragraph(tag.string, styles['BodyText']))
        # Add more tag handling as needed

        elements.append(Spacer(1, 12))
    return elements


def generate_pdf_from_md(md_path, pdf_path):
    base_path = os.path.dirname(md_path)
    html = md_to_html(md_path)
    elements = parse_html_to_pdf_elements(html, base_path)
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    doc.build(elements)




if __name__ == "__main__":
    main()