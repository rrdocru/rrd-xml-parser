# -*- coding: utf-8 -*-
from lxml.etree import QName
from rrd_xml_parser.parsers.base import BaseParser
from rrd_xml_parser.parsers.zu.zu_names import KVZU07_GroupList, KVZU_07_names, KVZU_XPath_SubParcel, KVZU_07_part_names
from rrd_xml_parser.parsers.names import NAMES
from rrd_xml_parser.parsers.utils import node2feature


class ParserKVZU7(BaseParser):
    """
    Класс для парсинга КВЗУ 07 версии
    """
    NAMESPACE = r'urn://x-artefacts-rosreestr-ru/outgoing/kvzu/7.0.1'

    GROUPS = KVZU07_GroupList
    LEVELS = dict(
        KVZU=dict(
            Parcels=dict(
                Parcel=None,
                # OffspringParcel=None
            )
        )
    )
    NAMESPACES = dict(
        # a можно заменить на root, например, но тогда придётся менять все xpath-выражения
        a="urn://x-artefacts-rosreestr-ru/outgoing/kvzu/7.0.1",
        smev="urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
        num="urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0",
        adrs="urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1",
        spa="urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1",
        cer="urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0",
        doc="urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1",
        nobj="urn://x-artefacts-rosreestr-ru/commons/complex-types/natural-objects-output/1.0.1",
    )

    @classmethod
    def _el2Parcel(cls, context, tag_exit):
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
            if element_tag == tag_exit and event == 'end':
                # Получение участка
                yield from node2feature(element, KVZU_07_names, NAMES[tag_exit], cls.NAMESPACES,
                                        lambda feature, element: int(getattr(feature, 'subtype_code', '1')))

                # Получение частей участка
                parts = element.xpath(KVZU_XPath_SubParcel, namespaces=cls.NAMESPACES)
                for part in parts:
                    part_tag = QName(part).localname
                    yield from node2feature(part, KVZU_07_part_names, NAMES[part_tag], cls.NAMESPACES,
                                            lambda feature, element: False)

                # Очистка xml-элемента
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)


setting_pars = {
    'kvzu': {
        'versions': {
            ParserKVZU7.NAMESPACE: ParserKVZU7,
        }
    }
}
