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
import os
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib import colors
from markitdown import MarkItDown




""" 0.2. Main Program """
def main():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    cfg_path = "settings.cfg"
    settings = read_settings(cfg_path)
    print_settings(settings)

    # print(f"{settings['classification']}") # Access individual settings.
    # print(f"{settings['content_directory']}")

    # PDF Printing pages
    markify(settings, base_dir)





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
        'content_directory': s.get('content_directory'),
    }

def print_settings(settings):
    print("Settings Readout:")
    for key, value in settings.items():
        print(f"{key} = {value}")




""" Convert ALL files in CONTENT DIRECTORY to MARKDOWN """
def markify(settings, base_dir):
    md = MarkItDown(enable_plugins=False)
    directory = os.path.join(base_dir, './config/content')
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            result = md.convert(file_path)  # Pass the file path, not the content
            results.append(result)
    for result in results:
        print(result.text_content)




if __name__ == "__main__":
    main()