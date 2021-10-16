# coding: utf-8
from lxml.etree import QName
from rrd_xml_parser.parsers.base import BaseParser
from rrd_xml_parser.parsers.mixins import BaseMixin
from rrd_xml_parser.parsers.names import NAMES
from rrd_xml_parser.parsers.utils import node2feature
from rrd_xml_parser.parsers.extract.extract_names import EAPL_GroupList, EAPL_01_XPATHS, EAPL_01_XPATH_PART, \
    EAPL_01_PART_XPATHS
from rrd_xml_parser.parsers.extract.extract_names import EAPC_GroupList, EAPC_01_XPATHS, EAPC_01_PART_XPATHS


# Выписка о земельном участке
class ParserExtractAboutPropertyLand01(BaseParser, BaseMixin):
    NAMESPACE = 'extract_about_property_land'
    LEVELS = dict(
        extract_about_property_land=dict(
            land_record=None
        )
    )
    GROUPS = EAPL_GroupList

    @classmethod
    def _el2land_record(cls, context, tag_exit):
        """
        Метод возвращает итератор по участкам и его частям

        :param context: контекст возвращающий пару event, element
        :param str tag_exit: тэг элемента по которому выходить из процеруды

        :return: итератор элементов
        :type: Iterator(Feature)
        """
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname

            # Если дошли до тега выхода, то выходим из цикла по context
            if element_tag == tag_exit and event == 'end':
                yield from node2feature(element, EAPL_01_XPATHS, NAMES[tag_exit], cls.NAMESPACES,
                                        lambda feature, element: int(getattr(feature, 'subtype_code', '1')))

                # Получение частей участка
                parts = element.xpath(EAPL_01_XPATH_PART)
                for part in parts:
                    part_tag = QName(part).localname
                    yield from node2feature(part, EAPL_01_PART_XPATHS, NAMES[part_tag], cls.NAMESPACES,
                                            lambda feature, element: bool(
                                                int(element.xpath('count(./contours/contour)'))))

                # Очистка ветки xml
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)


# Парсер типа Выписка о сооружении
class ParserExtractAboutPropertyConstruction01(BaseParser, BaseMixin):
    NAMESPACE = 'extract_about_property_construction'
    LEVELS = dict(
        extract_about_property_construction=dict(
            construction_record=None
        )
    )
    GROUPS = EAPC_GroupList

    @classmethod
    def _el2construction_record(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname

            # Если дошли до тега выхода, то выходим из цикла по context
            if element_tag == tag_exit and event == 'end':
                yield from node2feature(
                    element,
                    EAPC_01_XPATHS,
                    NAMES[tag_exit],
                    cls.NAMESPACES,
                    lambda feature, element: False
                )

                # Получение дополнительных частей сооружения
                parts = element.xpath('./object_parts/object_part')
                for part in parts:
                    part_tag = QName(part).localname
                    yield from node2feature(
                        part,
                        EAPC_01_PART_XPATHS,
                        NAMES[part_tag],
                        cls.NAMESPACES,
                        lambda feature, element: False
                    )

                # Очистка ветки xml
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)


setting_pars = {
    'extract_about_property_land': {
        'versions': {
            ParserExtractAboutPropertyLand01.NAMESPACE: ParserExtractAboutPropertyLand01
        }
    },
    'extract_about_property_construction': {
        'versions': {
            ParserExtractAboutPropertyConstruction01.NAMESPACE: ParserExtractAboutPropertyConstruction01
        }
    }
}
