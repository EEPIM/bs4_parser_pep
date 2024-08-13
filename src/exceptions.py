"""Исключения."""


class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class DoesNotFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
