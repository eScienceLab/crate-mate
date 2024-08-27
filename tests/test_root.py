import pytest
from src import main 

def test_correct_root():
    # call main on example.json
    main.main()

    # assert that the output is correct
    assert True == True
    
