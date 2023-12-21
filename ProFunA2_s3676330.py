"""
 This program is a retail management system that allows cashier to place an order for a customer, 
 add/update products and prices, and display existing customers and products, etc.

 - 14/12/2023: Create program acording to the requirement for PASS level in week 7.
 
 """
import sys
import os

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
        self.c_id = c_id
        self.c_name = c_name
        self.c_value = c_value

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
    def __str__(self) -> str:
        return f"ID: {self.c_id}\n \
                Name: {self.c_name}\n \
                Value: {self.c_value}\n \
                Discount Rate: 0"
# Create a new member class that inherited it attributes from customer
class Member(Customer):
    """
    This class will store the member information. 
    It will inherited the attributes from customer class

    Input:
    - m_id: the member id
    - m_name: the member name
    - m_value: the member value
    """
    discount_rate = 0.05 # Initialise a class inherited variable
    # Initialise the class member and inherited the attributes from customer class.
    def __init__(self, m_id, m_name:str, m_value:float = 0.00) -> None:
        # Initialise the class throught initialising the parent class variable.
        super().__init__(m_id,m_name,m_value)
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
     # Update new information in the display_infor class
    def __str__(self) -> str:
        """This function will print the information of the member"""
        return f"ID: {self.c_id}\n \
                Name: {self.c_name}\n \
                Value: {self.c_value}\n \
                Discount Rate: {self.discount_rate}"
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
    def __init__ (self, v_id, v_name:str, v_value:float = 0.00) -> None:
        super().__init__(v_id, v_name, v_value)
        self.discount_rate_1 = 0.10 # The default first discount rate is alway 10%
        self.discount_rate_2 = 0.15 # The default second discount rate is alway 5% higher than the first discount rate
    
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
    
    def __str__(self) -> str:
        """
        This function will return the string representation of the vip member
        """
        return f"ID: {self.c_id}\n" \
               f"Name: {self.c_name}\n" \
               f"Value: {self.c_value}\n" \
               f"Discount Rate 1: {float(self.discount_rate_1)}\n" \
               f"Discount Rate 2: {float(self.discount_rate_2)}"
    
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

class Product:
    """
    This class will store the product information

    Input:
    - id: the product id
    - name: the product name
    - price: the product price
    - stock: the product stock
    """
    def __init__(self, p_id, p_name:str, price:float, stock:int):
        self.p_id = p_id
        self.p_name = p_name
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
    def __str__(self):
        """This function will return the string representation of the product"""
        return f"ID: {self.p_id}\n \
                Name: {self.p_name}\n \
                Price: {self.price}\n \
                Stock: {self.stock}"

# Create a new bundle class that contain a list of product.
# I will be using composition to ensure the bundle is a list of product.
class Bundle:
    """
    This class will store the bundle information

    Input:
    - id: the bundle id
    - name: the bundle name
    - product_list: the list of product in the bundle
    """
    def __init__(self, b_id, b_name:str, product_list:list, stock:int):
        self.b_id = b_id
        self.b_name = b_name
        self.product_list = product_list
        # Initialise the price of the bundle
        self.price = 0
        # Calculate the price of the bundle and set it as the price of the bundle
        for product in self.product_list:
            self.price += product.price
        self.price *= 0.8
        self.stock = stock

    def add_product(self, product:Product):
        """This function will add a product into the bundle and also update the bundle price"""
        # Check to see if the product already exit in the bundle
        if product in self.product_list:
            raise ValueError("Product already in the bundle")
        self.product_list.append(product)
        # Update the price of the bundle after add new product.
        self.update_price()
    
    def update_price(self):
        """This function will update the price of the bundle"""
        # Set the price of the bundle to 0 to recalculate the price
        self.price = 0
        # Calculate the new price of the bundle
        for product in self.product_list:
            self.price += product.price
        # Applied a 20% discount of the bundle
        self.price = self.price * 0.8

    def set_stock(self, new_stock:int):
        """This function will update the stock of the bundle"""
        self.stock = int(new_stock)
    
    def display_info(self):
        """This function will print the information of the bundle"""
        print(f"ID: {self.b_id}\nName: {self.b_name}\nStock: {self.stock}")
        for product in self.product_list:
            print(product)

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
        self.customer.value = self.customer.value + (self.product.price * self.quantity)
    def list_order(self):
        """This function will list the order"""
        return f"Customer ID: {self.customer}\nProduct ID: {self.product}\nQuantity: {self.quantity}"

