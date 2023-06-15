from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
app.secret_key = 'Cadastros'
app.config['SQLALCHEMY_DATABASE_URI'] = \
        '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
            SGBD = 'mysql+mysqlconnector',
            usuario = 'root',
            senha = '123',
            servidor = 'localhost',
            database = 'rede_social')

db = SQLAlchemy(app=app)

class Base(db.Model):
    __abstract__ = True

class Instituicao(db.Model):
    __tablename__ = 'instituicao'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    ic_ativo = db.Column(db.Integer, nullable=False)

class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    instituicao_id = (db.Integer)
    ic_ativo = db.Column(db.Integer, nullable=False)

class CustomView(ModelView):
    create_modal = True
    edit_modal = True

class InstView(ModelView):
    def on_model_change(self, form, model, is_created):
        # Verifica se a regra de validação é atendida
        if model.nome == "admin":
            raise ValueError("Nome 'admin' não é permitido.")


admin = Admin(app, name='Cadastros', template_mode='bootstrap3')
admin.add_view(InstView(Instituicao, db.session, category="Cadastro"))
admin.add_view(CustomView(Curso, db.session, category="Cadastro"))
# Add administrative views here

app.run(debug=True)