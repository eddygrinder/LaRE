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

@views.route("/passaalto")
@login_required
def passaalto():
    return render_template("passaalto.html", user=current_user)

@views.route("/passabaixo")
@login_required
def passabaixo():
    return render_template("passabaixo.html", user=current_user)

@views.route("/bodediagram")
@login_required
def bodediagram():
    return render_template("passaalto.html", user=current_user)

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
        measure_parameter = request.args.get('parameter', 0, str)
        configOK = request.args.get('habilitar_parameter', 0, bool)
        configSTOP = request.args.get('desabilitar_parameter', 0, bool)
        print (Vcc, Resistance, measure_parameter, configOK, configSTOP)
        
        if configOK == True:
            print("OK")
            configVB.OK()
            measurement_result = 0       
        elif configSTOP == True:
            print("STOP")
            configVB.STOP()
            measurement_result = 0
        else:    
            configRelays.config_relays_ohm(Resistance, measure_parameter)
            time.sleep(2)
            measurement_result = configVB.test_parameters(Vcc, Resistance, measure_parameter)
            print("FODA-sE", measurement_result)
            configRelays.config_relays_ohm(0, measure_parameter)
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
        
        if frequency != 0: #Acontece se o utilizador carregar no OK, é enviado o valor da frequência=0
            mixed_signal_oscilloscope.config_instruments_HalfWave(frequency, Resistance, Capacitor)
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

        # DESTA FORMA FUNCIONA A ONDA DE ENTRADA - PONTO
        #configRelays.config_relays_ondacompleta(0, 0) NÃO GERA A ONDA DE SAÍDA COLOCANDO OS RELÉS A ZERO
        mixed_signal_oscilloscope.config_func_generatorMSO()
        configRelays.config_relays_vin()
        time.sleep(2) # Verificar estes atrasos

        mixed_signal_oscilloscope.config_mso_ondacompleta(onda_entrada=True, onda_saida=False)
        time.sleep(2) # Verificar estes atrasos

        configRelays.config_relays_ondacompleta(Resistance, Capacitor)
        time.sleep(2) # Verificar estes atrasos

        mixed_signal_oscilloscope.config_mso_ondacompleta(onda_entrada=False, onda_saida=True)


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
    
@views.route('/config_filters', methods=['GET', 'POST'])
@login_required
def config_filters():
    try:
        Capacitor = request.args.get('C', 0, int)
        Resistance = request.args.get('R', 0, int)
        frequency = request.args.get('f', 0, float)
        which_filter = request.args.get('filter_type', 0, str)
        
        print(Capacitor, Resistance, frequency, which_filter)
         
        if frequency != 0 and which_filter == "HPF": #Acontece se o utilizador carregar no OK, é enviado o valor da frequência=0
            print("HPF")
            mixed_signal_oscilloscope.config_instruments_PassFilters(frequency, Resistance, Capacitor, "HPF") # high-pass filter
        elif frequency != 0 and which_filter == "LPF":
            print("LPF")
            mixed_signal_oscilloscope.config_instruments_PassFilters(frequency, Resistance, Capacitor, "LPF") # low-pass filter
    except Exception as e:
        print(e)
        return jsonify({'measurement_result': 'ERROR'})
    finally:
        # Independentemente de uma exceção ocorrer ou não, renderiza o template
        return render_template("passaalto.html", user=current_user)

@views.route('/get_bodediagram', methods=['GET', 'POST'])
@login_required
def get_bodediagram():
    try:
        Capacitor = request.args.get('C', 0, int)
        Resistance = request.args.get('R', 0, int)
        which_filter = request.args.get('filter_type', 0, str)
        print(Capacitor, Resistance, which_filter)
        if which_filter == "HPF":
            mixed_signal_oscilloscope.bode_graphic_Filters(Resistance, Capacitor, which_filter)
        elif which_filter == "LPF":
            print("LPF")
            mixed_signal_oscilloscope.bode_graphic_Filters(Resistance, Capacitor, which_filter)
    except Exception as e:
        print(e)
        return jsonify({'measurement_result': 'ERROR'})
    finally:
        # Independentemente de uma exceção ocorrer ou não, renderiza o template
        return render_template("passaalto.html", user=current_user)