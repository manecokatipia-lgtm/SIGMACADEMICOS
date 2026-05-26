from flask import render_template, Blueprint
classe_blue= Blueprint('classe', __name__, template_folder='templates', url_prefix='/classes')

@classe_blue.route('/')
def listar_classe():
    return render_template("/classe/listar_classe.html")

@classe_blue.route('/cadastro', methods=['GETS', 'POST'])
def cadastrar_classe():
    return render_template('/classe/cadastrar_classe.html')

@classe_blue.route('/editar', methods=['GETS', 'POST'])
def editar_classe():
    return render_template('/classe/editar_classe.html')

@classe_blue.route('/apagar', methods=['GETS', 'POST'])
def apagar_classe():
    return render_template('/classe/apagar_classe.html')