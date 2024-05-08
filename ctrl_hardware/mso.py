#! /usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2016 Charles Armstrap <charles@armstrap.org>
# If you like this library, consider donating to: https://bit.ly/armstrap-opensource-dev
# Anything helps.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pyvirtualbench import PyVirtualBench, PyVirtualBenchException, MsoSamplingMode
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import numpy as np
from scipy.signal import argrelextrema


from scipy import stats

import os, sys
#import store_ps_dmm

def plot_graphic(analog_data, number_of_analog_samples_acquired, channels_number):
    # Seleciona os elementos pares da lista analog_data
    analog_data_pares = analog_data[::2] # Onda de entrada
    # Seleciona os elementos ímpares da lista analog_data
    analog_data_impares = analog_data[1::2] # Onda retificada - saída
    
    # Cria os rótulos para os eixos x
    # Calcula os valores dos eixos x
    #time = 1/50
    increment = 1/(250*number_of_analog_samples_acquired)
    print("Incremento: ", increment)
    print("Número de amostras: ", number_of_analog_samples_acquired)
    
    if channels_number == 12: # Ambos os canais estão activos
        
        '''
        ATENÇÃO!!!!
        O CÁLCULO DO INCREMENTO DEVE ESTAR FORA DOS IF'S
        '''

        '''
        DOIS CANAIS: ARMAZENA NA ESTRUTURA OS VALORES DO CANAL UM E DOIS, LOGO, O INCREMENTO TEM DE 
        
        Número de amostras [number_of_analog_samples_acquired] = 1002
        Número de valores na estrutura [len(analog_data)] = 2004
        
        '''
        x_values_increment = np.cumsum(np.full(int(number_of_analog_samples_acquired), increment)) 
        x_values_increment = 4 * x_values_increment # ALDRABICE!!! Será?! Ajustar a escala????
        #x_values = len(analog_data)/2 # São armazenados os valores dos dois canais, então, por cada canal é metade


        # Armazena o par frequência, tensão no array, logo, o resultado de len(analog_data) é o dobro de number_of_analog_samples_acquired
        # print("Número de amostras: ", len(analog_data)) = 2004
        # print("Número de amostras adquiridas: ", number_of_analog_samples_acquired) = 1002
        # frequency_values = frequency_values/2 # Armazena os valores de ambos os canais no array - divide por 2 para obter a frequência correta
        # Armazena o par frequência, tensão no array, logo, o resultado de len(analog_data) é o dobro de number_of_analog_samples_acquired
        #length = len(analog_data) = 2004, se a frequência for 200Hz.

        analog_data_array = np.array(analog_data)
        
        # Encontra o índice do primeiro máximo
        max_index = np.argmax(analog_data_array[::2])
        
        # Encontra o índice do primeiro mínimo
        min_index = np.argmin(analog_data_array[::2])

        # Coordenadas no eixo dos x correspondentes ao primeiro máximo e mínimo
        x_coordinate_of_max = x_values_increment[::2][max_index]
        x_coordinate_of_min = x_values_increment[::2][min_index]

        '''
        ATENÇÃO!!!! 
        Para frequências menores que 50Hz o cálculo do período e frequência tem um erro grande
        
        '''
        
        print("Máximo: ", x_coordinate_of_max)
        print("Minimo: ", x_coordinate_of_min)
        half_period = abs(x_coordinate_of_max - x_coordinate_of_min) # Diferença entre o máximo e o mínimo
        print("Meio período: ", half_period)
        print("Period: ", 2*half_period)
        T = 2*half_period
        
        frequency = 1/T # Frequência
        print("Frequência: ", frequency)

        frequency_trunc = round(frequency, 2)
        formatter_freq = EngFormatter(unit='Hz')
        frequency_text = formatter_freq.format_data_short(frequency_trunc)  # Formate a frequência truncada usando o EngFormatter        
        plt.text(0, -4, 'f~ ' + frequency_text, fontsize=12, color='red') 
        
        # Cria o gráfico
        # Cria o gráfico com duas curvas
        plt.plot(x_values_increment, analog_data[::2], label='Onde de entrada', marker=',')
        plt.plot(x_values_increment, analog_data[1::2], label='Onda de saída', marker=',')
    elif number_of_channels == 1: # Apenas o canal 1 está activo
         # Cria o gráfico
        # Cria o gráfico com duas curvas
        x_values_increment = 4 * x_values_increment # ALDRABICE!!! Será!? Ajustar a escala????
        plt.plot(x_values_increment[::2], analog_data[::2], label='Onda de entrada', marker=',')
    elif number_of_channels == 2: # Apenas o canal 2 está activo
        # Cria o gráfico
        # Cria o gráfico com duas curvas
        x_values_increment = 4 * x_values_increment # ALDRABICE!!! Será!? Ajustar a escala????
        plt.plot(x_values_increment[1::2], analog_data[1::2], label='Onda de saída', marker=',')
    
    plt.xlabel('Time (Seg)')
    plt.ylabel('Voltage (V)')
    plt.title('Rectificador meia-onda')

     # Define os valores específicos para o eixo x (frequência) e rotaciona os rótulos
    plt.xticks(rotation=45)

    # Define o EngFormatter para o eixo x
    formatter0 = EngFormatter(unit='s')
    plt.gca().xaxis.set_major_formatter(formatter0)

    # Define os limites do eixo y para -5 a 5
    plt.ylim(-5, 5)

    # Adiciona a legenda ao gráfico
    plt.legend(loc='best')

    plt.tight_layout()  # Ajusta automaticamente o layout do gráfico para evitar sobreposições

    # Adiciona a grade ao gráfico
    plt.grid(True)

    # Verifica se o diretório "static/images" existe, se não, cria-o
    if not os.path.exists("webserver/website/static/images"):
        os.makedirs("webserver/website/static/images")

    # Salva o gráfico como uma imagem dentro do diretório "static/images"
    plt.savefig("webserver/website/static/images/meia_onda.png")

    # Limpa a figura
    plt.clf()

