from flask import render_template, Blueprint, request
from Controller.escola_bd import *
from model.bd_model import Professor
from routa.routa_usuario import reload_pagina
professor_blue = Blueprint('professor', __name__, template_folder='templates',url_prefix='/professor')
@professor_blue.route('/', methods=['POST'])
def perfil_professor():
        return  render_template('/professor/listar_professor.html')
#----------------------------Professor-------------------------------------------------
@professor_blue.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        numero_agente = request.form['numero_agente']
        nome = request.form['nome']
        email = request.form['email']
        data_nasc = request.form['data_nascimento']
        genero = request.form['genero']
        foto=salvar_imagem(request.files.get("imagem"),"professor")
        cadastrar_professor(numero_agente, nome, email, data_nasc, genero,foto,0)
        #reload_pagina()
        return  render_template('/professor/listar_professor.html', professor=pesquisar_professor(),turmas=pesquisar_turma())     
#----------------------------Professor--------------------------------------------------------------------------------------
@professor_blue.route('/listar_professor')
def listar_professor():
    return  render_template('/professor/listar_professor.html', professor=pesquisar_professor())
#----------------------------Professor-------------------------------------------------------------------------------------
@professor_blue.route('/form_professor',methods=['GET','POST']    )
def form_professor():
    return  render_template('/professor/cadastrar_professor.html')
#----------------------------Professor------------------------------------------------------------------------------------
@professor_blue.route('/excluir_professor/<int:id>', methods=['DELETE'])
def excluir_professor(id):
    apagar_professor(id)
    return  render_template('/professor/listar_professor.html', professor=pesquisar_professor())
#----------------------------Professor-----------------------------------------------------------
@professor_blue.route('/form_professor_editar/<int:id>', methods=['GET'])
def form_professor_editar(id):
    prof = Professor.get_by_id(id)
    return  render_template('/professor/editar_professor.html', professor=prof)

#-----------------------------------------------------------------------------------------------
@professor_blue.route('/professor/pesquisar_sala')
def professor_pesquisar_sala():
    id_prof = session.get("professor_id")
    return render_template('/sala/listar_sala.html', salas=pesquisar_sala_prof(id_prof))

#----------------------------Professor----------------------------------------------------------
@professor_blue.route('/editar_professor/<int:id>', methods=['PUT'])    
def editar_professor(id):
    if request.method == 'PUT':
        np=request.form['numero_agente']
        nome = request.form['nome']
        email = request.form['email']
        data_nasc = request.form['data_nascimento']
        genero = request.form['genero']
        editar_professor_(id,np,nome,email,data_nasc,genero)
        return  render_template('/professor/listar_professor.html', professor=pesquisar_professor())
    return "Falha ao editar professor"
#----------------------------pesquisar-------------------------------------------------------------
@professor_blue.route('/pesquisar', methods=['POST'])    
def pesquisar():
    if request.method == 'POST':
        pesq=request.form['pesq']
        nome=request.form['nome']
        if nome !="":
            if pesq == 'professor':
                return  render_template('/professor/listar_professor.html', professor=pesquisar_professor_per(nome),turmas=pesquisar_turma())
            elif pesq == 'aluno':
                return  render_template('/aluno/listar_aluno.html', aluno=pesquisar_aluno_per(nome))
            elif pesq == 'disciplina':
                return  render_template('/disciplina/listar_disciplina.html', disciplina=pesquisar_disciplina_per(nome))
            elif pesq == 'turma':
                return  render_template('/turma/listar_turma.html', turma=pesquisar_turma_per(nome))
            elif pesq == 'usuario':
                 return  render_template('/usuario/listar_usuario.html', usuario=pesquisar_usuario_per(nome))
            elif pesq == 'sala':
                 return  render_template('/sala/listar_sala.html', salas=pesquisar_sala_per(nome)) 
        else:
            if pesq == 'professor':
                return  render_template('/professor/listar_professor.html', professor=pesquisar_professor(),turmas=pesquisar_turma())
            elif pesq == 'aluno':
                return  render_template('/aluno/listar_aluno.html',alunos=pesquisar_aluno())
            elif pesq == 'disciplina':
                return  render_template('/disciplina/listar_disciplina.html', disciplina=pesquisar_disciplina())
            elif pesq == 'turma':
                return  render_template('/turma/listar_turma.html',turmas=pesquisar_turma())
            elif pesq == 'usuario':
                 return  render_template('/usuario/listar_usuario.html', usuario=pesquisar_usuario())
            elif pesq == 'sala':
                print(pesquisar_sala())
                return  render_template('/sala/listar_sala.html',salas=pesquisar_sala())
            else:
                return "<div >Sem Resultados </div>"
        return "<div >Sem Resultados </div>"