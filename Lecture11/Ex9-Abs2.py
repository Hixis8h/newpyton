from abc import ABC, abstractmethod


class AbsClass(ABC):
    def print(self, value):
        print('Passed value:', value)

    @abstractmethod
    def task(self):
        pass


class TestClass(AbsClass):
    def task(self):
        print('We are inside test_class task')


class ExampleClass(AbsClass):
    def task(self):
        print('We are inside example_class task')


test_obj = TestClass()
test_obj.task()
test_obj.print(100)

example_obj = ExampleClass()
example_obj.task()
example_obj.print(200)

print('test_obj is instance of AbsClass?', isinstance(test_obj, AbsClass))
print('example_obj is instance of AbsClass?', isinstance(example_obj, AbsClass))
