"""
 This program is a retail management system that allows cashier to place an order for a customer, 
 add/update products and prices, and display existing customers and products, etc.

 - 14/12/2023: Create program acording to the requirement for PASS level in week 7.
 
 """
import sys
import os
import datetime

# Define the required classes for the program
class Customer:
    """
    This class will store the customer information

    Input:
    - id: the customer id
    - name: the customer name
    - value: the customer value
    """
    def __init__(self, c_id:str, c_name:str, c_value:float = 0.00):
        self.c_id = c_id # Initialise the customer id using c_id as a private variable to avoid conflict with the id() function
        self.c_name = c_name # Initialise the customer name using c_name as a private variable to avoid conflict with the name() function
        self.c_value = float(c_value) # Initialise the customer value using c_value as a private variable to avoid conflict with the value() function
    def __str__(self) -> str:
        return f"Customer Name: {self.c_name} (ID: {self.c_id})"
    def get_id(self) -> str:
        """This function will return the customer id"""
        return self.c_id
    def get_name(self) -> str:
        """This function will return the customer name"""
        return self.c_name
    def get_value(self) -> float:
        """This function will return the customer value"""
        return self.c_value
    def get_discount(self, price) -> tuple:
        """
        Calculate the discount for a given price.

        Parameters:
        - price (float): The original price of the item.

        Returns:
        - tuple: A tuple containing two values
        the discount percentage (0 in this case) 
        and the discounted price (same as the original price).
        """
        return (0, price)
    # Return the class information and the discount information.
    def display_info(self) -> str:
        """This function will print the information of the customer"""
        print( f"ID: {self.c_id}\n \
                Name: {self.c_name}\n \
                Value: {self.c_value}\n \
                Discount Rate: 0")
# Create a new member class that inherited it attributes from customer
class Member(Customer):
    """
    This class will store the member information. 
    It will inherited the attributes from customer class

    Input:
    - c_id: the member id
    - c_name: the member name
    - c_value: the member value
    """
    # Initialise the discount rate for the member class.
    # Since this is the same for all instance of the class, I will be using class variable.
    discount_rate = 0.05 
    # Initialise the class member and inherited the attributes from customer class.
    def __init__(self, c_id, c_name:str, c_value:float = 0.00) -> None:
        # Initialise the class throught initialising the parent class variable.
        super().__init__(c_id,c_name,c_value)
    # Update the get_discount method with new calculation
    def get_discount(self, price: float) -> tuple:
        """
        This function will calculate the discount for the member

        Input:
        - price: the price of the product

        Output:
        - return a tuple contain the discount rate and the new price
        """
        new_price = price * (1 - self.discount_rate)
        return (self.discount_rate, new_price)
    # Create a new class method to update the flat discount rate
    # I will be using @classmethod decorator to ensure the method is a class method
    @classmethod
    def set_rate(cls, new_rate: float) -> None:
        """
        This function will update the discount rate of the member class
        
        Input:
        - new_rate: the new discount rate
        """
        cls.discount_rate = new_rate
