from copy import deepcopy
from rrd_xml_parser.parsers.sp.schemaparcels import setting_pars

settings_pars_sp = dict()
settings_pars_sp.update(deepcopy(setting_pars))

__all__ = ['settings_pars_sp']
