from flask import render_template, Blueprint, request
from Controller.escola_bd import *
from model.bd_model  import Disciplina
disciplina_blue = Blueprint('disciplina', __name__, template_folder='templates',url_prefix='/disciplina')

#----------------------------Disciplina-------------------------------------------------
     
@disciplina_blue.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        sigla = request.form['sigla']
        cadastrar_disciplina(nome, sigla)
        return  render_template('/disciplina/listar_disciplina.html',disciplina=pesquisar_disciplina())     

@disciplina_blue.route('/listar_disciplina', methods=['GET'])
def listar_disciplina():
    return  render_template('/disciplina/listar_disciplina.html',disciplina=pesquisar_disciplina())

@disciplina_blue.route('/form_disciplina',methods=['GET','POST']    )
def form_disciplina():
    return  render_template('/disciplina/cadastrar_disciplina.html',disciplinas=pesquisar_disciplina())

@disciplina_blue.route('/excluir_disciplina/<int:id>', methods=['DELETE'])
def excluir_disciplina(id):
    apagar_disciplina(id)
    return  render_template('/disciplina/listar_disciplina.html',disciplina=pesquisar_disciplina())

@disciplina_blue.route('/form_disciplina_editar/<int:id>', methods=['GET'])
def form_disciplina_editar(id):
    disc = Disciplina.get_by_id(id)
    return  render_template('/disciplina/editar_disciplina.html',disciplina=disc)

@disciplina_blue.route('/editar_disciplina/<int:id>', methods=['PUT'])    
def editar_disciplina(id):
    if request.method == 'PUT':
        nome = request.form['nome']
        sigla = request.form['sigla']
        editar_disciplina_(id, nome, sigla)
        return  render_template('/disciplina/listar_disciplina.html',disciplina=pesquisar_disciplina())
    return "Falha ao editar disciplina"

@disciplina_blue.route('/pesq_disc',methods=['POST'])
def pesq_disc():
     if request.method == 'POST': 
        nome=request.form['disc']
        disc=pesquisar_disciplina_per(nome)
        return render_template('turma/form_add',disc=disc)
     
@disciplina_blue.route('/pesq_disciplina',methods=['POST'])
def pesq_disciplina():
    if request.method == 'POST':
        nome=request.form['disc']
        disciplina=pesquisar_disciplina_per(nome)
        return  render_template('/turma/listar_disc.html',disciplina=pesquisar_disciplina_per(nome))

#---------------------------------------------------------------------------
@disciplina_blue.route('/pesquisar_disciplina_id/<int:id_prof>', methods=['POST'])
def pesquisar_disciplina_id(id_prof):
    disciplina_id= pesquisar_disciplina_professor(id_prof)
    return render_template('professor/escolha_disc.html',disciplina=disciplina_id)