# Create a new vip member class that inherited it attributes from customer
class VipMember(Customer):
    """
    This class will store the vip member information

    Input:
    - id: the vip member id
    - name: the vip member name
    - value: the vip member value
    """
    # Initialise the two discount rate and threshold for the class
    threshold = 1000.00
    # Initialise the price for the membership.
    # This will be a class variable as it will be the same for all instance of the class
    price = 200.00

    # Initialise the class throught initialising the parent class
    def __init__ (self, c_id, c_name:str, c_value:float = 0.00) -> None:
        super().__init__(c_id, c_name, c_value)
        self.discount_rate_1 = 0.10 # The default first discount rate is alway 10%
        self.discount_rate_2 = 0.15 # The default second discount rate is alway 5% higher than the first discount rate
    # Update the get_discount method with new calculation
    def get_discount(self, price:float) -> tuple:
        """
        This function will calculate the discount for the vip member

        Input:
        - price: the price of the product
        """
        if price <= self.threshold:
            return (self.discount_rate_1, price * (1- self.discount_rate_1))
        else:
            return (self.discount_rate_2, price * (1- self.discount_rate_2))
    def display_info(self) -> str:
        """
       This function will print out the value of the vip member
        """
        print( f"ID: {self.c_id}\n \
               Name: {self.c_name}\n \
               Value: {self.c_value}\n \
               Discount Rate 1: {float(self.discount_rate_1)}\n \
               Discount Rate 2: {float(self.discount_rate_2)}")
    def set_rate(self, rate_type: str = "rate_1", new_rate:float = 0.00) -> None:
        """
        This function will update the discount rate of the vip member. The default rate type is rate_1
        When update rate_1, rate_2 will be updated automatically to ensure rate_2 is always 5% higher than rate_1 and vice versa
        
        Input:
        - rate_type: can either be "rate_1" or "rate_2"
        - new_rate: the new discount rate
        """
        if rate_type == "rate_1":
            self.discount_rate_1 = float(new_rate)
            self.discount_rate_2 = float(self.discount_rate_1 + (0.05 * self.discount_rate_1))
        elif rate_type == "rate_2":
            self.discount_rate_2 = new_rate
            self.discount_rate_1 = float(self.discount_rate_2 - (0.05 * self.discount_rate_2))
        else:
            raise ValueError("Invalid rate type. Rate can either be 'rate_1' or 'rate_2'")
    @classmethod
    def set_threshold(cls, new_threshold:float) -> None:
        """
        This function will update the discount threshold of the vip member class

        Input:
        - new_threshold: the new discount threshold
        """
        cls.threshold = new_threshold
# Create a new product class to store the product information
class Product:
    """
    This class will store the product information

    Input:
    - id: the product id
    - name: the product name
    - price: the product price
    - stock: the product stock
    """
    def __init__(self, p_id, p_name:str, p_price:float, p_stock:int):
        try:
            self.p_id = p_id
            self.p_name = p_name
            self.p_price = p_price
            self.p_stock = p_stock
        except ValueError as exc:
            raise ValueError("Invalid input") from exc
    def get_id(self)-> str:
        """This function will return the product id"""
        return self.p_id
    def get_name(self)-> str:
        """This function will return the product name"""
        return self.p_name
    def get_price(self)-> float:
        """This function will return the product price"""
        return float(self.p_price)
    def get_stock(self)-> int:
        """This function will return the product stock"""
        return int(self.p_stock)
    def __str__(self) -> str:
        """Create a string representation of the product"""
        return f"Product Name: {self.p_name} (ID: {self.p_id})"
    def set_price(self, new_price:float):
        """
        This function will update the price of the product
        
        Input:
        - new_price: the new price of the product
        """
        self.p_price = float(new_price,2)
    # Update the stock of the product
    def set_stock(self, new_stock:int):
        """
        This function will update the stock of the product
        
        Input:
        - new_stock: the new stock of the product
        """
        self.p_stock = int(new_stock)

    def display_info(self):
        """This function will return the string representation of the product"""
        print (f"ID: {self.p_id}\n \
                Name: {self.p_name}\n \
                Price: {self.p_price}\n \
                Stock: {self.p_stock}")
