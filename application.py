import os

from flask import Flask, jsonify
from flask_compress import Compress
from flask_cors import CORS
from flask_queryinspect import QueryInspect

from controller.report_controller import wipro_report_app
from controller.pdf_controller import pdf_app
from flaskrun import flaskrun

application = Flask(__name__,
                    template_folder='templates', static_folder="static")

config_name = os.getenv('FLASK_CONFIGURATION', 'default')
application.config['BUNDLE_ERRORS'] = True
application.config['TEMPLATES_AUTO_RELOAD'] = True
application.config.from_pyfile('config.cfg', silent=True)
application.debug = False
CORS(application)
Compress(application)
qi = QueryInspect(application)


@application.route('/')
def home():
    """

    Returns:

    """
    return jsonify({"Provided By": "Think Talent Services Pvt Ltd"})


@application.route('/favicon.ico')
def send_js():
    return ""


application.register_blueprint(wipro_report_app, url_prefix='/report')
application.register_blueprint(pdf_app, url_prefix='/pdf')

if __name__ == '__main__':
    flaskrun(application)
