"""
 This program is a retail management system that allows cashier to place an order for a customer, add/update products and prices, and display existing customers and products, etc.
"""
# Import the sys module to allow the program to exit
import sys

# Initialize the product directory. This is to allow for the program to allow multiple products to be added.
# In this directory, we are unable to truely identify the product as there is no unique identifier for the product due as we are assuming the product name is unique.
product_directory = [
    {"name": "Apple", "price": 1.00},
    {"name": "Banana", "price": 2.00},
    {"name": "Orange", "price": 3.00},
    {"name": "Pear", "price": 4.00},
    {"name": "Pineapple", "price": 5.00},
]

# Initialize the customer directory with the customer name and membership status.
# This is to allow for the program to allow multiple customers to be created.
# In this directory, we are unable to truely identify the customer as there is no unique identifier for the customer as we are assuming the customer name is unique.
customer_directory = [
    {"name": "John Doe", "membership": False},
    {"name": "Tony Stark", "membership": True},
    {"name": "Peter Parker", "membership": False},
    {"name": "Bruce Wayne", "membership": True},
    {"name": "Clark Kent", "membership": False},
]

# Initialize the order history with the customer name, order items, total price, membership discount, and final price. 
# This is to allow for the program to allow multiple products to be purchased in a single order.
# In this directory, we are unable to truely identify the order as there is no unique identifier for the order as we are assuming the customer name is unique and using it as the primary search key.
# We will organise the order history by append the most recent order to the last index of the list.
order_history = [
    {
        "customer_name": "Tony Stark",
        "purchase_history": [
            {"Apple": 2, "Banana": 1},
            {"Orange": 1, "Pear": 1},
            {"Pineapple": 1}
        ],
        "total_spend": [3.80, 6.65, 4.75],
    },
    {
        "customer_name": "Peter Parker",
        "purchase_history": [
            {"Pineapple": 2, "Banana": 1},
            {"Pear": 1},
            {"Apple": 1, "Orange": 1}
        ],
        "total_spend": [11.75, 4.00, 3.80],
    },
    {
        "customer_name": "Bruce Wayne",
        "purchase_history": [
            {"Apple": 2, "Banana": 1}
        ],
        "total_spend": [3.80]
    },
    {
        "customer_name": "Clark Kent",
        "purchase_history": [
            {"Pineapple": 2, "Banana": 1},
            {"Pear": 1},
            {"Apple": 1, "Orange": 1}
        ],
        "total_spend": [11.75, 4.00, 3.80],
    },
    {
        "customer_name": "John Doe",
        "purchase_history": [
            {"Orange": 1, "Pear": 1},
            {"Pineapple": 1}
        ],
        "total_spend": [6.65, 4.75],
    },
]

def main():
    """Main function"""
    print()
    print("Welcome to the TVC Retail Management System\n")
    menu()

def place_order():
    """Place an order for a customer"""
    customer= input("Enter the name of the customer [eg: John Doe]: ").strip().title() # Ask the user to enter the customer name and format the customer name to title case and strip any whitespace
    # Ask the user to enter the customer name, product name, and quantity of the product and continue to ask until the order is completed
    order_list = add_order_to_list()
    if order_list == []: # If the order list is empty then return to the menu
        return
    print('Order is created successfully\n')
    if check_membership(customer) == False:
        print(f'{customer} does not have a membership')
        membership = simple_bool_input("Would the customer like to sign up as a member? (Enter y or n): ")
    else:
        membership = check_membership(customer)
    discount = discount_percentage(membership)
    discount = discount_percentage(membership)
    total_price = order_list_price_cal(order_list) * (1 - discount)
    create_customer(customer, membership)
    add_purchase_history(customer, order_list, total_price)
    # Display the format cost for the customer.
    print()
    print("="*50)
    for order in order_list:
        product = order["product_name"]
        quantity = order["quantity"]
        product_price = get_product_price(product)
        print(f'{customer}  purchases {quantity} x {product}')
        print(f'Unit price: {product_price:.2f} (AUD)')
    print("-"*50)
    print(f'{customer} gets a discount of {discount*100:.0f}%.')
    print(f'Price to pay: {total_price:.2f} (AUD)')
    print("="*50)