# Create a new bundle class that is a composition of product class
# This is to ensure future change to the product class will not affect the bundle class
class Bundle:
    """
    This class will store the bundle information

    Input:
    - id: the bundle id
    - name: the bundle name
    - product_list: the list of product in the bundle
    """
    def __init__(self, b_id, b_name:str, b_product_list:list, b_stock:int):
        try:
            self.b_id = b_id
            self.b_name = b_name
            self.b_product_list = b_product_list
        except ValueError as exc:
            raise ValueError("Invalid input") from exc
        # Initialise the price of the bundle by calculate the product include in the bundle
        self.update_price()
        self.b_stock = b_stock
    def get_id(self):
        """This function will return the bundle id"""
        return self.b_id
    def update_price(self):
        """This function will update the price of the bundle"""
        # Calculate the price based on the products in the bundle
        self.b_price = sum(product.get_price() for product in self.b_product_list)
    def get_name(self):
        """This function will return the bundle name"""
        return self.b_name
    def get_product_list(self):
        """This function will return the list of product in the bundle"""
        return self.b_product_list
    def get_price(self):
        """This function will return the bundle price"""
        return self.b_price
    def get_stock(self):
        """This function will return the bundle stock"""
        return self.b_stock
    def __str__(self)-> str:
        """This function will return the string representation of the bundle"""
        return f"Bundle Name: {self.b_name} (ID: {self.b_id})"
    def add_product(self, product:Product):
        """This function will add a product into the bundle and also update the bundle price"""
        # Check to see if the product already exit in the bundle
        if product in self.b_product_list:
            raise ValueError("Product already in the bundle")
        self.b_product_list.append(product)
        # Update the price of the bundle after add new product.
        self.update_price()
    def set_stock(self, new_stock:int):
        """This function will update the stock of the bundle"""
        self.b_stock = int(new_stock)
    def display_info(self):
        """This function will print the information of the bundle"""
        print(f"ID: {self.b_id}\n \
              Name: {self.b_name}\n \
              Stock: {self.b_stock}")
        for product in self.b_product_list:
            print(product)
# Create a new order class to store the order information
class Order:
    """
    This class will store the order information

    Input:
    - customer: the customer object
    - product: the product or bundle object
    - quantity: the quantity of the product
    """
    def __init__(self, customer:Customer, product:Product, quantity:int):
        """
        This function will initialise the order object.
        """
        self.customer = customer
        self.product = product
        self.quantity = quantity
        # Record the date teh order is placed
        self.date = datetime.datetime.now()
    
    def update_product_stock(self):
        """This function will update the stock of the product after the order is placed"""
        # For this week requirement I will ignored the case there the value is negative.
        try:
            # Calculate the new stock
            self.product.stock = self.product.stock - self.quantity
            # Update the product stock
            self.product.set_stock(self.product.stock)
        except ValueError as exc:
            raise ValueError("Invalid quantity") from exc    
    def update_customer_value(self):
        """This function will update the customer value after the order is placed"""
        # Calculate the new value and update it.
        self.customer.c_value = self.customer.c_value + (self.product.price * self.quantity)
    def display_info(self):
        """return a string that represent the order when print"""
        return f"Customer ID: {self.customer}\n \
        Product ID: {self.product}\n \
        Quantity: {self.quantity}"
