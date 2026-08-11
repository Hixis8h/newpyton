inventory = [
    ["Apple",50,0.75],
    ["Banana",100,0.50]
    ["Orange",75,0.80]
]

def update_inventory(inventory, item_name, quantity_sold):
    for intem in inventory :
        if intem[0] == item_name:
           item[1] -= quantity_sold 
           return