import subprocess

def main:
    # Caminho para o visualizador de imagens (pode variar dependendo do seu sistema operacional)
    #visualizador = "xdg-open"  # Linux
    # visualizador = "open"  # macOS
    visualizador = "notepad"  # Windows

    # Caminho para a imagem que você deseja abrir
    caminho_imagem = "esquemaOhm.png"

    # Inicia o subprocesso para abrir a imagem
    subprocess.Popen([visualisador, caminho_imagem])

    # O programa continuará a execução a partir daqui
    print("O programa continuou a execução após abrir a imagem.")

if __name__ == "__main__":
    main()