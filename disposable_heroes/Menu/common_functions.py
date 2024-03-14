# common_functions.py

import subprocess
import schemdraw
from schemdraw import elements as elm

class CommonFunctions: 
    def option_output(self, option):
        self.draw_scheme(option)
        caminho_imagem = "esquemaOhm.jpg"
        subprocess.Popen([visualizador, caminho_imagem], shell=True)

    def draw_scheme(self, option):
        with schemdraw.Drawing(show=False) as d:
            d.config(unit=5) #tamanho do componente
            # Adicionando os elementos
            d += (V1 := elm.SourceV().label('Vin'))
            d += (I1 := elm.MeterA().right().label('Amp'))
            d += elm.Dot()
            d.push()
            d += (R1 := elm.Resistor().down().label(option, loc='bot'))
            d += elm.Dot()
            d.pop()
            d += (L1 := elm.Line())
            d += (Vol := elm.MeterV().down().label('Volt', loc='bot', rotate=True))
            d += (L2 := elm.Line().tox(V1.start))            
            #d.draw()
            d.save('esquemaOhm.jpg')
           
