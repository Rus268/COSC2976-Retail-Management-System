"""
 This program is a retail management system that allows cashier to place an order for a customer, 
 add/update products and prices, and display existing customers and products, etc.

 - 14/12/2023: Create program acording to the requirement for PASS level in week 7.
 
 """
import sys
import os

# Define the required classes for the program
class Customer:
    # Initialise the customer object with given ID, name, and value. If value not provided, default to 0.00
    def __init__(self, id:str, name:str, value:float = 0.00):
        self.id = id
        self.name = name
        self.value = value
    # Calculate the discount which return (0,price) - where the first value is discount rate and second is input price.
    # This will be the super method and will have more subclass implement
    def get_discount(self,price):
        return (0,price)
    # Return the class information and the discount information.
    def display_info(self):
        return f"ID: {self.id}\nName: {self.name}\nValue: {self.value}\nDiscount Rate: 0"
    
# Create a new member class that inherited it attributes from customer
class Member(Customer):
    discount_rate = 0.05 # Initialise a class inherited variable
    # Initialise the class member and inherited the attributes from customer class.
    def __init__(self,id, name:str, value:float = 0.00):
        # Initialise the class throught initialising the parent class variable.
        super().__init__(id,name,value) 
    # Update the get_discount method with new calculation
    def get_discount(self, price:float):
        """
        This function will calculate the discount for the member

        Input:
        - price: the price of the product

        Output:
        - return a tuple contain the discount rate and the new price
        """ 
        new_price = price * (1 - self.discount_rate)
        return (self.discount_rate, new_price)
     # Update new information in the display_infor class
    def display_info(self):
        """This function will print the information of the member"""
        return f"ID: {self.id}\nName: {self.name}\nValue: {self.value}\nDiscount Rate: {self.discount_rate}"
    # Create a new class method to update the flat discount rate
    # I will be using @classmethod decorator to ensure the method is a class method
    @classmethod
    def set_rate(cls, new_rate: float): # Create a new class method to update the flat discount rate
        cls.discount_rate = new_rate

# Create a new vip member class that inherited it attributes from customer
class VipMember(Customer):
    # Initialise the two discount rate and threshold for the class
    threshold = 1000.00
    # Initialise the price for the membership. This will be a class variable as it will be the same for all instance of the class
    price = 200.00

    # Initialise the class throught initialising the parent class
    def __init__ (self, id, name:str, value:float = 0.00):
        super().__init__(id, name, value)
        self.discount_rate_1 = 0.10 # The default first discount rate is alway 10%
        self.discount_rate_2 = 0.15 # The default second discount rate is alway 5% higher than the first discount rate
    
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
        self.price = price # Ensuring price is store as a float
        self.stock = stock # Ensuring stock is store as an integer

     # Update the price of the product
    def set_price(self, new_price:float):
        """
        This function will update the price of the product
        
        Input:
        - new_price: the new price of the product
        """
        self.price = float(new_price)
    # Update the stock of the product
    def set_stock(self, new_stock:int):
        """
        This function will update the stock of the product
        
        Input:
        - new_stock: the new stock of the product
        """
        self.stock = int(new_stock)
    # Print the product information
    def display_info(self):
        return f"ID: {self.id}\nName: {self.name}\nPrice: {self.price}\nStock: {self.stock}"
    
