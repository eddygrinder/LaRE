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

import random, socket

import os, sys, requests

# Caminho para o diretório ctrl_hardware
ctrl_hardware_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ctrl_hardware'))
# Adiciona o diretório ao sys.path
sys.path.append(ctrl_hardware_path)

#from shift_register import SRoutput

# This examples demonstrates how to make measurements using the Power

def config_Parameters (Vcc: int, Resistance: int, measeure_parameter: str):
    Vcc = int(Vcc) # É passado o parâmetro em forma de string mas é necessária a conversão para int

    if measeure_parameter == "voltage":
        print("Voltage measurement")
    elif measeure_parameter == "current":
        print("Current measurement")
    
    
    measurement_result = Vcc*random.uniform(1, 5)
    measurement_result = Vcc*random.uniform(1, 5)

    print("Measurement: %f V" % (Vcc))
    print("Measurement: %f V" % (measurement_result))
    #print("Measurement: %f KOhm" % (Resistence))
    
    config_Relays(Resistance)

    return measurement_result

def config_Relays(Resistance: int):
    stringValue = "11011"
            # Endereço IP e porta do Raspberry Pi
    HOST = '192.168.1.75'  # Substitua pelo endereço IP do Raspberry Pi
    PORT = 12345  # Porta de escuta no Raspberry Pi

    match Resistance:
        case 0:
            print("ERROR: Resistence is 0")
            stringValue = "000" # Valor de resistência inválido - relés OBRIGATORIAMENTE desligados

        case 1:
            Resistance = 1
            stringValue = "100"
        
        case 2:
            Resistance = 1.5
            stringValue = "010"
        
        case 3:
            Resistance = 2.2
            stringValue = "001"

        case _:
            print("ERROR: Resistence is not 1, 1.5 or 2.2 KOhm")
    
        # Criar um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conectar-se ao servidor (Raspberry Pi)
        s.connect((HOST, PORT))
        
        # Enviar a mensagem
        s.sendall(stringValue.encode())
        
        print("Mensagem enviada com sucesso.")