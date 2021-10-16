from copy import deepcopy
from rrd_xml_parser.parsers.oks.kvoks import setting_pars as settings_pars_kvoks
from rrd_xml_parser.parsers.oks.kpoks import setting_pars as settings_pars_kpoks

settings_pars_oks = dict()
settings_pars_oks.update(deepcopy(settings_pars_kvoks))
settings_pars_oks.update(deepcopy(settings_pars_kpoks))

__all__ = ['settings_pars_oks']
