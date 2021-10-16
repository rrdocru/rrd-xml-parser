from copy import deepcopy
from rrd_xml_parser.parsers.mp.mp import settings_pars

settings_pars_mp = dict()
settings_pars_mp.update(deepcopy(settings_pars))


__all__ = ['settings_pars_mp']
