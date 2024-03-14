import socket

def config_Relays(Resistence: int):
    stringValue = "11011"
            # Endereço IP e porta do Raspberry Pi
    HOST = '192.168.1.75'  # Substitua pelo endereço IP do Raspberry Pi
    PORT = 12345  # Porta de escuta no Raspberry Pi

    match Resistence:
        case 0:
            print("ERROR: Resistence is 0")
            stringValue = "000" # Valor de resistência inválido - relés OBRIGATORIAMENTE desligados

        case 1:
            Resistence = 1
            stringValue = "100"
        
        case 2:
            Resistence = 1.5
            stringValue = "010"
        
        case 3:
            Resistence = 2.2
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