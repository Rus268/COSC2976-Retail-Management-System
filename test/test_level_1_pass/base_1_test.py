'''
This code test for the exiting of required class, attributues and methods

'''
import os
import pytest

from ProFunA2_s3676330 import Customer, Member, VipMember, Product, Order, Record

def main():
    test_filename_format()
    test_classes_exist()    

def test_filename_format():
    """check for the requirement file name"""
    filename = 'ProFunA2_s3676330.py'
    assert os.path.exists(filename), "File name is not correct, please check the file name"
    assert os.path.startswith('ProFunA2_'), "File name is not correct, please check the file name"
    assert os.path.endswith('.py'), "File name type is not correct, please check the file name"
    assert 's3676330' in filename, "File name is missing student number. Please check the file name"

def test_classes_exist():
    """check for the requirement classes"""
    assert 'Customer' in globals(), "Customer class does not exist"
    assert 'Member' in globals(), "Member class does not exist"
    assert 'VipMember' in globals(), "VipMember class does not exist"
    assert 'Product' in globals(), "Product class does not exist"
    assert 'Order' in globals(), "Order class does not exist"
    assert 'Record' in globals(), "Record class does not exist"

if __name__ == '__main__':
    main()