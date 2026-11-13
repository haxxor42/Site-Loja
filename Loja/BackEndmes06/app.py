import os
from flask import Flask, app, redirect, render_template, request 
from models.models import init_db
from routes import register_blueprints
from routes.auth_decorator import login_required
from datetime import timedelta



def create_app():
    app = Flask(__name__)

  
    app.config['SECRET_KEY'] = os.getenv(
        "SECRET_KEY", "admin-key"
    )

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

    init_db(app)
    register_blueprints(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

