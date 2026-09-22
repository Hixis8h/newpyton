def apply_twice(func, value):
    return func(func(value))


def increment(x):
    return x + 1


print(apply_twice(increment, 5))
