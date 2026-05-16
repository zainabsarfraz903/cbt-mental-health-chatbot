from .emotion_detector import detect_emotion

def respond(user_text: str) -> str:
    """Placeholder chatbot response pipeline."""
    emo = detect_emotion(user_text)
    return f"(emotion={emo}) Thanks for sharing."
