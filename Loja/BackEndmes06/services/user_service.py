from flask import flash
from models.models import User, db

def get_user() -> list[User]:
    return db.session.query(User).limit(25).all()

def get_user_by_id(user_id: int) -> User:
    return db.session.query(User).filter_by(id=user_id).first()

def get_user_by_email(email: str) -> User:
    if not email:
        return None
    return db.session.query(User).filter_by(email=email.strip()).first()

def get_user_by_login(login_val: str) -> User:
    if not login_val:
        return None
    login_clean = login_val.strip()
    user = db.session.query(User).filter_by(email=login_clean).first()
    if not user:
        user = db.session.query(User).filter_by(username=login_clean).first()
    return user

def create_user(nome: str, email: str,
                telefone: str, senha: str) -> User:
    nome = (nome or "").strip()
    email = (email or "").strip()
    telefone = (telefone or "").strip()
    senha = (senha or "").strip()

    if not nome or not email or not telefone or not senha:
        raise ValueError("Todos os campos são obrigatórios.")

    existing_email_user = User.query.filter_by(email=email).first()
    if existing_email_user:
        raise ValueError("Este email já está cadastrado no sistema!")

    existing_name_user = User.query.filter_by(username=nome).first()
    if existing_name_user:
        raise ValueError("Este nome de usuário já está em uso.")

    user = User(nome=nome, email=email, telefone=telefone, senha=senha)
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user_id: int, nome: str, email: str, telefone: str) -> User:
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("Usuário não encontrado.")

    nome = (nome or "").strip()
    email = (email or "").strip()
    telefone = (telefone or "").strip()

    if not nome or not email or not telefone:
        raise ValueError("Por favor, preencha todos os campos.")

    existing_email_user = User.query.filter_by(email=email).first()
    if existing_email_user and existing_email_user.id != user.id:
        raise ValueError("Este email já está cadastrado!")

    user.nome = nome
    user.email = email
    user.telefone = telefone
    db.session.commit()
    return user

def delete_user(user_id: int) -> None:
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("Usuário não encontrado.")

    db.session.delete(user)
    db.session.commit()


def authenticate_user(login_val, senha):
    user = get_user_by_login(login_val)

    if not user:
        return None

    if user.senha != (senha or "").strip():
        flash("Senha incorreta. Tente novamente.", "error")
        return None

    flash("Login realizado com sucesso!", "success")
    return user