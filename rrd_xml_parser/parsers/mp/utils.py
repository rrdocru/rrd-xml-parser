# coding: utf-8
"""Модуль специально для парсинга межевого плана т.к. он ещё не переработан"""
from logging import getLogger

from rrd_xml_parser.parsers.utils import nodes2str
from rrd_xml_parser.models import Address


logger = getLogger(__name__)


def nodes2address(elements, xpaths, namespaces=None):
    """
    Функция преобразования xml-элемента с описанием адреса в модель адреса

    :param list[_Element] elements: список xml-элементов с адресом (по умолчанию всегда должен быть один)
    :param dict xpaths: словарь xpath-выражений для извлечения адреса
    :param dict namespaces: namespaces используемые в xml-документе
    :return: экземпляр модели адреса
    :rtype: Address
    """

    def _set_attribute_model(xpath):
        _value = nodes2str(element.xpath(xpath, namespaces=namespaces))
        return _value.strip('.') if _value else _value

    if len(elements) == 0:
        return None
    address = Address()
    element = elements[0]
    for k, v in xpaths.items():
        if isinstance(v, dict):
            value = None
            try:
                value = eval(k.title())()  # TODO: надеюсь  есть такая  модель
            except Exception as e:
                logger.error('Ошибка обработки элемента. Класс не описан: {}. Значение: {}'.format(k, v))
                logger.exception(e)

            for sub_k, sub_v in v.items():
                _value = _set_attribute_model(sub_v)
                setattr(value, sub_k, _value if _value else None)
        else:
            value = _set_attribute_model(v)

        setattr(address, k, value if value else None)
    return address
