import os, sys

ctrl_hardware_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ctrl_hardware'))
sys.path.append(ctrl_hardware_path)

#from controlVB import read_Vcc_R
from website import create_app
from flask import send_from_directory

app = create_app()
app.config['SECRET_KEY'] = 'thisisasecretkey'

# Rota definida para imagens da página
@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("static/images", filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #defenido para executar em todos os ip's disponíveis pela rede
