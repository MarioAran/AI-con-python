import math 
from Figure import Figura

class Circulo(Figura):
    def CalcularArea(self):
        return math.pi * self.__radio**2
    def CalcularPerimetro(self):
        return 2*math.pi*self.__radio
    def setValues(self,px,py):
        self.__x = px
        self.__y = py
    def getValues(self):
        return f"x: {self.__x} y:{self.__y}"
    def __init__(self,radio,pcordenadas):
        Figura.__init__(self,pcordenadas)
        self.__radio = radio
    def getcordenadas(self):
        return super().getcordenadas()