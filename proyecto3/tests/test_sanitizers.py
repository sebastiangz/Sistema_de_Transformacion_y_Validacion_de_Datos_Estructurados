from src.sanitizers import normalize_email

def test_normalize_email():
    assert normalize_email("  USUARIO@GMAIL.COM  ") == "usuario@gmail.com"
