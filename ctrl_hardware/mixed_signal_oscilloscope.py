#! /usr/bin/env python3
# -*- coding: utf-8 -*-

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

import os, pickle, socket, time
import store_ps_dmm, configRelays


# Falar do porquê da variável global e o porqê de iniciar a 1.0
# Tem a ver com o cálculo do incremento para o eixo x
# O incremento é calculado com base na frequência e no número de amostras adquiridas
# a«a primeira função a ser chamada é a config_func_generator(frequency:float), portanto, 
# o valor da frequência é passado para a variável global_frequency

def config_instruments_HalfWave(frequency:float, Resistance:int, Capacitor:int):
    try:
        virtualbench = PyVirtualBench('VB8012-30A210F')
        
        #############################
        # Waveform Configuration - Configuração do gerador de sinal
        #############################
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
        
        configRelays.config_relays_meiaonda(0, 0) # Independentemente do seu estado, coloca os relés a zero
        configRelays.config_relays_meiaonda(Resistance, Capacitor) # Configura os relés para a medição
        
        mso = virtualbench.acquire_mixed_signal_oscilloscope()

        # Configure the acquisition using auto setup
        mso.auto_setup()

        # Query the configuration that was chosen to properly interpret the data.
        sample_rate, acquisition_time, pretrigger_time, sampling_mode = mso.query_timing()
        channels = mso.query_enabled_analog_channels()
        channels_enabled, number_of_channels = virtualbench.collapse_channel_string(channels)
        
        # Start the acquisition.  Auto triggering is enabled to catch a misconfigured trigger condition.
        mso.run()       
        
        # Read the data by first querying how big the data needs to be, allocating the memory, and finally performing the read.
        analog_data, analog_data_stride, analog_t0, digital_data, digital_timestamps, digital_t0, trigger_timestamp, trigger_reason = mso.read_analog_digital_u64()

        analog_data_size = len(analog_data)
        number_of_analog_samples_acquired = analog_data_size / analog_data_stride
              
        plot_graphic(analog_data, number_of_analog_samples_acquired, frequency, graphtype='meiaonda')
        #print_digital_data(digital_data, digital_timestamps, 10)
              
        ps.enable_all_outputs(False) # Desliga a fonte de alimentação
        ps.release()
        mso.release()
        fgen.release()
    except PyVirtualBenchException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        virtualbench.release()

