# -*- coding: utf-8 -*-
from lxml.etree import QName
from rrd_xml_parser.parsers.names import NAMES
from rrd_xml_parser.parsers.oks.osk_names import KPOKS_04_GroupList
from rrd_xml_parser.parsers.oks.kvoks import ParserKVOKS3
from rrd_xml_parser.parsers.oks import osk_names
from rrd_xml_parser.parsers.utils import node2feature


class ParserKPOKS4(ParserKVOKS3):
    NAMESPACE = r'urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1'
    """Версия документа"""
    LEVELS = dict(
        KPOKS=dict(
            Realty=dict(
                Building=None,
                Construction=None,
                Uncompleted=None,
                Flat=None
            )
        )
    )
    GROUPS = KPOKS_04_GroupList
    NAMESPACES = dict(
        # a можно заменить на root, например, но тогда придётся менять все xpath-выражения
        a="urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1",
        smev="urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
        num="urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0",
        adrs="urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1",
        spa="urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1",
        param="urn://x-artefacts-rosreestr-ru/commons/complex-types/parameters-oks/2.0.1",
        cer="urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0",
        doc="urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1",
        flat="urn://x-artefacts-rosreestr-ru/commons/complex-types/assignation-flat/1.0.1",
        ch="urn://x-artefacts-rosreestr-ru/commons/complex-types/cultural-heritage/2.0.1",
    )
    """Словарь namespaces"""

    @classmethod
    def _el2Flat(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname
            if element_tag == tag_exit and event == 'end':
                # Получение участка
                yield from node2feature(element, osk_names.KVOKS_03_REALTY_XPATHS, NAMES[tag_exit], cls.NAMESPACES,
                                        lambda feature, element: False)

                # Получение частей участка
                parts = element.xpath(osk_names.KVOKS_03_XPath_SubConstruction, namespaces=cls.NAMESPACES)
                for part in parts:
                    part_tag = QName(part).localname
                    yield from node2feature(part, osk_names.KVOKS03_PART_XPATHS, NAMES[part_tag], cls.NAMESPACES,
                                            lambda feature, element: False)
                # Очистка xml-элемента
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)




setting_pars = {
    'kpoks': {
        'versions': {
            ParserKPOKS4.NAMESPACE: ParserKPOKS4,
        }
    }
}