def add_order_to_list() -> list:
        """This function take the customer order and add them into a list. It will ignored any product that does not have a price in the product directory.
        
        Parameter:
        - None
        Return:
        - item_list: the list that contains a dictionary of the product name, quantity, and price of the product
        """
        try:
            item_list = [] # Initialize the order list
            not_completed = True # Generate a flag to check if the order is completed
            print("-"*50)
            print("Enter the product name and quantity")
            print("Use control + z and Enter on Windows or command + z on and Enter on Mac to complete the order at any time, current order will not be save")
            print("-"*50)
            while not_completed == True:
                product = product_input("Enter the name of the product [Eg: Apple]: ")
                quantity = quantity_input("Enter the quantity of the product [eg: 12]: ")
                product_price = get_product_price(product)
                if product_price == None: # Pass the product if the product does not have a price in the product directory
                    continue
                item_list.append({"product_name": product, "quantity": quantity, "product_price": product_price})
                print(f'{quantity} x {product} added to the order')
                not_completed = simple_bool_input("Would you like to add another product? (Enter y or n): ")
            print("-"*50)
            return item_list
        except EOFError:
            print("-"*50)
            return item_list

def order_price_cal(price, quantity):
    """Calculate the price of the product"""
    return round(float((price * quantity)), 2)

def order_list_price_cal(order_list):
    """Calculate the total price of the order"""
    total_price = 0
    for order in order_list:
        total_price += order_price_cal(get_product_price(order["product_name"]), order["quantity"])
    return round(float(total_price), 2)

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
        print("6. Reveal the most valuable customer")
        print("7. Display a customer order history")
        print("0. Exit the program")
        print("#"*30)
        print()
    while True:
        display_menu()
        user_input = input("Choose one option: ")
        print()
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
        elif user_input == "6":
            display_most_valuable_customer()
        elif user_input == "7":
            display_customer_order_history()
        elif user_input == "0":
            print("Thank you for using the program")
            sys.exit()
        else:
            print("Invalid input, please try again")
            continue
        # Pause the program and wait for the user to press enter to continue
        print()
        input("Press enter to continue!")
        print()
  
def add_update_product():
    """Add or update the product from the product directory"""
    product_list = new_product_list_input("Enter products name separate by commas [Eg: Apple, Pear, Mango]: ") # Format the list elements into correct format strip any whitespace and capitalize the first letter of each word.
    price_list = new_price_list_input("Enter the product price separte by commas [Eg: 2, 10, 30]: ")  # Process the price and put it into a list
    for i, p in enumerate(product_list): # Loop throught the product list for the product name and index
        if p in [product["name"] for product in product_directory]: # Check if the product name is in the product directory
            index = [product["name"] for product in product_directory].index(p)  # Find the index of the product in the product directory
            # if the price is provided then update the price of the product in the product directory
            if i < len(price_list): 
                product_directory[index]["price"] = float(price_list[i]) if price_list[i] else None  # Update the price of the product
            else:
                product_directory[index]["price"] = None  # If no price provided mark price as None
        else:
            if i < len(price_list):
                price_value = float(price_list[i]) if price_list[i] else None
            else:
                price_value = None  # No price provided then assign price as None
            product_directory.append({"name": p, "price": price_value})
    print("Product updated successfully")

def new_product_list_input(prompt) -> list:
    """
    Prompt an input string from user and split the string into a list 
    and format the list elements into correct format strip any whitespace and capitalize the first letter of each word.
    
    Parameter:
    - prompt: the prompt that will be displayed to the user
    
    Return:
    - new_list: the list that contains the product name
    """
    new_list = []
    input_str = input(prompt)
    input_list = input_str.strip().split(',')
    for element in input_list:
        new_list.append(element.strip().title())
    return new_list

def new_price_list_input(prompt) -> list:
    """
    Prompt an input string from user and split the string into a list.
    
    Parameter:
    - prompt: the prompt that will be displayed to the user
    
    Return:
    - new_list: the list that contains the price of the product in integer
    """
    input_str = input(prompt)
    new_list = input_str.strip().split(',')
    for i, element in enumerate(new_list):
        try:
            new_list[i] = float(element.strip())
        except ValueError:
            new_list[i] = None
    return new_list

def display_customer():
    """Display the customer from the customer directory"""
    print("Customer List")
    print("-"*30)
    for customer in customer_directory:
        print(f'Customer Name: {customer["name"]}')
    print("-"*30)

def display_customer_membership():
    """Display the customer with membership as true from the customer directory"""
    print("Customer List with Membership")
    print("-"*30)
    for customer in customer_directory:
        if customer["membership"] == True:
            print(f'Customer Name: {customer["name"]}')
    print("-"*30)

