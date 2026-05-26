# todas as funções relacionadas com a escola_bd
import email
import os
from urllib import response
from utils.security import hash_senha, validar_senha
from werkzeug.utils import secure_filename
from turtle import width
from werkzeug.security import generate_password_hash, check_password_hash


from model.bd_model import *
from flask import session,make_response, session
from peewee import JOIN,fn
import uuid
import smtplib
from email.message import EmailMessage
import random
import string
from datetime import date
hoje = date.today()


# --------------------Validações de Imagens--------------------------------------------------------------
UPLOAD_FOLDER = "static/img"
EXTENSOES_PERMITIDAS = ("png","jpg","jpeg","gif","heic","docx","pdf","mp4","mkv","avi","mp3","m4a","wav","flac")
#---------------------------------------------------------------------------------------------------------
def arquivo_permitido(nome):
    if "." not in nome:
        return False
    extensao = nome.rsplit(".", 1)[1].lower()
    return extensao in (EXTENSOES_PERMITIDAS)
#______________________________________________________________________________________
def salvar_imagem(arquivo,destino):
   
    pasta_destino = os.path.join(UPLOAD_FOLDER, destino)
    codigo = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=8))
    if not arquivo or arquivo.filename == "":
        return None
    if not arquivo_permitido(arquivo.filename):
        return None
    os.makedirs(pasta_destino, exist_ok=True)  
    nome_seguro = secure_filename(f"{codigo}_{arquivo.filename}")
    caminho = os.path.join(pasta_destino,nome_seguro)
    arquivo.save(caminho)
    return nome_seguro
#--------------------Salvar Conteúdo----------------------------------------------------------------------
def salvar_conteudo(conteudo_1,conteudo_2,destino_1,destino_2):
    codigo = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=8))
    if destino_2 !="":
        pasta_destino_1 = os.path.join(UPLOAD_FOLDER,destino_1)
        pasta_destino_2 = os.path.join(UPLOAD_FOLDER,destino_2)
        for img in conteudo_1:
            if not img or img.filename == "":
                print("Imagem vazia")
                continue  
            if not arquivo_permitido(img.filename):
                print("Formato inválido")
                continue  
            os.makedirs(pasta_destino_1, exist_ok=True)  
            nome_seguro1 = secure_filename(f"{codigo}_{img.filename}")
            caminho1 = os.path.join(pasta_destino_1,nome_seguro1)
            img.save(caminho1)
        for img1 in conteudo_2:
            if not img1 or img1.filename == "":
                print("Imagem vazia")
                continue  
            if not arquivo_permitido(img1.filename):
                print("Formato inválido")
                continue  
            os.makedirs(pasta_destino_2, exist_ok=True)
            nome_seguro2 = secure_filename(f"{codigo}_{img1.filename}")
            caminho2 = os.path.join(pasta_destino_2,nome_seguro2)
            img1.save(caminho2)
        return codigo
    elif destino_2=="":
        pasta_destino_1 = os.path.join(UPLOAD_FOLDER,destino_1)
        for img in conteudo_1:
            if not img or img.filename == "":
                print("Imagem vazia")
                continue
            if not arquivo_permitido(img.filename):
                print("Formato inválido")
                continue
            os.makedirs(pasta_destino_1, exist_ok=True)  
            nome_seguro = secure_filename(f"{codigo}_{img.filename}")
            caminho = os.path.join(pasta_destino_1,nome_seguro)
            img.save(caminho)
            print(codigo)
        return codigo

# -----------------------Envio de E-mail---------------------------------------


def gerar_senha(tamanho=8):
    # Apenas letras (maiúsculas e minúsculas) + dígitos
    caracteres = string.ascii_letters + string.digits
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha



