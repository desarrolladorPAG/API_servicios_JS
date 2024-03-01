from flask import Blueprint
from flask_cors import cross_origin
from controllers import login_controller

login = Blueprint('login', __name__,url_prefix='/api/v1')

@cross_origin()
@login.route('/login', methods=['POST'])
def login_normal():
    return login_controller.login()