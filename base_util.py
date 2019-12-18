import os
from configparser import ConfigParser

import pdfkit

basepath = os.path.dirname(__file__)
profile = os.getenv('STAGE', "dev")

config_dir = os.path.join(basepath, "conf")
image_dir = os.path.join(os.path.join(basepath, "static"), "image")
pdf_dir = os.path.join(os.path.join(basepath, "static"), "report")
font_dir = os.path.join(os.path.join(basepath, "static"), "font")

print(config_dir, profile)

config = ConfigParser()
config.read(os.path.join(config_dir, 'app-{0}.cfg'.format(profile)))
print(config.get("PDF", 'wkhtmltopdf'))
pdf_config = pdfkit.configuration(wkhtmltopdf=config.get("PDF", 'wkhtmltopdf'))
# pdf_config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
project_url = config.get("PDF", 'project_url')
