import logging
from copy import deepcopy
from lxml.etree import QName
from rrd_xml_parser.parsers.base import BaseParser, BaseMixin
from rrd_xml_parser.parsers.bozo import bozo_names
from rrd_xml_parser.parsers.names import NAMES
from rrd_xml_parser.parsers.utils import node2feature

logger = logging.getLogger(__name__)


class KVZoneParser(BaseParser):
    NAMESPACE = "urn://x-artefacts-rosreestr-ru/outgoing/kv-zone/1.0.1"
    GROUPS = bozo_names.KVZone_GroupNames
    LEVELS = dict(
        KVZone=dict(
            Zone=None
        )
    )
    # схемы
    NAMESPACES = dict(
        a="urn://x-artefacts-rosreestr-ru/outgoing/kv-zone/1.0.1",
        cer="urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0",
        # namespace для SpatialElement должен быть spa, это хардкод в node2wkt
        spa="urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1",
        doc="urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1"
    )

    @classmethod
    def _node2feature(cls, context, tag_exit, xpaths, check_geometry_callback):
        """
        Функция преобразования xml-элемента в Feature

        :param context: итератор по xml-документу
        :param str tag_exit: имя xml-элемента для выхода из функции
        :param dict xpaths: словарь xpath-выражений для извлечения атрибутов
        :param check_geometry_callback: функция проверки типа геометрии объекта
        """
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname

            # Если дошли до тега выхода, то выходим из цикла по context
            if element_tag == tag_exit and event == 'end':
                yield from node2feature(
                    element=element,
                    xpaths=xpaths,
                    feature_type=NAMES[tag_exit],
                    namespaces=cls.NAMESPACES,
                    check_object_subtype=check_geometry_callback
                )

                # Очистка ветки xml
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)

    @classmethod
    def _el2Zone(cls, context, tag_exit):
        yield from cls._node2feature(context, tag_exit, bozo_names.KVZone_XPaths,
                                     lambda feature, element: False)


# Зона (zone_territory_coastline_surveying)
class ExtractAboutZone01(BaseParser, BaseMixin):
    NAMESPACE = 'extract_about_zone'
    GROUPS = ['zone_territory_coastline_surveying', ]
    LEVELS = dict(
        extract_about_zone=dict(
            zone_territory_coastline_surveying=None
        )
    )

    @classmethod
    def _el2zone_territory_coastline_surveying(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname

            # Если дошли до тега выхода, то выходим из цикла по context
            if element_tag == tag_exit and event == 'end':
                yield from node2feature(
                    element,
                    bozo_names.EAZ_XPATHS,
                    NAMES[tag_exit],
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
    'kvzone': {
        'versions': {
            KVZoneParser.NAMESPACE: KVZoneParser
        }
    },
    'extract_about_zone': {
        'versions': {
            ExtractAboutZone01.NAMESPACE: ExtractAboutZone01
        }
    }
}
