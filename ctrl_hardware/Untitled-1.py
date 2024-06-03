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

from pyvirtualbench import PyVirtualBench, PyVirtualBenchException, Waveform, MsoSamplingMode
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import numpy as np

import os, sys, pickle

# Verifica se o diretório "static/images" existe, se não, cria-o
if not os.path.exists("webserver/website/static/images"):
    os.makedirs("webserver/website/static/images")

    # Caminho completo do arquivo
pickle_file_path = os.path.join("webserver/website/static/images", "onda-completa.pickle")
png_file_path = os.path.join("webserver/website/static/images", "onda-completa.png")

with open(pickle_file_path, 'rb') as f:
            fig = pickle.load(f)
            # Adicione o novo plot ao gráfico carregado
            plt.figure(fig.number)  # Certifique-se de que o novo plot seja adicionado à figura carregada
            plt.legend()  # Adicione a legenda para ambos os plots
                
            plt.xlabel('Time (Seg)')
            plt.ylabel('Voltage (V)')
            plt.title('Rectificador onda completa')

            # Define os valores específicos para o eixo x (frequência) e rotaciona os rótulos
            plt.xticks(rotation=45)

            # Define o EngFormatter para o eixo x
            formatter0 = EngFormatter(unit='s')
            plt.gca().xaxis.set_major_formatter(formatter0)

            # Define os limites do eixo y para -5 a 5
            plt.ylim(-15, 15)

            # Adiciona a legenda ao gráfico
            plt.legend(loc='best')

            plt.tight_layout()  # Ajusta automaticamente o layout do gráfico para evitar sobreposições

            # Adiciona a grade ao gráfico
            plt.grid(True)
            # Salve o gráfico atualizado como uma imagem PNG
            fig.savefig(png_file_path)
        