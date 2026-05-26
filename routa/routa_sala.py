from flask import render_template, Blueprint, request   
from model.bd_model import Aluno
from Controller.escola_bd import *

sala_blue = Blueprint('sala', __name__, template_folder='templates',url_prefix='/sala')
#----------------------------SALA-------------------------------------------------
@sala_blue.route('/', methods=['POST'])
def perfil_aluno():
        return  render_template('/sala/listar_aluno.html')
#----------------------------Sala-------------------------------------------------
@sala_blue.route('/cadastrar', methods=['POST'])
def cadastrar():
    id_prof = session.get("professor_id") or request.form.get("professor_id")
    if not id_prof:
        return "Erro: professor não identificado"

    nome = "SV - " + request.form['nome']
    nivel = request.form['nivel']
    observacao = request.form['observacao']
    foto = salvar_imagem(request.files.get("imagem"), "sala")

    mensagem = criar_sala(id_prof, nome, nivel, observacao, foto)
    return mensagem

#----------------------------SALA-------------------------------------------------
@sala_blue.route('/cadastrar_conteudo', methods=['POST'])
def cadastrar_conteudo():
    destino_1=""
    destino_2=""
    if request.method == 'POST':
        id_prof = session.get("professor_id")
        titulo =request.form['titulo']
        nivel= request.form['nivel']
        formato_1 = request.form['formato_1']
        conteudo_1 = request.files.getlist('conteudo_1')        
        formato_2 = request.form['formato_2']
        conteudo_2=request.files.getlist('conteudo_2')
        obs = request.form['obs']
        if formato_2 !="":
            destino_1="material"+"/"+nivel+"/"+formato_1
            destino_2="material"+"/"+nivel+"/"+formato_2
            codigo =salvar_conteudo(conteudo_1,conteudo_2,destino_1,destino_2)
            if criar_conteudo(titulo, nivel,formato_1,formato_2,codigo,obs,id_prof)==1:
                return  "Conteúdo criado com sucesso"
            else:
                return "Falha Na Inserção Dos Dados"
        else:
            destino_1="material"+"/"+nivel+"/"+formato_1
            codigo =salvar_conteudo(conteudo_1,conteudo_2,destino_1,destino_2)
            if criar_conteudo(titulo, nivel,formato_1,formato_2,codigo,obs,id_prof)==1:
                return  "Conteúdo criado com sucesso"
            else:
                return "Falha Na Inserção Dos Dados"
#------------------------------------------------------------------------------------------------------
@sala_blue.route('/listar_sala')
def listar_sala():
    return  render_template('/sala/listar_sala.html', salas=pesquisar_sala())
#----------------------------SALA-------------------------------------------------
@sala_blue.route('/form_sala',methods=['GET','POST']    )
def form_sala():
    return  render_template('/sala/cadastrar_sala.html')
#----------------------------SALA-------------------------------------------------
@sala_blue.route('/form_conteudo/',defaults={'id':None})
@sala_blue.route('/form_conteudo/<int:id>',methods=['GET','POST'])
def form_conteudo(id):
    if id:
        return  render_template('/sala/cadastrar_conteudo.html',id_professor=id)
    else:
        return  render_template('/sala/cadastrar_conteudo.html')
#----------------------------SALA-------------------------------------------------
@sala_blue.route('/excluir_sala/<int:id>', methods=['DELETE'])
def excluir_sala(id):
    apagar_sala(id)
    return  render_template('/sala/listar_sala.html', salas=pesquisar_sala())
#----------------------------SALA-------------------------------------------------
@sala_blue.route('/form_sala_editar/<int:id>', methods=['GET'])
def form_sala_editar(id):
    sala = Sala.get_by_id(id)
    return  render_template('/sala/editar_sala.html', sala=sala)
#----------------------------SALA-------------------------------------------------
@sala_blue.route('/editar_sala/<int:id>', methods=['POST'])    
def editar_sala(id):
    if request.method == 'POST':
        nome ="SV - " +request.form['nome']
        nivel = request.form['nivel']
        observacao = request.form['observacao']
        editar_sala_(id,nome,nivel,observacao)
        return  render_template('/sala/listar_sala.html', salas=pesquisar_sala())
    return "Falha ao editar aluno"

#----------------------------SALA-------------------------------------------------
@sala_blue.route('/sala/listar_conteudo')
def listar_conteudo():
    professor_id = session.get('professor_id')
    nivel = request.args.get('nivel')
    titulo = request.args.get('titulo')
    data = request.args.get('data')

    conteudos = pesquisar_conteudo(professor_id, nivel, titulo, data)

    # Se for requisição HTMX, retorna só o fragmento da tabela
    if request.headers.get('HX-Request'):
        return render_template('/sala/_conteudo_table.html', conteudos=conteudos)
    else:
        return render_template('/sala/listar_conteudos.html', conteudos=conteudos)
#----------------------------SALA-------------------------------------------------

@sala_blue.route('/excluir_conteudo/<int:id>', methods=['DELETE'])
def excluir_conteudo(id):
    apagar_conteudo(id)
    return  render_template('/sala/listar_conteudo.html', conteudos=pesquisar_conteudo())


@sala_blue.route('/listar_conteudo_professor',methods=['GET'])
def listar_conteudo_professor():
    id_prof = session.get("professor_id")
    return  render_template('/perfil/listar_conteudo.html',conteudos=pesquisar_conteudo_prof(id_prof))    

