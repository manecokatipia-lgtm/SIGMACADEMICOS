from flask import render_template, Blueprint, request
from Controller.escola_bd import *
from model.bd_model import Turma
turma_blue = Blueprint('turma', __name__, template_folder='templates',url_prefix='/turma')

#---------------------------------------------------------------------------------------------------------

@turma_blue.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        capacidade = request.form['capacidade']
        cadastrar_turma(nome, capacidade)
        return  render_template('/turma/listar_turma.html',turmas=pesquisar_turma())     
#---------------------------------------------------------------------------------------------------------

@turma_blue.route('/listar_turma', methods=['GET'])
def listar_turma():
    return  render_template('/turma/listar_turma.html',turmas=pesquisar_turma())
#---------------------------------------------------------------------------------------------------------

@turma_blue.route('/form_turma',methods=['GET','POST'])
def form_turma():
    return  render_template('/turma/cadastrar_turma.html',turmas=pesquisar_turma())
#---------------------------------------------------------------------------------------------------------

@turma_blue.route('/excluir_turma/<int:id>', methods=['DELETE'])
def excluir_turma(id):
    apagar_turma(id)
    return  render_template('/turma/listar_turma.html',turmas=pesquisar_turma())
#---------------------------------------------------------------------------------------------------------

@turma_blue.route('/form_turma_editar/<int:id>', methods=['GET'])
def form_turma_editar(id):
    turma = Turma.get_by_id(id)
    return  render_template('/turma/editar_turma.html',turma=turma)
#---------------------------------------------------------------------------------------------------------------------------------
@turma_blue.route('/form_add/',defaults={'id':None})
@turma_blue.route('/form_add/<int:id>',methods=['GET','POST'])
def  form_add(id):
    if id is None:
        #reload()
        return render_template('/turma/form_add.html',prof=pesquisar_professor(),disc=pesquisar_disciplina(),turma=pesquisar_turma())
    else:
        #reload()
        turma=Turma.get_by_id(id)
        return render_template('/turma/form_add.html',prof=pesquisar_professor(),disc=pesquisar_disciplina(),turma=turma)
#----------------------------------------------------------------------------------------------------------------------------
@turma_blue.route('/receber_prof/',methods=['POST'])
def  receber_prof():
     if request.method=="POST":
        id_prof=request.form.getlist("id_prof")
        return id_prof 
#---------------------------------------------------------------------------------------------------------

@turma_blue.route('/receber_disc/',methods=['POST'])
def  receber_disc():
     if request.method=="POST":
        id_disc=request.form.getlist("id_disc")
        return id_disc 
#----------------------------------------------------------------------------------------------------------    
@turma_blue.route('/vincular_prof/',methods=['POST'])
def  vincular_prof():
     if request.method=="POST":
        id_disc=request.form.getlist("id_disc")
        id_turma=request.form['id_turma']
        
        val=""
        for id in id_disc:
            if verificar_vinculo_disciplina_turma(int(id),int(id_turma)):
                resultado = verificar_vinculo_disciplina_turma(int(id), int(id_turma)).get()
                #print(resultado.professor_id)
                val= f"A Disciplina {Disciplina.get_by_id(int(id)).nome} foi atribuida ao professor {Professor.get_by_id(resultado.professor_id).nome} Nesta Turma {Turma.get_by_id(id_turma).nome} " 
            else:
                #print(contar_vinculos_professor(int(receber_prof()[0]),int(id)))
                if contar_vinculos_professor(int(receber_prof()[0]),int(id)) > 0:
                    vincular(id_turma,int(receber_prof()[0]),int(id))
                    val= f"Professor {Professor.get_by_id(receber_prof()[0]).nome} vinculado a Turma {Turma.get_by_id(id_turma).nome} com sucesso"
                elif contar_vinculos_professor(int(receber_prof()[0]),int(id)) == 0:
                    print(f"ID Professor: {receber_prof()[0]}, ID Disciplina: {id}")
                    val= f"A Disciplina de {Disciplina.get_by_id(id).nome} não está vinculada ao professor/a {Professor.get_by_id(receber_prof()[0]).nome}"
                elif contar_vinculos_professor(int(receber_prof()[0]),int(id)) == -1:
                    val= "Operação validada anterirmente, não é possível vincular novamente" 
        return val
