"""Модуль с базовыми классами для парсинга xml-документов"""
# coding: utf-8
from abc import abstractmethod
from logging import getLogger
from types import GeneratorType
from lxml.etree import _Element, _XSLTProcessingInstruction, iterparse, QName
from rrd_xml_parser.parsers.mixins import BaseMixin


logger = getLogger(__name__)


class BaseContextIterator:
    """
    Базовый класс для итерации по xml-документу
    """
    def __init__(self, xml):
        """
        Метод инициализации экземпляра базового класса

        :param str xml: полный пусть к xml-документу
        """
        self.xml = xml
        self._context = None
        self._current = None
        self._event = None

    @property
    def context(self):
        if not self._context:
            self._context = iter(iterparse(self.xml, events=('start', 'end',)))
        for event, element in self._context:
            self._current = element
            self._event = event
            yield event, element

    @context.deleter
    def context(self):
        if self.context:
            for event, element in self.context:
                if event == 'end':
                    element.clear()
                    while element.getprevious() is not None:
                        if type(element.getprevious()) == _Element:
                            if element.getparent() is not None:
                                del element.getparent()[0]
                        else:
                            break
        del self._context

    @abstractmethod
    def get_features(self, includes=None, excludes=None):
        pass


class BaseParser(BaseContextIterator, BaseMixin):
    """
    Базовый класс для парсинга xml-документа
    """
    NAMESPACE = None
    """Версия документа"""
    LEVELS = None
    GROUPS = None
    STYLESHEET = None
    NAMESPACES = None
    """Словарь namespaces"""

    def _get_groups(self, tag_exit, includes=None, excludes=None):
        for event, element in self.context:
            element_tag = QName(element.tag).localname

            if element_tag == tag_exit:
                if event == 'end':
                    element.clear()
                    return

            elif excludes and element_tag in excludes:
                self._clear(self.context, element_tag)

            elif includes and element_tag in includes:
                method = getattr(self, '_el2' + element_tag, None)
                if method:
                    feature = method(self.context, element_tag)
                    if isinstance(feature, GeneratorType):
                        yield from feature
                    else:
                        yield feature
                    continue
                else:
                    self._clear(self.context, element_tag)
            else:
                self._clear(self.context, element_tag)

    def _get_features(self, levels, tag_exit, includes=None, excludes=None):
        for event, element in self.context:
            element_tag = QName(element.tag).localname

            if element_tag == tag_exit:
                if event == 'end':
                    element.clear()
                    return

            elif element_tag not in levels.keys():
                self._pass(self.context, element_tag)

            else:
                next_level = levels[element_tag]
                if isinstance(next_level, list):
                    yield from self._get_groups(element_tag, includes, excludes)
                    element.clear()
                elif isinstance(next_level, dict):
                    yield from self._get_features(next_level, element_tag, includes, excludes)
                    element.clear()
                elif not next_level:
                    if element_tag in excludes:
                        logger.debug('{} is excluding'.format(element_tag))
                        self._clear(self.context, element_tag)
                    elif element_tag not in includes:
                        logger.debug('{} excluding'.format(element_tag))
                        self._clear(self.context, element_tag)
                    else:
                        method = getattr(self, '_el2' + element_tag, None)
                        if method:
                            feature = method(self.context, element_tag)
                            if isinstance(feature, GeneratorType):
                                yield from feature
                            else:
                                yield feature
                else:
                    self._clear(self.context, element_tag)

    def get_features(self, includes=None, excludes=None):
        """
        Получение объектов недвижимости

        :param list includes: список получемых объектов недвижимости
        :param list excludes: список атрибутов для пропуска
        :return: итератор объектов недвижимости
        :rtype: collections.Iterable[Feature]
        """
        _includes = includes or self.GROUPS
        _excludes = excludes or []
        for event, element in self.context:
            element_tag = QName(element.tag).localname

            previous = element.getprevious()
            if previous is not None and type(previous) == _XSLTProcessingInstruction:
                self.STYLESHEET = previous.attrib['href']

            next_levels = self.LEVELS[element_tag]
            if isinstance(next_levels, list):
                yield from self._get_groups(element_tag, _includes)
            elif isinstance(next_levels, dict):
                yield from self._get_features(self.LEVELS[element_tag], element_tag, _includes, _excludes)
            element.clear()
