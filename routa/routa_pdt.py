from flask import render_template, Blueprint
pdt_blue=Blueprint('pdt', __name__, template_folder='templates', url_prefix='/pdt')

@pdt_blue.route('/')
def listar_produtos():
    return render_template('pdt/listar_pdt.html')

@pdt_blue.route('/cadastro', methods=['GET', 'POST'])
def cadastrar_produto():
    return render_template('pdt/cadastrar_pdt.html')

@pdt_blue.route('/editar', methods=['GET', 'POST'])
def editar_produto():
    return render_template('pdt/editar_pdt.html')

@pdt_blue.route('/apagar', methods=['POST'])
def apagar_produto():
    return render_template('pdt/apagar_pdt.html')