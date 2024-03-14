from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

import os, sys

# Obtém o diretório atual do script
current_dir = os.path.dirname(__file__)
# Adiciona o diretório ctrl_hardware ao caminho de busca de módulos do Python
ctrl_hardware_dir = os.path.join(current_dir, '..', 'ctrl_hardware')
sys.path.append(ctrl_hardware_dir)

from ctrl_hardware.configVB import config_VB_DMM
from ctrl_hardware.configRelays import config_Parameters

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
    Resistance = request.args.get('R',0, int)
    measure_parameter = request.args.get('parameter')

    print(f'measure_parameter: {measure_parameter}')
    
    config_Parameters(Resistance, measure_parameter)
    measurement_result = config_VB_DMM (Vcc, measure_parameter)

    print(f'MeAsure: {measurement_result}')

    return jsonify({'measurement_result': measurement_result})