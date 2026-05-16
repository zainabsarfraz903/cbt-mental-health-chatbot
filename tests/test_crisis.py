from src.crisis_detector import check_crisis

def test_crisis():
    assert isinstance(check_crisis("I want to die"), tuple)
