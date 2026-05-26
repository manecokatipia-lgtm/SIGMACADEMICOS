from flask import render_template, Blueprint, request
from model.bd_model import *
from Controller.escola_bd import *
material_blue= Blueprint('material', __name__, template_folder='templates', url_prefix='/material')


@material_blue.route('/cadastro', methods=['GET ', 'POST'])
def cadastrar_materias():
    return render_template('/materias/cadastrar_materias.html')

@material_blue.route('/editar_materiais', methods=['GETS', 'POST'])
def editar_materias():
    return render_template('/materias/editar_materias.html')

@material_blue.route('/apagar', methods=['GETS', 'POST'])
def apagar_materias():
    return render_template('/materias/apagar_materias.html')

#_________________________________________Materiais Didaticos___________________________
@material_blue.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        descrisao = request.form['descrisao']
        data_upload = request.form['data_upload']
        foto = salvar_imagem(request.files.get('imagem'))
        cadastrar_material(nome, tipo, descrisao, data_upload, foto)
        return  render_template('/material/listar_material.html', material=pesquisar_material())     

@material_blue.route('/listar_material', methods=['GET'])
def listar_material():
    return  render_template('/material/listar_material.html', Material=pesquisar_material())


@material_blue.route('/excluir_material/<int:id>', methods=['DELETE'])
def excluir_material(id):
    apagar_material(id)
    return  render_template('/material/listar_material.html', material=pesquisar_material())

@material_blue.route('/form_material_editar/<int:id>', methods=['GET'])
def form_material_editar(id):
    materiais = Material.get_by_id(id)
    return render_template('/material/editar_material.html', material=materiais)

@material_blue.route('/editar_material/<int:id>', methods=['PUT'])    
def editar_material(id):
    if request.method == 'PUT':
        nome = request.form['nome']
        tipo = request.form['tipo']
        descrisao = request.form['descrisao']
        data_upload = request.form['data_upload']
        foto = salvar_imagem(request.files.get('imagem'))
        editar_material_(id, nome, tipo, descrisao, data_upload, foto)
        return  render_template('/material/listar_material.html', material=pesquisar_material())
    return "Falha ao editar Material"

@material_blue.route('/form_material',methods=['GET','POST'])
def form_material():
    return  render_template('/material/cadastrar_material.html')