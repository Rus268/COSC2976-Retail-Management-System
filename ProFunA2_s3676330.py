"""
 This program is a retail management system that allows cashier to place an order for a customer, add/update products and prices, and display existing customers and products, etc.
"""
import sys
import os

# Define the required classes for the program
class Customer:
    # Initialise the customer object with given ID, name, and value. If value not provided, default to 0.00
    def __init__(self, id:str, name:str, value:float = 0.00):
        self.id = id
        self.name = name
        self.value = float(value) # Ensuring value is store as a float
    # Calculate the discount which return (0,price) - where the first value is discount rate and second is input price.
    # This will be the super method and will have more subclass implement
    def get_discount(self,price):
        return (0,price)
    
    @property
    def get_id(self): # Method to get the customer ID
        return self.id
    
    @property
    def get_name(self): # Method to get the customer name
        return self.name
    
    @property
    def get_value(self): # method to get the customer total money spend to date
        return self.value
    
    # Print the class Customer attributes and the discount rate associated:
    def display_info(self):
        return print(f"ID: {self.id}\nName: {self.name}\nValue: {self.value}\nDiscount Rate: 0")
# Create a new member class that inherited it attributes from customer
class Member(Customer):
    discount_rate = 0.05 # initialise a class inherited variable

    # Initialise the class member and inherited the attributes from customer class.
    def __init__(self,id, name:str, value:float = 0.00):
        super().__init__(id,name,value)

    def get_discount(self, price:float): # Update the get_discount method with new calculation
        new_price = price * (1 - self.discount_rate)
        return (self.discount_rate, new_price)
    
    def display_info(self): # Update new information in the display_infor class
        print(f"ID: {self.id}\nName: {self.name}\nValue: {self.value}\nDiscount Rate: {self.discount_rate}")
    
    # Create a new class method to update the flat discount rate
    # I will be using @classmethod decorator to ensure the method is a class method
    @classmethod
    def set_rate(member_cls, new_rate: float): # Create a new class method to update the flat discount rate
        member_cls.discount_rate = new_rate
# Create a new vip member class that inherited it attributes from customer
class VipMember(Customer):
    # Initialise the two discount rate and threshold for the class
    threshold = 1000.00
    # Initialise the price for the membership. This will be a class variable as it will be the same for all instance of the class
    price = 200.00

    # Initialise the class throught initialising the parent class
    def __init__ (self, id, name:str, value:float = 0.00):
        super().__init__(id, name, value)
        self.discount_rate_1 = float(0.10)
        self.discount_rate_2 = float(self.discount_rate_1 + 0.05) # The second discount rate is alway 5% higher than the first discount rate
        
    
    def get_discount(self, price):
        if price <= self.threshold:
            return (self.discount_rate_1, price * (1- self.discount_rate_1))
        else:
            return (self.discount_rate_2, price * (1- self.discount_rate_2))
    
    def display_info(self): # Print the information of the vip member
        print(f"ID: {self.id}\nName: {self.name}\nValue: {self.value}\nDiscount Rate 1: {float(self.discount_rate_1)}\nDiscount Rate 2: {float(self.discount_rate_2)}")
    
    def set_rate(self, rate_type: str = "rate_1", new_rate:float = 0.00):
        """
        This function will update the discount rate of the vip member. The default rate type is rate_1
        When update rate_1, rate_2 will be updated automatically to ensure rate_2 is always 5% higher than rate_1 and vice versa
        
        Input:
        - rate_type: can either be "rate_1" or "rate_2"
        - new_rate: the new discount rate

        Output:
        - return None
        """
        if rate_type == "rate_1":
            self.discount_rate_1 = float(new_rate)
            self.discount_rate_2 = float(self.discount_rate_1 + 0.05)
        elif rate_type == "rate_2":
            self.discount_rate_2 = new_rate
            self.discount_rate_1 = float(self.discount_rate_2 - 0.05)
        else:
            raise ValueError("Invalid rate type. Rate can either be 'rate_1' or 'rate_2'")
    
    @classmethod
    def set_threshold(cls, new_threshold:float):
        """
        This function will update the discount threshold of the vip member

        Input:
        - new_threshold: the new discount threshold
        """
        cls.threshold = new_threshold
# Create a new product class
class Product:

    def __init__(self, id, name:str, price:float, stock:int):
        self.id = id
        self.name = name
        self.price = float(price) # Ensuring price is store as a float
        self.stock = int(stock) # Ensuring stock is store as an integer
    
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
    
    def get_price(self):
        return self.price
    
    def get_stock(self):
        return self.stock
     # Update the price of the product
    def set_price(self, new_price:float):
        self.price = float(new_price)
    # Update the stock of the product
    def set_stock(self, new_stock:int): 
        self.stock = int(new_stock)
    # Print the product information
    def display_info(self):
        print(f"ID: {self.id}\nName: {self.name}\nPrice: {self.price}\nStock: {self.stock}")
