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

from pyvirtualbench import PyVirtualBench, PyVirtualBenchException, Waveform, MsoSamplingMode
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import numpy as np

import os, sys, pickle


# Falar do porquê da variável global e o porqê de iniciar a 1.0
# Tem a ver com o cálculo do incremento para o eixo x
# O incremento é calculado com base na frequência e no número de amostras adquiridas
# a«a primeira função a ser chamada é a config_func_generator(frequency:float), portanto, 
# o valor da frequência é passado para a variável global_frequency


def config_func_generator(frequency:float):
    try:
        virtualbench = PyVirtualBench('VB8012-30A210F')
        # Waveform Configuration
        waveform_function = Waveform.SINE
        amplitude = 10.0      # 10V
        dc_offset = 0.0       # 0V
        duty_cycle = 50.0     # 50% (Used for Square and Triangle waveforms)

        # You will probably need to replace "myVirtualBench" with the name of your device.
        # By default, the device name is the model number and serial number separated by a hyphen; e.g., "VB8012-309738A".
        # You can see the device's name in the VirtualBench Application under File->About
        
        fgen = virtualbench.acquire_function_generator()
        fgen.configure_standard_waveform(waveform_function, amplitude, dc_offset, frequency, duty_cycle)
        # Start driving the signal. The waveform will continue until Stop is called, even if you close the session.
        fgen.run()
        
        #############################
        # Power Supply Configuration
        #############################
        ps = virtualbench.acquire_power_supply()
        channel = "ps/+25V"
        voltage_level = 12.0
        current_limit = 0.5 
        ps.enable_all_outputs(True)
        ps.configure_voltage_output(channel, voltage_level, current_limit)        
        
        mso = virtualbench.acquire_mixed_signal_oscilloscope()

        # Configure the acquisition using auto setup
        mso.auto_setup()

        # Query the configuration that was chosen to properly interpret the data.
        sample_rate, acquisition_time, pretrigger_time, sampling_mode = mso.query_timing()
        channels = mso.query_enabled_analog_channels()
        channels_enabled, number_of_channels = virtualbench.collapse_channel_string(channels)
        
        # POVAVELMENTE ISTO PODE SALTAR FORA - PARTE-SE DUM PRINCÍPIO QUE AMBAS AS PONTAS
        # ESTÃO SEMPRE LIGADAS AO VIRTUAL BENCH
        if channels_enabled == "VB8012-30A210F/mso/1:2":
            channels_numbers = 12 # Ambos os canais estão activos
        elif channels_enabled == "VB8012-30A210F/mso/1":
            channels_numbers = 1 #Somente o canal 1 está activo
        elif channels_enabled == "VB8012-30A210F/mso/2":
            channels_numbers = 2 # Somente o canal 2 está activo
        # Start the acquisition.  Auto triggering is enabled to catch a misconfigured trigger condition.
        mso.run()

        # Read the data by first querying how big the data needs to be, allocating the memory, and finally performing the read.
        analog_data, analog_data_stride, analog_t0, digital_data, digital_timestamps, digital_t0, trigger_timestamp, trigger_reason = mso.read_analog_digital_u64()

        analog_data_size = len(analog_data)
        number_of_analog_samples_acquired = analog_data_size / analog_data_stride
        plot_graphic_meiaonda(analog_data, number_of_analog_samples_acquired, channels_numbers, frequency)
        #print_digital_data(digital_data, digital_timestamps, 10)
        ps.release()
        mso.release()
        fgen.release()
    except PyVirtualBenchException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        virtualbench.release()

def plot_graphic_meiaonda(analog_data, number_of_analog_samples_acquired, channels_number, frequency):
    # Seleciona os elementos pares da lista analog_data
    #analog_data_pares = analog_data[::2] # Onda de entrada
    # Seleciona os elementos ímpares da lista analog_data
    #analog_data_impares = analog_data[1::2] # Onda retificada - saída

    # Cria os rótulos para os eixos x
    # Calcula os valores dos eixos x
    increment = 1/(frequency*number_of_analog_samples_acquired)

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

        frequency_trunc = round(frequency, 2)
        formatter_freq = EngFormatter(unit='Hz')
        frequency_text = formatter_freq.format_data_short(frequency_trunc)  # Formate a frequência truncada usando o EngFormatter        
        plt.text(0, -4, 'f= ' + frequency_text, fontsize=12, color='red') 
        
        # Cria o gráfico
        # Cria o gráfico com duas curvas
        plt.plot(x_values_increment, analog_data[::2], label='Onde de entrada', marker=',')
        plt.plot(x_values_increment, analog_data[1::2], label='Onda de saída', marker=',')
    elif channels_number == 1: # Apenas o canal 1 está activo
         # Cria o gráfico
        # Cria o gráfico com duas curvas
        x_values_increment = 4 * x_values_increment # ALDRABICE!!! Será!? Ajustar a escala????
        plt.plot(x_values_increment[::2], analog_data[::2], label='Onda de entrada', marker=',')
    elif channels_number == 2: # Apenas o canal 2 está activo
        # Cria o gráfico
        # Cria o gráfico com duas curvas
        x_values_increment = 4 * x_values_increment # ALDRABICE!!! Será!? Ajustar a escala????
        plt.plot(x_values_increment[1::2], analog_data[1::2], label='Onda de saída', marker=',')
    
    plt.xlabel('Time (Seg)')
    plt.ylabel('Voltage (V)')
    plt.title('Rectificador onda completa')

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

