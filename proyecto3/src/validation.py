"""Validación composable de esquemas y reglas de negocio."""
import re
from .types import Success, Failure
from .schemas import USER_SCHEMA

EMAIL_PATTERN = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')

def validate_schema(data, schema=USER_SCHEMA):
    if not isinstance(data, dict):
        return Failure(('El registro debe ser un objeto/diccionario',))
    errors = []
    for name, rule in schema.items():
        if name not in data or data[name] is None:
            if rule.required:
                errors.append(f'Falta el campo obligatorio: {name}')
            continue
        value = data[name]
        if type(value) is not rule.kind:
            errors.append(f'{name}: se esperaba {rule.kind.__name__}')
            continue
        if rule.minimum is not None and value < rule.minimum:
            errors.append(f'{name}: mínimo {rule.minimum}')
        if rule.maximum is not None and value > rule.maximum:
            errors.append(f'{name}: máximo {rule.maximum}')
        if rule.email and not EMAIL_PATTERN.fullmatch(value):
            errors.append(f'{name}: correo electrónico inválido')
        if name == 'tags' and not all(isinstance(tag, str) for tag in value):
            errors.append('tags: todos los elementos deben ser texto')
    return Failure(tuple(errors)) if errors else Success(data)

def validate_user(data):
    return validate_schema(data)