def enviar_email(nome, destinatario, senha):
    # Corpo em texto simples (fallback)
    mensagem_texto = (
        f"Olá {nome},\n\n"
        f"Seja muito bem-vindo ao SIGMA – Sistema de Gestão de Materiais Académicos!\n"
        f"Estamos felizes em tê-lo conosco.\n\n"
        f"SUA SENHA DE ACESSO É: {senha}\n\n"
        f"Por favor, altere-a após o primeiro login para maior segurança.\n\n"
        f"Atenciosamente,\nEquipe SIGMA"
    )

    # Corpo em HTML (apenas a senha destacada)
    mensagem_html = f"""
    <html>
      <body>
        <p>Olá {nome},</p>
        <p>Seja muito bem-vindo ao <b>SIGMA – Sistema de Gestão de Materiais Académicos</b>!<br>
        Estamos felizes em tê-lo conosco.</p>
        <p>
          🔑 SUA SENHA DE ACESSO É:
          <span style="font-size:22px; color:#d32f2f;"><b>{senha}</b></span>
        </p>
        <p>Por favor, altere-a após o primeiro login para maior segurança.</p>
        <p>Atenciosamente,<br>Equipe SIGMA</p>
      </body>
    </html>
    """

    msg = EmailMessage()
    msg["Subject"] = "Seja bem-vindo ao nosso sistema Acadêmico!"
    msg["From"] = "sgmdacademicos@gmail.com"
    msg["To"] = destinatario
    msg.set_content(mensagem_texto)
    msg.add_alternative(mensagem_html, subtype="html")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            # ⚠️ Usa senha de app do Gmail
            server.login("sgmdacademicos@gmail.com", "yvsg ljkb heap rfvb")
            server.send_message(msg)
        print("Email enviado com sucesso!")
        return senha   # só retorna se o envio deu certo
    except Exception as e:
        # Levanta exceção para impedir cadastro
        raise RuntimeError(f"Erro ao enviar email: {e}")


# --------------------------Fechar BD------------------------------------------
def close_db():
    if not db.is_closed():
        db.close()
# ------------------------------Reload------------------------------------------------
def reload():
    response = make_response("")
    response.headers["HX-Refresh"] = "true"
    return response

#---------------------------------------------------------------------------------------------
def cadastrar_professor(np, nome, email, data_nasc, genero, imagem, n_disciplinas):
    Professor.create(np=np, nome=nome, email=email,data_nasc=data_nasc, genero=genero, foto=imagem, n_disciplina=n_disciplinas)
    close_db()
    return "Professor criado com sucesso"

def editar_professor_(id, np, nome, email, data_nasc, genero):
    with bd.atomic():
        professor = Professor.get_by_id(id)
        professor.np = np
        professor.nome = nome
        professor.data_nasc = data_nasc
        professor.email = email
        professor.genero = genero
        professor.save()
        close_db()
        return "Professor editado com sucesso"
#---------------------------------------------------------------------------------------------------------
def apagar_professor(professor_id):
    professor = Professor.get_by_id(professor_id)
    professor.delete_instance()
    close_db()
    return "Professor apagado com sucesso"
#---------------------------------------------------------------------------------------------------------
def pesquisar_professor():
    professor = Professor.select().limit(10)
    close_db()
    return professor
#--------------------------------------------------------------------------------
def pesquisar_professor_usuario():
    usuario = Usuario.select(Usuario.email)
    professor = Professor.select().where(Professor.email.not_in(usuario))   
    close_db()
    return professor
#-----------------------------------------------------------------------------------------
def pesquisar_professor_per(nome):
    if nome is not None:
        professor = Professor.select().where(Professor.nome.contains(nome))
        return professor
    else:
        return Professor.select().limit(10)
    close_db()  
# ----------------------------Aluno-------------------------------------------------
def cadastrar_aluno(mat, nome, email, data_nasc, genero,foto,curso,classe):
    Aluno.create(mat=mat, nome=nome, email=email,data_nasc=data_nasc, genero=genero,foto=foto,curso=curso,classe=classe)
    close_db()
    return "Aluno criado com sucesso"
#---------------------------------------------------------------------------------------------------------

def editar_aluno_(id, mat, nome, email, data_nasc, genero):
    aluno = Aluno.get_by_id(id)
    aluno.mat = mat
    aluno.nome = nome
    aluno.data_nasc = data_nasc
    aluno.email = email
    aluno.genero = genero
    aluno.save()
    close_db()
    return "Aluno editado com sucesso"
#--------------------------------------------------------------------------------------------------------
def apagar_aluno(aluno_id):
    aluno = Aluno.get_by_id(aluno_id)
    aluno.delete_instance()
    close_db()
    return "Aluno apagado com sucesso"
#---------------------------------------------------------------------------------------------------------
def pesquisar_aluno():
    aluno = Aluno.select().limit(10)
    close_db()
    return aluno
#---------------------------------------------------------------------------------------------------------
def pesquisar_aluno_usuario():
    usuario = Usuario.select(Usuario.email)
    aluno = Aluno.select().where(Aluno.email.not_in(usuario))   
    close_db()
    return aluno
