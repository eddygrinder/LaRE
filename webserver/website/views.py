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

@views.route("/ohm", methods=['GET', 'POST'])
@login_required
def pagina_seguinte():
    return render_template("ohm.html", user=current_user)

@views.route("/meiaonda")
@login_required
def meiaonda():
    return render_template("meiaonda.html", user=current_user)


#########################################################
# Rota para passar parâmetros para o script controlVB.py
# Só passa os parâmetros de escolha    
#########################################################

# Rota para controlar e obter o resultado da medição
@views.route('/config_VirtualBench', methods=['GET', 'POST'])
@login_required
def config_VirtualBench():
    try:
        Vcc = request.args.get('Vcc', 0, int)
        Resistance = request.args.get('R', 0, int)
        measure_parameter = request.args.get('parameter', None, str)
        configOK = request.args.get('habilitar_parameter', None, bool)
        configSTOP = request.args.get('desabilitar_parameter', None, bool)
        print (Vcc, Resistance, measure_parameter, configOK, configSTOP)
        if Resistance:
            configRelays.config_Parameters(Resistance, measure_parameter)
            time.sleep(2)

        measurement_result = configVB.test_parameters(Vcc, Resistance, measure_parameter, configOK, configSTOP)
        #print(Vcc, Resistance, measure_parameter, configOK, configSTOP)
        
        configRelays.config_Parameters(0, measure_parameter)

        '''
        São passados vários parâmetros do ficheiro home.html para esta função.
        De entre eles, são feitas quatro possíveis combinações que correspondem a quatro situações diferentes:
        1 - Vcc, Resistance, measure_parameter, configOK, configSTOP = 0, 0, None, True, None - Botão OK premido
            Sistema adquire a fonte de alimentação e o multímetro e pronto para realizar medição
        2 - Vcc, Resistance, measure_parameter, configOK, configSTOP = 0, 0, None, None, True - Botão STOP premido
            Sistema "desliga" a fonte de alimentação e o multímetro, e os relés são desligados (configuração inicial)
        3/4 - Vcc, Resistance, measure_parameter, configOK, configSTOP = !=0, !=0, V or I, None, None
            Sistema realiza medição de tensão ou corrente, conforme os parâmetros passados
        '''
    except Exception as e:
        print(e)
        return jsonify({'measurement_result': 'ERROR'})
    finally:
        return jsonify({'measurement_result': measurement_result})


@views.route('/config_meiaonda', methods=['GET', 'POST'])
@login_required
def config_meiaonda():
    print("Meia onda")
    return render_template("meiaonda.html", user=current_user)