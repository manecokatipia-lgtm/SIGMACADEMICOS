from flask import render_template, Blueprint
adm_blue = Blueprint('adm', __name__, template_folder='templates',url_prefix='/adm')

@adm_blue.route('/home', methods=['GET'])
def home():
    return render_template('/principal.html')