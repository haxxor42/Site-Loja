from flask import Blueprint, render_template, request, redirect, url_for, session

main_bp = Blueprint('main', __name__, url_prefix='/', template_folder='templates')

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/index")
def index():
    return home()
    
@main_bp.route("/login")
def login():
    return render_template("login.html")

@main_bp.route("/cadastro")
def cadastro():
    return redirect(url_for('user.cadastro_usuario'))

@main_bp.route("/produtos")
def produtos():
    return redirect(url_for('loja.index'))

@main_bp.route("/cadastrar-produto")
def cadastrar_produto_redirect():
    return redirect(url_for('loja.cadastrar_produto'))

@main_bp.route("/contatos")
def contatos():
    return render_template("contatos.html")

@main_bp.route("/config")
def config():
    return render_template("config.html")