def display_product():
    """Display the product from the product directory"""
    # Calculate the max length of the product name
    max_length = max([len(product["name"]) for product in product_directory])
    print("Product List")
    print("-"*30)
    # Print the product name and price a and use the max length to format the product name to the same length
    for product in product_directory:
        print(f'Product Name: {product["name"]: <{max_length}} | {product["price"]} (AUD)')
    print("-"*30)

def display_customer_order_history():
    """Display the customer order history from the order history directory"""
    print("Order History")
    print("-" * 30)
    while True:
        customer_name = input("Enter the name of the customer [eg: John Doe]: ").strip()
        print()
        for customer in order_history:
            if customer["customer_name"] == customer_name:
                print(f"This is the order history of {customer_name}.")
                print(" " * 20, end="")
                unique_items = set()

                for purchase in customer["purchase_history"]:
                    unique_items.update(purchase.keys())

                for item in sorted(unique_items):
                    print("{:<15}".format(item), end="")
                print()

                for index, purchase in enumerate(customer["purchase_history"], start=1):
                    print(f"Purchase {index}", end=" "*10)
                    for item in sorted(unique_items):
                        quantity = purchase.get(item, 0)
                        print("{:<15}".format(str(quantity)), end="")
                    print()
                return
        # If the loop completes without finding a matching customer
        print(f"{customer_name} does not exist in the order history. Please try again.")

def display_most_valuable_customer():
    """Display the most valuable customer from the order history directory"""
    print("Most Valuable Customer")
    print("-"*30)
    mvc = {"customer_name": None, "total_purchase": 0} # Initialize the most valuable customer dictionary
    for customer in order_history:
        total = sum(customer.get("total_spend",[])) # Calculate the total purchase of the customer
        if total > mvc["total_purchase"]: # Check if the total purchase of the customer is greater than the current most valuable customer
            mvc["customer_name"] = customer["customer_name"] # Update the most valuable customer name
            mvc["total_purchase"] = total # Update the most valuable customer total purchase
    print(f'Customer name: {mvc["customer_name"]}')
    print(f'Total Purchase: {mvc["total_purchase"]:.2f}')
    print("-"*30)

# Currently the most valuable customer is assume to be the customer that has the highest total purchase. 
# If ther are multiple customers with the same total purchase, the program will only display the first customer that has the highest total purchase
# To improve this function, we can add a new key to the order history directory to store the number of orders the customer has made and use that to determine the most valuable customer in the next version of the program.

def product_input(prompt: str) -> str:
    """Ask the user to enter the name of the product and continue to ask until the product name match a name in the product directory"""
    while True:
        item = input(prompt)
        item = item.strip().title()
        if item in [product["name"] for product in product_directory]:
            return item
        if item == "":
            print("Product name cannot be empty")
            continue
        else:
            print( f"Product {item} does not exist")
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
    """Create a customer if the customer does not exist in the customer directory if the customer exists return a message"""
    if customer_name in [customer["name"] for customer in customer_directory]:
        print( f"Customer {customer_name} already exists")
    else:
        customer_directory.append({"name": customer_name, "membership": membership})
        print( f"Customer {customer_name} created successfully")

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

def simple_bool_input(prompt) -> bool:
    """This function take in either the letter "y" or "n" and return True or False respectively and continue to ask until the user enter the correct input
    
    Parameter:
    - prompt: the prompt that will be displayed to the user
    
    Return:
    - True if the user enter "y"
    - False if the user enter "n"

    """
    while True:
        _ = input(prompt)
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

def simplify_order_dict(input_dict: dict) -> dict:
    """Format the dict elements into a simplify format and strip any whitespace and capitalize the first letter of each word.
    
    Parameter:
    - input_list: the list that will be formatted
    
    Return:
    - new_list: the list that contains the formatted list elements
    """
    new_dict = {}
    for element in input_dict:
        name = element["product_name"].strip().title()
        quantity = element["quantity"]
        new_dict.update({name:quantity})
    return new_dict

def add_purchase_history(customer_name, recent_order: list, total_price: float):
    """Add the customer order history to the order history directory
    
    Parameter:
    - customer_name: the name of the customer
    - recent_order: the list that contains the product name and quantity of the product customer purchased
    
    Return:
    - None
    """
    edit_order = simplify_order_dict(recent_order)
    for customer in order_history:
        if customer["customer_name"] == customer_name: # Check if the customer name is in the order history
            customer["purchase_history"].append(edit_order) # Get the purchase history of the customer from the order history
            customer["total_spend"].append(total_price)
            break
    order_history.append({"customer_name": customer_name, "purchase_history": [edit_order],  "total_spend":[total_price]}) # Add the customer order history to the order history directory"

if __name__ == "__main__":
    main()
