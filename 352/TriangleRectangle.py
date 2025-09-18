import math
class TrianguloRectangulo:
    def CalcularArea(self):
        return (self.__base*self.__altura)/2
    def CalcularPerimetro(self):
        hipotenusa = (math.sqrt(self.__base**2 + self.__altura **2))
        return self.__base+self.__altura+hipotenusa
    def __init__(self,pbase, paltura,pcordenadas):
        self.__base= pbase
        self.__altura = paltura
        self.__cordenadas = pcordenadas
    def getcordenadas(self):
        return self.__cordenadas