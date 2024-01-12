# Step 1: Read the Customer.txt file and store the total value of orders for each customer.
customers = {}
with open('customers.txt', 'r') as file:
    for line in file:
        name, _, _, value = line.strip().split(', ')
        customers[name] = float(value)


def get_product_price(product_id):
    with open('products.txt', 'r') as file:
        for line in file:
            _id, _name, _price, _stock = line.strip().split(', ')
            if _id == product_id or _name == product_id:
                return float(_price) if _price else 0
    return 0

# Step 2: Read the orders.txt file and calculate the total value of orders for each customer.
orders = {}
with open('orders.txt', 'r') as file:
    for line in file:
        name, *products, _ = line.strip().split(', ')
        for product in products:
            # You would need to implement the `get_product_price` function.
            price = get_product_price(product)
            if name in orders:
                orders[name] += price
            else:
                orders[name] = price

# Step 3: Compare the total value of orders for each customer from the Customer.txt file with the total value of orders from the orders.txt file.
for name, value in customers.items():
    if name in orders and value != orders[name]:
        print(f'The total value of orders for {name} in the Customer.txt file does not match the total value of their orders in the orders.txt file.')