#---------------------------------------------------------------------------------------------------------
def pesquisar_aluno_per(nome):
    aluno = Aluno.select().where(Aluno.nome.contains(nome))
    close_db()
    return aluno
# ----------------------------Usuário-------------------------------------------------
def cadastrar_usuario(nome, email, nivel, estado, ex_aluno, ex_professor):
    senha = gerar_senha()
    senha_hash = generate_password_hash(senha)

    try:
        # envia primeiro o e-mail
        enviar_email(nome, email, senha)

        # cria e retorna o objeto
        usuario = Usuario.create(
            nome=nome,
            senha=senha_hash,
            email=email,
            nivel=nivel,
            estado=estado,
            aluno_id=ex_aluno,
            professor_id=ex_professor
        )
        close_db()
        return usuario   # <-- retorna o objeto, não string
    except Exception as e:
        close_db()
        raise  # deixa o erro subir para ser tratado na rota

#---------------------------------------------------------------------------------------------------------

def editar_usuario_(id, nome, senha, email, nivel, estado):
    usuario = Usuario.get_by_id(id)
    usuario.nome = nome
    usuario.senha = hash_senha(senha)  # aplica hash
    usuario.email = email
    usuario.nivel = nivel
    usuario.estado = estado
    usuario.ultima_alteracao_senha = datetime.now()  # registra a alteração
    close_db()
    usuario.save()
   
    return usuario
#---------------------------------------------------------------------------------------------------------
def alterar_estado_(id, estado):
    usuario = Usuario.get_by_id(id)
    usuario.estado = estado
    usuario.save()
    close_db()
    return usuario
#---------------------------------------------------------------------------------------------------------
def apagar_usuario(usuario_id):
    usuario = Usuario.get_by_id(usuario_id)
    usuario.delete_instance()
    close_db()
#---------------------------------------------------------------------------------------------------------
def pesquisar_usuario():
    usuario = (Usuario
        .select(Usuario,Aluno.foto,Professor.foto)
        .join(Aluno, JOIN.LEFT_OUTER, on=(Usuario.aluno_id == Aluno.id))
        .switch(Usuario)
        .join(Professor, JOIN.LEFT_OUTER, on=(Usuario.professor_id == Professor.id))
    )
    close_db()
    return usuario
#---------------------------------------------------------------------------------------------------------
def pesquisar_usuario_per(nome):
    usuario = (Usuario
        .select( Usuario, Aluno.foto,Professor.foto)
        .join(Aluno, JOIN.LEFT_OUTER, on=(Usuario.aluno_id == Aluno.id))
        .switch(Usuario)
        .join(Professor, JOIN.LEFT_OUTER, on=(Usuario.professor_id == Professor.id))
    ).where(Usuario.nome.contains(nome))
    close_db()
    return usuario
#-------------------------------------------------valida_usuario--------------------------------------------------------------------


def valida_usuario(senha_digitada, email):
    usuario = (Usuario
        .select(Usuario, Aluno.foto, Aluno.curso, Aluno.classe, Professor.foto)
        .join(Aluno, JOIN.LEFT_OUTER, on=(Usuario.aluno_id == Aluno.id) or (Usuario.aluno_id == None))
        .switch(Usuario)
        .join(Professor, JOIN.LEFT_OUTER, on=(Usuario.professor_id == Professor.id) or (Usuario.professor_id == None))
        .where((Usuario.email == email) & (Usuario.estado == True))
        .first()
    )

    # Se não encontrou usuário, retorna None
    if not usuario:
        close_db()
        return None

    # Se encontrou, valida a senha com hash
    if check_password_hash(usuario.senha, senha_digitada):
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome 
        session['professor_id'] = usuario.professor_id     
        session['aluno_id'] = usuario.aluno_id    
        close_db()
        return usuario
    else:
        close_db()
        return None
#------------------------------trocar_senha--------------------------------------------------------------------

def trocar_senha(usuario_id, senha_atual, nova_senha, confirmar_senha):
    usuario = Usuario.get_or_none(Usuario.id == usuario_id)
    if not usuario:
        return {"status": "erro", "mensagem": "Usuário não encontrado"}

    # verifica senha atual
    if not check_password_hash(usuario.senha, senha_atual):
        return {"status": "erro", "mensagem": "Senha atual incorreta"}

    # valida nova senha
    if nova_senha != confirmar_senha:
        return {"status": "erro", "mensagem": "As senhas não coincidem"}
    if len(nova_senha) < 8:
        return {"status": "erro", "mensagem": "Senha deve ter pelo menos 8 caracteres"}

    # aplica hash e salva
    usuario.senha = hash_senha(nova_senha)
    usuario.save()

    return {"status": "sucesso", "mensagem": "Senha alterada com sucesso"}

