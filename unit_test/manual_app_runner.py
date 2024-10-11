AVG_FPS = 60
def to_frames(seconds):
    return seconds * AVG_FPS

def run_ursina_for(app,seconds):
    for i in range(0,to_frames(seconds)):
        app.step()

def assert_true():
    assert True

def assert_false():
    assert False