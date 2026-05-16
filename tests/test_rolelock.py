from src.role_lock import enforce_role

def test_rolelock():
    assert enforce_role("test") == "test"
