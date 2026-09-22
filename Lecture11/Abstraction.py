from abc import ABC, abstractmethod


class Employee(ABC):
    @abstractmethod
    def emp_id(self):
        pass


class ChildEmployee(Employee):
    def emp_id(self):
        print('emp_id is 12345')


employee = ChildEmployee()
employee.emp_id()
