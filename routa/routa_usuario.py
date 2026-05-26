from flask import render_template, Blueprint, request   
from model.bd_model import Usuario,Professor, Aluno
from Controller.escola_bd import*

usuario_blue = Blueprint('usuario', __name__, template_folder='templates',url_prefix='/usuario')
#----------------------------Aluno-------------------------------------------------
@usuario_blue.route('/', methods=['POST'])
def perfil_aluno():
        return  render_template('/usuario/listar_usuario.html')
#----------------------------------------------------------------
@usuario_blue.route('/cadastrar', methods=['POST'])
def cadastrar():
    ex_professor = None
    ex_aluno = None
    nome = request.form['nome']
    email = request.form['email']
    nivel = request.form['nivel']

    try:
        if request.form['np1'] == "professor":
            ex_professor = request.form['id_usuario']
            usuario = cadastrar_usuario(nome, email, nivel, True, ex_aluno, ex_professor)
            return render_template('/usuario/listar_usuario_func.html',
                                   professores=pesquisar_professor_usuario())

        elif request.form['np1'] == "aluno":
            ex_aluno = request.form['id_usuario']
            usuario = cadastrar_usuario(nome, email, nivel, True, ex_aluno, ex_professor)
            return render_template('/usuario/listar_usuario_aluno.html',
                                   alunos=pesquisar_aluno_usuario())

    except Exception as e:
        # Se enviar_email falhar, nada é salvo e mostramos erro
        return f"Erro ao cadastrar usuário: {str(e)}"

#-----------------------------------------------------------------------------
@usuario_blue.route('/listar_usuario')
def listar_usuario():
    return  render_template('/usuario/listar_usuario.html', usuario=pesquisar_usuario())
#-----------------------------------------------------------------------------------------------------
@usuario_blue.route('/listar_usuario_func',methods=['GET','POST']    )
def listar_usuario_func():
    return  render_template('/usuario/listar_usuario_func.html',professores=pesquisar_professor_usuario())
#--------------------------------------------------------------------------------------------------------
@usuario_blue.route('/listar_usuario_aluno',methods=['GET','POST']    )
def listar_usuario_aluno():
    return  render_template('/usuario/listar_usuario_aluno.html',alunos=pesquisar_aluno_usuario())
#-----------------------------------------------------------------------------------------------
@usuario_blue.route('/form_usuario/<int:id>/<string:np>',methods=['GET'])
def form_usuario(id,np):
    if np=="professor":
        usuario=Professor.get_by_id(id)
        return  render_template('/usuario/cadastrar_usuario.html',usuarios=usuario,np=np)
    elif np=="aluno":
        usuario=Aluno.get_by_id(id)
        return  render_template('/usuario/cadastrar_usuario.html',usuarios=usuario,np=np)
#----------------------------Aluno-------------------------------------------------------
@usuario_blue.route('/excluir_usuario/<int:id>',methods=['DELETE'])
def excluir_usuario(id):
    apagar_usuario(id)
    return  render_template('/usuario/listar_usuario.html',usuario=pesquisar_usuario())
#----------------------------Aluno-------------------------------------------------
@usuario_blue.route('/form_usuario_editar/<int:id>', methods=['GET'])
def form_usuario_editar(id):
    usuario = Usuario.get_by_id(id)
    return  render_template('/usuario/editar_usuario.html', usuario=usuario)
#----------------------------Usuario-------------------------------------------------
@usuario_blue.route('/editar_usuario/<int:id>', methods=['POST'])    
def editar_usuario(id):
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']
        nivel = request.form['nivel']
        estado = request.form['estado']
        editar_usuario_(id,nome,senha,email,nivel,estado)
        return  render_template('/usuario/listar_usuario.html', usuario=pesquisar_usuario())
    return "Falha ao editar aluno" 
#---------------------------------------------------------------------------------
@usuario_blue.route('/validar_usuario',methods=['GET','POST'])
def validar_usuario():
    if request.method == 'POST':
        senha = request.form['senha']
        email = request.form['email']
        usuarios = valida_usuario(senha, email)
        usuario_id = session.get("usuario_id")
        # print(usuarios.professor.foto)
        if usuarios is not None and usuarios.id == usuario_id:
            if usuarios.nivel == "adm":
                return render_template('/index.html', usuario=usuarios) 
            elif usuarios.nivel == "coordenador":
                return render_template('/perfil/perfil_coord.html', usuario=usuarios) 
            elif usuarios.nivel == "professor":
                return render_template('/perfil/professor.html', usuario=usuarios)
            elif usuarios.nivel == "aluno":
                perfil_aluno = Aluno.get_by_id(session.get("aluno_id"))
                return render_template('/perfil/perfil_aluno.html', usuario=usuarios)
            else:
                return render_template('login.html', error="Credenciais inválidas")
        else:
            # se não encontrou ou senha errada → volta para login
            return render_template('login.html', error="Email ou senha inválidos")
   
    #--------------------------------------------------------------------------------
#Rota para editar o numero de disciplinas do professor
@usuario_blue.route('/alterar_estado/<int:id>', methods=['GET'])
def alterar_estado(id):
    usuario = Usuario.get_by_id(id)
    return render_template('usuario/editar_estado.html',usuario=usuario)

@usuario_blue.route('/salvar_estado_usuario/<int:id>', methods=['POST'])
def salvar_estado_usuario(id):
    usuario = Usuario.get_by_id(id)
    usuario.estado = "estado" in request.form
    usuario.save()
    return f'<td>{usuario.estado}</td>'

@usuario_blue.route('/perfil_professor/<int:id>')
def perfil_professor(id):
    professor = Professor.get_by_id(id)  # ou join com Usuario se precisar
    return render_template('perfil_professor.html', professor=professor)


@usuario_blue.route("/usuario/trocar_senha", methods=["GET", "POST"])
def trocar_senha():
    if request.method == "POST":
        usuario_id = request.form.get("usuario_id")
        senha_atual = request.form.get("senha_atual")
        nova_senha = request.form.get("nova_senha")
        confirmar_senha = request.form.get("confirmar_senha")

        resultado = trocar_senha(usuario_id, senha_atual, nova_senha, confirmar_senha)
        return render_template("trocar_senha.html", resultado=resultado)

    return render_template("c")



@usuario_blue.route('/reload_pagina', methods=['GET'])
def reload_pagina():
    return reload()