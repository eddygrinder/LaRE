import os, sys, socket

ctrl_hardware_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ctrl_hardware'))
sys.path.append(ctrl_hardware_path)

#from controlVB import read_Vcc_R
from website import create_app
from flask import send_from_directory
from waitress import serve

app = create_app()
app.config['SECRET_KEY'] = 'thisisasecretkey'

# Rota definida para imagens da página
@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("static/images", filename)

# ===================== MAIN =====================

if __name__ == "__main__":
    host = '0.0.0.0'   # Permite acesso de outras máquinas da rede
    port = 5000
    threads = 8        # Número de threads para processar múltiplas requisições

    # Descobre o IP local da máquina
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print("="*50)
    print(f"Servidor Flask a correr com Waitress")
    print(f"Aceder localmente: http://127.0.0.1:{port}")
    print(f"Aceder na rede local: http://{local_ip}:{port}")
    print("="*50)

    serve(app, host=host, port=port, threads=threads)