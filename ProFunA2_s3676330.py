"""
 This program is a retail management system that allows cashier to place an order for a customer, add/update products and prices, and display existing customers and products, etc.
"""
import sys
import os

# Define class for the program
# CUSTOMER:
class Customer:
    # Initialise the customer object with given ID, name, and value. If value not provided, default to 0.00
    def __init__(self, id, name:str, value:float = 0.00):
        self.id = id
        self.name = name
        self.value = value

    # Calculate the discount which return (0,price) - where the first value is discount rate and second is input price.
    # This will be the super method and will have more subclass implement
    def get_discount(self,price):
        return (0,price)
    
    def get_id(self): # Method to get the customer ID
        return self.id
    
    def get_name(self): # Method to get the customer name
        return self.name
    
    def get_value(self): # method to get the customer total money spend to date
        return self.value
    
    # Print the class Customer attributes and the discount rate associated:
    def display_info(self):
        return print(f"ID: {self.id}\nName: {self.name}\nValue: {self.value}\nDiscount Rate: 0")

# Create a new member class that inherited it attributes from customer
class Member(customer):
    discount_rate = 0.05 # initialise a class inherited variable

    # Initialise the class member and inherited the attributes from customer class.
    def __init__(self,id, name:str, value:float = 0.00):
        super().__init__(id,name,value)

    def get_discount(self, price:float): # Update the get_discount method with new calculation
        new_price = price * (1 - self.discount_rate)
        return (self.discount_rate, new_price)
    
    def display_info(self): # Update new information in the display_infor class
        print(f"ID: {self.id}\nName: {self.name}\nValue: {self.value}\nDiscount Rate: {self.discount_rate}")
    
    @classmethod
    def set_rate(member_cls, new_rate: float): # Create a new class method to update the flat discount rate
        member_cls.discount_rate = new_rate

class VipMember(customer):

    # Initialise the two discount rate and threshold for the class
    discount_rate_1 = 0.10
    discount_rate_2 = 0.15
    threshold = 1000.00
    # Initialise the class throught initialising the parent class
    def __init__ (self,id, name:str, value:float = 0.00):
        super().__init__(id,name,value)
    
    def get_discount(self, price):
        if price <= self.threshold:
            return (self.discount_rate_1, price * (1- self.discount_rate_1))
        else:
            return (self.discount_rate_2, price * (1- self.discount_rate_2))
    
    def display_info(self): # Print the information of the vip member
        print(f"ID: {self.id}\nName: {self.id}\nValue: {self.value}\nDiscount Rate 1: {self.discount_rate_1}\nDiscount Rate 2: {self.discount_rate_2}")
    
    @classmethod
    def set_rate(vip_cls, rate_type: str = "rate_1",new_rate:float):
        if rate_type == "rate_1":
            vip_cls.discount_rate_1 = new_rate
        elif rate_type == "rate_2":
            vip_cls.discount_rate_2 = new_rate
        else:
            raise ValueError("Invalid rate type")
        
    def set_threhold(vip_cls, new_threshold:float):
        vip_cls.threshold = new_threshold

# Product class
class Product:

    def __init__(self, id, name:str, price:float, stock:int):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
    
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_price(self):
        return self.price
    def get_stock(self):
        return self.stock
    
    def set_price(self, new_price:int): # Update the price of the product
        self.price = new_price

    def set_stock(self, new_stock:int): # Update the stock of the product
        self.stock = new_stock
    
    def display_info(self):
        print(f"ID: {self.id}\nName: {self.name}\nPrice: {self.price}\nStock: {self.stock}")


# Order Class
class Order:
    """This class is to manage the order of the customer"""
    def __init__(self, order_id,customer_id, product_id, quantity:int):
        self.order_id = order_id # Initialise a order_id in order to keep track of the order
        self.customer_id = customer_id # We will be using customer id as it ensure we are reference to the correct customer everytime
        self.product_id = product_id # We will be using product id to ensure we are reference to to the correct product everytime
        self.quantity = quantity

    def get_id(self):
        return self.order_id
    
    def get_customer(self):
        return self.customer
    
    def get_product(self):
        return self.product
    
    def get_quantity(self):
        return self.quantity
    
    def update_product_stock(self):
        

# Record
class Record:
    """This class is the central data repository of the program"""
    # Specify the relative path to relevant file for the program to run correctly
    # Since the record will only be create once at the start we will be using class variable instead of instance variable.
    # This is to avoid manually managing the file path across multiple record.
    customer_file = "COSC2976_Assignment2\\files_PASSlevel\customers.txt"
    product_file = "COSC2976_Assignment2\\files_PASSlevel\products.txt"

    def __init__(self):
        """The class will create new instance of customer list and product list"""
        self.customer_list = [] # In this list we will be storing a list of customer id in order to ensure uniqueness
        self.product_list = [] # In this list we will be storeing a list of product id in order to ensure uniqueness

    def read_customer(self):
        """This function will look for the  """
        try:
            with open(customer_file,"r") as f:
                line = f.readline()
                while line:
                    id, name, discount_rate, value = line.strip().split(',')
                    customer_id = customer (id, name, discount_rate, value)
                    customer_list.append(customer_id)
        except FileNotFoundError
    
    def read_product(self):
        """This function will read the specify file that was  """
        with open(product_file,"r") as f:
            line = f.readline()
            while line:
                item_id, name, price, stock = line.strip().split(',')
                product_id = product(item_id, name, price, stock)
                self.product_list.append(product_id) # Add the new product into the product id
    
    def find_customer(key:str = "id", value):
        """ 
        Take a search key and find the customer detail from the customer list
        
        Input:
        - key : can either be "id" or "name"
        - value: the search value

        Output:
        - return customer detail if customer exit else print customer does not exit

        """
        for item in self.customer_list:
            if getattr(item,key) == value:
                return item
            else:
                raise ValueError (f'{key}: {value} does not exit in customer list')

    def find_product(key:str, value:str):
        """ 
        Take a search key and fine the product teails from the product list
        
        Input:
        - key: can either be product id or name

        Output:
        - return product detail is product exit else print product does not exit
        """
        pass


def main():
    # Initalise main system record.
    SysRecord = Record()
    try:
        SysRecord.read_customer()
        SysRecord.read_product()
    except FileNotFoundError as e:
        # Exit the program if the require file is missing and notify the user of the missing file.
        sys.exit(str(e)) 



if __name__ == "__main__":
    main()