# ------------------------------criar_disciplina------------------------------------------------

def cadastrar_disciplina(nome, sigla):
    if nome is None or sigla is None:
        return "Nome e sigla são obrigatórios"
    Disciplina.create(nome=nome,sigla=sigla)
    close_db()
    return "Disciplina criada com sucesso"

def editar_disciplina_(id, nome, sigla):
    disciplina = Disciplina.get_by_id(id)
    disciplina.nome = nome
    disciplina.sigla = sigla
    disciplina.save()
    close_db()
    return "Disciplina editada com sucesso"
#---------------------------------------------------------------------------------------------------------
def apagar_disciplina(disciplina_id):
    disciplina = Disciplina.get_by_id(disciplina_id)
    disciplina.delete_instance()
    close_db()
    return "Disciplina apagada com sucesso"
#---------------------------------------------------------------------------------------------------------
def pesquisar_disciplina():
    disciplina = Disciplina.select().limit(10)
    return disciplina
#---------------------------------------------------------------------------------------------------------
def pesquisar_disciplina_per(nome):
    disciplina = Disciplina.select().where(Disciplina.nome.contains(nome))
    close_db()
    return disciplina
# ------------------------------Turma------------------------------------------------
def cadastrar_turma(nome,capacidade):
    if nome is None or capacidade is None:
        return "Nome e capacidade são obrigatórios"
    Turma.create(nome=nome,capacidade=capacidade)
    close_db()
    return "Turma criada com sucesso"
#---------------------------------------------------------------------------------------------------------
def vincular(id_turma,id_prof,id_disc):
    PDT.create(turma_id=id_turma,professor_id=id_prof,disciplina_id=id_disc)
    close_db()
    return "Turma criada com sucesso"
#---------------------------------------------------------------------------------------------------------
def vincular_pd(id_prof,id_disc):
    PD.create(professor_id=id_prof,disciplina_id=id_disc)
    close_db()   
#---------------------------------------------------------------------------------------------------------
#verificar se a disciplina está mesmo vinculada a um professor
def contar_vinculos_professor(id_prof,id_disc):
    vinculos = (PD.select(fn.COUNT(PD.disciplina_id)).where(PD.professor_id == id_prof & PD.disciplina_id == id_disc).scalar())
    try:
        return vinculos 
    except PD.DoesNotExist:
        return -1
#---------------------------------------------------------------------------------------------------------
#verificar quantas vezes o id_professor está vinculado a uma disciplina- PD
def contar_vinculos_disciplina(id_prof):
    vinculos = (PD.select(fn.COUNT(PD.professor_id)).where(PD.professor_id == id_prof).scalar())
    try:
        return vinculos 
    except PD.DoesNotExist:
        return -1
#---------------------------------------------------------------------------------------------------------
#verificar se uma determinada disciplina está vinculada a um professor na turma- TPD
def verificar_vinculo_disciplina_turma(id_disc,id_turma):
    vinculos = (PDT.select().where((PDT.disciplina_id == id_disc) & (PDT.turma_id == id_turma)))
    if vinculos:
        return vinculos 
    else:
        return None
#---------------------------------------------------------------------------------------------------------
#verificar quantas vezes a turma está vinculada a um professor
def contar_vinculos_turma(id_turma):
    vinculos = PDT.select().where(PDT.turma_id == id_turma).count()
    if vinculos:
        return vinculos
    else:
        return 0
#---------------------------------------------------------------------------------------------------------
#verificar se o professor já está vinculado a uma turma
def verificar_vinculo_professor_turma(id_prof, id_turma, id_disc):   
    vinculo = PDT.select().where((PDT.professor_id == id_prof) & (PDT.turma_id == id_turma) &  (PDT.disciplina_id == id_disc)).first()
    if vinculo:
        return vinculo
    else:
        return None
#---------------------------------------------------------------------------------------------------------
def editar_turma(id, nome, capacidade):
    turma = Turma.get_by_id(id)
    turma.nome = nome
    turma.capacidade = capacidade
    turma.save()
    close_db()
    return "Turma editada com sucesso"
