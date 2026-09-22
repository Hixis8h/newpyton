class Employee:
    def __init__(self):
        self.__maxearn = 30000

    def earn(self):
        print(f'earning is:{self.__maxearn}')

    def setmaxearn(self, earn):
        self.__maxearn = earn


employee = Employee()
employee.earn()
employee.setmaxearn(15000)
employee.earn()
