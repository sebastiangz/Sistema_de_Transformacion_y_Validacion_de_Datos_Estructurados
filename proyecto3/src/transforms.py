"""Transformadores puros y composición de funciones."""
from functools import reduce

def compose(*functions):
    return lambda value: reduce(lambda acc, fn: fn(acc), reversed(functions), value)

def pipe(value, *functions):
    return reduce(lambda acc, fn: fn(acc), functions, value)

def uppercase_name(data):
    return {**data, 'name': data['name'].upper()} if 'name' in data else dict(data)

def normalize_email(data):
    return {**data, 'email': data['email'].lower()} if 'email' in data and isinstance(data['email'], str) else dict(data)

def normalize_tags(data):
    return {**data, 'tags': [tag.lower() for tag in data['tags']]} if isinstance(data.get('tags'), list) else dict(data)

transform_user = compose(normalize_tags, normalize_email, uppercase_name)