#---------------------------------------------------------------------------------------------------------
def apagar_turma(turma_id):
    turma = Turma.get_by_id(turma_id)
    turma.delete_instance()
    close_db()
    return "Turma apagada com sucesso"
#---------------------------------------------------------------------------------------------------------
def pesquisar_turma():
    turma = Turma.select().limit(10)
    close_db()
    return turma
#---------------------------------------------------------------------------------------------------------
def pesquisar_turma_id_(id_prof):
    turma = (Turma  
        .select(Turma, PDT.disciplina_id)
        .join(PDT, on=(Turma.id == PDT.turma_id) & (PDT.professor_id == id_prof))
    )
    close_db()
    return turma
#---------------------------------------------------------------------------------------------------------
def pesquisar_disciplina_professor(id_prof):
    disciplina = (Disciplina  
        .select(Disciplina, PD.disciplina_id)
        .join(PD, on=(Disciplina.id == PD.disciplina_id) & (PD.professor_id == id_prof))
    )
    close_db()
    return disciplina
#---------------------------------------------------------------------------------------------------------
def pesquisar_disciplina_id_(id_prof, id_turma):
    disciplina = (Disciplina  
        .select(Disciplina, PDT)
        .join(PDT, on=(Disciplina.id == PDT.disciplina_id) & (PDT.professor_id == id_prof)& (PDT.turma_id == id_turma)) 
    )
    close_db()
    return disciplina
#---------------------------------------------------------------------------------------------------------
def pesquisar_turma_per(nome):
    turma = Turma.select().where(Turma.nome.contains(nome))
    close_db()
    return turma
#---------------------------------------------------------------------------------------------------------
def pesquisar_PDT(id):
    query = (Turma.select(Turma,PDT)
    .join(PDT).where((Turma.id == PDT.turma_id) and (PDT.professor_id==id)))
    return query
#---------------------------------------------------------------------------------------------------------
# -----------------------------------SALA-----------------------------------------------------------------
def criar_sala(professor_id, nome, nivel, observacao, foto):
    try:
        # Busca o objeto Professor pelo ID
        professor = Professor.get_by_id(int(professor_id))

        # Verifica se já existe sala para esse professor
        sala_existente = Sala.get_or_none(Sala.professor == professor)
        if sala_existente:
            return "Professor já possui uma sala cadastrada"

        # Cria sala vinculada ao professor
        Sala.create(
            professor=professor,
            nome=nome,
            nivel=nivel,
            observacao=observacao,
            foto=foto,
            data=date.today()
        )
        return "Sala criada com sucesso"
    except Exception as e:
        print("ERRO criar_sala:", e)
        return "Falha ao criar sala"

#---------------------------------------------------------------------------------------------------------

def editar_sala_(id, nome,nivel,obs):
    sala = Sala.get_by_id(id)
    sala.nome = nome
    sala.nivel = nivel
    sala.observacao = obs
    sala.save()
    close_db()
    return "Aluno editado com sucesso"
#--------------------------------------------------------------------------------------------------------
def apagar_sala(sala_id):
    sala = Sala.get_by_id(sala_id)
    sala.delete_instance()
    close_db()
    return "Aluno apagado com sucesso"
#---------------------------------------------------------------------------------------------------------
def pesquisar_sala():
    sala = (Sala
        .select(Sala, Professor)
        .join(Professor, on=(Sala.professor_id == Professor.id)))

    return sala
#---------------------------------------------------------------------------------------------------------
def pesquisar_sala_per(nome):
    sala = (Sala
        .select(Sala, Professor)
        .join(Professor, on=(Sala.professor_id == Professor.id)).where(Sala.nome.contains(nome)))
    close_db()
    return sala

#------------------------------------------------------------------------------------------------------------
def pesquisar_sala_prof(id_prof):
    sala = (Sala
        .select(Sala, Professor)
        .join(Professor, on=(Sala.professor_id == Professor.id))
        .where(Sala.professor_id == id_prof)
    )
    close_db()
    return sala

