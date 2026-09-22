class Dog:
    species = 'mammal'

    def __init__(self, name, age):
        self.name = name
        self.age = age


dog1 = Dog('Philo', 5)
dog2 = Dog('Mikey', 6)

print(f'{dog1.name} is {dog1.age} and {dog2.name} is {dog2.age}.')
if dog1.species == 'mammal':
    print(f'{dog1.name} is a {dog1.species}!')
