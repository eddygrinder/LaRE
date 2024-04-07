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

import random, socket, time
import os, sys, requests

#from shift_register import SRoutput
# This examples demonstrates how to make measurements using the Power
def config_Parameters (Resistance: int, measeure_parameter: str):
    if measeure_parameter == "voltage":
        match Resistance:
            case 0:
                print("ERROR: Resistence is 0")
                config_Relays("00000000") # Valor de resistência inválido - relés OBRIGATORIAMENTE desligados
            case 1:
                Resistance = 1
                config_Relays("10011011") # Relés - K1...|K8
                #config_Relays("11011001") # Relés - K8...|K1
                # Atraso para medição?
                # time.sleep(1)
            case 2:
                Resistance = 1.5
                config_Relays("01011011")
                # Atraso para medição?
                # time.sleep(1)
            case 3:
                Resistance = 2.2
                config_Relays("00111011")
                #config_Relays("11011100")

                # Atraso para medição?  
                # time.sleep(1)
            case _:
                print("ERROR: Resistence is not 1, 1.5 or 2.2 KOhm")

    elif measeure_parameter == "current":
        match Resistance:
            case 0:
                print("ERROR: Resistence is 0")
                config_Relays("00000000") # Valor de resistência inválido - relés OBRIGATORIAMENTE desligados
            case 1:
                Resistance = 1
                config_Relays("10010110")
                print("Atraso para medição?")
                # time.sleep(1)            
            case 2:
                Resistance = 1.5
                config_Relays("01010110")
                # Atraso para medição?
                # time.sleep(1)            
            case 3:
                Resistance = 2.2
                config_Relays("00110110")
                # Atraso para medição?
                # time.sleep(1)
            case _:
                print("ERROR: Resistence is not 1, 1.5 or 2.2 KOhm")
    

def relays_requests(stringValue: str):
    # Envia a string para o Raspberry Pi
    # Endereço IP e porta do Raspberry Pi
    url = "http://192.168.1.71/endpoint"
    string = stringValue
    data = {"string": string}
    # Envia a requisição usando o dicionário
    response = requests.post(url, data)
    if response.status_code == 200:
        print("Requisição enviada com sucesso!")
    else:
        print("Erro ao enviar requisição:", response.status_code)

def config_Relays(stringValue: str):
    # Envia a string para o Raspberry Pi
    # Endereço IP e porta do Raspberry Pi
    HOST = '172.16.0.11'  # Substitua pelo endereço IP do Raspberry Pi
    PORT = 12345  # Porta de escuta no Raspberry Pi 
    
        # Criar um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conectar-se ao servidor (Raspberry Pi)
        s.connect((HOST, PORT))
        
        # Enviar a mensagem
        s.sendall(stringValue.encode())
        print("Mensagem enviada com sucesso.")

# Receber a resposta
