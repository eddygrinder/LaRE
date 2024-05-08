import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Arquivo para armazenar os valores ps e dmm
# Não esquecer de documentar a escolha do módulo para manter e aceder aos valores de ps e dmm
ps = None
dmm = None
voltage_ctrl_index = 0
current_ctrl_index = 0
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
    global voltage_ctrl_index, current_ctrl_index
    ps = None
    dmm = None
    voltage_ctrl_index = 0
    current_ctrl_index = 0

def voltage_index(voltage): # Recebe os valores de tensão e armazena no dicionário
# Recebe um valor de tensão e o armazena no dicionário
    global voltage_measurements, voltage_ctrl_index, current_ctrl_index
    # Adicione o novo valor de tensão ao array
    voltage_measurements = np.append(voltage_measurements, voltage)
    print ("voltage_values: ", voltage_measurements)
    voltage_ctrl_index += 1 # Incrementa o índice a partit do 1 devido aos return's
    return voltage_ctrl_index, current_ctrl_index

def current_index(current): # Recebe os valores de corrente e armazena no dicionário
    global current_measurements, voltage_ctrl_index, current_ctrl_index
    # Adicione o novo valor de corrente ao array
    current_measurements = np.append(current_measurements, current)
    print ("current_values: ", current_measurements)
    current_ctrl_index += 1 # Incrementa o índice
    return voltage_ctrl_index, current_ctrl_index

def voltage_values():
    return voltage_measurements

def current_values():
    return current_measurements
