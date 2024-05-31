from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json, time

import os, sys, subprocess

# Adiciona o diretório do projeto ao caminho de busca de módulos do Python
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

#from configVB import config_VB_DMM
from ctrl_hardware import configRelays, configVB, mixed_signal_oscilloscope

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

@views.route("/ondacompleta")
@login_required
def ondacompleta():
    return render_template("ondacompleta.html", user=current_user)


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
        #print (Vcc, Resistance, measure_parameter, configOK, configSTOP)
        configRelays.config_relays_ohm(Resistance, measure_parameter)
        time.sleep(2)

        measurement_result = configVB.test_parameters(Vcc, Resistance, measure_parameter, configOK, configSTOP)
        #print(Vcc, Resistance, measure_parameter, configOK, configSTOP)
      #  while(True):
       #     time.sleep(1)
        configRelays.config_relays_ohm(0, measure_parameter)

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
    try:
        Capacitor = request.args.get('C', 0, int)
        Resistance = request.args.get('R', 0, int)
        frequency = request.args.get('f', 0, float)
        
        # Colocar os relés a zero
        configRelays.config_relays_meiaonda(0, 0)
        time.sleep(2) # Verificar estes atrasos

        if frequency != 0: #Acontece se o utilizador carregar no OK, é enviado o valor da frequência=0
            configRelays.config_relays_meiaonda(Resistance, Capacitor)
            time.sleep(2)
            mixed_signal_oscilloscope.config_func_generator(frequency)
            #mixed_signal_oscilloscope.config_signal_oscilloscope(frequency)
                        
            # Execute o comando diretamente
            # Explicar porque se usou este comando
            #os.system('python ctrl_hardware/mixed_signal_oscilloscope.py')

    except Exception as e:
        print(e)
        return jsonify({'measurement_result': 'ERROR'})
    finally:
        # Independentemente de uma exceção ocorrer ou não, renderiza o template
        return render_template("meiaonda.html", user=current_user)
    
@views.route('/config_ondacompleta', methods=['GET', 'POST'])
@login_required
def config_ondacompleta():
    try:
        Capacitor = request.args.get('C', 0, int)
        Resistance = request.args.get('R', 0, int)
        # Colocar os relés a zero
       

        frequency = 60
        # devido ao problema de massas da rectificação de onda completa, a onda de entrada tem de ser medida primeiro
        # e só depois a onda de saída - PROBLEMA DE MASSAS. Os gráficos têm de ser desenhados independentemente.
        # Os relés activos consoante o caso.

        ############################################################
        # Activar os respectivos relés para a medição da onda de entrada
        # Relés - K1...|K9 - 000000000
        ############################################################
        #mixed_signal_oscilloscope.config_func_generator(frequency)

        # O VB detecta os dois canais CH1 e CH2, não há possibilidade, por software, de desligar um dos canais
        # O que se pode fazer é desligar o canal fisicamente
        # A leitura é armazenada no array analog_data[1::2] - canal 2 e analog_data[0::2] - canal 1
        # Como é feita a leitura se os dois canais forem chamados, um a um?
        # Os valores mantêm-se ou terá de ser feita uma nova leitura?
        

        configRelays.config_relays_ondacompleta(Capacitor, Resistance)
        mixed_signal_oscilloscope.config_mso_ondacompleta(onda_entrada=True, onda_saida=False)
        
        configRelays.config_relays_ondacompleta(0, 0)
        mixed_signal_oscilloscope.config_mso_ondacompleta(onda_entrada=False, onda_saida=True)

        time.sleep(2) # Verificar estes atrasos



        #mixed_signal_oscilloscope.config_signal_oscilloscope(frequency)
                    
            # Execute o comando diretamente
            # Explicar porque se usou este comando
            #os.system('python ctrl_hardware/mixed_signal_oscilloscope.py')

    except Exception as e:
        print(e)
        return jsonify({'measurement_result': 'ERROR'})
    finally:
        # Independentemente de uma exceção ocorrer ou não, renderiza o template
        return render_template("ondacompleta.html", user=current_user)