def plot_graphic(analog_data, number_of_analog_samples_acquired, frequency, graphtype:str):
    
    # Converte para array NumPy
    analog_data = np.array(analog_data)
    
    # Seleciona os elementos pares da lista analog_data
    onda_entrada = analog_data[::2] # Onda de entrada
    # Seleciona os elementos ímpares da lista analog_data
    onda_saida = analog_data[1::2] # Onda retificada - saída

    # Cálculo dos máximos com NumPy
    max_entrada = np.max(onda_entrada)
    min_saida = np.min(onda_saida)
    max_saida = np.max(onda_saida)
    vripple= max_saida - min_saida # Ripple de saída

    
    # Índices dos máximos para obter também o tempo correspondente
    idx_max_entrada = np.argmax(onda_entrada)
    idx_max_saida = np.argmax(onda_saida)
    idx_min_saida = np.argmin(onda_saida)
    
    # Cria os rótulos para os eixos x
    # Calcula os valores dos eixos x
    increment = 1/(frequency*number_of_analog_samples_acquired)

        
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
    vripple_trunc = round(vripple, 2)
    formatter_vripple = EngFormatter(unit='V')
    vripple_text = formatter_vripple.format_data_short(vripple_trunc)  # Formate a frequência truncada usando o EngFormatter     
    if graphtype == 'HPF' or graphtype == 'LPF':
        plt.text(0, -4, 'f= ' + frequency_text, fontsize=12, color='red') 
    elif graphtype == 'meiaonda':
        plt.text(0, -5.5, 'vripple= ' + vripple_text, fontsize=12, color='red') 
    
    # Cria o gráfico
    # Cria o gráfico com duas curvas
    plt.plot(x_values_increment, onda_entrada, label='Onde de entrada', marker=',')
    plt.plot(x_values_increment, onda_saida, label='Onda de saída', marker=',')
    
    # Mostrar os valores máximos no ponto correspondente
    plt.text(x_values_increment[idx_max_entrada], max_entrada, f'{max_entrada:.2f} V', color='blue', fontsize=9, ha='left', va='top')
    plt.text(x_values_increment[idx_max_saida], max_saida, f'{max_saida:.2f} V', color='orange', fontsize=9, ha='left', va='bottom')
    plt.text(x_values_increment[idx_min_saida], min_saida, f'{min_saida:.2f} V', color='orange', fontsize=9, ha='left', va='bottom')

    plt.xlabel('Time (Seg)')
    plt.ylabel('Voltage (V)')
    
    if graphtype == 'meiaonda':
        plt.title('Rectificador meia onda')
    elif graphtype == 'LPF':
        plt.title('Filtro passa-baixo')
    elif graphtype == 'HPF':
        plt.title('Filtro passa-alto')   

     # Define os valores específicos para o eixo x (frequência) e rotaciona os rótulos
    plt.xticks(rotation=45)

    # Define o EngFormatter para o eixo x
    formatter0 = EngFormatter(unit='s')
    plt.gca().xaxis.set_major_formatter(formatter0)

    # Define os limites do eixo y para -5 a 5
    plt.ylim(-6, 6)

    # Adiciona a legenda ao gráfico
    plt.legend(loc='best')

    plt.tight_layout()  # Ajusta automaticamente o layout do gráfico para evitar sobreposições

    # Adiciona a grade ao gráfico
    plt.grid(True)

    # Verifica se o diretório "static/images" existe, se não, cria-o
    if not os.path.exists("webserver/website/static/images"):
        os.makedirs("webserver/website/static/images")

    # Salva o gráfico como uma imagem dentro do diretório "static/images"
    if graphtype == 'meiaonda':
        plt.savefig("webserver/website/static/images/meia_onda.png")
    elif graphtype == 'LPF':
        plt.savefig("webserver/website/static/images/filtro_passa-baixo.png")
    elif graphtype == 'HPF':
        plt.savefig("webserver/website/static/images/filtro_passa-alto.png")

    # Limpa a figura
    plt.clf()


############################################
# Configuração do gerador de sinal para a rectificação de onda completa
############################################
def config_func_generatorMSO():
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

        # o gerador pode ser feito o release - está nos comentários da biblioteca
        # a PS não  

    except PyVirtualBenchException as e:
            print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        virtualbench.release()

def config_mso_ondacompleta(onda_entrada:bool, onda_saida:bool):
    try:
        virtualbench = PyVirtualBench('VB8012-30A210F')        

        mso = virtualbench.acquire_mixed_signal_oscilloscope()

        # Configure the acquisition using auto setup
        mso.auto_setup()
        # cANAL 1 - DESACTIVADO PAA PODER LER SÓ O CANAL 2	
        mso.configure_analog_channel('VB8012-30A210F/mso/1', False, 10, 1, 1, 0)


        ##################################
        # AO QUE PARECE PARA QUE DESTA FORMA A LEITURA SEJA FEITA CORRETAMENTE
        # É NECESSÁRIO QUE O CANAL 1 ESTEJA LIGADO DIRETAMENTE AO CANAL DOIS
        # E DESACTIVADO COM A LINHA ACIMA
        ##################################



        # Query the configuration that was chosen to properly interpret the data.
        # POVAVELMENTE ISTO PODE SALTAR FORA - PARTE-SE DUM PRINCÍPIO QUE AMBAS AS PONTAS
        # ESTÃO SEMPRE LIGADAS AO VIRTUAL BENCH
        sample_rate, acquisition_time, pretrigger_time, sampling_mode = mso.query_timing()
        channels = mso.query_enabled_analog_channels()
        channels_enabled, number_of_channels = virtualbench.collapse_channel_string(channels)
        
        # Start the acquisition.  Auto triggering is enabled to catch a misconfigured trigger condition.
        mso.run()

        # Read the data by first querying how big the data needs to be, allocating the memory, and finally performing the read.
        analog_data, analog_data_stride, analog_t0, digital_data, digital_timestamps, digital_t0, trigger_timestamp, trigger_reason = mso.read_analog_digital_u64()
        analog_data_size = len(analog_data)
        number_of_analog_samples_acquired = analog_data_size / analog_data_stride
        print("Número de amostras: ", number_of_analog_samples_acquired)

        frequency = 50 # Frequência da rede elétrica
        increment = 1/(frequency*number_of_analog_samples_acquired)
        x_values_increment = np.cumsum(np.full(int(number_of_analog_samples_acquired/2), increment))
        print("comprimento_x_values: ", len(x_values_increment))

        if onda_entrada == True: # A função foi chamada para medir a onda de entrada. É atribuído o valor 1 ao canal 1 e 0 ao canal 2
            #channel_number = 1 # Somente para fazer a leitura do canal 1
            plot_graphic_ondacompleta(analog_data, x_values_increment, 1)
        if onda_saida == True: # A função foi chamada para medir a onda de saída
            #channel_number = 2 # Somente para fazer a leitura do canal 2
            plot_graphic_ondacompleta(analog_data, x_values_increment, 2)
        
        #print_digital_data(digital_data, digital_timestamps, 10)
        #ps.release()
        mso.release()
    except PyVirtualBenchException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        virtualbench.release()

