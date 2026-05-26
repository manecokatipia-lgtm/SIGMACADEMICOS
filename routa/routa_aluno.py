from flask import render_template, Blueprint, request  
from Controller.escola_bd import * 
from model.bd_model import Aluno
aluno_blue = Blueprint('aluno', __name__, template_folder='templates',url_prefix='/aluno')
#----------------------------Aluno-------------------------------------------------
@aluno_blue.route('/', methods=['POST'])
def perfil_aluno():
        return  render_template('/aluno/listar_aluno.html')
#----------------------------Aluno-------------------------------------------------
@aluno_blue.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        numero_aluno = request.form['numero_aluno']
        nome = request.form['nome']
        email = request.form['email']
        data_nasc = request.form['data_nascimento']
        genero = request.form['genero']
        foto=salvar_imagem(request.files.get("imagem"),"aluno")
        curso = request.form['curso']
        classe = request.form['classe']
        cadastrar_aluno(numero_aluno, nome, email, data_nasc, genero,foto,curso,classe)
        return  render_template('/aluno/listar_aluno.html',alunos=pesquisar_aluno())     
#----------------------------Aluno-------------------------------------------------
@aluno_blue.route('/listar_aluno')
def listar_aluno():
    return  render_template('/aluno/listar_aluno.html', aluno=pesquisar_aluno())
#----------------------------Aluno-------------------------------------------------
@aluno_blue.route('/form_aluno',methods=['GET','POST']    )
def form_aluno():
    return  render_template('/aluno/cadastrar_aluno.html')
#----------------------------Aluno-------------------------------------------------

@aluno_blue.route('/excluir_aluno/<int:id>', methods=['DELETE'])
def excluir_aluno(id):
    apagar_aluno(id)
    return  render_template('/aluno/listar_aluno.html', aluno=pesquisar_aluno())
#----------------------------Aluno-------------------------------------------------
@aluno_blue.route('/form_aluno_editar/<int:id>', methods=['GET'])
def form_aluno_editar(id):
    aluno = Aluno.get_by_id(id)
    return  render_template('/aluno/editar_aluno.html', aluno=aluno)
#----------------------------Aluno-------------------------------------------------
@aluno_blue.route('/editar_aluno/<int:id>', methods=['POST'])    
def editar_aluno(id):
    if request.method == 'POST':
        mat = request.form['numero_aluno']
        nome = request.form['nome']
        email = request.form['email']
        data_nasc = request.form['data_nascimento']
        genero = request.form['genero']
        editar_aluno_(id,mat,nome,email,data_nasc,genero)
        return  render_template('/aluno/listar_aluno.html', aluno=pesquisar_aluno())
    return "Falha ao editar aluno"