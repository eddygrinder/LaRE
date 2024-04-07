import matplotlib.pyplot as plt
from configVB import get_voltage_values, get_current_values

# Arquivo para armazenar os valores ps e dmm
# Não esquecer de documentar a escolha do módulo para manter e aceder aos valores de ps e dmm
ps = None
dmm = None

# Dicionário para armazenar os valores de corrente e tensão
voltage_measurements = {}
current_measurements = {}

def set_values(ps_value, dmm_value):
    global ps, dmm
    ps = ps_value
    dmm = dmm_value

def get_values():
    return ps, dmm

def clear_values():
    global ps, dmm
    ps = None
    dmm = None

def set_voltage_graphic(voltage): # Recebe os valores de tensão e armazena no dicionário
    voltage_measurements ['measure'] = voltage

def get_voltage_values():
    return voltage_measurements.get('measure')

def set_current_graphic(current): # Recebe os valores de corrente e armazena no dicionário
    current_measurements ['measure'] = current

def get_current_values():
    return current_measurements.get('measure')

def plot_graphic_corrente_tensao():
    # Obtenha os valores de corrente e tensão
    tensao = get_voltage_values()
    corrente = get_current_values()

    # Verifique se os valores estão presentes antes de plotar o gráfico
    if tensao is not None and corrente is not None:
        # Crie o gráfico de dispersão
        plt.scatter(corrente, tensao)
        plt.xlabel('Corrente (A)')
        plt.ylabel('Tensão (V)')
        plt.title('Gráfico de Corrente vs Tensão')
        plt.show()
    else:
        print("Não há dados suficientes para plotar o gráfico.")