#----------------------------------------------------------------------------------------------------------    
@turma_blue.route('/vincular_disc/',methods=['POST'])
def  vincular_disc():
     if request.method=="POST":
        prof_id=request.form['id_prof']
        val=""
        for id in receber_disc():
            if contar_vinculos_disciplina(prof_id) < Professor.get_by_id(prof_id).n_disciplina:
                vincular_pd(prof_id,int(id))
                val= f"Disciplina {Disciplina.get_by_id(id).nome} vinculada ao professor {Professor.get_by_id(prof_id).nome} com sucesso"
            elif contar_vinculos_disciplina(prof_id) >= Professor.get_by_id(prof_id).n_disciplina:
                val ="O professor já atingiu o número máximo de disciplinas vinculadas"   
            elif contar_vinculos_disciplina(prof_id) ==-1:
                val ="O professor já  esta vinculado a essa disciplina"
        return val        
#---------------------------------------------------------------------------------------------------------
    
@turma_blue.route('/editar_turma/<int:id>', methods=['PUT'])    
def editar_turma(id):
    if request.method == 'PUT':
        nome = request.form['nome']
        capacidade = request.form['capacidade']
        editar_turma(id, nome, capacidade)
        return  render_template('/turma/listar_turma.html',turmas=pesquisar_turma())
    return "Falha ao editar turma"
#---------------------------------------------------------------------------------------------------------
@turma_blue.route('/pesq_prof',methods=['POST'])
def pesq_prof():
    if request.method == 'POST':
        nome=request.form['prof']
        return render_template('turma/listar_prof.html',professores=pesquisar_professor_per(nome))
#---------------------------------------------------------------------------------------------------------
#Rota para editar o numero de disciplinas do professor
@turma_blue.route('/editar_n_disciplinas/<int:id>', methods=['GET'])
def editar_n_disciplinas(id):
    professor = Professor.get_by_id(id)
    return render_template('turma/editar_disciplina.html',professor=professor)
#---------------------------------------------------------------------------------------------------------
@turma_blue.route('/salvar_n_disciplinas/<int:id>', methods=['POST'])
def salvar_n_disciplinas(id):
    professor = Professor.get_by_id(id)
    professor.n_disciplina = request.form['n_disciplinas']
    professor.save()
    return f'<td>{professor.n_disciplina}</td>'

#---------------------------------------------------------------------------
@turma_blue.route('/turma_pdt/<int:id>', methods=['POST'])
def turma_pdt(id):
        turmas=pesquisar_PDT(id)
        return f'<td>{turmas}</td>'

#---------------------------------------------------------------------------
@turma_blue.route('/pesquisar_turma_id/<int:id>',methods=['POST', 'POST'])
def pesquisar_turma_id(id):
        turma_id=pesquisar_turma_id_(id)
        if turma_id:
            return render_template('professor/escolha_turma.html',turma_id=turma_id)
        else:
            return "Turma não encontrada", 404
#---------------------------------------------------------------------------
@turma_blue.route('/routa/routa_turma/pesquisar_disciplina_id/<int:turma_id>/<int:prof_id>')
def pesquisar_disciplina_id(turma_id, prof_id):
        print(f"ID Professor:{prof_id}, ID Turma: {turma_id}")
        disciplina=pesquisar_disciplina_id_(prof_id,turma_id)
        resultado = []
        for disc in disciplina:
            resultado.append({
                "id": disc.id,
                "nome": disc.nome
            })
        return jsonify(resultado)     
        

