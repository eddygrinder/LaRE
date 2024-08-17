#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random, socket, time
#import os, sys, requests

#from shift_register import SRoutput
# This examples demonstrates how to make measurements using the Power
def config_relays_ohm (Resistance: int, measeure_parameter: str):
    if measeure_parameter == "voltage":
        match Resistance:
            case 0:
                print("ERROR: Resistence is 0")
                config_Relays("00000000") # Valor de resistência inválido - relés OBRIGATORIAMENTE desligados
            case 1:
                Resistance = 1
                config_Relays("10011011") # Relés - K1...|K8
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

def config_relays_meiaonda (Resistance: int, Capacitance: int):
    match Resistance, Capacitance:
        case 0, 0:
            # colocar os relés a zero
            config_Relays("0000000000000") #relés OBRIGATORIAMENTE desligados
        case 1, 1:
            # Resistência = 1KOhm e Capacitância = 1uF
            #config_Relays("010101101") # Relés - K1...|K9 - R=1K e C=1uF
            config_Relays("1011010100000") # Relés - K1...|K9 - R=1K e C=1uF

        case 1, 2:
            # Resistência = 1KOhm e Capacitância = 3.3uF
            config_Relays("101101001") # Relés - K1...|K9 - R=1K e C=3.3uF
        case 2, 1:
            # Resistência = 10KOhm e Capacitância = 1uF
            config_Relays("101100110") # Relés - K1...|K9 - R=10K e C=1uF
        case 2, 2:
            # Resistência = 10KOhm e Capacitância = 3.3uF
            config_Relays("101100101") # Relés - K1...|K9 - R=10K e C=3.3uF
        case _:
            print("ERROR: Resistence or Capacitance outside values")

def config_relays_ondacompleta (Resistance: int, Capacitance: int):
    match Resistance, Capacitance:
        case 0, 0:
            # colocar os relés a zero
            config_Relays("000000000000") #relés OBRIGATORIAMENTE desligados
        case 1, 1:
            # Resistência = 1KOhm e Capacitância = 1uF
            #config_Relays("010101101") # Relés - K1...|K9 - R=1K e C=1uF
            config_Relays("010011010000") # Relés - K1...|K9 - R=1K e C=1uF

        case 1, 2:
            # Resistência = 1KOhm e Capacitância = 3.3uF
            config_Relays("010010110000") # Relés - K1...|K9 - R=1K e C=3.3uF
        case 2, 1:
            # Resistência = 10KOhm e Capacitância = 1uF
            config_Relays("010010101000") # Relés - K1...|K9 - R=10K e C=1uF
        case 2, 2:
            # Resistência = 10KOhm e Capacitância = 3.3uF
            config_Relays("010011001000") # Relés - K1...|K9 - R=10K e C=3.3uF
        case _:
            print("ERROR: Resistence or Capacitance outside values")

def config_relays_passaalto (Resistance: int, Capacitance: int):
    match Resistance, Capacitance:
        case 0, 0:
            # colocar os relés a zero
            config_Relays("0000000000000") #relés OBRIGATORIAMENTE desligados
        case 1, 1:
            # Resistência = 1KOhm e Capacitância = 1uF
            #config_Relays("010101101") # Relés - K1...|K9 - R=1K e C=1uF
            config_Relays("100101000010") # Relés - K1...|K9 - R=1K e C=1uF

        case 2, 1:
            # Resistência = 1KOhm e Capacitância = 3.3uF
            config_Relays("1001001000010") # Relés - K1...|K9 - R=1K e C=3.3uF
        case _:
            print("ERROR: Resistence or Capacitance outside values")

def config_relays_vin ():
    config_Relays("010011000000") # K12 Activo para ler vin

def config_Relays(stringValue: str):
    # Envia a string para o Raspberry Pi
    # Endereço IP e porta do Raspberry Pi
    HOST = '192.168.1.75'  # Substitua pelo endereço IP do Raspberry Pi
    PORT = 12345  # Porta de escuta no Raspberry Pi 
    
        # Criar um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conectar-se ao servidor (Raspberry Pi)
        s.connect((HOST, PORT))
        
        # Enviar a mensagem
        s.sendall(stringValue.encode())
        print("Mensagem enviada com sucesso.")

       # Espera pela resposta do servidor
        while True:
            data = s.recv(1024)
            if not data:
                break
            response = data.decode()
            if response == 'True':  # Espera por uma confirmação específica do servidor
                print("Confirmação recebida do servidor:", response)
                break
# Receber a resposta
'''
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
'''