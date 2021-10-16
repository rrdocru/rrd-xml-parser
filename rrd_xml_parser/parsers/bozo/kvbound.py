import logging
from copy import deepcopy
from lxml.etree import QName
from rrd_xml_parser.parsers.base import BaseParser
from rrd_xml_parser.parsers.bozo import bozo_names
from rrd_xml_parser.parsers.names import NAMES
from rrd_xml_parser.parsers.utils import node2feature

logger = logging.getLogger(__name__)


class KVBoundParser(BaseParser):
    NAMESPACE = "urn://x-artefacts-rosreestr-ru/outgoing/kv-bound/1.0.1"
    GROUPS = bozo_names.KVBound_GroupNames
    LEVELS = dict(
        KVBound=dict(
            Bound=None
        )
    )
    # схемы
    NAMESPACES = dict(
        a="urn://x-artefacts-rosreestr-ru/outgoing/kv-bound/1.0.1",
        cer="urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0",
        smev="urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
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
    def _el2Bound(cls, context, tag_exit):
        yield from cls._node2feature(context, tag_exit, bozo_names.KVBound_BoundXPaths,
                                     lambda feature, element: False)


class ExtractAboutBoundary01(BaseParser):
    NAMESPACE = 'extract_about_boundary'
    GROUPS = bozo_names.EAB_GroupNames
    LEVELS = dict(
        extract_about_boundary=dict(
            boundary_record=None
        )
    )

    @classmethod
    def _el2boundary_record(cls, context, tag_exit):

        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname

            # Если дошли до тега выхода, то выходим из цикла по context
            if element_tag == tag_exit and event == 'end':
                yield from node2feature(
                    element=element,
                    xpaths=bozo_names.EAB_XPaths,
                    feature_type=NAMES[tag_exit],
                    namespaces=cls.NAMESPACES,
                    check_object_subtype=lambda feature, element: False
                )

                # Очистка ветки xml
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)


setting_pars = {
    'kvbound': {
        'versions': {
            KVBoundParser.NAMESPACE: KVBoundParser
        }
    },
    'extract_about_boundary': {
        'versions': {
            ExtractAboutBoundary01.NAMESPACE: ExtractAboutBoundary01
        }
    }
}
