"""Tipos de resultados funcionales sin excepciones en el flujo normal."""
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class Success:
    value: Any
    def bind(self, fn: Callable):
        try:
            return fn(self.value)
        except Exception as exc:
            return Failure((str(exc),))
    def map(self, fn: Callable):
        return self.bind(lambda value: Success(fn(value)))
    def match(self, success: Callable, failure: Callable):
        return success(self.value)
    def value_or(self, default):
        return self.value

@dataclass(frozen=True)
class Failure:
    errors: tuple[str, ...]
    def bind(self, fn: Callable):
        return self
    def map(self, fn: Callable):
        return self
    def match(self, success: Callable, failure: Callable):
        return failure(self.errors)
    def value_or(self, default):
        return default

@dataclass(frozen=True)
class Some:
    value: Any
    def map(self, fn):
        return Some(fn(self.value))

@dataclass(frozen=True)
class Nothing:
    def map(self, fn):
        return self