def plot_graphic_ondacompleta(analog_data, x_values_increment, channel_number):
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

    #####################################
    # 06/06 - FUNCIONA SÓ COM O CANAL 1 LIGADO
    # APARENTEMENTE NÃO FUNCIONA SÓ COM O CANAL 2 LIGADO
    #  O NÚMERO DE AMSOSTRAS SÓ É IGUAL QUANDO ESTÁ O CANAL UM LIGADO
    #####################################


     # Verifica se o diretório "static/images" existe, se não, cria-o
    images_dir = "webserver/website/static/images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
      # Caminho completo do arquivo
    pickle_file_path = os.path.join(images_dir, "onda-completa.pickle")
    png_file_path = os.path.join(images_dir, "onda-completa.png")

    if channel_number == 1: # Apenas o canal 1 está activo
         # Cria o gráfico
        # Cria o gráfico com duas curvas
        #x_values_increment = 2 * x_values_increment # ALDRABICE!!! Será!? Ajustar a escala????
        #plt.plot(x_values_increment, analog_data[0::2], label='Onda de entrada', marker=',')
        # Salva o gráfico atual em um arquivo
        print("Número de amostras: ", len(analog_data[0::2]))
        with open(pickle_file_path, 'wb') as f:
            #pickle.dump(analog_data[0::2], f)
            pickle.dump(analog_data[0::2], f)
            pickle.dump(x_values_increment, f)
        plt.close() # Fecha o gráfico para libertar recursos
       
    elif channel_number == 2: # Apenas o canal 2 está activo
        # Cria o gráfico
        # Cria o gráfico com duas curvas
        #x_values_increment = 8 * x_values_increment # ALDRABICE!!! Será!? Ajustar a escala????
        # Carregue o gráfico do arquivo pickle
        with open(pickle_file_path, 'rb') as f:
            data = pickle.load(f)
            data_increment = pickle.load(f)
            # Adicione o novo plot ao gráfico carregado
        #plt.figure(fig.number)  # Certifique-se de que o novo plot seja adicionado à figura carregada
            plt.plot(4*data_increment, data, label='Vin', marker=',')
    
        plt.plot(4*x_values_increment, analog_data[1::2], label='Vout', marker=',')
        # A multiplicação do 4 é para ajustar o valor da escala e tem a ver com o cálculo do incremento e
        # o facto de o VB ou a libraria gravar no mesmo array os valores dos dois canais

        plt.legend()  # Adicione a legenda para ambos os plots

        frequency = 50 # Frequência da rede elétrica
        formatter_freq = EngFormatter(unit='Hz')
        frequency_text = formatter_freq.format_data_short(frequency)  # Formate a frequência truncada usando o EngFormatter        
        plt.text(0, -4, 'f= ' + frequency_text, fontsize=12, color='red') 

        plt.xlabel('Time (Seg)')
        plt.ylabel('Voltage (V)')
        plt.title('Rectificador onda completa')

        # Define os valores específicos para o eixo x (frequência) e rotaciona os rótulos
        plt.xticks(rotation=45)

        # Define o EngFormatter para o eixo x
        formatter0 = EngFormatter(unit='s')
        plt.gca().xaxis.set_major_formatter(formatter0)

        # Define os limites do eixo y para -5 a 5
        plt.ylim(0, 15)

        # Adiciona a legenda ao gráfico
        plt.legend(loc='best')

        plt.tight_layout()  # Ajusta automaticamente o layout do gráfico para evitar sobreposições

        # Adiciona a grade ao gráfico
        plt.grid(True)
        # Salve o gráfico atualizado como uma imagem PNG
        plt.savefig(png_file_path)
        plt.close()
        # Apaga o arquivo pickle após o uso para evitar reutilização
        os.remove(pickle_file_path)
        # Renomeia o arquivo pickle após o uso
        #os.remove(pickle_file_path, os.path.join(images_dir, "onda-completa.pickle"))


        #FUNCIONA CM OS DOIS CANAIS LIGADOS

