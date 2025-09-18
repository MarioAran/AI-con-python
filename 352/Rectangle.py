class Rectangulo:
    def CalcularArea(self):
        return int(self.__base * self.__altura)
    def CalcularPerimetro(self):
        return int(2*(self.__base + self.__altura))
    def setValues(self,px,py):
        self.__x = px
        self.__y = py
    def getValues(self):
        return f"x: {self.__x} y:{self.__y}"
    def __init__(self,pbase, paltura,pcordenadas):
        self.__base= pbase
        self.__altura = paltura
        self.__cordenadas = pcordenadas
    def getcordenadas(self):
        return self.__cordenadas