from rrd_xml_parser.parsers.zu.zu_names import KPZU06_GroupList
from rrd_xml_parser.parsers.zu.kvzu import ParserKVZU7


class ParserKPZU6(ParserKVZU7):
    """
    Класс для парсинга КПЗУ 06 версии
    """
    NAMESPACE = r'urn://x-artefacts-rosreestr-ru/outgoing/kpzu/6.0.1'
    GROUPS = KPZU06_GroupList
    LEVELS = dict(
        KPZU=dict(
            Parcel=None
        )
    )
    NAMESPACES = dict(
        # a можно заменить на root, например, но тогда придётся менять все xpath-выражения
        a="urn://x-artefacts-rosreestr-ru/outgoing/kpzu/6.0.1",
        smev="urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
        num="urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0",
        adrs="urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1",
        spa="urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1",
        cer="urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0",
        doc="urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1",
        nobj="urn://x-artefacts-rosreestr-ru/commons/complex-types/natural-objects-output/1.0.1",
    )


setting_pars = {
    'kpzu': {
        'versions': {
            ParserKPZU6.NAMESPACE: ParserKPZU6,
        }
    }
}
