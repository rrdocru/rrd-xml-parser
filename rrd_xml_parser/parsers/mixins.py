# -*- coding: utf-8 -*-
from lxml.etree import QName, _Element
from rrd_xml_parser.parsers.names import NAMES
from rrd_xml_parser.parsers.utils import node2feature


class BaseMixin:
    """
    Миксин для преобразования незначимых элементов
    """
    @classmethod
    def _clear(cls, context, tag_exit):
        for event, element in context:
            if event == 'start':
                element_tag = QName(element.tag).localname
                cls._clear(context, element_tag)
            elif event == 'end':
                element.clear()
                element_tag = QName(element.tag).localname
                if element_tag == tag_exit:
                    return

    @classmethod
    def _pass(cls, context, tag_exit):
        for event, element in context:
            if event == 'start':
                element_tag = QName(element.tag).localname
                cls._pass(context, element_tag)
            elif event == 'end':
                element_tag = QName(element.tag).localname
                if element_tag == tag_exit:
                    return
