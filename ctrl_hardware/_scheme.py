import matplotlib
import schemdraw
import schemdraw.elements as elm

import threading
#import cv2

matplotlib.rcParams['svg.fonttype'] = 'none'

def main():
    R1_Value = input ("Escolha o valor da Resistência 1 - ")
    R2_Value = input ("Escolha o valor da Resistência 2 - ")

    with schemdraw.Drawing(show=False) as d:
        d.config(unit=5) #tamanho do componente
        d += (V1 := elm.SourceV().label('20V'))
        d += (R1 := elm.Resistor().right().label(R1_Value))
        d += elm.Dot()    
        d += (R2 := elm.Resistor().down().label(R2_Value, loc='bot', rotate=True))
        d += elm.Dot()    
        d.push() 
        d.pop()
        d += (L2 := elm.Line().tox(V1.start))
        d.draw()
        d.save('divisor.png')
    
main ()
