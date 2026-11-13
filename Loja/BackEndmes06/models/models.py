from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()


class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    telefone = db.Column(db.String(20), unique=False)
    senha = db.Column(db.String(100), nullable=True)

    @property
    def nome(self):
        return self.username

    @nome.setter
    def nome(self, value):
        self.username = value

    def __init__(self, *args, **kwargs):
        if 'nome' in kwargs and 'username' not in kwargs:
            kwargs['username'] = kwargs.pop('nome')
        super().__init__(*args, **kwargs)


class Produto(db.Model):
    __tablename__ = 'produtos'
    id_p = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=True)
    valor = db.Column(db.Float, nullable=False)
    qtd_produto = db.Column(db.Integer)
    descricao_produto = db.Column(db.String(300), nullable=False)