class Order:
    def __init__(self, customer:Customer, product:Product, quantity:int):
        self.customer = customer # We will be using customer id as it ensure we are reference to the correct customer everytime
        self.product = product # We will be using product id to ensure we are reference to to the correct product everytime
        self.quantity = quantity

    def update_product_stock(self):
        """This function will update the stock of the product after the order is placed"""
        # For this week requirement I will ignored the case there the value is negative.
        try:
            # Calculate the new stock
            self.product.stock = self.product.stock - self.quantity
            # Update the product stock
            self.product.set_stock(self.product.stock)
        except ValueError:
            raise ValueError("Invalid quantity")
        
    def update_customer_value(self):
        """This function will update the customer value after the order is placed"""
        # Calculate the new value and update it.
        self.customer.value = self.customer.value + (self.product.price * self.quantity)
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
                    elements = line.strip().split(',')
                    # Validate the customer record
                    if len(elements) == 4:
                         id, name, discount_rate, value = elements
                    else:
                        raise ValueError(f"Invalid customer record {elements}")
                    # Validate the customer id and create the customer object
                    if id.startswith("C"):
                        customer_id = Customer (id, name, value)
                        self.customer_list.append(customer_id)
                        line = f.readline()
                    elif id.startswith("M"):
                        customer_id = Member (id, name, value)
                        self.customer_list.append(customer_id)
                        line = f.readline()
                    elif id.startswith("V"):
                        customer_id = VipMember (id, name, value)
                        customer_id.set_rate("rate_1",discount_rate)
                        self.customer_list.append(customer_id)
                        line = f.readline()
                    else:
                        raise ValueError(f"Invalid customer id {id}")
                    # Validate that the customer id is unique
                    if id in [customer.id for customer in self.customer_list]:
                        raise ValueError(f"Duplicate customer id {id}")
                    if value in [customer.value for customer in self.customer_list < 0]:
                        raise ValueError(f"Invalid customer value {value}")
        except FileNotFoundError:
            raise FileNotFoundError(f'File {self.customer_file} is missing!')
    
    def read_product(self):
        """This function will read the product file and import into the record """
        try:
            with open(self.product_file,"r") as f:
                line = f.readline()
                while line:
                    elements = line.strip().split(',')
                    # Validate the product record
                    if len(elements) == 4:
                        item_id, name, price, stock = elements
                    else:
                        raise ValueError(f"Invalid product record {elements}")
                    # Validate the product id and create the product object
                    if not item_id.startswith("P"):
                        raise ValueError(f"Invalid product id {item_id}")
                    if price < 0:
                        raise ValueError(f"Invalid product price {price}")
                    if stock < 0:
                        raise ValueError(f"Invalid product stock {stock}")
                    product_id = Product(item_id, name, price, stock)
                    self.product_list.append(product_id) # Add the new product into the product id
                    # Check if the product id is unique
                    if id in [product.get_id for product in self.product_list]:
                        raise ValueError(f"Duplicate product id {id}")
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


def get_info(data:Record):
    """
    This function will take information from the client
    
    Input:
    - Data: the main record object that contain the customer and product list
    """
    name = input("Please enter the customer name [e.g. Loki]: ")
    # We will be creating a new customer attributes to track the customer details
    customer = data.find_customer("name", name)
    print()
    product = get_product_info(data)
    print()
    quantity = get_product_quantity(product)
    print()
    # If the customer does not exit, we will be creating a new customer and check if they want a membership
    if customer is None:
        member_type = get_membership()
        id = generate_new_customer_id(member_type, data)
        new_customer = Customer(id, name)
        data.add_customer(new_customer)
    return customer, product, quantity

def get_membership():
    """This function will take the membership information from the client"""
    while True:
        _membership = input("This is a new customer. \
                            Does the customer want to have a membership [e.g. enter y or n]: ")
        if _membership == "y":
            print("We have two type of membership: V for VIP and M for Member")
            while True:
                _type = input("Please enter the membership type [e.g. V or M]: ")
                if _type == "V":
                    return "V"
                elif _type == "M":
                    return "M"
                print("Invalid input. Please enter V or M")
        elif _membership == "n":
            return "C"
        print('Invalid input. Please enter y or n')

def get_product_info(data: Record):
    """
    This function will take information from the client
    
    Input:
    - Data: the main record object that contain the customer and product list
    """
    while True:
        name = input("Please enter the product name [e.g. Apple]: ")
        # We will be creating a new customer attributes to track the customer details
        _product = data.find_product("name",name)
        if _product is not None:
            return _product

def get_product_quantity(item:Product):
    """
    This function will take the product quantity from the client
    """
    stock = item.stock
    while True:
        try:
            _quantity = int(input("Please enter the quantity [e.g. 10]: "))
            if _quantity < 0:
                print ("Invalid input, please try again")
            elif _quantity > stock:
                print("Insufficient stock, please try again")
            else:
                return _quantity
        except ValueError:
            print("Invalid input, please try again")
            continue        

def generate_new_customer_id(type:str, data:Record):
    """
    This function will generate a new unique customer id for the new customer
    
    Input:
    - type: the type of customer
    - data: the record object that contain the customer list
    """
    i = 1
    new_id = type + str(len(data.customer_list) + i)
    while new_id in [customer.get_id for customer in data.customer_list]:
        i += 1
        id = type + str(len(data.customer_list) + i) 
    return new_id

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
    except FileNotFoundError as _e:
        print(f"{_e}")
        sys.exit("Please check the file path and try again!")
    # Run the menu
    menu(SysRecord)


if __name__ == "__main__":
    try:
       main()
    # Exit the program gracefully when sys.exit() is called
    # This is to ensure consistent behaviour across IDE or terminal
    except SystemExit as e:
        print(f"{e}")