def config_instruments_PassFilters(frequency:float, Resistance:int, Capacitor:int, which_filter:str):
    try:
        virtualbench = PyVirtualBench('VB8012-30A210F')
        
        #############################
        # Waveform Configuration - Configuração do gerador de sinal
        #############################
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
        
        configRelays.config_relays_PassFilter(0, 0, which_filter) # Independentemente do seu estado, coloca os relés a zero
        configRelays.config_relays_PassFilter(Resistance, Capacitor, which_filter) # Configura os relés para a medição
        
        mso = virtualbench.acquire_mixed_signal_oscilloscope()

        # Configure the acquisition using auto setup
        mso.auto_setup()

        # Query the configuration that was chosen to properly interpret the data.
        sample_rate, acquisition_time, pretrigger_time, sampling_mode = mso.query_timing()
        channels = mso.query_enabled_analog_channels()
        channels_enabled, number_of_channels = virtualbench.collapse_channel_string(channels)
        
        # Start the acquisition.  Auto triggering is enabled to catch a misconfigured trigger condition.
        mso.run() 
        
        # Read the data by first querying how big the data needs to be, allocating the memory, and finally performing the read.
        analog_data, analog_data_stride, analog_t0, digital_data, digital_timestamps, digital_t0, trigger_timestamp, trigger_reason = mso.read_analog_digital_u64()

        analog_data_size = len(analog_data)
        number_of_analog_samples_acquired = analog_data_size / analog_data_stride
              
        plot_graphic(analog_data, number_of_analog_samples_acquired, frequency, which_filter)
        #print_digital_data(digital_data, digital_timestamps, 10)
        
        ps.enable_all_outputs(False) # Desliga a fonte de alimentação
        ps.release()
        mso.release()
        fgen.release()
    except PyVirtualBenchException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        virtualbench.release()