# Create a new record class to store the customer and product list
class Record:
    """
    This class will be the main record for the program. It will load the customer and product file into the record.
    All main function will be run through this class.
    """
    # I will be using os.path.join to ensure the file path to ensure the file path is correct regardless of operating system used.
    customer_file = os.path.join(os.path.dirname(__file__),r"COSC2976_assignment2\\files_CREDITlevel\\customers.txt")
    product_file = os.path.join(os.path.dirname(__file__),r"COSC2976_assignment2\\files_CREDITlevel\\products.txt")

    def __init__(self):
        """The class will create new instance of customer list and product list"""
        self.customer_list = [] # In this list we will be storing a list of customer id in order to ensure uniqueness
        self.item_list = [] # In this list we will be storeing a list of product id and bundle in order to ensure uniqueness

    def read_customer(self):
        """This function will look for the customer file and import it into the record"""
        try:
            with open(self.customer_file, "r", encoding = "utf-8") as f:
                line = f.readline()
                while line:
                    elements = line.strip().split(',')
                    # Validate the customer record
                    if len(elements) == 4:
                        r_id, r_name, discount_rate, value = elements
                    else:
                        raise ValueError(f"Invalid customer record {elements} in {self.customer_file}")
                    # Validate the customer id and create the customer object
                    if r_id.startswith("C"):
                        customer_id = Customer (r_id, r_name, value)
                        self.customer_list.append(customer_id)
                        line = f.readline()
                    elif r_id.startswith("M"):
                        customer_id = Member (r_id, r_name, value)
                        self.customer_list.append(customer_id)
                        line = f.readline()
                    elif r_id.startswith("V"):
                        customer_id = VipMember (r_id, r_name, value)
                        customer_id.set_rate("rate_1",discount_rate)
                        self.customer_list.append(customer_id)
                        line = f.readline()
                    else:
                        raise ValueError(f"Invalid customer id {id} in {self.customer_file}")
                    # Validate that the customer id is unique
                    if r_id in [customer.c_id for customer in self.customer_list]:
                        raise ValueError(f"Duplicate customer id {id} in {self.customer_file}")
                    if value in [customer.value for customer in self.customer_list < 0]:
                        raise ValueError(f"Invalid customer value {value} in {self.customer_file}")
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self.customer_file} is missing!') from exp
    
    def read_product(self):
        """This function will read the product file and import into the record """
        try:
            with open(self.product_file,"r", encoding = "utf-8") as f:
                line = f.readline()
                while line:
                    elements = line.strip().split(',')
                    # check the product record type
                    if elements[0].startswith("P") and len(elements) == 4:
                        # If line have a standard product record structure
                        item_id, name, price, stock = elements
                        # Validate the product id and create the product object
                        if not item_id.startswith("P"):
                            raise ValueError(f"Invalid product id {item_id} in {self.product_file}")
                        if not item_id.startswith('B'):
                            raise ValueError(f"Invalid product id {item_id} in {self.product_file}")
                        if price < 0:
                            raise ValueError(f"Invalid product price {price}in {self.product_file}")
                        if stock < 0:
                            raise ValueError(f"Invalid product stock {stock}")
                        product_id = Product(item_id, name, price, stock)
                        self.item_list.append(product_id)
                    elif elements[0].startswith("B") and len(elements) > 4:
                        # If line have a bundle product record structure
                        item_id = elements[0]
                        name = elements[1]
                        stock = elements[-1]
                        list_product = []
                        for i in elements[2:-1]:
                            # add the product into the list
                            if not i.startswith("P"):
                                # Check if the product id is valid
                                raise ValueError(f"Invalid product id {i} in {self.product_file}")
                            _product = elements[i]
                            list_product.append(_product)
                        if stock < 0:
                            raise ValueError(f"Invalid bundle stock {stock}")
                        bundle_id = Bundle(item_id, name, list_product, stock)
                        self.item_list.append(bundle_id)
                    else:
                        raise ValueError(f"Invalid product record {elements} in {self.product_file}")     
                    # Add the new product into the product id
                    # Check if the product id is unique
                    if id in [product.get_id for product in self.item_list]:
                        raise ValueError(f"Duplicate product id {id}")
                    line = f.readline() # Read the next line
        except FileNotFoundError as exp:
            raise FileNotFoundError(f'File {self.product_file} is missing!') from exp

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
        for item in self.item_list:
            if getattr(item,key).strip().lower() == search.strip().lower():
                return item # Return the product if it exit
        return None # If the product does not exit return None
    
    def list_customer(self):
        """This function will return the list of customer in the record"""
        for customer in self.customer_list:
            customer.display_info()

    def list_product(self):
        """This function will return the list of product in the record"""
        for product in self.item_list:
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
            self.item_list.append(product)
        else:    
            raise TypeError("product must be a Product or Bundle object")
    
def menu(data:Record):
    """
    This function will display the menu and run the selected function based on the user input.
    """
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
            customer, product, quantity = get_info(data)
            place_order(customer, product, quantity)
        elif user_input == "2":
            # Display the customer list
            data.list_customer()
        elif user_input == "3":
            # Display the product list
            data.list_product()
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
        n_id = generate_new_customer_id(member_type, data)
        new_customer = Customer(n_id, name)
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

def generate_new_customer_id(r_type:str, data:Record):
    """
    This function will generate a new unique customer id for the new customer
    
    Input:
    - type: the type of customer
    - data: the record object that contain the customer list
    """
    i = 1
    new_id = r_type + str(len(data.customer_list) + i)
    while new_id in [customer.get_id for customer in data.customer_list]:
        i += 1
        new_id = r_type + str(len(data.customer_list) + i) 
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
