from BD.escola_bd import db
from peewee import *
from datetime import datetime


class BaseModel(Model):
 class Meta:
        database = db
        
class Turma(BaseModel):
    nome = CharField(max_length=100,unique=True)
    capacidade = IntegerField(null=True)
    
    
class Aluno(BaseModel):
    mat=IntegerField(unique=True)
    nome = CharField(max_length=100)
    email = CharField(max_length=30) 
    data_nasc=DateField(formats='%d/%m/%Y')
    genero = CharField(max_length=10)
    foto = CharField(null=True)
    ex_turma=ForeignKeyField(Turma, backref='alunos',null=True)
    curso = CharField(max_length=100,null=True)
    classe = CharField(max_length=100,null=True)

class Professor(BaseModel):
    np = IntegerField(unique=True)
    nome = CharField(max_length=100)
    email = CharField(max_length=30,unique=True)
    data_nasc=DateField(formats='%d/%m/%Y')
    genero = CharField(max_length=10)
    foto = CharField(null=True)
    n_disciplina=IntegerField(null=True)

class Disciplina(BaseModel):
    nome = CharField(max_length=50, unique=True)
    sigla = CharField(max_length=10)
    professor = ForeignKeyField(Professor, backref='disciplinas', null=True) 

class PDT(BaseModel):
    turma_id=ForeignKeyField(Turma, backref='pdt', null=True)
    professor_id=ForeignKeyField(Professor, backref='pdt', null=True)
    disciplina_id=ForeignKeyField(Disciplina, backref='pdt', null=True)
    estado =IntegerField(null=True)
    class Meta:
        primary_key  = CompositeKey('turma_id', 'professor_id', 'disciplina_id')

class PD(BaseModel):
    professor_id = ForeignKeyField(Professor, backref='professor_disciplinas')
    disciplina_id = ForeignKeyField(Disciplina, backref='disciplina_professores') 
    class Meta:
        primary_key  = CompositeKey('professor_id', 'disciplina_id')

class Usuario(BaseModel):
    nome = CharField(max_length=100)
    senha = CharField(max_length=100)
    email = CharField(max_length=30, unique=True)
    nivel = CharField(max_length=15)
    estado = BooleanField(default=True)
    aluno=ForeignKeyField(Aluno, backref='usuario',null=True,on_delete='CASCADE',on_update='CASCADE')
    professor=ForeignKeyField(Professor, backref='usuario',null=True,on_delete='CASCADE',on_update='CASCADE')
    #ultima_alteracao_senha = DateTimeField(default=datetime.now)  # novo campo

class Conteudo(BaseModel):
    titulo = CharField(max_length=100)
    nivel = CharField(max_length=100) 
    data=DateField(formats='%d/%m/%Y')
    formato_1 = CharField(null=True)
    formato_2 = CharField(null=True)
    codigo = CharField(null=True)
    descricao = CharField(max_length=100)
    ex_professor_id=ForeignKeyField(Professor, backref='conteudo',null=False)

class Sala(BaseModel):
    professor = ForeignKeyField(Professor, backref='sala', primary_key=True)
    nome = CharField(max_length=100)
    nivel = CharField(max_length=30)
    data = DateField()   # precisa dos parênteses
    observacao = CharField(max_length=100)
    foto = CharField(null=True)


class SAC(BaseModel):
    sala_id = ForeignKeyField(Sala, backref='sac')
    aluno_id = ForeignKeyField(Aluno, backref='sac') 
    conteudo_id = ForeignKeyField(Conteudo, backref='sac')
    estado = BooleanField(default=True)
    class Meta:
        primary_key  = CompositeKey('sala_id','aluno_id')