class Order:
    def __init__(self, customer:Customer, product:Product, quantity:int):
        self.customer = customer # We will be using customer id as it ensure we are reference to the correct customer everytime
        self.product = product # We will be using product id to ensure we are reference to to the correct product everytime
        self.quantity = quantity
    # I will be using @property decorator to ensure the attribute is read only for getter method
    @property
    def get_customer(self):
        return self.customer
    @property
    def get_product(self):
        return self.product
    @property
    def get_quantity(self):
        return self.quantity
    
    def update_product_stock(self):
        """This function will update the stock of the product after the order is placed"""
        # For this week requirement I will ignored the case there the value is negative.
        try:
            self.product.stock = self.product.stock - self.quantity
        except ValueError:
            raise ValueError("Invalid quantity")

    def list_order(self):
        """This function will list the order"""
        print(f"Customer ID: {self.customer_id}\nProduct ID: {self.product_id}\nQuantity: {self.quantity}")
# Create a new record class to store the customer and product list
class Record:
    # Specify the relative path to relevant file for the program to run correctly
    # I will be using os.path.join to ensure the file path to ensure the file path is correct regardless of operating system used.
    customer_file = os.path.join(os.path.dirname(__file__),r"COSC2976_assignment2\\files_PASSlevel\\customers.txt")
    product_file = os.path.join(os.path.dirname(__file__),r"COSC2976_assignment2\\files_PASSlevel\\products.txt")

    def __init__(self):
        """The class will create new instance of customer list and product list"""
        self.customer_list = [] # In this list we will be storing a list of customer id in order to ensure uniqueness
        self.product_list = [] # In this list we will be storeing a list of product id in order to ensure uniqueness

    def read_customer(self):
        """This function will look for the customer file and import it into the record"""
        try:
            with open(self.customer_file, "r") as f:
                line = f.readline()
                while line:
                    id, name, discount_rate, value = line.strip().split(',')
                    # I will be using if statement to determine the type of customer
                    # I will be using the first letter of the id to determine the type of customer to create the correct object
                    if "C" in id:
                        customer_id = Customer (id, name, value)
                        self.customer_list.append(customer_id)
                        line = f.readline()
                    elif "M" in id:
                        customer_id = Member (id, name, value)
                        self.customer_list.append(customer_id)
                        line = f.readline()
                    elif "V" in id:
                        customer_id = VipMember (id, name, value)
                        customer_id.set_rate("rate_1",discount_rate)
                        self.customer_list.append(customer_id)
                        line = f.readline()
        except FileNotFoundError:
            raise FileNotFoundError(f'File {self.customer_file} is missing!')
    
    def read_product(self):
        try:
            """This function will read the product file and import into the record """
            with open(self.product_file,"r") as f:
                line = f.readline()
                while line:
                    item_id, name, price, stock = line.strip().split(',')
                    product_id = Product(item_id, name, price, stock)
                    self.product_list.append(product_id) # Add the new product into the product id
                    line = f.readline() # Read the next line
        except FileNotFoundError:
            raise FileNotFoundError(f'File {self.product_file} is missing!')

    def find_customer(self,key:str = "name", value:str = None):
        """ 
        Take a search key and find the customer detail from the customer list
        
        Input:
        - key : can either be "id" or "name"
        - value: the search value

        Output:
        - return customer detail if customer exit return None if customer does not exit

        """
        for customer in self.customer_list:
            if getattr(customer,key).strip().lower() == value.strip().lower():
                return customer # Return the customer if it exit
        return None # If the customer does not exit return None
        
    def find_product(self, key:str = "name", search:str = None):
        """ 
        Take a search key and fine the product teails from the product list
        
        Input:
        - key: can either be product id or name

        Output:
        - return product detail is product exit else print product does not exit
        """
        for item in self.product_list:
            if getattr(item,key).strip().lower() == search.strip().lower():
                return item # Return the product if it exit
        return None # If the product does not exit return None
    
    def list_customer(self):
        """This function will return the list of customer in the record"""
        for customer in self.customer_list:
            customer.display_info()

    def list_product(self):
        """This function will return the list of product in the record"""
        for product in self.product_list:
            product.display_info()
    
    def add_customer(self, customer:Customer):
        """
        This function will add a new customer into the record
        
        Input:
        - customer: the customer object that want to add into the record
        """
        if isinstance(customer, Customer):
            self.customer_list.append(customer)
        else:   
            raise TypeError("customer must be a Customer object or it subclass")
        
    def add_product(self, product:Product):
        """
        This function will add a new product into the record
        
        Input:
        - product: the product object that want to add into the record
        """
        if isinstance(product, Product):
            self.product_list.append(product)
        else:    
            raise TypeError("product must be a Product object")
    
    # TODO: add a function to update the customer and product list
    

