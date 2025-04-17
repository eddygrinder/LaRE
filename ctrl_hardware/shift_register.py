#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random, socket, time
#import os, sys, requests



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
            config_Relays("1011010010000") # Relés - K1...|K9 - R=1K e C=3.3uF
        case 2, 1:
            # Resistência = 10KOhm e Capacitância = 1uF
            config_Relays("00000000") # Relés - K1...|K9 - R=10K e C=1uF
        case 2, 2:
            # Resistência = 10KOhm e Capacitância = 3.3uF
            config_Relays("1011001010000") # Relés - K1...|K9 - R=10K e C=3.3uF
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

def config_Relays(stringValue: str):
    # Envia a string para o Raspberry Pi
    # Endereço IP e porta do Raspberry Pi
    HOST = '192.168.1.77'  # Substitua pelo endereço IP do Raspberry Pi
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