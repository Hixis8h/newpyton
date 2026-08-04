def is_armstrong(number):
    num_str = str(number)
    digits = len(num_str)
    total = 0
    for digit in num_str:
        total += int(digit) ** digits
    if total == number:
        return True
    else:
        return False
num = int(input("Enter a number: "))

if is_armstrong(num):
    print(num, "is an Armstrong number.")
else:
    print(num, "is not an Armstrong number.")
    