def menu(Data:Record):
    def display_menu():
        """Display the menu"""
        print("#"*30)
        print("You can choose from the following option:")
        print("1. Place an order")
        print("2. Display exiting customers")
        print("3. Display exiting products")
        print("0. Exit the program")
        print("#"*30)
        print()
    while True:
        display_menu()
        user_input = input("Choose one option: ")
        print()
        if user_input == "1":
            # Take the information from the client and place an order
            customer, product, quantity = get_info(Data)
            place_order(customer, product, quantity)
        elif user_input == "2":
            # Display the customer list
            Data.list_customer()
        elif user_input == "3":
            # Display the product list
            Data.list_product()
        elif user_input == "0":
            sys.exit("Thank you for using the program!")
        else:
            print("Invalid input, please try again")
            continue
        # Pause the program and wait for the user to press enter to continue
        print()
        input("Press enter to continue!")
        print()


def get_info(Data:Record):
    """
    This function will take information from the client
    
    Input:
    - Data: the record object that contain the customer and product list
    """
    name = input("Please enter the customer name [e.g. Loki]: ")
    # We will be creating a new customer attributes to track the customer details
    customer = Data.find_customer("name",name)
    print()
    product = input("Please enter the product name [e.g. Apple]: ")
    product = Data.find_product("name",product)
    print()
    quantity = int(input("Please enter the quantity [e.g. 10]: "))
    print()
    # If the customer does not exit, we will be creating a new customer and check if they want a membership
    if customer == None:
        membership = input("This is a new customer. Does the customer want to have a membership [e.g. enter y or n]: ")
        if membership == "y":
            print("We have two type of membership: V for VIP and M for Member")
            type = input("Please enter the membership type [e.g. V or M]: ")
            if type == "V":
                id = "V" + str(len(Data.customer_list) + 1)
                customer = VipMember(id,name,0.00)
            elif type == "M":
                id = "M" + str(len(Data.customer_list) + 1)
                customer = Member(id,name,0.00)
        elif membership == "n":
            id = "C" + str(len(Data.customer_list) + 1)
            customer = Customer(id,name,0.00)
        else:
            raise ValueError("Invalid input")
        # Add the new customer into the record
        Data.add_customer(customer)
    if product == None:
        # TODO: handle when product does not exit in next version
        raise ValueError("Invalid product")
    
    return customer, product, quantity

def place_order(customer:Customer, product: Product, quantity:int):
    """
    This function will place an order for the customer

    Input:
    - customer: the customer object
    - product: the product object
    - quantity: the quantity of the product
    """
    # Creating a new order
    new_order = Order(customer, product, quantity)
    # Update the item stock
    new_order.update_product_stock()
    # Calculate the discount
    discount_rate, new_price = customer.get_discount(product.price)
    if isinstance(customer, VipMember):
        vip_fee = VipMember.price
        total_price = float(new_price * quantity + vip_fee)
    else:
        total_price = float(new_price * quantity)
    customer.value = customer.value + total_price
    # Obtain detail from class
    customer_name = customer.name.strip()
    product_name = product.name.strip()
    product_price = product.price
    # Print the order detail
    print()
    print("="*50)
    print(f'{customer_name} purchases {quantity} x {product_name}')
    print(f'Unit price: {product_price:.2f} (AUD)')
    if isinstance(customer, VipMember):
        print(f'Membership price: {vip_fee:.2f} (AUD) not discounted')
    print(f'{customer_name} gets a discount of {discount_rate*100:.0f}%.')
    print(f'Price to pay: {total_price:.2f} (AUD)')
    print("="*50)

def main():
    # Initalise main system record.
    SysRecord = Record()
    # read the customer and product file
    try:
        SysRecord.read_customer()
        SysRecord.read_product()
    except FileNotFoundError as e:
        print(f"{e}")
        sys.exit("Please check the file path and try again!")
    # Run the menu
    menu(SysRecord)


if __name__ == "__main__":
    try:
     main()
     # Exit the program gracefully when sys.exit() is called. This is to ensure consistent behaviour across IDE or terminal
    except SystemExit as e:
        print(f"{e}")

