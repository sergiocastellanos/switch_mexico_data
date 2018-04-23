import os
from context import src


script_path = os.path.dirname(__file__)
parent_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(parent_path, 'data/clean/loads')
output_path  = os.path.join(parent_path, 'data/clean/switch_outputs')

def test_check_folders():
    assert os.path.exists(os.path.join(parent_path, 'data'))
    assert os.path.exists(os.path.join(parent_path, 'data/clean'))

def test_load_zones():
    assert (2 + 2) == 4

