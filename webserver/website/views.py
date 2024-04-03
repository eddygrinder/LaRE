from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json, time

import os, sys

# Adiciona o diretório do projeto ao caminho de busca de módulos do Python
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

#from configVB import config_VB_DMM
from ctrl_hardware import configRelays, configVB

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

#########################################################
# Rota para passar parâmetros para o script controlVB.py
# Só passa os parâmetros de escolha    
#########################################################

# Rota para controlar e obter o resultado da medição
@views.route('/config_VirtualBench', methods=['GET', 'POST'])
@login_required
def config_VirtualBench():
    Vcc = request.args.get('Vcc', 0, int)
    Resistance = request.args.get('R', 0, int)
    measure_parameter = request.args.get('parameter', 0, str)
  
    configRelays.config_Parameters(Resistance, measure_parameter)

    measurement_result = configVB.config_VB_DMM(Vcc, measure_parameter)

    time.sleep(5)
    configRelays.config_Parameters(0, measure_parameter)

    return jsonify({'measurement_result': measurement_result})