# This examples demonstrates how to configure and acquire data from the
# Mixed Signal Oscilloscope (MSO) instrument on a VirtualBench using
# the built in auto setup functionality.

'''
def print_analog_data(analog_data, analog_data_stride, number_of_channels, sample_mode, number_to_print):
    analog_data_size = len(analog_data)
    if (analog_data_size == 0):
        return # Nothing to print if there is no data

    number_of_analog_samples_acquired = analog_data_size / analog_data_stride
    if (number_of_analog_samples_acquired < number_to_print):
        number_to_print = number_of_analog_samples_acquired

    print("Analog Data (%d of %d):" % (number_to_print, number_of_analog_samples_acquired))

    # Print channel header information.
    print("Channel:\t", end='')
    for chan in range(number_of_channels):
        if (chan != 0):
            print("\t\t", end='')
        print("%d" % chan, end='')
        if (sample_mode == MsoSamplingMode.PEAK_DETECT):
            print(" (min)\t\t%d (max)" % chan, end='')
    print("")

    # Print the data itself.
    for sample_index in range(number_to_print):
        #print("Sample %d:\t" % sample_index, end='')
        for channel_index in range(analog_data_stride):
            if (channel_index != 0):
                print("\t", end='')
            print("%4.6f" % analog_data[sample_index * analog_data_stride + channel_index], end='')
        print("")

    return (number_of_analog_samples_acquired)
'''

try:
    # You will probably need to replace "myVirtualBench" with the name of your device.
    # By default, the device name is the model number and serial number separated by a hyphen; e.g., "VB8012-309738A".
    # You can see the device's name in the VirtualBench Application under File->About
    virtualbench = PyVirtualBench('VB8012-30A210F')
    mso = virtualbench.acquire_mixed_signal_oscilloscope()

    # Configure the acquisition using auto setup
    mso.auto_setup()

    # Query the configuration that was chosen to properly interpret the data.
    sample_rate, acquisition_time, pretrigger_time, sampling_mode = mso.query_timing()
    channels = mso.query_enabled_analog_channels()
    channels_enabled, number_of_channels = virtualbench.collapse_channel_string(channels)
    print("Channels:", channels_enabled)
    if channels_enabled == "VB8012-30A210F/mso/1:2":
        channels_numbers = 12 # Ambos os canais estão activos
    elif channels_enabled == "VB8012-30A210F/mso/1":
        channels_numbers = 1 #Somente o canal 1 está activo
    elif channels_enabled == "VB8012-30A210F/mso/2":
        channels_numbers = 2 # Somente o canal 2 está activo
    print(number_of_channels)

    # Start the acquisition.  Auto triggering is enabled to catch a misconfigured trigger condition.
    mso.run()

    # Read the data by first querying how big the data needs to be, allocating the memory, and finally performing the read.
    analog_data, analog_data_stride, analog_t0, digital_data, digital_timestamps, digital_t0, trigger_timestamp, trigger_reason = mso.read_analog_digital_u64()
    print("Data Stride:", analog_data_stride)

    analog_data_size = len(analog_data)
    print("Analog Data Size:", analog_data_size)
    number_of_analog_samples_acquired = analog_data_size / analog_data_stride

    plot_graphic(analog_data, number_of_analog_samples_acquired, channels_numbers)
    #print_digital_data(digital_data, digital_timestamps, 10)

    mso.release()
except PyVirtualBenchException as e:
    print("Error/Warning %d occurred\n%s" % (e.status, e))
finally:
    virtualbench.release()

