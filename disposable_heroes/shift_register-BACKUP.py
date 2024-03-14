import RPi.GPIO as GPIO

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

import serial
import time

import sys
import cv2

import schemdraw
import schemdraw.elements as elm

import subprocess

# Resistencias:
# R1 = 470
# R2 = 1.2K
# R3 = 10K

SER = 5         # GPIO 5 - SER/DS (serial data input, SPI data)
RCLK = 6        # GPIO 6 - RCLK/STCP
SRCLK = 13      # GPIO 13 - SRCLK/SHCP (storage register clock pin, SPI clock)
SRCLR = 26      # GPIO 26 - O registo de deslocamento é limpo (ACTIVO BAIXO)

# Setup dos pinos
GPIO.setup(SER, GPIO.OUT)               
GPIO.setup(RCLK, GPIO.OUT)                     
GPIO.setup(SRCLOCK, GPIO.OUT)
GPIO.setup(SRCLR, GPIO.OUT)

# Inicializar a variavel correspondente a R1
# Reles 1 e 2
rele_1_2 = b0011

# Valor por defeito de espera nas operações do registo de deslocamento
WaitTimeSR = 0.1

# Inicaializa o pino de clear dos registos a 1 - o clear é controlado e feito numa função
GPIO.output(SRCLR, 1)


# Caminho para o visualizador de imagens (pode variar dependendo do seu sistema operacional)
visualizador = "xdg-open"  # Linux
# visualizador = "open"  # macOS
# vi

import warnings
warnings.filterwarnings("ignore")

#arduino = serial.Serial (port='/dev/ttyACM1', baudrate='9600')
#time.sleep(2)

# Caminho para o visualizador de imagens (pode variar dependendo do seu sistema operacional)
visualizador = "xdg-open"  # Linux
# visualizador = "open"  # macOS
# visualizador = "start"  # Windows

def main():
    # Escolha do valor da resistência
    # Não sai do ciclo enquanto não for feita uma escolha válida
    print("Para o estudo da Lei de Ohm escolha uma das três resistências:")
    print("- 470 Ohm")
    print ("- 1.2K")
    print ("- 10K")

    while True:
        try:
            R1_Value = input("Escolha o valor da Resistência - ")

            # Validação da escolha
            if R1_Value in ("470", "1K2", "10K"):
                caminho_imagem = "esquemaOhm.png"
                subprocess.Popen([visualizador, caminho_imagem])
                draw_schematic(R1_Value)
                # Enviar os bits para o Shift register e activar os relés 
                register_clear() # Efectua a limpeza do registo
                SRoutput(rele_1_2)
                break
            else:
                raise ValueError("Escolha não é válida")
        except ValueError as e:
            print(e)    


#if (escolha == 'R1'):
#print("escolheu R1")
#cv2.destroyAllWindows() # destroy all windows
#byte_R1 = "004002000000\n"
#arduino.write(byte_R1.encode())
#time.sleep(0.5)
#arduino.close

def draw_schematic(R1_Value):
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=5) #tamanho do componente
        # Adicionando os elementos
        d += (V1 := elm.SourceV().label('Vin'))
        d += (I1 := elm.MeterA().right().label('Amp'))
        d += elm.Dot()
        d.push()
        d += (R1 := elm.Resistor().down().label(R1_Value, loc='bot'))
        d += elm.Dot()
        d.pop()
        d += (L1 := elm.Line())
        d += (Vol := elm.MeterV().down().label('Volt', loc='bot', rotate=True))
        d += (L2 := elm.Line().tox(V1.start))            
        #d.draw()
        d.save('esquemaOhm.png')

# Funcao que limpa o registo
def register_clear ()
    GPIO.output(SRCLR, 0) # É feito o clear
    time.sleep(waitTimeSR) # espera 100ms
    GPIO.output(SRCLR, 1)

# Função que verifica e desloca os bits para armazenar no registo de deslocamento
def SRoutput(bit_Reles):
    for i in range(4):
        checkshift = shiftnum & 1
        if checkshift == 1:
            WriteReg (checkshift, WaitTimeSR)
        else:
            WriteReg(checkshift, WaitTimeSR)
    shiftnum = shiftnum >> 1


# Definição da função que envia os dados para o registo de deslocamento,
# segundo o algoritmo descrito em baixo

### ALGORITMO ###
# Enviar um bit para o pino SER/DS
### Depois de enviado, é dado um impulso de clock (SRCLK/SHCP) e o bit armazenado nos registos
###### ... um segundo bit é enviado, repetindo os dois passos em cima - É repetido até estarem armazenados 8 bits
######### Por ultimo é dado um impulso aos registos (RCLK/STCP) para obter os 8 bits na saida

def WriteReg (WriteBit, WaitTimeSR):
    GPIO.output (SER,WriteBit) # Envia o bit 1 para o registo
    # Clock - flanco POSITIVO
    time.sleep (WaitTimeSR) # Espera 100ms
    GPIO.output(SRCLK, 0)
    time.sleep (WaitTimeSR) # Espera 100ms
    GPIO.output(SRCLK,1)
    time.sleep(WaitTimeSR) # Espera 100ms
    # Armazenar o valor no registo
    GPIO.output(RCLK, 0)
    time.sleep(WaitTimeSR) # Espera 100ms
    GPIO.output(RCLK, 1)

if __name__ == "__main__":
    main()
