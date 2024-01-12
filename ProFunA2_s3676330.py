"""
This program is a retail management system that allows cashier to place an order for a customer, 
 add/update products and prices, and display existing customers and products, etc.

 - 14/12/2023: Create program acording to the requirement for PASS level in week 7.
 - 20/12/2023: Create program acording to the requirement for CREDIT level in week 8.
 - 9/01/2023: Create program acording to the requirement for DISTINCTION level in week 9.
 - 11/01/2024: Create program acording to the requirement for HIGH DISTINCTION level in week 10.
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
        # Use string representation method to return the customer information in storage format
        return f"{self._id}, {self._name}, 0, {self._value}"
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
    # Return the class information and the discount information for user to check
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
    def __str__(self) -> str:
        return f"{self._id}, {self._name}, {self.discount_rate}, {self._value}"
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
    def display_info(self) -> str:
        """This function will print the information of the customer"""
        print( f"ID: {self._id}\n \
                Name: {self._name}\n \
                Value: {self._value}\n \
                Discount Rate: {self.discount_rate}")
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
    def __str__(self) -> str:
        return f"{self._id}, {self._name}, {self.discount_rate_1}, {self._value}"
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
            self.discount_rate_2 = float(self.discount_rate_1 + 0.05)
        elif rate_type == "rate_2":
            self.discount_rate_2 = new_rate
            self.discount_rate_1 = float(self.discount_rate_2 - 0.05)
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
        return self._price
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
    def __init__(self, _id: str, _name: str, _product_list:list[Product], _stock:int):
        self._id = _id
        self._name = _name
        self._product_list = _product_list
        self._price = 0
        self._stock = _stock
        self.update_price() # Call the function to calculate the price of the bundle
    def __str__(self)-> str:
        """This function will return the string representation of the bundle"""
        item_strs = [f"{item.id}" for item in self._product_list]
        return f"{self._id}, {self._name}, {item_strs}, {self._stock}"
    def update_price(self):
        """This function will update the price of the bundle"""
        # Calculate the price based on the products in the bundle.
        # Adding method to handle None price.
        self._price = sum(float(product.price) if product.price is not None \
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
class Order():
    """
    This class will store the order information

    Input:
    - customer: the customer object
    - product: the product or bundle object
    - quantity: the quantity of the product
    """
    def __init__(self,_customer:Customer, _items, _date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        """
        This function will initialise the order object.
        """
        self._customer = _customer
        self._items = _items # A list of tuple that contain (product, quantity)
        # Record the date the order is placed. If the time was not provided the date is set to the current date and time
        self._date = _date
    def __str__(self) -> str:
        """This function will return the string representation of the order"""
        item_strs = [f"{item.id}, {quantity}" for item, quantity in self._items]
        item_str = ', '.join(item_strs)
        return f"{self._customer.id}, {item_str}, {self._date}"
    @property
    def customer(self):
        """This function will return the customer object"""
        return self._customer
    @property
    def items(self):
        """This function will return the product or bundle object"""
        return self._items
    @property
    def date(self):
        """This function will return the date the order is placed"""
        return self._date
    def update_stock_and_value(self, record:'Record'):
        """This function will update the stock and value of the customer and product

        input:
        - record: the main record object that contain the customer and product list
        """
        for item, quantity in self._items:
            if isinstance(item, Product):
                try:
                    # Update the stock of the item in the order
                    item.set_stock(int(item.stock) - int(quantity))
                    # Get the corresponding Product in the Record
                    record_product = record.record_items.get(item.id)
                    if record_product is not None:
                        # Update the stock of the Product in the Record
                        record_product.set_stock(int(record_product.stock) - int(quantity))
                except ValueError as exc:
                    raise ValueError("Invalid quantity") from exc
            elif isinstance(item, Bundle):
                try:
                    # Update the stock of the product in the order
                    item.set_stock(int(item.stock) - int(quantity))
                    # Get the corresponding Bundle in the Record
                    record_bundle = record.record_items.get(item.id)
                    if record_bundle is not None:
                        # Update the stock of the Bundle in the Record
                        record_bundle.set_stock(int(record_bundle.stock) - int(quantity))
                except ValueError as exc:
                    raise ValueError("Invalid quantity") from exc
            # Once the stock is updated, update the value of the customer
            self._customer.set_value(float(self._customer.value) + (float(item.price) * float(quantity)))
# Create a new record class to store the customer and product list
class Record():
    """
    This class will be the main record for the program. 
    It will load the customer and product file into the record.
    All main function will be run through this class.
    """
    # Record will be a singleton pattern class in order to ensure there is only one record in the program.
    _instance = None # Initialise the class variable
    def __new__(cls, *args, **kwargs):
        """This function will ensure the class is a singleton class"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self,_customer_file, _product_file, _order_file):
        """The class will create new instance of customer, product, and order record"""
        self.record_customers= {}
        self.record_items = {}
        self.record_order = {}
        self._customer_file = _customer_file
        self._product_file = _product_file
        self._order_file = _order_file
    @staticmethod
    def parse_line(line):
        """Parse a line from a file and return the elements as a list."""
        return [element.strip() for element in line.strip().split(',')]
    def read_customer(self):
        """This function will look for the customer file and import it into the record"""
        try:
            with open(self._customer_file, "r", encoding="utf-8") as f:
                for line in f:
                    elements = self.parse_line(line)
                    # The expected length of the customer record can be changed based on requirement level
                    expected_length = 4
                    # Validate the customer record
                    if len(elements) == expected_length:
                        _customer_id, _customer_name, _customer_rate, _customer_value = elements
                        # Validate the customer id and create the customer object
                        if _customer_id.startswith(("C", "M", "V")):
                            if _customer_id.startswith("V"):
                                customer = VipMember(_customer_id, _customer_name, _customer_value)
                                customer.set_rate("rate_1", _customer_rate)
                            elif _customer_id.startswith("M"):
                                customer = Member(_customer_id, _customer_name, _customer_value)
                            else:
                                customer = Customer(_customer_id, _customer_name, _customer_value)
                            self.add_record(customer)
                        else:
                            raise ValueError(f"Invalid customer id {_customer_id} in {self._customer_file}")
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self._customer_file} is missing!') from exp
    @staticmethod
    def create_product(elements):
        """Create a Product object from a list of elements."""
        _item_id, _item_name, _item_price, _item_stock = elements
        # Format item id for search.
        _item_id = _item_id.strip()
        if not _item_price or _item_price.strip() == "":
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
                raise ValueError(f"Invalid product record {elements} in {self._product_file}")
            _list_product.append(product)
        # Create the bundle record with the list that contains the product objects.
        return Bundle(_item_id, _item_name, _list_product, _item_stock)
    def read_product(self):
        """This function will read the product file and import into the record"""
        try:
            with open(self._product_file, "r", encoding="utf-8") as f:
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
                        raise ValueError(f"Invalid product record {elements} in {self._product_file}")
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self._product_file} is missing!') from exp
    def read_order(self):
        """This function will read the order file and import it into the record"""
        try:
            with open(self._order_file, "r", encoding="utf-8") as f:
                # Create an internal tracking id for the order
                for line in f:
                    elements = self.parse_line(line)
                    # Split expected length for future change
                    _customer_id = elements[0]
                    _date = elements[-1]
                    _date = datetime.datetime.strptime(_date.strip(), "%d/%m/%Y %H:%M:%S")
                    _customer = self.find_customer(_customer_id)
                    if _customer is None:
                        raise ValueError(f"Invalid customer id {_customer_id} in {self._order_file}")
                    _items = []
                    for i in range(1, len(elements)-1, 2):
                        _item_id = elements[i]
                        _product = self.find_item(_item_id)
                        _quantity = int(elements[i+1])
                        if _product is None:
                            raise ValueError(f"Invalid product id {_item_id} in {self._order_file}")
                        _items.append((_product, _quantity))
                    order = Order(_customer, _items, _date)
                    order.update_stock_and_value(self)
                    self.add_record(order)
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self._order_file} is missing!') from exp
    def write_record_customer(self):
        """This function will write the customer record into the customer file"""
        try:
            lines = []
            for customer in self.record_customers.values():
                if customer.id.startswith("C"):
                    lines.append(f"{customer.id}, {customer.name}, 0, {customer.value}")
                elif customer.id.startswith("M"):
                    lines.append(f"{customer.id}, {customer.name}, {customer.discount_rate}, {customer.value}")
                elif customer.id.startswith("V"):
                    lines.append(f"{customer.id}, {customer.name}, {customer.discount_rate_1}, {customer.value}")
            
            with open(self._customer_file, "w", encoding="utf-8") as f:
                f.write('\n'.join(lines))
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self._customer_file} is missing!') from exp
    def write_record_product(self):
        """This function will write the product record into the product file"""
        try:
            lines = []
            for product in self.record_items.values():
                if isinstance(product, Product):
                    if product.price is None:
                        lines.append(f"{product.id}, {product.name}, , {product.stock}")
                    else:
                        lines.append(f"{product.id}, {product.name}, {product.price}, {product.stock}")
                elif isinstance(product, Bundle):
                    product_ids = [product.id for product in product.product_list]
                    product_ids_str = ','.join(product_ids)
                    lines.append(f"{product.id}, {product.name}, {product_ids_str}, {product.stock}")

            with open(self._product_file, "w", encoding="utf-8") as f:
                f.write('\n'.join(lines))
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self._product_file} is missing!') from exp
    def write_record_order(self):
        """This function will write the order record into the order file"""
        try:
            lines = []
            for _, orders in self.record_order.items():
                for order in orders:
                    lines.append(str(order))
            with open(self._order_file, "w", encoding="utf-8") as f:
                f.write('\n'.join(lines))
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self._order_file} is missing!') from exp
    def update_order_record_num(self, customer_id:str):
        """Update the number of order for a customer in order record"""
        pass
    def update_order_qty(self,quantity:int):
        """Update the quantity of the order for a customer in order record"""
    def read_record(self):
        """This function will update the record by reading the customer, product, and order file"""
        try:
            self.read_customer()
            self.read_product()
        except FileNotFoundError as _e:
            print(f"{_e}\n")
            sys.exit("Please check the file path and try again!\n")
        try:
            self.read_order()
        except FileNotFoundError as _e:
            print(f"{_e}\n")
            print("Cannot load the order file. Run as if there is no order previously\n")
    def write_record(self):
        """This function will write the record into the customer, product, and order file"""
        self.write_record_customer()
        self.write_record_product()
        self.write_record_order()
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
        for customer in self.record_customers.values():
            customer.display_info()
    def list_record_items(self):
        """This function will return the list of product or bundles in the record"""
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
            print("-"*50)
            print(f'{customer.name} orders history:\n')
            print(order)
            print("-"*50)
    def summarize_all_order(self):
        """ This function will summarize and display all rpevious order in the record"""
        # Print the header
        # print the customer name row following by the product
    def add_record(self, record):
        """
        This function will add a new record into the corresponding record dictionary.
        Base on the object type it will handle the record differently.

        Input:
        - record: record of Customer or Product or Order
        """
        if isinstance(record, Customer):
            # Add the customer record into the record_customers dictionary with customer id as the key
            self.record_customers[record.id] = record
            self.record_order[record] = []  # Initialize an empty list for this customer
        elif isinstance(record, Product) or isinstance(record, Bundle):
            # Add the product record into the record_items dictionary with product id as the key
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
        _items = []
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
            try:
                _quantity = int(input('Please enter the quantity [e.g. 1]: \n'))
                if _quantity <= 0:
                    print("Quantity must be a positive number. Please try again.\n")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid quantity.\n")
                continue
            _items.append((_item, _quantity))
            _continue = input("Do you want to add more items? [y/n]: \n")
            if _continue.lower() == "n":
                break
            elif _continue.lower() == "y":
                continue
        print()
        # If the customer does not exist, we will be creating a new customer and check if they want a membership
        if _customer is None:
            member_type = new_customer_membership_option()
            _id = self.generate_new_id(self.record_customers,member_type)
            new_customer = Customer(_id, _name)
            self.add_record(new_customer)
            return new_customer, _items, _quantity
        return _customer, _item, _quantity
    def create_order(self, customer, item, quantity):
        """
        This function will create a new order object in the record"

        Input:
        - customer: the customer object
        - order: the order object which include requirement details
        """
        # Update the item stock that contain within the orders
        _order = Order(customer, item, quantity)
        self.add_record(_order)
        _order.update_stock_and_value(self)
        _total_order_price = 0
        print()
        print("="*50)
        # Calculate the discount
        for item, quantity in order.items():
            _discount_rate, _discounted_price = item.get_discount(item.price)
            if isinstance(_order.customer, VipMember):
                _vip_fee = VipMember.price
                _total_order_price = float(_discounted_price * quantity + _vip_fee)
            print(f'{_order.customer.name} purchases {quantity} x {item.name}')
            print(f'Unit price: {item.price:.2f} (AUD)')
        if isinstance(_order.customer, VipMember):
            print(f'Membership price: {_vip_fee:.2f} (AUD) not discounted')
        print(f'{_order.customer.name} gets a discount of {_discount_rate*100:.0f}%.')
        print(f'Price to pay: {_total_order_price:.2f} (AUD)')
        print("="*50)
    @staticmethod
    def generate_new_id(record, prefix:str):
        """
        This function will generate a new unique id based on exiting record and the id prefix.
            
        Input:
        - type: the type of the record. Can be either ["C","V","M"] for customer, 
        "P" for product, or "B" for bundle.
        """
        # Initialise the id number
        i = 1
        # Create a list of numeric part of the record with the same type.
        existing_ids = [int(item.id.replace(prefix, '')) for item in record.values()]
        if existing_ids != []:
            # If the list is not empty, find the max value and add 1 to it.
            i = max(existing_ids) + 1
        new_id = prefix + str(i)
        return new_id
    def most_valuable_customer(self):
        """
        Finds and returns the most valuable customer based on their total purchases.

        Returns:
            str: The name of the most valuable customer.
        """
        max_value = 0
        max_order_value = 0
        mv_customer = None
        for customer, history in self.record_order.items():
            if customer.value > max_value:
                max_value = customer.value
                mv_customer = customer
                for order,_,_ in history:
                    if order.value > max_order_value:
                        max_order_value = order.value
        return mv_customer, max_order_value, max_value
    def most_popular_product(self):
        """
        Returns the most popular product in the retail management system.

        This method analyzes the sales data and determines the product that has been sold the most.
        It returns the name or ID of the most popular product.

        Returns:
            str: The name or ID of the most popular product.
        """
        product_orders = {}
        for orders in self.record_order.items():
            for order in orders["Order"]:
                if order.product not in product_orders:
                    product_orders[order.product] = 1
                else:
                    product_orders[order.product] += 1
        return max(product_orders, key=product_orders.get)
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
                order = Order(customer, product, quantity)
                order.place_order()
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
                while True:
                    try:
                        new_threshold = float(input("Please enter the new threshold: "))
                        if new_threshold <= 0:
                            print("Threshold must be a positive integer. Please try again.\n")
                            continue
                        VipMember.set_threshold(new_threshold)
                        break
                    except ValueError:
                        print('Invalid input. Threshold must be a positive integer.\n')
                        continue
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
                break
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

