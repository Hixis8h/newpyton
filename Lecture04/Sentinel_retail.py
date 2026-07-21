keep_gogin = 'y'

while keep_gogin == 'y':
    wholeasle_cost =float(input("Enter the item's wholesale cost: "))
    retail_price = wholeasle_cost*2.5
    print(f'Retail price: ${retail_price:.2f}')
    keep_gogin = input('Doa you have another item? (Enter Y for yes)')