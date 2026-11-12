"""Parsers funcionales, con combinadores simples y lectura JSON/CSV/XML."""
import csv
import io
import json
import xml.etree.ElementTree as ET
from .types import Success, Failure

def parser(fn):
    def parse(text):
        try:
            return Success(fn(text))
        except (ValueError, TypeError, ET.ParseError, csv.Error) as exc:
            return Failure((f'Error de formato: {exc}',))
    return parse

@parser
def parse_json(text):
    return json.loads(text)

@parser
def parse_csv(text):
    return list(csv.DictReader(io.StringIO(text)))

@parser
def parse_xml(text):
    root = ET.fromstring(text)
    return [{child.tag: child.text or '' for child in element} for element in root] if len(root) and all(len(element) > 0 for element in root) else {child.tag: child.text or '' for child in root}

def map_parser(base_parser, fn):
    return lambda text: base_parser(text).map(fn)

def then(first, second):
    return lambda text: first(text).bind(second)

def parse_by_extension(text, extension):
    parsers = {'.json': parse_json, '.csv': parse_csv, '.xml': parse_xml}
    selected = parsers.get(extension.lower())
    return selected(text) if selected else Failure((f'Formato no soportado: {extension}',))
