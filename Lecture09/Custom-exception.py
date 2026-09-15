class NagativeNumberError(Exception):
    def __intit__(self, value):
        self.value =value
        super(). __init__(f"Invalid input: {value} is a negative number")
        
def checek_positive_number(num):
    if num < 0 :
        raise  NagativeNumberError(Exception)
    else: 
        print(f"{num} is a valid positive number.")

try:
    number = int(input("Enter a positive number: "))
    checek_positive_number(number)
except NagativeNumberError as e:
    print(e)
except ValueError:
    print("Error: Please enter a valid integer.")
finally:
    print("Program excution finished.")