class Employee:
    def __init__(self):
        self.name = 'Peter'
        self._age = 45
        self.__salary = 35000


employee = Employee()
print(employee.name)
print(employee._age)

# Name mangling allows internal access to the private attribute.
print(employee._Employee__salary)
