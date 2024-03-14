import schemdraw
import schemdraw.elements as elm

import threading

def draw_scheme(option):
    print(option)
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
        d.draw()
        d.save('esquemaOhm.png')

#if __name__ != "__main__":
#    draw_scheme(option)
    #GPIO.cleanup()