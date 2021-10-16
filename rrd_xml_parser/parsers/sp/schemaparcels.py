import logging
from lxml.etree import QName
from rrd_xml_parser.parsers.base import BaseParser
from rrd_xml_parser.parsers.names import NAMES
from rrd_xml_parser.parsers.utils import node2feature
from rrd_xml_parser.parsers.sp import sp_names

logging.getLogger(__name__)


class SchemaParcels01Parser(BaseParser):
    NAMESPACE = '01'
    GROUPS = sp_names.SP_GroupNames
    LEVELS = dict(
        SchemaParcels=dict(
            NewParcels=dict(
                NewParcel=None
            )
        )
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
    def _el2NewParcel(cls, context, tag_exit):
        yield from cls._node2feature(context, tag_exit, sp_names.SP_XPATHS,
                                     lambda feature, element: element.xpath("boolean(./Contours)"))


setting_pars = {
    "schemaparcels": {
        "versions": {
            SchemaParcels01Parser.NAMESPACE: SchemaParcels01Parser
        }
    }
}
