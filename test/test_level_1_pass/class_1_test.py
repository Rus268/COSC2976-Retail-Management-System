'''
This function test all of the basic requirement for the class of the project
'''

from ProFunA2_s3676330 import Customer, Member, VipMember, Product, Order, Record

def main():
    mock_customer = Customer("John", "Smith", "1234567890")
    mock_vip_member = VipMember("Loky", "Smith", "1234567890")
    test_customer_class()
    test_member_class()
    test_vip_member_class()
    test_product_class()
    test_order_class()
    test_record_class()

def test_customer_class():
    """Test the Customer class and it function"""
    _mock_customer = mock_customer
    assert _mock_customer.name == "John"
    assert _mock_customer.id == '1234567890'
    assert _mock_customer.value == 0
    assert _mock_customer.display_info() == 


if __name__ == "__main__":
    main()