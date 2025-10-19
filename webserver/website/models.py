#! /usr/bin/env python3

"""
===============================================================================
 Projeto: LaRE - Laboratório Remoto Expansível
 Ficheiro: models.py
 Autor: Eduardo Ramalhadeiro
 Instituição: Instituto Superior de Engenharia do Porto (ISEP)
 Curso: Mestrado em Engenharia Eletrotécnica e de Computadores
 Data: Outubro de 2025

 Descrição:
Define as classes de modelo da aplicação, representando as tabelas da base de dados
e a sua estrutura, relações e comportamento associado.
===============================================================================
"""

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
