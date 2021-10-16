# coding: utf-8
from rrd_xml_parser.parsers.extract.about_property import ParserExtractAboutPropertyLand01, \
    ParserExtractAboutPropertyConstruction01
from rrd_xml_parser.parsers.extract.extract_names import EAPC_01_XPATHS, EAPC_GroupList


class ParserExtractBaseParamLand01(ParserExtractAboutPropertyLand01):
    """Класс извлечения сведений из документа extract_base_params_land"""
    NAMESPACE = 'extract_base_params_land'
    LEVELS = dict(
        extract_base_params_land=dict(
            land_record=None
        )
    )
    GROUPS = ['land_record', ]


# Парсер базовых параметров сооружений
class ParserExtractBaseParamConstruction01(ParserExtractAboutPropertyConstruction01):
    """Класс извлечения сведений из документа extract_base_params_construction"""
    NAMESPACE = 'extract_base_params_construction'
    GROUPS = EAPC_GroupList
    LEVELS = dict(
        extract_base_params_construction=dict(
            construction_record=None
        )
    )


setting_pars = {
    'extract_base_params_land': {
        'versions': {
            ParserExtractBaseParamLand01.NAMESPACE: ParserExtractBaseParamLand01
        }
    },
    'extract_base_params_construction': {
        'versions': {
            ParserExtractBaseParamConstruction01.NAMESPACE: ParserExtractBaseParamConstruction01
        }
    }
}
