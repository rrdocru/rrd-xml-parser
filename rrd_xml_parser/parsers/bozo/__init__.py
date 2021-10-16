from copy import deepcopy

from rrd_xml_parser.parsers.bozo.kvbound import setting_pars as settings_pars_kvbound
from rrd_xml_parser.parsers.bozo.kvzone import setting_pars as settings_pars_kvzone

settings_pars_bozo = dict()
settings_pars_bozo.update(deepcopy(settings_pars_kvbound))
settings_pars_bozo.update(deepcopy(settings_pars_kvzone))

__all__ = ['settings_pars_bozo']