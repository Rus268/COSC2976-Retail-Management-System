"""
 This program is a retail management system that allows cashier to place an order for a customer, add/update products and prices, and display existing customers and products, etc.
"""

# Define class for the program

# CUSTOMER:
class customer:
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

class member(customer): # inherited the attributes from customer class

    def __init__(self,id, name:str, value:float = 0.00, discount_rate = 0.05):
        super().__init__(id,name,value)
        self.discount_rate = discount_rate

    def get_discount(self, price:float): # Update the get_discount method with new calculation
        new_price = price * (1 - self.discount_rate)
        return (self.discount_rate, new_price)
    
    def display_info(self): # Update new information in the display_infor class
        print(f"ID: {self.id}\nName: {self.id}\nValue: {self.value}\nDiscount Rate: {self.discount_rate}")
    
    def set_rate(self, new_rate: float): # Create a new method to update the discount rate for all class.
        self.discount_rate = new_rate

class vip_member(customer):
    pass


# Product class
class product:

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
class order:
    def __init__(self) ->:
        pass

# Record
class record:
    def __init__(self) -> None:
        pass

def main()


if __name__ == "__main__":
    main()
