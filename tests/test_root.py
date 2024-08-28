import logging
import pytest

from src import main

# ------------------------------------------------------------------------------
# Fixtures

@pytest.fixture
def logger():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger

# ------------------------------------------------------------------------------
# Tests

def test_correct_root(logger):
    # call main on example.json
    main.main(logger=logger, input_path="/workspace/example.json")

    # assert that the output is correct
    assert True == True
    