def config_mso_ondacompleta(onda_entrada:bool, onda_saida:bool):
    try:
        virtualbench = PyVirtualBench('VB8012-30A210F')        
        #############################
        # Power Supply Configuration
        #############################
        ps = virtualbench.acquire_power_supply()
        channel = "ps/+25V"
        voltage_level = 12.0
        current_limit = 0.5 
        ps.enable_all_outputs(True)
        ps.configure_voltage_output(channel, voltage_level, current_limit)        
        
        mso = virtualbench.acquire_mixed_signal_oscilloscope()

        # Configure the acquisition using auto setup
        mso.auto_setup()

        # Query the configuration that was chosen to properly interpret the data.
        # POVAVELMENTE ISTO PODE SALTAR FORA - PARTE-SE DUM PRINCÍPIO QUE AMBAS AS PONTAS
        # ESTÃO SEMPRE LIGADAS AO VIRTUAL BENCH
        sample_rate, acquisition_time, pretrigger_time, sampling_mode = mso.query_timing()
        channels = mso.query_enabled_analog_channels()
        channels_enabled, number_of_channels = virtualbench.collapse_channel_string(channels)
        
        if onda_entrada == True: # A função foi chamada para medir a onda de entrada. É atribuído o valor 1 ao canal 1 e 0 ao canal 2
            channel_number = 1 # Somente para fazer a leitura do canal 1
        if onda_saida == True: # A função foi chamada para medir a onda de saída
            channel_number = 2 # Somente para fazer a leitura do canal 2
        print("Canais activos: ", channel_number)
        # Start the acquisition.  Auto triggering is enabled to catch a misconfigured trigger condition.
        mso.run()

        # Read the data by first querying how big the data needs to be, allocating the memory, and finally performing the read.
        analog_data, analog_data_stride, analog_t0, digital_data, digital_timestamps, digital_t0, trigger_timestamp, trigger_reason = mso.read_analog_digital_u64()

        analog_data_size = len(analog_data)
        number_of_analog_samples_acquired = analog_data_size / analog_data_stride
        plot_graphic_ondacompleta(analog_data, number_of_analog_samples_acquired, channel_number)
        #print_digital_data(digital_data, digital_timestamps, 10)
        ps.release()
        mso.release()
    except PyVirtualBenchException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        virtualbench.release()

