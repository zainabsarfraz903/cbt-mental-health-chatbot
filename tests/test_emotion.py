from src.emotion_detector import detect_emotion

def test_detect_emotion():
    assert detect_emotion("hello") in ("neutral", "happy", "sad")
