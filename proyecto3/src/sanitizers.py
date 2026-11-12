"""Limpieza sin modificar los objetos de entrada."""

def sanitize_text(value):
    return ' '.join(value.strip().split()) if isinstance(value, str) else value

def sanitize_input(data):
    if isinstance(data, dict):
        return {key: sanitize_input(value) for key, value in data.items()}
    if isinstance(data, list):
        return [sanitize_input(value) for value in data]
    return sanitize_text(data)
