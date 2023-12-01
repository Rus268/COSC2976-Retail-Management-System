"""
 This program is a retail management system that allows customers to purchase products and organise the data of the customers and products.

"""

import sys

# Initialize the product directory
product_directory = [
    {"name": "Apple", "price": 1.00},
    {"name": "Banana", "price": 2.00},
    {"name": "Orange", "price": 3.00},
    {"name": "Pear", "price": 4.00},
    {"name": "Pineapple", "price": 5.00},
]

# Initialize the customer directory with the customer name and membership status
customer_directory = [
    {"name": "John Doe", "membership": False},
    {"name": "Tony Stark", "membership": True},
]

# Initialize the order directory. Inside the order directory we use a list of dictionaries to store the order information. 
# This is to allow for future expansion of the program to allow multiple products to be purchased in a single order.
# order_directory = [
#     {
#         "customer_name": "Tony Stark",
#         "order_items": [{"product_id": "p-002", "quantity": 2}],
#         "total_price": 4.00,
#         "membership_price": 0.00,
#     }
# ]
def main():
    """Main function"""
    print("Welcome to the Retail Management System\n")
    menu()

def place_order():
    customer= input("Enter the name of the customer: ") 
    product = product_input("Enter the name of the product: ")
    product_price = get_product_price(product)
    quantity = quantity_input("Enter the quantity of the product: ") # Assume positive integer
# 4. Calculate the total cost for the customer including the discount (see No. 5 below).
# 5. For customers with membership, 5% discount will apply. No discount for customers without
# membership.
    if check_membership(customer) == False:
        membership = membership_input()
    else:
        membership = check_membership(customer)
    discount = discount_percentage(membership)
    total_price = order_price_cal( discount, product_price, quantity)
    discount = discount_percentage(membership)
    create_status = create_customer(customer, membership)
# 6. The total cost will be displayed as a formatted message to the user, e.g.
    print(create_status)
    print()
    print("-"*30)
    print(f'{customer}  purchases {quantity} x {product}')
    print(f'Unit price: {product_price} (AUD)')
    print(f'{customer} gets a discount of {discount*100}%.')
    print(f'Total price: {total_price} (AUD)')
    print("-"*30)


def menu():
    def display_menu():
        """Display the menu"""
        print("#"*30)
        print("You can choose from the following option:")
        print("1. Place an order")
        print("2. Add/update products and prices")
        print("3. Display exiting customers")
        print("4. Display exiting customers with membership")
        print("5. Display exiting products")
        print("0. Exit the program")
        print("#"*30)
        print()
    while True:
        display_menu()
        user_input = input("Choose one option: ")
        if user_input == "1":
            place_order()
        elif user_input == "2":
            add_update_product()
        elif user_input == "3":
            display_customer()
        elif user_input == "4":
            display_customer_membership()
        elif user_input == "5":
            display_product()
        elif user_input == "0":
            print("Thank you for using the program")
            sys.exit()
        else:
            print("Invalid input, please try again")
            continue
        # Pause the program and wait for the user to press enter to continue
        input("Press enter to continue")
        print()
  
def add_update_product():
    """Add or update the product"""
    product = input("Enter products name separate by commas: ")
    product_list = product.strip().split(',')  # Process the name to ensure name is formatted correctly and put it into a list
    price = input("Enter price of all products above separate by commas: ")
    price_list = price.strip().title().split(',')  # Process the price and put it into a list
    for i, p in enumerate(product_list):
        if p in [product["name"] for product in product_directory]:
            index = [product["name"] for product in product_directory].index(p)  # Find the index of the product in the product directory
            if i < len(price_list):
                product_directory[index]["price"] = float(price_list[i]) if price_list[i] else None  # Update the price of the product
            else:
                product_directory[index]["price"] = None  # No price provided
        else:
            if i < len(price_list):
                price_value = float(price_list[i]) if price_list[i] else None
            else:
                price_value = None  # No price provided
            product_directory.append({"name": p, "price": price_value})
    print("Product updated successfully")

def list_element_format(input_list: list) -> str:
    """Format the list elements into a string"""
    for i, element in enumerate(input_list):
        input_list[i] = element.strip().title()
    return ", ".join(input_list)


def display_customer():
    """Display the customer"""
    print("Customer List")
    print("-"*30)
    for customer in customer_directory:
        print(f'Customer Name: {customer["name"]}')
    print("-"*30)

def display_customer_membership():
    """Display the customer with membership"""
    print("Customer List with Membership")
    print("-"*30)
    for customer in customer_directory:
        if customer["membership"] == True:
            print(f'Customer Name: {customer["name"]}')
    print("-"*30)

def display_product():
    """Display the product"""
    print("Product List")
    print("-"*30)
    for product in product_directory:
        print(f'Product Name: {product["name"]} | {product["price"]} (AUD)')
    print("-"*30)

def product_input(prompt: str) -> str:
    """Ask the user to enter the name of the product and continue to ask until the product exists"""
    while True:
        _ = input(prompt)
        _ = _.strip().title()
        if _ in [product["name"] for product in product_directory]:
            return _
        else:
            print( f"Product {product_name} does not exist")
            continue

def quantity_input(prompt: str) -> int:
    """Ask the user to enter the quantity of the product and continue to ask until the quantity is a positive integer"""
    while True:
        _ = input(prompt)
        try:
            _ = int(_)
            if _ > 0:
                return _
            else:
                print("Quantity must be a positive integer")
                continue
        except ValueError:
            print("Quantity must be a positive integer")
            continue

def create_customer(customer_name, membership) -> str:
    """Create a customer"""
    if customer_name in [customer["name"] for customer in customer_directory]:
        return f"Customer {customer_name} already exists"
    else:
        customer_directory.append({"name": customer_name, "membership": membership})
        return f"Customer {customer_name} created successfully"

def check_membership(customer_name) -> bool:
    """Check if the customer has a membership"""
    for customer in customer_directory:
        if customer["name"] == customer_name:
            return customer["membership"]
    return False  

def get_product_price(product_name:str) -> float:
    for product in product_directory:
        if product["name"] == product_name:
            return product["price"]

def order_price_cal(discount: float, price: float, quantity: int) -> float:
    """Calculate the price of the product"""
    return round(float((price * quantity) * (1.00 - discount)), 2)

def membership_input() -> bool:
    """Ask the user if the customer has a membership"""
    while True:
        _ = input("Does the customer have a membership? (y/n): ")
        _ = _.strip().lower()
        if _ == "y":
            return True
        elif _ == "n":
            return False
        else:
            print("Only y/n is accepted, please try again")
            continue
    
def discount_percentage(membership: bool) -> str:
    """Calculate the discount percentage"""
    if membership == True:
        return 0.05
    else:
        return 0.00

if __name__ == "__main__":
    main()