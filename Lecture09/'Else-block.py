def divide (a,b):
    return a / b
a , b = map(int , input().split())
print(divide(a,b))
print("End of program")

def divide(a,b):
    try:
        result = a / b
    except ZeroDivisionError as e:
        print("Exception: ", e)
    else:
        return result
a , b = map(int,input().split())

print(divide(a , b))
print("End of program")