def plot_graphic_ondacompleta(analog_data, number_of_analog_samples_acquired, channel_number):
    # Seleciona os elementos pares da lista analog_data
    #analog_data_pares = analog_data[::2] # Onda de entrada
    # Seleciona os elementos ímpares da lista analog_data
    #analog_data_impares = analog_data[1::2] # Onda retificada - saída

    # ATENÇÃO!!!!
    # Como os dois canais estão activos, analog_data contém os valores dos dois canais.
    # Como se pretende desenhar os gráficos de cada canal separadamente, é necessário dividir o array analog_data
    # Neste caso o número de elementos do gráfico é metade do número de elementos de analog_data
    # No cálculo dos x_values_increment este valor tem de satisfazer esta condição.
    # Portanto, o número de elementos de x_values_increment = analog_data[0::2]

    # Cria os rótulos para os eixos x
    # Calcula os valores dos eixos x

     # Verifica se o diretório "static/images" existe, se não, cria-o
    images_dir = "webserver/website/static/images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
      # Caminho completo do arquivo
    pickle_file_path = os.path.join(images_dir, "ondacompleta.pickle")
    png_file_path = os.path.join(images_dir, "ondacompleta.png")

    frequency = 60 # Frequência da rede elétrica
    increment = 1/(frequency*number_of_analog_samples_acquired)
    x_values_increment = np.cumsum(np.full(int(number_of_analog_samples_acquired), increment))
    print("Canais activos: ", channel_number)
    if channel_number == 12: # Ambos os canais estão activos
        
        '''
        ATENÇÃO!!!!
        O CÁLCULO DO INCREMENTO DEVE ESTAR FORA DOS IF'S
        '''

        '''
        DOIS CANAIS: ARMAZENA NA ESTRUTURA OS VALORES DO CANAL UM E DOIS, LOGO, O INCREMENTO TEM DE 
        
        Número de amostras [number_of_analog_samples_acquired] = 1002
        Número de valores na estrutura [len(analog_data)] = 2004
        
        '''
        x_values_increment = 4 * x_values_increment # ALDRABICE!!! Será?! Ajustar a escala????
        #x_values = len(analog_data)/2 # São armazenados os valores dos dois canais, então, por cada canal é metade


        # Armazena o par frequência, tensão no array, logo, o resultado de len(analog_data) é o dobro de number_of_analog_samples_acquired
        # print("Número de amostras: ", len(analog_data)) = 2004
        # print("Número de amostras adquiridas: ", number_of_analog_samples_acquired) = 1002
        # frequency_values = frequency_values/2 # Armazena os valores de ambos os canais no array - divide por 2 para obter a frequência correta
        # Armazena o par frequência, tensão no array, logo, o resultado de len(analog_data) é o dobro de number_of_analog_samples_acquired
        #length = len(analog_data) = 2004, se a frequência for 200Hz.

        frequency_trunc = round(frequency, 2)
        formatter_freq = EngFormatter(unit='Hz')
        frequency_text = formatter_freq.format_data_short(frequency_trunc)  # Formate a frequência truncada usando o EngFormatter        
        plt.text(0, -4, 'f= ' + frequency_text, fontsize=12, color='red') 
        
        # Cria o gráfico
        # Cria o gráfico com duas curvas
        plt.plot(x_values_increment, analog_data[::2], label='Onde de entrada', marker=',')
        plt.plot(x_values_increment, analog_data[1::2], label='Onda de saída', marker=',')
    elif channel_number == 1: # Apenas o canal 1 está activo
         # Cria o gráfico
        # Cria o gráfico com duas curvas
        #x_values_increment = 2 * x_values_increment # ALDRABICE!!! Será!? Ajustar a escala????
        plt.plot(x_values_increment, analog_data[1::2], label='Onda de entrada', marker=',')
        # Salva o gráfico atual em um arquivo
        with open(pickle_file_path, 'wb') as f:
            pickle.dump(plt.gcf(), f)
        plt.close() # Fecha o gráfico para libertar recursos
       
    elif channel_number == 2: # Apenas o canal 2 está activo
        # Cria o gráfico
        # Cria o gráfico com duas curvas
        #x_values_increment = 8 * x_values_increment # ALDRABICE!!! Será!? Ajustar a escala????
        
        # Carregue o gráfico do arquivo pickle
        with open(pickle_file_path, 'rb') as f:
            fig = pickle.load(f)
            # Adicione o novo plot ao gráfico carregado
            plt.figure(fig.number)  # Certifique-se de que o novo plot seja adicionado à figura carregada
            print("Número de amostras: ", analog_data[1::2])
            plt.plot(x_values_increment, analog_data[1::2], label='Onda de saída', marker=',')
            plt.legend()  # Adicione a legenda para ambos os plots
                
            plt.xlabel('Time (Seg)')
            plt.ylabel('Voltage (V)')
            plt.title('Rectificador onda completa')

            # Define os valores específicos para o eixo x (frequência) e rotaciona os rótulos
            plt.xticks(rotation=45)

            # Define o EngFormatter para o eixo x
            formatter0 = EngFormatter(unit='s')
            plt.gca().xaxis.set_major_formatter(formatter0)

            # Define os limites do eixo y para -5 a 5
            plt.ylim(-15, 15)

            # Adiciona a legenda ao gráfico
            plt.legend(loc='best')

            plt.tight_layout()  # Ajusta automaticamente o layout do gráfico para evitar sobreposições

            # Adiciona a grade ao gráfico
            plt.grid(True)
            # Salve o gráfico atualizado como uma imagem PNG
            fig.savefig(png_file_path)
            # Renomeia o arquivo pickle após o uso
            #os.rename(pickle_file_path, os.path.join(images_dir, "fig1_processed.pickle"))
        