#--------------------------------------------------------------------------------------------------------
def criar_conteudo(titulo, nivel, formato_1, formato_2, codigo, obs, id_prof):
    try:
        # ✅ Validação básica
        if not titulo or len(titulo) > 255:
            raise ValueError("Título inválido")
        if nivel not in ["basico", "medio", "avancado"]:
            raise ValueError("Nível inválido")
        if not isinstance(id_prof, int):
            raise ValueError("ID do professor inválido")

        Conteudo.create(
            titulo=titulo.strip(),
            nivel=nivel,
            data=hoje,
            formato_1=formato_1.strip() if formato_1 else None,
            formato_2=formato_2.strip() if formato_2 else None,
            codigo=codigo.strip() if codigo else None,
            descricao=obs.strip() if obs else None,
            ex_professor_id=id_prof
        )
        return 1
    except Exception as e:
        # Logar tentativa suspeita
        import logging
        logging.warning(f"Erro ao criar conteúdo: {e}")
        return 0
    finally:
        close_db()

#-------------------------------------------------------------------------------------------------------------
def pesquisar_conteudo(professor_id=None, nivel=None, titulo=None, data=None):
    query = (Conteudo
        .select(
            Conteudo,
            Professor.nome, Professor.id,
            SAC.aluno_id, SAC.estado,
            Turma.nome, Turma.id
        )
        .join(Professor, JOIN.LEFT_OUTER, on=(Conteudo.ex_professor_id == Professor.id))
        .switch(Conteudo)
        .join(SAC, JOIN.LEFT_OUTER, on=(Conteudo.id == SAC.conteudo_id))
        .switch(SAC)
        .join(Turma, JOIN.LEFT_OUTER, on=(SAC.aluno_id == Turma.id))
    )

    # 🔎 Filtros opcionais com validação
    if professor_id and isinstance(professor_id, int):
        query = query.where(Conteudo.ex_professor_id == professor_id)
    if nivel and nivel in ["basico", "medio", "avancado"]:
        query = query.where(Conteudo.nivel == nivel)
    if titulo and len(titulo) <= 255:
        query = query.where(Conteudo.titulo.contains(titulo.strip()))
    if data:
        query = query.where(Conteudo.data == data)

    result = list(query)  # ✅ Executa antes de fechar
    close_db()
    return result

#---------------------------------------------------------------------------------------------------------
def pesquisar_conteudo_per(nome=None, professor_id=None, nivel=None, data=None):
    query = (Conteudo
        .select(Conteudo, Professor.nome, SAC.aluno_id, Turma.nome)
        .join(Professor, JOIN.LEFT_OUTER, on=(Conteudo.ex_professor_id == Professor.id))
        .switch(Conteudo)
        .join(SAC, JOIN.LEFT_OUTER, on=(Conteudo.id == SAC.conteudo_id))
        .switch(SAC)
        .join(Turma, JOIN.LEFT_OUTER, on=(SAC.aluno_id == Turma.id))
    )

    # 🔎 Filtros opcionais com validação
    if nome and len(nome) <= 255:
        query = query.where(Conteudo.titulo.contains(nome.strip()))
    if professor_id and isinstance(professor_id, int):
        query = query.where(Conteudo.ex_professor_id == professor_id)
    if nivel and nivel in ["basico", "medio", "avancado"]:
        query = query.where(Conteudo.nivel == nivel)
    if data:
        query = query.where(Conteudo.data == data)

    result = list(query)  # ✅ Executa antes de fechar
    close_db()
    return result

#---------------------------------------------------------------------------------------------------------
def apagar_conteudo(conteudo_id):
    try:
        if not isinstance(conteudo_id, int):
            raise ValueError("ID inválido")

        conteudo = Conteudo.get_by_id(conteudo_id)
        with db.atomic():
            conteudo.delete_instance()
        return "Conteúdo apagado com sucesso"
    except Exception as e:
        import logging
        logging.warning(f"Tentativa suspeita ao apagar conteúdo: {e}")
        return "Erro ao apagar conteúdo"
    finally:
        close_db()




#_---------------------------------------------------------------------------------------------
def pesquisar_conteudo_prof(id_prof):
    conteudo = (Conteudo
        .select(Conteudo,Professor.nome,SAC.aluno_id,Turma.nome)
        .join(Professor, JOIN.LEFT_OUTER, on=(Conteudo.id == Professor.id))
        .switch(Conteudo)
        .join(SAC, JOIN.LEFT_OUTER, on=(Conteudo.id == SAC.aluno_id))
        .switch(SAC)
        .join(Turma, JOIN.LEFT_OUTER, on=(SAC.aluno_id == Turma.aluno_id))
    ).where((Conteudo.ex_professor == id_prof)).limit(10)
    close_db()
    return conteudo