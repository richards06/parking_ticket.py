from abc import ABC, abstractmethod
import math

class BasicShape(ABC):
    
    def __init__(self):
        self._area = 0.0
        self._name = ""
        
    @property
    def area(self):
        return self._area
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    @abstractmethod
    def calc_area(self):
        pass
    
class Circle(BasicShape):
    
    def __init__(self, x, y, r, n="Circle"):
        super().__init__()
        self._x_center = x
        self._y_center = y
        self._radius = r
        self.name = n
        self.calc_area()
        
    def calc_area(self):
        self._area = math.pi * (self._radius ** 2)
            
    @property
    def x_center(self):
        return self._x_center
    
    @property
    def y_center(self):
        return self._y_center
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._radius = value
        self.calc_area()
        
class Rectangle(BasicShape):
    
    def __init__(self, l, w, n="Rectangle"):
        super().__init__()
        self._length = l
        self._width = w
        self.name = n
        self.calc_area()
        
    def calc_area(self):
        self._area = self._length * self._width
            
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        self._length = value
        self.calc_area()
        
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        self.calc_area()
        
class Square(Rectangle):
    
    def __init__(self, s, n="Square"):
        self._side = s
        super().__init__(s, s, n)
        self.name = n
        
    @property
    def side(self):
        return self._side
    
    @side.setter
    def side(self, value):
        self._side = value
        self._length = value
        self._width = value
        self.calc_area()
        
if __name__ == "__main__":
    
    shapes = []
    
    shapes.append(Rectangle(10, 20, "Rectangle_1"))
    shapes.append(Rectangle(20,30, "Rectangle_2"))
    shapes.append(Circle(0, 0, 4, "Circle_1"))
    shapes.append(Circle(5, 5, 9, "Circle_2"))
    shapes.append(Square(10, "Square"))
    
print("--- Polymorphism check ---")
for shape in shapes:
    print(f"{shape.name} Area = {shape.area}")
    
print("\n--- Getter/setter check ---")

circle = shapes[2]
print(f"{circle.name} Current: {circle.radius} {circle.area}")
circle.radius = circle.radius * 2
print(f"{circle.name} Doubled: {circle.radius} {circle.area}")

rect = shapes[0]
print(f"{rect.name} Current: {rect.length} {rect.width} {rect.area}")
rect.length *= 2
rect.width *= 2
print(f"{rect.name} Doubled: {rect.length} {rect.width} {rect.area}")

square = shapes[4]
print(f"{square.name} Current: {square.side} {square.area}")
square.side *= 2
print(f"{square.name} Doubled: {square.side} {square.area}")

