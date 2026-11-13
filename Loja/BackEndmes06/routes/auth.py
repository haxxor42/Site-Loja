from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from services.user_service import authenticate_user, get_user_by_email
from .auth_decorator import login_required

auth_bp = Blueprint("auth", __name__, url_prefix = "/auth", template_folder = 'templates')

@auth_bp.route('/submit-login', methods=['GET', 'POST'])
def submit_login():
    if request.method == 'POST':
        login_val = request.form.get('login') or request.form.get('email')
        senha = request.form.get('senha')

        if not login_val or not senha:
            flash("Por favor, preencha todos os campos.", "danger")
            return redirect(url_for('auth.login'))
     
        user = authenticate_user(login_val, senha)

        if not user:
            flash('Email/usuário ou senha incorretos.', "danger")
            return redirect(url_for('auth.login'))

        session.permanent = True
        session['user_id'] = user.id
        session['user_nome'] = user.username or user.nome

        return redirect(url_for('user.meusdados'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

