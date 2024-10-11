import pytest
from ursina import *
from .scene_creation import run_generic_test_scene

@pytest.fixture
def start_ursina(): 
    app = Ursina()
    yield app
    app.shutdown()

@pytest.fixture
def run_test_scene():
    app = run_generic_test_scene()
    yield app
    app.shutdown()