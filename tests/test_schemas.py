"""
Tests para los validadores definidos en schemas.py:
- PositiveFloat: valida floats positivos
- DateValidator: valida formatos de fecha
- CountryWhitelist: valida países permitidos
"""

from returns.result import Success, Failure  # third-party

from src.schemas import PositiveFloat, DateValidator, CountryWhitelist  # first-party

def test_positive_float_accepts_valid_positive_number():
    """Acepta floats positivos válidos."""
    validator = PositiveFloat()
    result = validator(12.5)
    assert isinstance(result, Success)
    assert result.unwrap() == 12.5

def test_positive_float_rejects_zero_and_negative():
    """Rechaza cero y números negativos."""
    validator = PositiveFloat()
    assert isinstance(validator(0), Failure)
    assert isinstance(validator(-3.2), Failure)

def test_positive_float_rejects_non_numeric():
    """Rechaza valores no numéricos."""
    validator = PositiveFloat()
    result = validator("abc")
    assert isinstance(result, Failure)
    assert result.failure() == "Invalid float"

def test_date_validator_accepts_valid_formats():
    """Acepta fechas en formatos válidos."""
    validator = DateValidator()
    valid_dates = [
        "11/20/2025 21:47",
        "20/11/2025 21:47",
        "11/20/2025 21:47:00",
        "20/11/2025 21:47:00"
    ]
    for date in valid_dates:
        result = validator(date)
        assert isinstance(result, Success)
        assert result.unwrap() == date

def test_date_validator_rejects_invalid_format():
    """Rechaza fechas con formato incorrecto."""
    validator = DateValidator()
    result = validator("2025-11-20T21:47")
    assert isinstance(result, Failure)
    assert "Date must match one of" in result.failure()

def test_country_whitelist_accepts_allowed_country():
    """Acepta países permitidos."""
    validator = CountryWhitelist(['MX', 'US', 'IN'])
    result = validator('MX')
    assert isinstance(result, Success)
    assert result.unwrap() == 'MX'

def test_country_whitelist_rejects_disallowed_country():
    """Rechaza países no permitidos."""
    validator = CountryWhitelist(['MX', 'US', 'IN'])
    result = validator('FR')
    assert isinstance(result, Failure)
    assert result.failure() == "Country FR not allowed"
