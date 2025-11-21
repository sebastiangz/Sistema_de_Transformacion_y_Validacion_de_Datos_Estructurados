"""
Tests para las funciones de sanitización definidas en sanitizers.py:
- Limpieza de texto, escape HTML, conversión numérica y booleana, normalización de país.
"""

from src.sanitizers import (
    sanitize_text_fields,
    escape_html,
    convert_numeric_fields,
    convert_booleans,
    normalize_country,
    sanitize_input
)

def test_sanitize_text_fields_removes_whitespace_and_newlines():
    """Elimina espacios y saltos de línea en campos de texto."""
    d = {'name': '  Juan\n', 'note': 'Hola\r\nMundo  '}
    result = sanitize_text_fields(d)
    assert result['name'] == 'Juan'
    assert result['note'] == 'Hola Mundo'

def test_escape_html_replaces_special_characters():
    """Escapa caracteres HTML peligrosos."""
    d = {'comment': '<script>alert("x")</script>'}
    result = escape_html(d)
    assert result['comment'] == '&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;'

def test_convert_numeric_fields_parses_valid_numbers():
    """Convierte strings numéricos en floats."""
    d = {'amount': '123.45', 'count': '10', 'text': 'abc'}
    result = convert_numeric_fields(d)
    assert result['amount'] == 123.45
    assert result['count'] == 10.0
    assert result['text'] == 'abc'

def test_convert_numeric_fields_ignores_invalid_numbers():
    """Ignora strings que no son números válidos."""
    d = {'value': '12.3.4', 'other': 'abc'}
    result = convert_numeric_fields(d)
    assert result['value'] == '12.3.4'
    assert result['other'] == 'abc'

def test_convert_booleans_recognizes_true_values():
    """Convierte strings verdaderos en True."""
    d = {'a': 'true', 'b': 'YES', 'c': '1'}
    result = convert_booleans(d)
    assert result['a'] is True
    assert result['b'] is True
    assert result['c'] is True

def test_convert_booleans_recognizes_false_values():
    """Convierte strings falsos en False."""
    d = {'x': 'false', 'y': 'No', 'z': '0'}
    result = convert_booleans(d)
    assert result['x'] is False
    assert result['y'] is False
    assert result['z'] is False

def test_convert_booleans_ignores_non_boolean_strings():
    """No convierte strings que no son booleanos conocidos."""
    d = {'flag': 'maybe'}
    result = convert_booleans(d)
    assert result['flag'] == 'maybe'

def test_normalize_country_maps_known_names():
    """Normaliza nombres conocidos de países a sus códigos."""
    d = {'Merchant_Country': 'México'}
    result = normalize_country(d)
    assert result['Merchant_Country'] == 'MX'

def test_normalize_country_preserves_unknown_names():
    """Preserva nombres de países no reconocidos."""
    d = {'Merchant_Country': 'Atlantis'}
    result = normalize_country(d)
    assert result['Merchant_Country'] == 'Atlantis'

def test_sanitize_input_applies_all_sanitizers():
    """Aplica todos los sanitizadores en orden funcional."""
    d = {
        'Merchant_Country': 'United States',
        'note': '  <b>Oferta</b>\n',
        'amount': '99.99',
        'confirmed': 'yes'
    }
    result = sanitize_input(d)
    assert result['Merchant_Country'] == 'US'
    assert result['note'] == '&lt;b&gt;Oferta&lt;/b&gt;'
    assert result['amount'] == 99.99
    assert result['confirmed'] is True
