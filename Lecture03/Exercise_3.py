hours_work =int(input("Enter Your hours worked: "))
pay_rate = float(input("Enter Your pay rate: "))
if hours_work >= 40:
    gross_pay = hours_work*pay_rate
else :
    gross_pay = (hours_work-40)*pay_rate * 1.5 +(40+hours_work)
    print("Gross pay is : $",format(gross_pay,".2f"))