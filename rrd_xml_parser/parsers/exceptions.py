# coding: utf-8
"""Модуль содержит исключения возникающие в работе парсера"""


class NotImplementedTypeError(Exception):
    """Исключение возникающее при неподдреживаемых типах документов"""
    pass


class NotImplementedValueError(Exception):
    """Исключение возникающее при неподдреживаемых версиях документов"""
    pass
