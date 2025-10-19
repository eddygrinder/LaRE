#! /usr/bin/env python3

"""
===============================================================================
 Projeto: LaRE - Laboratório Remoto Expansível
 Ficheiro: __init__.py
 Autor: Eduardo Ramalhadeiro
 Instituição: Instituto Superior de Engenharia do Porto (ISEP)
 Curso: Mestrado em Engenharia Eletrotécnica e de Computadores
 Data: Outubro de 2025

 Descrição:
Marca este diretório como um pacote Python e pode incluir inicialização
de módulos ou configurações do pacote.
===============================================================================
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
