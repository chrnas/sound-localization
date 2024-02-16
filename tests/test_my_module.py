import pytest
from my_module import add_numbers

def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(0, 0) == 0
    assert add_numbers(-1, 1) == 0
    assert add_numbers(-1, -1) == -2

if __name__ == "__main__":
    pytest.main()
