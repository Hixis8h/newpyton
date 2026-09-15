try:
    numerator = float(input("Enter the numerator: " ))
    denominator = float(input("Enter the denominator"))
    
    result = numerator / denominator
    print(f"The result is : {result}")
    
except ZeroDivisionError:
    print("Error : You connot devide by zero.")
    
except ValueError:
    print("Error : Invalid input. Please enter numeric value.")

finally:
    print("Excution completed , whether an exception occured ro not.")
    
print("End of program")
