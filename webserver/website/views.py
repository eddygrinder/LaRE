from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from configVB import config_Parameters
from configString import config_Relays

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
    
    measurement_voltage = config_Parameters(Vcc, Resistance, measure_parameter)

    print(f'MeAsure: {measurement_voltage}')

    return jsonify({'measurement_result': measurement_voltage})

@views.route('/read_Voltage', methods=['GET', 'POST'])
@login_required
def read_Voltage():
    Vcc = request.args.get('Vcc', 0, int)
    Resistance = request.args.get('R',0, int)
    print(f'MeAsure: {Vcc}')
    print(Resistance)

    return jsonify({'measurement_result': 12})