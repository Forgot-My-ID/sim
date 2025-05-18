import random

m = 0
reorder_point = int(input("\n Enter reorder point: "))
reorder_quantity = int(input("\n Enter reorder quantity: "))

while m != 5:
    units = 0
    equivalent_stock = 0
    day = 1
    due_day = 0
    demand = 0
    total_cost = 0
    current_stock = 100

    while day <= 180:
        if due_day == day:
            current_stock += reorder_quantity
            units = 0

        demand = random.randint(0, 99)

        if demand <= current_stock:
            current_stock -= demand
            total_cost += current_stock * 1
        else:
            total_cost += (demand - current_stock) * 10
            current_stock = 0

        equivalent_stock = current_stock + units

        if equivalent_stock <= reorder_point:
            units = reorder_quantity
            total_cost += 75
            due_day = day + 3
        day += 1

    print("\n Reorder point:", reorder_point)
    print(" Reorder Quantity:", reorder_quantity)
    print(" Total cost is:", total_cost)

    m += 1
