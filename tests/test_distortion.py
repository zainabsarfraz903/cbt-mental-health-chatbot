from src.distortion_classifier import classify_distortion

def test_distortion():
    assert isinstance(classify_distortion("I always fail"), list)
