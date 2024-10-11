# import pytest
# from ursina import Ursina
# from util import run_generic_scene

# AVG_FPS = 60

# def to_frames(seconds):
#     return seconds * AVG_FPS

# def run_ursina_for(app,seconds):
#     for i in range(0,to_frames(seconds)):
#         app.step()

# @pytest.fixture
# def start_ursina():
#     app = Ursina()
#     yield app
#     app.shutdown()

# @pytest.fixture
# def run_test_scene():
#     app = run_generic_scene()
#     yield app
#     app.shutdown()
