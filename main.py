from flask import Flask,render_template
import os
import webbrowser
from threading import Timer


from routa.routa_usuario import usuario_blue
from routa.routa_aluno import aluno_blue
from routa.routa_professor import professor_blue
from routa.routa_turma import turma_blue
from routa.routa_disciplina import disciplina_blue
from routa.routa_pdt import pdt_blue
from routa.routa_sala import sala_blue

from BD.escola_bd import db
from model.bd_model import *

app=Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(usuario_blue)
app.register_blueprint(aluno_blue)
app.register_blueprint(professor_blue)
app.register_blueprint(turma_blue)
app.register_blueprint(disciplina_blue)
app.register_blueprint(pdt_blue)
app.register_blueprint(sala_blue)

@app.route('/')
def index():
    return render_template('index.html')



with db: 
     db.create_tables([Usuario, Aluno, Professor, Disciplina,Turma, PDT, PD, Sala, Conteudo,SAC])


def open_browser():
    webbrowser.open_new("http://127.0.0.1:8080/")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, port=8080) 