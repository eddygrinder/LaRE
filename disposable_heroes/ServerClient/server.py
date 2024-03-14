import socket
import time
from threading import Timer

def background_controller():
       message = "Hello client"
       print (message)
       clientsocket.send(bytes(message, "utf-8"))
       time.sleep(5)

def start_server():
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.bind(('localhost', 5000))  # Binding to localhost on port 5000
       s.listen(5)
       print('Server is now running')
       
       while  True:
              clientsocket, address = s.accept()
              print(f"Connection from (address) has been established.")
              Timer(1, background_controller, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()