def bode_graphic_Filters(Resistance:int, Capacitor:int, which_filter:str):
    try:
        
        '''
        Explicação das Modificações
        Gerar Frequências com np.logspace:

        np.logspace(np.log10(start_freq), np.log10(stop_freq), num=num_points) gera num_points frequências logaritmicamente espaçadas entre start_freq e stop_freq.
        Iterar sobre as Frequências:

        Em vez de calcular cada frequência dentro do loop, você itera diretamente sobre as frequências geradas por np.logspace.
        Coleção de Máximos:

        Você coleta os valores máximos correspondentes às frequências geradas no loop.
        Vantagens
        Simplicidade: O código é mais direto e legível.
        Performance: Usar np.logspace pode ser mais eficiente do que calcular manualmente cada frequência dentro de um loop.
        Manutenção: É mais fácil ajustar a faixa de frequências alterando os parâmetros de np.logspace.
        Usar np.logspace é geralmente uma abordagem melhor para gerar uma série de frequências logarítmicas, especialmente quando a simplicidade e a eficiência são desejáveis.
        '''
                
        # Defina o número de pontos por década e a faixa de frequências
        points_per_decade = 5 #Padrão ISO 12 pontos por década
        start_freq = 50  # Frequência inicial
        stop_freq = 1e6  # Frequência final
        num_points = int(np.log10(stop_freq / start_freq) * points_per_decade)

        # Gerar frequências espaçadas logaritmicamente
        frequencies = np.logspace(np.log10(start_freq), np.log10(stop_freq), num=num_points)
        max_vout_values = []
                
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
        
        configRelays.config_relays_PassFilter(0, 0, which_filter) # Independentemente do seu estado, coloca os relés a zero
        configRelays.config_relays_PassFilter(Resistance, Capacitor, which_filter) # Configura os relés para a medição
        if which_filter == "HPF":
            file_name = "webserver/website/static/images/bode_hpf.png"
            plt.title('Diagrama de Bode - Passa-Alto')

        elif which_filter == "LPF":
            file_name = "webserver/website/static/images/bode_lpf.png"
            plt.title('Diagrama de Bode - Passa-Baixo')
        
        #############################
        # Waveform Configuration - Configuração do gerador de sinal
        #############################
        waveform_function = Waveform.SINE
        amplitude = 10.0      # 10V - Valor PICO-a-PICO, não PICO
        vin = 5.0
        dc_offset = 0.0       # 0V
        duty_cycle = 50.0     # 50% (Used for Square and Triangle waveforms)

        # You will probably need to replace "myVirtualBench" with the name of your device.
        # By default, the device name is the model number and serial number separated by a hyphen; e.g., "VB8012-309738A".
        # You can see the device's name in the VirtualBench Application under File->About
        
        fgen = virtualbench.acquire_function_generator()
        fgen.run()

        for frequency in frequencies:
            fgen.configure_standard_waveform(waveform_function, amplitude, dc_offset, frequency, duty_cycle)
            # Start driving the signal. The waveform will continue until Stop is called, even if you close the session.
                
            
            mso = virtualbench.acquire_mixed_signal_oscilloscope()

            # Configure the acquisition using auto setup
            mso.auto_setup()
         
            ########################################################
            # POSE-SE RETIRAR PARA ACELARAR O PROCESSO DE CONSTRUÇÃO DO GRÁFICO
            ########################################################
            
            # Query the configuration that was chosen to properly interpret the data.
            #sample_rate, acquisition_time, pretrigger_time, sampling_mode = mso.query_timing()
            #channels = mso.query_enabled_analog_channels()
            #channels_enabled, number_of_channels = virtualbench.collapse_channel_string(channels)
            
            # Start the acquisition.  Auto triggering is enabled to catch a misconfigured trigger condition.
            mso.run() 
            
            # Read the data by first querying how big the data needs to be, allocating the memory, and finally performing the read.
            analog_data, analog_data_stride, analog_t0, digital_data, digital_timestamps, digital_t0, trigger_timestamp, trigger_reason = mso.read_analog_digital_u64()
               
            #print_digital_data(digital_data, digital_timestamps, 10)
            vout_max = (max(analog_data[1::2]))
            # Armazene a frequência e o máximo correspondente
            max_vout_values.append(vout_max)
            mso.release()
            time.sleep(0.05) # Aguarde 50ms antes de passar para a próxima frequência
        Av = np.array(max_vout_values)/vin
        
        # Procurar o índice do valor mais próximo de 0.707
        idx_mais_proximo = np.argmin(np.abs(Av - 0.707))
        # Obter a frequência correspondente
        frequencia_corte_aprox = frequencies[idx_mais_proximo]
        print(f"Frequência aproximada de corte (ganho ≈ 0.707): {frequencia_corte_aprox:.2f} Hz")
        
        # Plotar o gráfico logarítmico
        plt.figure(figsize=(10, 6))
        plt.plot(frequencies, Av, '.-', label='Ganho de tensão')

        # Adicionar linha vertical no gráfico
        plt.axvline(x=frequencia_corte_aprox, color='red', linestyle='--', label=f'Frequência de corte ≈ {frequencia_corte_aprox:.1f} Hz')

        # Anotar o ponto
        plt.annotate(f'{frequencia_corte_aprox:.1f} Hz',
             xy=(frequencia_corte_aprox, 0.707),
             xytext=(frequencia_corte_aprox * 1.2, 0.75),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10,
             color='red')
        
        plt.xscale('log')
        plt.xlabel('Frequência (Hz)')
        plt.ylabel('Av')
        plt.grid(True, which='both', ls='--', lw=0.5)
        plt.legend()
        plt.ylim(0, 1)
         # Adiciona a legenda ao gráfico
        plt.legend(loc='best')

        
         # Verifica se o diretório "static/images" existe, se não, cria-o
        if not os.path.exists("webserver/website/static/images"):
            os.makedirs("webserver/website/static/images")

        # Salva o gráfico como uma imagem dentro do diretório "static/images"
        plt.savefig(file_name)

        # Limpa a figura
        plt.clf()
       
        fgen.stop()                           # <-- Primeiro paras
        fgen.release()                        # <-- Depois libertas
        ps.enable_all_outputs(False)
        ps.release()

    except PyVirtualBenchException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        virtualbench.release()
