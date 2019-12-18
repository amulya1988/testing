from flask import Blueprint, render_template

from database.db_config import create_session, close_session
from repository.crud_repository import UserRepository

wipro_report_app = Blueprint('report', __name__)


@wipro_report_app.route('/front_page/<int:bpm_id>', methods=['GET'])
def front_page(bpm_id):
    session, con = create_session()
    user = UserRepository(session).find_bpm_id(bpm_id)
    close_session(session, con)
    return render_template('/front_page.html', user=user)


@wipro_report_app.route('/introduction/<int:bpm_id>', methods=['GET'])
def introduction_page(bpm_id):
    return render_template('/introduction.html')


@wipro_report_app.route('/score_by_result/<int: bpm_id>', methods=['GET'])
def score_by_result(bpm_id):
    session, con = create_session()
    close_session(session, con)
    return "null"


@wipro_report_app.route('/last_page/<int:bpm_id>', methods=['GET'])
def last_page(bpm_id):
    return render_template('/last_page.html')
