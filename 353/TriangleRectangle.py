import math
from Figure import Figura

class TrianguloRectangulo(Figura):
    def CalcularArea(self):
        return (self.__base*self.__altura)/2
    def CalcularPerimetro(self):
        hipotenusa = (math.sqrt(self.__base**2 + self.__altura **2))
        return self.__base+self.__altura+hipotenusa
    def __init__(self,pbase, paltura,pcordenadas):
        Figura.__init__(self,pcordenadas)        
        self.__base= pbase
        self.__altura = paltura
    def getcordenadas(self):
        return super().getcordenadas()