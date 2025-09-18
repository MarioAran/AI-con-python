from Circle import Circulo
from Rectangle import Rectangulo
from TriangleRectangle import TrianguloRectangulo
from Cordinates import Cordenadas
cordenadasTriangulo = Cordenadas(1.1,1.2)
TrianguloRectangulo = TrianguloRectangulo(10,20,cordenadasTriangulo)
print("Triangle Area: {}".format(TrianguloRectangulo.CalcularArea()))
print("Triangle Perimeter: {:.1f}".format(TrianguloRectangulo.CalcularPerimetro()))
print(TrianguloRectangulo.getcordenadas().getter())


cordenadasRectangulo = Cordenadas(3.2,5.8)
Rectangulo = Rectangulo(5,7,cordenadasRectangulo)
print("Rectangle Area: {}".format(Rectangulo.CalcularArea()))
print("Rectangle Perimeter: {}".format(Rectangulo.CalcularPerimetro()))
print(format(Rectangulo.getcordenadas().getter()))


cordenadasCirculo = Cordenadas(1.9,10.2)
Circulo = Circulo(2,cordenadasCirculo)
print("Circle Area: {:.2f}".format(Circulo.CalcularArea()))
print("Circle Perimeter: {:.2f}".format(Circulo.CalcularPerimetro()))
print(Circulo.getcordenadas().getter())