# Create a new record class to store the customer and product list
class Record:
    """
    This class will be the main record for the program. It will load the customer and product file into the record.
    All main function will be run through this class.
    """
    # Record will be a singleton pattern class in order to ensure there is only one record in the program.
    _instance = None # Initialise the class variable
    # I will be using os.path.join to ensure the file path to ensure the file path is correct regardless of operating system used.
    customer_file = os.path.join(os.path.dirname(__file__),r"COSC2976_assignment\\files_CREDITlevel\\customers.txt")
    product_file = os.path.join(os.path.dirname(__file__),r"COSC2976_assignment\\files_CREDITlevel\\products.txt")
    def __new__(cls, *args, **kwargs):
        """This function will ensure the class is a singleton class"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """The class will create new instance of customer list and product list"""
        self.record_customers= [] # In this list we will be storing a list of customer id in order to ensure uniqueness
        self.record_items = [] # In this list we will be storeing a list of product id and bundle in order to ensure uniqueness

    def read_customer(self):
        """This function will look for the customer file and import it into the record"""
        try:
            with open(self.customer_file, "r", encoding = "utf-8") as f:
                line = f.readline()
                while line:
                    elements = line.strip().split(',')
                    # The expected length of the customer record can be change base on requirement level
                    expected_length = 4 
                    # Validate the customer record
                    if len(elements) == expected_length:
                        _customer_id, _customer_name, _customer_rate, _customer_value = elements
                    # Validate the customer id and create the customer object
                    if _customer_id.startswith("C"):
                        customer = Customer (_customer_id, _customer_name, _customer_value)
                        self.record_customers.append(customer)
                        line = f.readline()
                    elif _customer_id.startswith("M"):
                        customer = Member (_customer_id, _customer_name, _customer_value)
                        self.record_customers.append(customer)
                        line = f.readline()
                    elif _customer_id.startswith("V"):
                        customer = VipMember (_customer_id, _customer_name, _customer_value)
                        customer.set_rate("rate_1",_customer_rate)
                        self.record_customers.append(customer)
                        line = f.readline()
                    else:
                        raise ValueError(f"Invalid customer id {id} in {self.customer_file}")
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self.customer_file} is missing!') from exp
    def read_product(self):
        """This function will read the product file and import into the record"""
        try:
            with open(self.product_file, "r", encoding="utf-8") as f:
                line = f.readline()
                while line:
                    elements = line.strip().split(',')
                    # Split expected length for future change
                    min_length = 4
                    if elements[0].startswith("P") and len(elements) == min_length:
                        _item_id, _item_name, _item_price, _item_stock = elements
                        product = Product(_item_id, _item_name, _item_price, _item_stock)
                        self.record_items.append(product)
                    elif elements[0].startswith("B") and len(elements) > min_length:
                        _item_id = elements[0]
                        _item_name = elements[1]
                        _item_stock = int(elements[-1])
                        _list_product = [] # Initialise the list of product in the bundle
                        for product in elements[2:-1]:
                            #loop through the product id in the bundle and find the product object
                            product = self.find_item(product)
                            if product is None:
                                raise ValueError(f"Invalid product record {elements} in {self.product_file}")
                            _list_product.append(product)
                        # Create the bundle record with the list that contain the product object.
                        bundle = Bundle(_item_id, _item_name, _list_product, _item_stock)
                        # Add the generate bundle into the record items list
                        self.record_items.append(bundle)
                    else:
                        raise ValueError(f"Invalid product record {elements} in {self.product_file}")     
                    line = f.readline()
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self.product_file} is missing!') from exp

    def find_customer(self, value:str = None):
        """ 
        Take a search key and find the customer detail from the customer list
        
        Input:
        - key : can either be "id" or "name"
        - value: the search value

        Output:
        - return customer detail if customer exit return None if customer does not exit

        """
        if value is None:
            raise ValueError("Invalid search value")    
        for customer in self.record_customers:
            try:
                # Preprocess value for comparison
                _value = value.strip().lower()
                if _value == customer.get_id().strip().lower() or _value == customer.get_name().strip().lower():
                    return customer # Return the customer if it exit
            except AttributeError as exc:
                raise ValueError(f"Invalid search key {_value}") from exc
        return None # If the customer does not exit return None
        
    def find_item(self, value:str = None):
        """ 
        Take a search key and find the product from the product list
        
        Input:
        - key: can either be product id or name

        Output:
        - return product detail is product exit else print product does not exit
        """
        if value is None:
            raise ValueError("Invalid search value")
    
        for item in self.record_items:
            try:
                # Preprocess value for searching
                _value = value.strip().lower()
                if _value == item.get_id().strip().lower() or _value == item.get_name().strip().lower():
                    return item # Return the product if it exit
            except AttributeError as exc:
                raise ValueError(f"Invalid search key {_value}") from exc
        return None # If the product does not exit return None


    def list_record_customers(self):
        """This function will return the list of customer in the record"""
        for customer in self.record_customers:
            customer.display_info()

    def list_record_items(self):
        """This function will return the list of product in the record"""
        for item in self.record_items:
            item.display_info()
    
    def add_customer(self, customer:Customer):
        """
        This function will add a new customer into the record
        
        Input:
        - customer: the customer object that want to add into the record
        """
        if isinstance(customer, Customer):
            self.record_customers.append(customer)
        else:
            raise TypeError("customer must be a Customer object or it subclass")
        
    def add_product(self, product:Product):
        """
        This function will add a new product into the record
        
        Input:
        - product: the product object that want to add into the record
        """
        if isinstance(product, Product) or isinstance(product, Bundle):
            self.record_items.append(product)
        else:
            raise TypeError("product must be a Product or Bundle object")
    
    def input_info(self):
        """
        This function will take information from the client
        
        Input:
        - Data: the main record object that contain the customer and product list
        """
        name = input("Please enter the customer name [e.g. Loki]: ")
        # We will be creating a new customer attributes to track the customer details
        customer = self.find_customer(name)
        print()
        product = input("Please enter the product name [e.g. Apple]: ")
        print()
        quantity = int(input('Please enter the quantity [e.g. 1]: '))
        print()
        # If the customer does not exit, we will be creating a new customer and check if they want a membership
        if customer is None:
            member_type = new_customer_membership_option()
            _id = generate_new_customer_id(member_type, self)
            new_customer = Customer(_id, name)
            self.add_customer(new_customer)
        return customer, product, quantity
        
def generate_new_customer_id(r_type:str, data:Record):
    """
    This function will generate a new unique customer id for the new customer
    
    Input:
    - type: the type of customer
    - data: the record object that contain the customer list
    """
    i = 1
    new_id = r_type + str(len(data.record_customers) + i)
    while new_id in [customer.get_id for customer in data.record_customers]:
        i += 1
        new_id = r_type + str(len(data.record_customers) + i)
    return new_id

def menu_loop(data:Record):
    """
    This function will display the menu and run the selected function based on the user input.
    It will continue to run until the user choose to exit the program
    """
    def display_menu(): # Since display_menu is only use in this function, I will be defining it as a sub function
        """Sub function to display the menu"""
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
            customer, product, quantity = data.input_info()
            place_order(customer, product, quantity)
        elif user_input == "2":
            # Display the customer list
            data.list_record_customers()
        elif user_input == "3":
            # Display the product list
            data.list_record_items()
        elif user_input == "0":
            sys.exit("Thank you for using the program!")
        else:
            print("Invalid input, please try again")
            continue
        # Pause the program and wait for the user to press enter to continue
        print()
        input("Press enter to continue!")
        print()

def new_customer_membership_option():
    """This function will take the membership information from a new client who did not have a membership"""
    print("This is a new customer \n")
    while True:
        _membership = input("Does the customer want to have a membership [e.g. enter y or n]: ")
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

def place_order(customer:Customer, product: Product, quantity:int):
    """
    This function will place an order for the customer

    Input:
    - customer: the customer object
    - product: the product object
    - quantity: the quantity of the product
    """
    # Check if the inputs are valid
    # TODO: Create a while loop here to prompt the user to enter the correct input
    if not isinstance(customer, Customer) or not isinstance(product, (Product, Bundle)) or quantity <= 0:
        raise ValueError("Invalid input")
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
    customer_name = customer.c_name.strip()
    product_name = product.p_name.strip()
    product_price = product.c_price
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
    """This will be the main function of the program"""
    data = Record()
    # Read the customer and product file
    try:
        data.read_customer()
        data.read_product()
    except FileNotFoundError as _e:
        print(f"{_e}")
        sys.exit("Please check the file path and try again!")
    # Use the menu function to interact with the user
    menu_loop(data)


if __name__ == "__main__":
    try:
        main()
    # Exit the program gracefully when sys.exit() is called
    # This is to ensure consistent behaviour across IDE or terminal
    except SystemExit as e:
        print(f"{e}")
