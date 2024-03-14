import subprocess

# Caminho para o visualizador de imagens (pode variar dependendo do seu sistema operacional)
visualizador = "xdg-open"  # Linux
# visualizador = "open"  # macOS
# visualizador = "start"  # Windows

# Caminho para a imagem que você deseja abrir
caminho_imagem = "divisor.png"

# Inicia o subprocesso para abrir a imagem
subprocess.Popen([visualizador, caminho_imagem])

# O programa continuará a execução a partir daqui
print("O programa continuou a execução após abrir a imagem.")
