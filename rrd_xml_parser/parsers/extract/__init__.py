from copy import deepcopy
from rrd_xml_parser.parsers.extract.about_property import setting_pars as settings_pars_ap
from rrd_xml_parser.parsers.extract.base_param import setting_pars as settings_pars_bp

settings_pars_extract = dict()
settings_pars_extract.update(deepcopy(settings_pars_ap))
settings_pars_extract.update(deepcopy(settings_pars_bp))

__all__ = ['settings_pars_extract']
