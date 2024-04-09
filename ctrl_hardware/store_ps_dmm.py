import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# Arquivo para armazenar os valores ps e dmm
# Não esquecer de documentar a escolha do módulo para manter e aceder aos valores de ps e dmm
ps = None
dmm = None
v = 0
i = 0
# Dicionário para armazenar os valores de corrente e tensão
voltage_measurements = np.array([])
current_measurements = np.array([])

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
# Recebe um valor de tensão e o armazena no dicionário
    global voltage_measurements, v
    # Adicione o novo valor de tensão ao array
    voltage_measurements = np.append(voltage_measurements, voltage)
    print ("voltage_values: ", voltage_measurements)
    v+=1 # Incrementa o índice a partit do 1 devido aos return's
    if v == 3:
        return voltage_measurements, v
    else:
        return None, v

def set_current_graphic(current): # Recebe os valores de corrente e armazena no dicionário
    global current_measurements, i
    # Adicione o novo valor de corrente ao array
    current_measurements = np.append(current_measurements, current)
    print ("current_values: ", current_measurements)
    i+=1 # Incrementa o índice a partit do 1 devido aos return's
    if i == 3:
        return current_measurements
    else:
        return None

def plot_graphic():
   # Cria os rótulos para os eixos x
    x_labels = range(1, len(voltage_measurements) + 1)

    # Cria o gráfico
    #plt.plot(x_labels, current_measurements, label='Corrente (A)')
    plt.plot(current_measurements, x_labels, label='Tensão (V)', marker = 'o')
    slope, intercept, r_value, p_value, std_err = stats.linregress(current_measurements, voltage_measurements)
    print ("slope: %f    intercept: %f" % (slope, intercept))

    plt.xlabel('Voltage')
    plt.ylabel('Current')
    plt.title('Gráfico de Tensão e Corrente')
    plt.legend("declive: %f" % slope)
    plt.grid(True)
    plt.show()