from flask import Flask
from .user_routes import user_bp
from .auth import auth_bp
from .main_routes import main_bp
from .auth_decorator import login_required
from .loja_routes import loja_bp

def register_blueprints(app: Flask):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(loja_bp)
