from copy import deepcopy
from rrd_xml_parser.parsers.zu.kpzu import setting_pars as settings_pars_kpzu
from rrd_xml_parser.parsers.zu.kvzu import setting_pars as settings_pars_kvzu

settings_pars_zu = dict()
settings_pars_zu.update(deepcopy(settings_pars_kpzu))
settings_pars_zu.update(deepcopy(settings_pars_kvzu))

__all__ = ['settings_pars_zu']
