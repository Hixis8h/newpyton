class Calculate_area:
    def rectangle_area(self, width, height):
        return width * height

    @classmethod
    def triangle_area(cls, base, height):
        return 0.5 * base * height

    @staticmethod
    def circle_area(radius):
        return 3.14 * radius * radius


calculator = Calculate_area()
rectangle = calculator.rectangle_area(4, 5)
triangle = calculator.triangle_area(4, 5)
circle = calculator.circle_area(5)

print('Rectangle Area =', rectangle)
print('Triangle Area =', triangle)
print('Circle Area =', circle)
