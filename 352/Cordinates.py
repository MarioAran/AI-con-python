class Cordenadas:
    def __init__(self,px="",py=""):
        self.__x = px 
        self.__y = py
    def getter(self):
        return f"x:{self.__x} y:{self.__y}\n"
    def setter(self,px="",py=""):
        self.__x = px 
        self.__y = py