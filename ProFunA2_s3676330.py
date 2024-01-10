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
    def __init__(self, _id:str, _name:str, _value:float = 0.00):
        self._id = _id # Initialise the customer id using c_id as a private variable to avoid conflict with the id() function
        self._name = _name # Initialise the customer name using c_name as a private variable to avoid conflict with the name() function
        self._value = _value # Initialise the customer value using c_value as a private variable to avoid conflict with the value() function
    def __str__(self) -> str:
        return f"{self._id}"
    @property
    def id(self) -> str:
        """This function will return the customer id"""
        return self._id
    @property
    def name(self) -> str:
        """This function will return the customer name"""
        return self._name
    @property
    def value(self) -> float:
        """This function will return the customer value"""
        return self._value
    def set_value(self, new_value:float) -> None:
        """This function will update the customer value"""
        self._value = float(new_value)
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
        print( f"ID: {self._id}\n \
                Name: {self._name}\n \
                Value: {self._value}\n \
                Discount Rate: 0")
# Create a new member class that inherited it attributes from customer
class Member(Customer):
    """
    This class will store the member information. 
    It will inherited the attributes from customer class

    Input:
    - id: the member id
    - name: the member name
    - value: the member value represent by float
    """
    # Initialise the discount rate for the member class.
    # Since this is the same for all instance of the class, I will be using class variable.
    discount_rate = 0.05
    # Initialise the class member and inherited the attributes from customer class.
    def __init__(self, _id, _name:str, _value:float = 0.00) -> None:
        # Initialise the class throught initialising the parent class variable.
        super().__init__(_id,_name,_value)
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
    def __init__ (self, _id, _name:str, _value:float = 0.00) -> None:
        super().__init__(_id, _name, _value)
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
        print( f"ID: {self._id}\n \
               Name: {self._name}\n \
               Value: {self._value}\n \
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
    def __init__(self, _id, _name:str, _price:float, _stock:int):
        try:
            self._id = _id
            self._name = _name
            self._price = _price # The price of the product can be None or negative
            self._stock = _stock
        except ValueError as exc:
            raise ValueError("Invalid input") from exc
    def __str__(self) -> str:
        """Create a string representation of the product"""
        return f"{self._id}"
    @property
    def id(self)-> str:
        """This function will return the product id"""
        return self._id
    @property    
    def name(self)-> str:
        """This function will return the product name"""
        return self._name
    @property    
    def price(self)-> float:
        """This function will return the product price"""
        if self._price is None:
            return None
        return float(self._price)
    @property    
    def stock(self)-> int:
        """This function will return the product stock"""
        return int(self._stock)
    def set_price(self, new_price:float):
        """
        This function will update the price of the product
        
        Input:
        - new_price: the new price of the product
        """
        self._price = float(new_price,2)
    # Update the stock of the product
    def set_stock(self, new_stock:int):
        """
        This function will update the stock of the product
        
        Input:
        - new_stock: the new stock of the product
        """
        self._stock = int(new_stock)

    def display_info(self):
        """This function will return the string representation of the product"""
        print (f"ID: {self._id}\n \
                Name: {self._name}\n \
                Price: {self._price}\n \
                Stock: {self._stock}")      
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
    def __init__(self, _id, _name:str, _product_list:list, _stock:int):
        try:
            self._id = _id
            self._name = _name
            self._product_list = _product_list
        except ValueError as exc:
            raise ValueError("Invalid input") from exc
        # Initialise the price of the bundle by calculate the product include in the bundle
        self._price = 0
        self._stock = _stock
        self.update_price()
    def __str__(self)-> str:
        """This function will return the string representation of the bundle"""
        return f"{self._id}"
    def update_price(self):
        """This function will update the price of the bundle"""
        # Calculate the price based on the products in the bundle.
        # Adding method to handle None price.
        self._price = sum(product.price if product.price is not None \
                           else 0 for product in self._product_list)
    @property
    def id(self):
        """This function will return the bundle id"""
        return self._id
    @property
    def name(self):
        """This function will return the bundle name"""
        return self._name
    @property
    def product_list(self):
        """This function will return the list of product in the bundle"""
        return self._product_list
    @property
    def price(self):
        """This function will return the bundle price"""
        return self._price
    @property
    def stock(self):
        """This function will return the bundle stock"""
        return self._stock
    def add_product(self, product:Product):
        """This function will add a product into the bundle and also update the bundle price"""
        # Check to see if the product already exit in the bundle
        if product in self._product_list:
            raise ValueError("Product already in the bundle")
        self._product_list.append(product)
        # Update the price of the bundle after add new product.
        self.update_price()
    def set_stock(self, new_stock:int):
        """This function will update the stock of the bundle"""
        self._stock = int(new_stock)
    def display_info(self):
        """This function will print the information of the bundle"""
        product_ids = [product.id for product in self._product_list]
        print(f"ID: {self._id}\n \
                Name: {self._name}\n \
                Stock: {self._stock}\n \
                Price: {self._price}\n \
                Product List: {product_ids}")
# Create a new order class to store the order information
class Order:
    """
    This class will store the order information

    Input:
    - customer: the customer object
    - product: the product or bundle object
    - quantity: the quantity of the product
    """
    def __init__(self, customer:Customer, product:Product, quantity:int, date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        """
        This function will initialise the order object.
        """
        self.customer = customer
        self.product = product
        self.quantity = quantity
        # Record the date the order is placed. If the time was not provided the date is set to the current date and time
        self.date = date
    def __str__(self) -> str:
        """This function will return the string representation of the order"""
        return f"{self.customer.name}, {self.product}, {self.quantity}, {self.date}"
    def update_stock_and_value(self):
        """This function will update the stock of the product/bundle and customer value after the order is placed"""
        if isinstance(self.product, Product):
            # Update stock for product
            try:
                # Calculate the new stock
                _stock = int(self.product.stock) - int(self.quantity)
                # Update the product stock
                self.product.set_stock(_stock)
            except ValueError as exc:
                raise ValueError("Invalid quantity") from exc
        elif isinstance(self.product, Bundle):
            # Update stock for each product in the bundle
            for product in self.product.product_list:
                try:
                    # Calculate the new stock
                    product.set_stock(int(product.stock)- int(self.quantity))
                    # Update the product stock
                    product.set_stock(product.stock)
                except ValueError as exc:
                    raise ValueError("Invalid quantity") from exc
        # Update customer value
        self.customer.set_value(float(self.customer.value) + (float(self.product.price) * float(self.quantity)))
# Create a new record class to store the customer and product list
class Record:
    """
    This class will be the main record for the program. It will load the customer and product file into the record.
    All main function will be run through this class.
    """
    # Record will be a singleton pattern class in order to ensure there is only one record in the program.
    _instance = None # Initialise the class variable
    # I will be using os.path.join to ensure the file path to ensure the file path is correct regardless of operating system used.
    customer_file = os.path.join(os.path.dirname(__file__),r"COSC2976_assignment\\files_DIlevel\\customers.txt")
    product_file = os.path.join(os.path.dirname(__file__),r"COSC2976_assignment\\files_DIlevel\\products.txt")
    order_file = os.path.join(os.path.dirname(__file__),r"COSC2976_assignment\\files_DIlevel\\orders.txt")
    def __new__(cls, *args, **kwargs):
        """This function will ensure the class is a singleton class"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        """The class will create new instance of customer list and product list"""
        self.record_customers= {} 
        self.record_items = {}
        self.record_order = {}
    @staticmethod
    def parse_line(line):
        """Parse a line from a file and return the elements as a list."""
        return [element.strip() for element in line.strip().split(',')]
    def read_customer(self):
        """This function will look for the customer file and import it into the record"""
        try:
            with open(self.customer_file, "r", encoding = "utf-8") as f:
                line = f.readline()
                while line:
                    elements = self.parse_line(line)
                    # The expected length of the customer record can be change base on requirement level
                    expected_length = 4
                    # Validate the customer record
                    if len(elements) == expected_length:
                        _customer_id, _customer_name, _customer_rate, _customer_value = elements
                    # Validate the customer id and create the customer object
                    if _customer_id.startswith("C"):
                        customer = Customer (_customer_id, _customer_name, _customer_value)
                        self.add_record(customer)
                        line = f.readline()
                    elif _customer_id.startswith("M"):
                        customer = Member (_customer_id, _customer_name, _customer_value)
                        self.add_record(customer)
                        line = f.readline()
                    elif _customer_id.startswith("V"):
                        customer = VipMember (_customer_id, _customer_name, _customer_value)
                        customer.set_rate("rate_1",_customer_rate)
                        self.add_record(customer)
                        line = f.readline()
                    else:
                        raise ValueError(f"Invalid customer id {id} in {self.customer_file}")
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self.customer_file} is missing!') from exp
    @staticmethod
    def create_product(elements):
        """Create a Product object from a list of elements."""
        _item_id, _item_name, _item_price, _item_stock = elements
        # Format item id for search.
        _item_id = _item_id.strip()
        if _item_price == " ":
            # Mark the price as None if the price is not available
            _item_price = None
        return Product(_item_id, _item_name, _item_price, _item_stock)
    def create_bundle(self, elements):
        """Create a Bundle object from a list of elements."""
        _item_id = elements[0]
        _item_name = elements[1]
        _item_stock = int(elements[-1])
        _list_product = []  # Initialise the list of product in the bundle
        for product_id in elements[2:-1]:
            # Loop through the product IDs in the bundle and find the product object
            product = self.find_item(product_id)
            if product is None:
                raise ValueError(f"Invalid product record {elements} in {self.product_file}")
            _list_product.append(product)
        # Create the bundle record with the list that contains the product objects.
        return Bundle(_item_id, _item_name, _list_product, _item_stock)
    def read_product(self):
        """This function will read the product file and import into the record"""
        try:
            with open(self.product_file, "r", encoding="utf-8") as f:
                for line in f:
                    elements = self.parse_line(line)
                    # Split expected length for future change
                    min_length = 4
                    if elements[0].startswith("P") and len(elements) == min_length:
                        product = self.create_product(elements)
                        self.add_record(product)
                    elif elements[0].startswith("B") and len(elements) > min_length:
                        bundle = self.create_bundle(elements)
                        self.add_record(bundle)
                    else:
                        raise ValueError(f"Invalid product record {elements} in {self.product_file}")
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self.product_file} is missing!') from exp
    def read_order(self):
        """This function will read the order file and import it into the record"""
        try:
            with open(self.order_file, "r", encoding="utf-8") as f:
                for line in f:
                    elements = self.parse_line(line)
                    if len(elements) != 4:
                        raise ValueError(f"Invalid order record {elements} in {self.order_file}")
                    _customer_id, _item_id, _quantity, _date = elements
                    _date = datetime.datetime.strptime(_date.strip(), "%d/%m/%Y %H:%M:%S")
                    _customer = self.find_customer(_customer_id)
                    _quantity = int(_quantity)
                    if _customer is None:
                        raise ValueError(f"Invalid customer id {_customer_id} in {self.order_file}")
                    _product = self.find_item(_item_id)
                    if _product is None:
                        raise ValueError(f"Invalid product id {_item_id} in {self.order_file}")
                    order = Order(_customer, _product, _quantity, _date)
                    order.update_stock_and_value()
                    self.add_record(order)
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self.order_file} is missing!') from exp
        
    # Define the find function to find the customer, product, and order
    @staticmethod
    def search_process(value:str = None):
        """This function will preprocess the value for searching"""
        if value is None:
            raise ValueError("Invalid search value")
        return value.strip().lower()
    def find_customer(self, value:str = None):
        """ 
        Take a search key and find the customer detail from the customer list
        
        Input:
        - key : can either be "id" or "name"
        - value: the search value

        Output:
        - return customer detail if customer exit, return None if customer does not exit.

        """
        if value is None:
            raise ValueError("Invalid search value")    
        for customer in self.record_customers.values():
            try:
                if self.search_process(value) == self.search_process(customer.id) or self.search_process(value) == self.search_process(customer.name):
                    return customer # Return the customer if it exit
            except AttributeError as exc:
                raise ValueError(f"Invalid search key {value}") from exc
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

        for item in self.record_items.values():
            try:
                if self.search_process(value) == self.search_process(item.id) or \
                    self.search_process(value) == self.search_process(item.name):
                    return item # Return the product if it exit
            except AttributeError as exc:
                raise ValueError(f"Invalid search key {value}") from exc
        return None # If the product does not exit return None
    def find_order(self, value:Customer = None):
        """
        Take a search key and find the order from the order list

        Input:
        - key: can either be customer id or name

        Output:
        - return order detail is order exit else print order does not exit
        """
        if value is None:
            raise ValueError("Invalid search value")
        for item in self.record_order.values():
            try:
                if self.search_process(value) == self.search_process(item.name):
                    return item # Return the order if it exit
            except AttributeError as exc:
                raise ValueError(f"Invalid search key {value}") from exc
            
    def list_record_customers(self):
        """This function will return the list of customer in the record"""
        print('Insie list_record_customers')
        for customer in self.record_customers.values():
            customer.display_info()
    def list_record_items(self):
        """This function will return the list of product in the record"""
        for item in self.record_items.values():
            item.display_info()
    def list_all_record_order(self):
        """This function will return the list of order in the record"""
        for customer, orders in self.record_order.items():
            print()
            print(f"Customer ID: {customer}")
            if orders == []:
                print(f"Customer {customer} does not have any order")
                continue
            for order in orders:
                print(order)
    def list_customer_order(self, customer:Customer):
        """
        This function will return the list of order for a specific customer

        Input:
        - customer: the customer object
        """
        if customer not in self.record_order:
            print(f"Customer {customer} does not have any order")
            return
        for order in self.record_order[customer]:
            if self.record_order:
                print(order)
    def print_record(self):
        """This function will print the record of the the """
    # Define the add function to add new customer, product, and order
    def add_record(self, record):
        """
        This function will add a new record into the corresponding record dictionary.
        Base on the object type it will handle the record differently.

        Input:
        - record: record of Customer or Product or Order
        """
        if isinstance(record, Customer):
            self.record_customers[record.id] = record
            self.record_order[record] = []  # Initialize an empty list for this customer
        elif isinstance(record, Product) or isinstance(record, Bundle):
            self.record_items[record.id] = record
        elif isinstance(record, Order):
            customer = record.customer  # Assuming the Order has a reference to the Customer
            if customer in self.record_order:
                self.record_order[customer].append(record)
            else:
                print("Error: Order's customer not found in record_order")
        else:
            raise TypeError("Invalid record type")
    def input_info(self):
        """
        This function will take information from the client
        
        Input:
        - Data: the main record object that contain the customer and product list
        """

        _name = input("Please enter the customer name [e.g. Loki]: \n")
        # We will be creating a new customer attributes to track the customer details
        _customer = self.find_customer(_name)
        print()
        while True:
            _item = input("Please enter the product name [e.g. product id = 'P1' or product name = 'Pant']: \n")
            # We will be creating a new product attributes to track the product details
            _item = self.find_item(_item)
            if _item is None:
                print("Item does not exit. Please try again.\n")
                continue
            if _item.price is None or _item.price < 0:
                print("Item price is invalid. Please try again.\n")
                continue
            # If the item 
            break
        print()
        while True:
            try:
                _quantity = int(input('Please enter the quantity [e.g. 1]: \n'))
                if _quantity <= 0:
                    print("Quantity must be a positive number. Please try again.\n")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid quantity.\n")
        print()
        # If the customer does not exist, we will be creating a new customer and check if they want a membership
        if _customer is None:
            member_type = new_customer_membership_option()
            _id = self.generate_new_customer_id(member_type)
            new_customer = Customer(_id, _name)
            self.add_record(new_customer)
        return new_customer, _item, _quantity
    def generate_new_customer_id(self, r_type:str):
        """
        This function will generate a new unique customer id for the new customer
            
        Input:
        - type: the type of customer
        - data: the record object that contain the customer list
        """
        i = 1
        new_id = r_type + str(len(self.record_customers) + i)
        while new_id in [customer.id for customer in self.record_customers.values()]:
            i += 1
            new_id = r_type + str(len(self.record_customers) + i)
        return new_id
    def most_valuable_customer(self):
        """
        Finds and returns the most valuable customer based on their total purchases.

        Returns:
            str: The name of the most valuable customer.
        """
        pass
    def most_popular_product(self):
        """
        Returns the most popular product in the retail management system.

        This method analyzes the sales data and determines the product that has been sold the most.
        It returns the name or ID of the most popular product.

        Returns:
            str: The name or ID of the most popular product.
        """
        pass
# Define the main interactive method
    def menu_loop(self):
        """
        This function will display the menu and run the selected function based on the user input.
        It will continue to run until the user choose to exit the program
        """
        def display_menu(): # Since display_menu is only use in this function, I will be defining it as a sub function
            """Sub function to display the menu"""
            print("#"*30)
            print("You can choose from the following option:")
            print("1. Place an order")
            print("2. Display existing customers")
            print("3. Display existing products")
            print("4. Adjust the discount rate for VIP members")
            print("5. Set a new threshold for VIP members")
            print("6. Display all orders")
            print("7. Display all orders for a customer")
            print("8. Summarize all orders")
            print("9. Review the most valuable customer")
            print("10. Review the most popular product")
            print("0. Exit the program")
            print("#"*30)
            print()
        while True:
            display_menu()
            user_input = input("Choose one option: ")
            print()
            if user_input == "1":
                # Take the information from the client and place an order
                customer, product, quantity = self.input_info()
                place_order(customer, product, quantity)
            elif user_input == "2":
                # Display the customer list
                self.list_record_customers()
            elif user_input == "3":
                # Display the product list
                self.list_record_items()
            elif user_input == "4":
                # Adjust the discount rate for the vip member
                adjust_vip_discount_rate('Please enter the vip member name or id [e.g. V1]: \n')
            elif user_input == "5":
                new_threshold = float(input("Please enter the new threshold: "))
                VipMember.set_threshold(new_threshold)
            elif user_input == "6":
                self.list_all_record_order()
            elif user_input == "7":
                _customer = input("Please enter the customer name or id [e.g. Loki]: \n")
                print()
                _customer = self.find_customer(_customer)
                self.list_customer_order(_customer)
            elif user_input == "8":
                #TODO: Summarize all orders
                pass
            elif user_input == "9":
                #TODO: Review the most valuable customer
                pass
            elif user_input == "10":
                #TODO: Review the most popular product
                pass
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
    while True:
        _membership = input("This is a new customer. Does the customer want to have a membership [e.g. enter y or n]: \n")
        if _membership == "y":
            while True:
                _type = input("Please enter the membership type [e.g. V for VIP or M for regular member]: \n")
                if _type == "V":
                    return "V"
                elif _type == "M":
                    return "M"
                print("Invalid input. Please enter V or M\n")
        elif _membership == "n":
            return "C"
        print('Invalid input. Please enter y or n\n')

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
    new_order.update_stock_and_value()
    # Calculate the discount
    discount_rate, new_price = customer.get_discount(product.price)
    if isinstance(customer, VipMember):
        vip_fee = VipMember.price
        total_price = float(new_price * quantity + vip_fee)
    else:
        total_price = float(new_price * quantity)
    customer.set_value(customer.value + total_price)
    # Print the order detail
    print()
    print("="*50)
    print(f'{customer.name} purchases {quantity} x {product.name}')
    print(f'Unit price: {product.price:.2f} (AUD)')
    if isinstance(customer, VipMember):
        print(f'Membership price: {vip_fee:.2f} (AUD) not discounted')
    print(f'{customer.name} gets a discount of {discount_rate*100:.0f}%.')
    print(f'Price to pay: {total_price:.2f} (AUD)')
    print("="*50)

def adjust_vip_discount_rate(prompt):
    """This function will adjust the discount rate for the vip member"""
    while True:
        try:
            _customer = input(prompt)
            _vip_member = Record.find_customer(_customer)
            if not isinstance(_vip_member, VipMember):
                print("Invalid customer!\n")
                continue
            break
        except ValueError as exc:
            print(f"{exc}")
            continue
    while True:
        try:
            _rate = float(input("Please enter the new discount rate [e.g. 0.1]: \n"))
            print()
            _vip_member.set_rate(_rate)
            break
        except ValueError as exc:
            print(f"{exc}")
            continue
    print(f"Discount rate for {_vip_member.name} has been updated to {_rate} \n")

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
    try:
        data.read_order()
    except FileNotFoundError as _e:
        print(f"{_e}")
        print("Cannot load the order file. Run as if there is no order previously")
    # Use the menu function to interact with the user
    data.menu_loop()

if __name__ == "__main__":
    try:
        main()
    # Exit the program gracefully when sys.exit() is called
    # This is to ensure consistent behaviour across IDE or terminal
    except SystemExit as e:
        print(f"{e}")