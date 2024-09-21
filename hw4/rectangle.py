class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)

    def __str__(self):
        return f"Rectangle(length={self.length}, width={self.width})"

rectangle1 = Rectangle(5, 3)
print(rectangle1.area())
