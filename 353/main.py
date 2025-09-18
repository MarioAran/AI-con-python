from Circle import Circulo
from Rectangle import Rectangulo
from TriangleRectangle import TrianguloRectangulo
from Cordinates import Cordenadas

triangulo_result= []
rectangulo_result=[]
circulo_result=[]

for i in range(2):
    base = int(input())
    altura = int(input())
    x = float(input())
    y = float(input())

    cordenadasTriangulo = Cordenadas(x, y)
    triangulo = TrianguloRectangulo(base, altura, cordenadasTriangulo)

    triangulo_result.append("Triangle Area: {}".format(triangulo.CalcularArea()))
    triangulo_result.append("Triangle Perimeter: {:.1f}".format(triangulo.CalcularPerimetro()))
    triangulo_result.append(triangulo.getcordenadas().getter())
for i in range(2):
    base = int(input())
    altura = int(input())
    x = float(input())
    y = float(input())

    cordenadasRectangulo = Cordenadas(x, y)
    rectangulo = Rectangulo(base, altura, cordenadasRectangulo)

    rectangulo_result.append("Rectangle Area: {} ".format(rectangulo.CalcularArea()))
    rectangulo_result.append("Rectangle Perimeter: {} ".format(rectangulo.CalcularPerimetro()))
    rectangulo_result.append(rectangulo.getcordenadas().getter())
for i in range(2): 
    radio = int(input())
    x = float(input())
    y = float(input())

    cordenadasCirculo = Cordenadas(x, y)
    circulo = Circulo(radio, cordenadasCirculo)

    circulo_result.append("Circle Area: {:.2f} ".format(circulo.CalcularArea()))
    circulo_result.append("Circle Perimeter: {:.2f} ".format(circulo.CalcularPerimetro()))
    circulo_result.append(circulo.getcordenadas().getter())

for r in triangulo_result:
    print(r)
print()
for p in rectangulo_result:
    print(p)
print()
for a in circulo_result:
    print(a)    