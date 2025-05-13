import pytest
import csv
from extract_1 import list_nicely

def test_list_nicely():
    with open('data/test_data.csv', 'r') as file:
        reader = csv.reader(file)
        test_orders = list(reader)
        assert list_nicely(test_orders) == None