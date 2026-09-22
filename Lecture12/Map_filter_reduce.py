from functools import reduce

# List of numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Using map to square each number
squared_numbers = map(lambda x: x ** 2, numbers)

# Using filter to keep only even numbers
even_squared_numbers = filter(lambda x: x % 2 == 0, squared_numbers)

# Using reduce to sum the even squared numbers
sum_of_even_squared_numbers = reduce(
    lambda x, y: x + y,
    even_squared_numbers,
)

print(sum_of_even_squared_numbers)