def command_line_read():
    """This is function is use to read the command line when first start the program"""
   
    if len(sys.argv) == 4:
        # If the command line have three arguments, take the file path from the command line
        customer_file = sys.argv[1]
        product_file = sys.argv[2]
        order_file = sys.argv[3]
    elif len(sys.argv) == 3:
        # If the command line only have two arguments, assume there is no order file
        customer_file = sys.argv[1]
        product_file = sys.argv[2]
        order_file = None
    elif len(sys.argv) == 1:
        # If the command line is empty, use the default file path
        customer_file = os.path.join(os.path.dirname(__file__),r"customers.txt")
        product_file = os.path.join(os.path.dirname(__file__),r"products.txt")
        order_file = os.path.join(os.path.dirname(__file__),r"orders.txt")
    else:
        print("Command line will only accept three arguments (customer file, product file, and order file)\n \
            with two (customer file, and product file) as minimum\n")
        print('Acceptable format: \n\
              py ProFunA2_s3676330.py "customers.txt" "products.txt" "orders.txt"\n\
              py ProFunA2_s3676330.py "customers.txt" "products.txt"\n\
              py ProFunA2_s3676330.py\n')
        sys.exit("Please try again")
    return customer_file, product_file, order_file
    

def main():
    """This will be the main function of the program"""
    customer_file, product_file, order_file = command_line_read()
    data = Record(customer_file, product_file, order_file)
    data.read_record()
    # Use the menu function to interact with the user
    data.menu_loop()
    # Write the record into the file prior to exit the program
    data.write_record()
    sys.exit("Thank you for using the program!")

if __name__ == "__main__":
    try:
        main()
    # Exit the program gracefully when sys.exit() is called
    # This is to ensure consistent behaviour across IDE or terminal
    except SystemExit as e:
        print(f"{e}")
        